# Python standard library modules
import curses

# Local application modules
import menus.assume_role
import menus.base_menu
import menus.manage_key_pairs
import menus.request_temporary_credentials
import menus.set_default_profile


class Menu(menus.base_menu.BaseMenu):
    def __init__(self, config):
        self.config = config
        self.selected_option = 1

        while True:
            selection = self.get_selection()
            if selection == 1:
                if len(self.config.data['key_pairs'].keys()) == 0:
                    self.msg_box(5, 8, 42, [
                        [0, 'You have not added any key pairs yet'],
                        [5, 'Select "Manage key pairs"'],
                        [0, ''],
                        [6, 'Press any key to continue']
                    ], 3)
                else:
                    menus.request_temporary_credentials.Menu(config)
            elif selection == 2:
                if len(self.config.data['key_pairs'].keys()) == 0:
                    self.msg_box(5, 8, 42, [
                        [0, 'You have not added any key pairs yet'],
                        [5, 'Select "Manage key pairs"'],
                        [0, ''],
                        [6, 'Press any key to continue']
                    ], 3)
                else:
                    menus.set_default_profile.Menu(config)
            elif selection == 3:
                menus.assume_role.Menu(config)
            elif selection == 4:
                menus.manage_key_pairs.Menu(config)
            elif selection == 5:
                break

        curses.endwin()

    def get_selection(self):
        self.menu_init()

        input_key = None

        while input_key not in [ord('\n'), curses.KEY_RIGHT]:
            pos = 1
            option_count = 0

            self.screen.addstr(pos, 2, ' _____ _ _ _ _____ _____ _____', curses.A_BOLD)
            pos += 1
            self.screen.addstr(pos, 2, '|  _  | | | |   __|  _  |     |', curses.A_BOLD)
            pos += 1
            self.screen.addstr(pos, 2, '|     | | | |__   |   __| | | |', curses.A_BOLD)
            pos += 1
            self.screen.addstr(pos, 2, '|__|__|_____|_____|__|  |_|_|_|', curses.A_BOLD)
            pos += 2

            if self.config.data['default_profile_name'] is not None:
                self.screen.addstr(pos, 2, 'Current profile: ')

                self.screen.addstr(pos, 19, self.config.data['default_profile_name'], curses.color_pair(2))
                if self.config.data['default_profile_type'] == 'key_pair':
                    if self.config.data['key_pairs'][self.config.data['default_profile_name']]['use_temporary_credentials']:
                        self.screen.addstr(
                            pos,
                            20 + len(self.config.data['default_profile_name']),
                            '(using temporary credentials)',
                        )
                elif self.config.data['default_profile_type'] == 'assumed_role':
                    self.screen.addstr(
                        pos,
                        20 + len(self.config.data['default_profile_name']),
                        '(assumed role)',
                    )

                pos += 2

            color = curses.color_pair(1) if self.selected_option == 1 else curses.A_NORMAL
            self.screen.addstr(pos, 2, 'Request temporary credentials', color)
            option_count += 1
            pos += 1

            color = curses.color_pair(1) if self.selected_option == 2 else curses.A_NORMAL
            self.screen.addstr(pos, 2, 'Set default key pair/assumed role', color)
            option_count += 1
            pos += 1

            color = curses.color_pair(1) if self.selected_option == 3 else curses.A_NORMAL
            self.screen.addstr(pos, 2, 'Assume a role', color)
            option_count += 1
            pos += 1

            color = curses.color_pair(1) if self.selected_option == 4 else curses.A_NORMAL
            self.screen.addstr(pos, 2, 'Manage key pairs/assumed roles', color)
            option_count += 1
            pos += 1

            pos += 1
            color = curses.color_pair(1) if self.selected_option == 5 else curses.A_NORMAL
            self.screen.addstr(pos, 2, '< Exit', color)
            option_count += 1

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
