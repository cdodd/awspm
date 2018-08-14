# Python standard library modules
import curses

# Local application modules
import menus.add_role
import menus.base_menu
import menus.toggle_temporary_credentials
import menus.remove_key_pair
import menus.remove_role


class Menu(menus.base_menu.BaseMenu):
    def __init__(self, config):
        self.selected_option = 1
        self.config = config

        while True:
            selection = self.get_selection()

            if selection == 1:
                new_kp_box = curses.newwin(10, 42, 5, 8)
                new_kp_box.box()
                new_kp_box.addstr(1, 12, 'Add a Key Pair:')

                new_kp_box.addstr(3, 5, 'Key pair name:')
                new_kp_box.addstr(4, 6, 'IAM username:')
                new_kp_box.addstr(5, 5, 'Access key ID:')
                new_kp_box.addstr(6, 1, 'Secret access key:  (hidden)')
                new_kp_box.addstr(7, 8, 'Account ID:')
                new_kp_box.addstr(8, 4, 'Default region:')
                curses.echo()
                curses.curs_set(1)
                new_kp_box.refresh()
                key_pair_name = new_kp_box.getstr(3, 20).decode('utf-8')
                if key_pair_name == '':
                    continue
                iam_username = new_kp_box.getstr(4, 20).decode('utf-8')
                access_key_id = new_kp_box.getstr(5, 20).decode('utf-8')
                curses.echo(0)
                secret_access_key = new_kp_box.getstr(6, 20).decode('utf-8')
                curses.echo()
                account_id = new_kp_box.getstr(7, 20).decode('utf-8')
                default_region = new_kp_box.getstr(8, 20).decode('utf-8')
                new_kp_box.erase()

                # TODO: Check if key pair already exists

                self.config.data['key_pairs'][key_pair_name] = {
                    'access_key_id': access_key_id,
                    'account_id': account_id,
                    'iam_username': iam_username,
                    'temporary_credentials': {
                        'access_key_id': None,
                        'expiration': None,
                        'secret_access_key': None,
                        'session_token': None,
                    },
                    'use_temporary_credentials': False,
                    'options': {'region': default_region},
                    'roles': {},
                    'secret_access_key': secret_access_key,
                }

                # If this is the only key pair then set it as the default
                if len(self.config.data['key_pairs']) == 1:
                    self.config.data['default_profile_name'] = key_pair_name
                    self.config.data['default_profile_type'] = 'key_pair'

                self.config.save()

                self.msg_box(5, 8, 32, [
                    [10, 'SUCCESS'],
                    [1, ''],
                    [1, 'Press any key to continue']
                ], 2)

                break

            elif selection == 2:
                menus.remove_key_pair.Menu(self.config)

            elif selection == 3:
                menus.toggle_temporary_credentials.Menu(self.config)

            elif selection == 4:
                menus.add_role.Menu(self.config)

            elif selection == 5:
                menus.remove_role.Menu(self.config)

            elif selection == 6:
                curses.endwin()
                break

            else:
                self.msg_box(5, 8, 32, [
                    [0, 'Not yet implemented, sorry'],
                    [1, ''],
                    [1, 'Press any key to continue']
                ], 3)

        curses.endwin()

    def get_selection(self):
        self.menu_init()

        input_key = None

        while input_key not in [ord('\n'), curses.KEY_RIGHT]:
            pos = 1
            option_count = 0

            # Write title and message
            self.screen.addstr(pos, 2, 'awspm > Manage key pairs/assumed roles', curses.A_BOLD)
            pos += 1
            self.screen.addstr(pos, 2, '======================================', curses.A_BOLD)
            pos += 2
            self.screen.addstr(pos, 2, 'Select an option:')
            pos += 1
            self.screen.addstr(pos, 2, '-----------------')
            pos += 2

            option_count += 1
            color = curses.color_pair(1) if self.selected_option == option_count else curses.A_NORMAL
            self.screen.addstr(pos, 2, 'Add a key pair', color)
            pos += 1

            option_count += 1
            color = curses.color_pair(1) if self.selected_option == option_count else curses.A_NORMAL
            self.screen.addstr(pos, 2, 'Remove a key pair', color)
            pos += 1

            option_count += 1
            color = curses.color_pair(1) if self.selected_option == option_count else curses.A_NORMAL
            self.screen.addstr(pos, 2, 'Enable/disable temporary credentials', color)
            pos += 1

            option_count += 1
            color = curses.color_pair(1) if self.selected_option == option_count else curses.A_NORMAL
            self.screen.addstr(pos, 2, 'Add a role', color)
            pos += 1

            option_count += 1
            color = curses.color_pair(1) if self.selected_option == option_count else curses.A_NORMAL
            self.screen.addstr(pos, 2, 'Remove a role', color)
            pos += 1

            # option_count += 1
            # color = curses.color_pair(1) if self.selected_option == option_count else curses.A_NORMAL
            # self.screen.addstr(pos, 2, 'Add a key/value option', color)
            # pos += 1

            # option_count += 1
            # color = curses.color_pair(1) if self.selected_option == option_count else curses.A_NORMAL
            # self.screen.addstr(pos, 2, 'Remove a key/value option', color)
            # pos += 1

            pos += 1
            option_count += 1
            color = curses.color_pair(1) if self.selected_option == option_count else curses.A_NORMAL
            self.screen.addstr(pos, 2, '< Back to main menu', color)
            pos += 1

            self.screen.refresh()

            down_keys = [curses.KEY_DOWN, ord('j')]
            up_keys = [curses.KEY_UP, ord('k')]
            exit_keys = [curses.KEY_LEFT, ord('q')]

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
