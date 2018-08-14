# Python standard library modules
import curses

# 3rd party modules
import boto3
import botocore.exceptions

# Local application modules
import menus.base_menu


class Menu(menus.base_menu.BaseMenu):
    def __init__(self, config):
        self.selected_option = 1
        self.config = config

        while True:
            selection = self.get_selection()
            if selection == self.option_count:
                curses.endwin()
                break

            keypair_role_list = []

            for key_pair_name in sorted(self.config.data['key_pairs'].keys()):
                for role_name in sorted(self.config.data['key_pairs'][key_pair_name]['roles'].keys()):
                    keypair_role_list.append([
                        key_pair_name,
                        role_name,
                        self.config.data['key_pairs'][key_pair_name]['roles'][role_name],
                    ])

            key_pair_role = keypair_role_list[selection - 1]
            key_pair_info = self.config.get_active_key_pair(key_pair_role[0])

            sts_client = boto3.client(
                'sts',
                aws_access_key_id=key_pair_info['aws_access_key_id'],
                aws_secret_access_key=key_pair_info['aws_secret_access_key'],
                aws_session_token=key_pair_info['aws_session_token'],
            )

            try:
                response = sts_client.assume_role(
                    RoleArn=key_pair_role[2],
                    RoleSessionName='{0:s}-{1:s}'.format(key_pair_role[0], key_pair_role[1]),
                )
            except (botocore.exceptions.ClientError, botocore.exceptions.ParamValidationError) as e:
                err_msg = str(e).replace('\n', ' ')
                err_msg_lines = []
                while True:
                    if len(err_msg) > 44:
                        err_msg_lines.append([0, err_msg[0:44]])
                        err_msg = err_msg[44:]
                    else:
                        err_msg_lines.append([0, err_msg])
                        break

                self.msg_box(5, 8, 50, err_msg_lines, 3)
            else:
                self.config.data['assumed_roles']['{0:s}-{1:s}'.format(key_pair_role[0], key_pair_role[1])] = {
                    'access_key_id': response['Credentials']['AccessKeyId'],
                    'expiration': str(response['Credentials']['Expiration']),
                    'secret_access_key': response['Credentials']['SecretAccessKey'],
                    'session_token': response['Credentials']['SessionToken'],
                }

                self.config.data['default_profile_name'] = '{0:s}-{1:s}'.format(key_pair_role[0], key_pair_role[1])
                self.config.data['default_profile_type'] = 'assumed_role'
                self.config.save()

                self.msg_box(5, 8, 32, [
                    [10, 'SUCCESS'],
                    [1, ''],
                    [1, 'Press any key to continue']
                ], 2)
                break

        curses.endwin()

    def get_selection(self):
        self.menu_init()

        input_key = None

        while input_key not in [ord('\n'), curses.KEY_RIGHT]:
            pos = 1
            self.option_count = 0

            # Write title and message
            self.screen.addstr(pos, 2, 'awspm > Assume a role', curses.A_BOLD)
            pos += 1
            self.screen.addstr(pos, 2, '=====================', curses.A_BOLD)
            pos += 2
            self.screen.addstr(pos, 2, 'Select a role to assume:')
            pos += 1
            self.screen.addstr(pos, 2, '------------------------')
            pos += 2

            i = 1
            for key_pair_name in sorted(self.config.data['key_pairs'].keys()):
                for role_name, role_arn in self.config.data['key_pairs'][key_pair_name]['roles'].items():
                    color = curses.color_pair(1) if self.selected_option == self.option_count + 1 else curses.A_NORMAL
                    self.screen.addstr(pos, 2, '{0:s} ({1:s})'.format(role_name, key_pair_name), color)
                    i += 1
                    pos += 1
                    self.option_count += 1

            pos += 1
            color = curses.color_pair(1) if self.selected_option == self.option_count + 1 else curses.A_NORMAL
            self.screen.addstr(pos, 2, '< Back to main menu', color)
            self.option_count += 1
            pos += 1

            down_keys = [curses.KEY_DOWN, ord('j')]
            up_keys = [curses.KEY_UP, ord('k')]
            exit_keys = [curses.KEY_LEFT, ord('q')]

            self.screen.refresh()
            input_key = self.screen.getch()
            if input_key in down_keys:
                if self.selected_option < self.option_count:
                    self.selected_option += 1
                else:
                    self.selected_option = 1

            if input_key in up_keys:
                if self.selected_option > 1:
                    self.selected_option -= 1
                else:
                    self.selected_option = self.option_count

            if input_key in exit_keys:
                return self.option_count

        return self.selected_option
