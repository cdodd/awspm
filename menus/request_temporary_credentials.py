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

        selection = self.get_selection()
        if selection == len(self.config.data['key_pairs'].keys()) + 1:
            curses.endwin()
            return

        key_pair_name = sorted(self.config.data['key_pairs'].keys())[selection - 1]

        valid_mfa = False
        while not valid_mfa:
            mfa_box = curses.newwin(5, 42, 5, 8)
            mfa_box.box()
            mfa_box.addstr(1, 1, 'Enter MFA token (leave blank to cancel):')
            curses.echo()
            curses.curs_set(1)
            mfa_box.refresh()
            mfa_code = mfa_box.getstr(3, 2).decode('utf-8')
            curses.echo(0)
            curses.curs_set(0)
            mfa_box.refresh()

            if mfa_code.strip() == '':
                valid_mfa = True
            elif len(mfa_code) != 6 or not mfa_code.isdigit():
                self.msg_box(5, 8, 38, [[0, 'MFA code must be a 6 digit value'], [1, ''], [5, 'Press any key to continue']], 3)
            else:
                valid_mfa = True

            mfa_box.erase()

        if mfa_code == '':
            curses.endwin()
            return

        sts_client = boto3.client(
            'sts',
            aws_access_key_id=self.config.data['key_pairs'][key_pair_name]['access_key_id'],
            aws_secret_access_key=self.config.data['key_pairs'][key_pair_name]['secret_access_key'],
        )

        try:
            response = sts_client.get_session_token(
                SerialNumber='arn:aws:iam::{0:s}:mfa/{1:s}'.format(
                    self.config.data['key_pairs'][key_pair_name]['account_id'],
                    self.config.data['key_pairs'][key_pair_name]['iam_username'],
                ),
                TokenCode=mfa_code,
            )

            self.config.data['key_pairs'][key_pair_name]['temporary_credentials'] = {
                'access_key_id': response['Credentials']['AccessKeyId'],
                'expiration': str(response['Credentials']['Expiration']),
                'secret_access_key': response['Credentials']['SecretAccessKey'],
                'session_token': response['Credentials']['SessionToken'],
            }
            self.config.data['key_pairs'][key_pair_name]['use_temporary_credentials'] = True

        except botocore.exceptions.ClientError as e:
            err_msg = str(e)
            err_msg_lines = []
            while True:
                if len(err_msg) > 44:
                    err_msg_lines.append([0, err_msg[0:44]])
                    err_msg = err_msg[44:]
                else:
                    err_msg_lines.append([0, err_msg])
                    break

            self.msg_box(5, 8, 50, err_msg_lines, 3)
            return

        self.config.data['key_pairs'][key_pair_name]['use_temporary_credentials'] = True
        self.config.save()

        self.msg_box(5, 8, 32, [
            [10, 'SUCCESS'],
            [1, ''],
            [1, 'Press any key to continue']
        ], 2)

        curses.endwin()

    def get_selection(self):
        self.menu_init()

        input_key = None

        while input_key not in [ord('\n'), curses.KEY_RIGHT]:
            pos = 1
            option_count = 0

            # Write title and message
            self.screen.addstr(pos, 2, 'awspm > Request temporary credentials', curses.A_BOLD)
            pos += 1
            self.screen.addstr(pos, 2, '=====================================', curses.A_BOLD)
            pos += 2
            self.screen.addstr(pos, 2, 'Select a key pair:')
            pos += 1
            self.screen.addstr(pos, 2, '------------------')
            pos += 2

            for i, key in enumerate(sorted(self.config.data['key_pairs'].keys())):
                color = curses.color_pair(1) if self.selected_option == i + 1 else curses.A_NORMAL
                self.screen.addstr(pos, 2, '{0:s} ({1:s})'.format(key, self.config.data['key_pairs'][key]['iam_username']), color)
                option_count += 1
                pos += 1

            pos += 1
            color = curses.color_pair(1) if self.selected_option == len(self.config.data['key_pairs'].keys()) + 1 else curses.A_NORMAL
            self.screen.addstr(pos, 2, '< Back to main menu', color)
            option_count += 1
            pos += 1

            down_keys = [curses.KEY_DOWN, ord('j')]
            up_keys = [curses.KEY_UP, ord('k')]
            exit_keys = [curses.KEY_LEFT, ord('q')]

            self.screen.refresh()
            input_key = self.screen.getch()
            if input_key in down_keys:
                if self.selected_option < option_count:
                    self.selected_option += 1
                else:
                    self.selected_option = 1

            if input_key in up_keys:
                if self.selected_option > 1:
                    self.selected_option -= 1
                else:
                    self.selected_option = option_count

            if input_key in exit_keys:
                return option_count

        return self.selected_option
