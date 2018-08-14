# Python standard library modules
import curses

# Local application modules
import menus.base_menu


class Menu(menus.base_menu.BaseMenu):
    def __init__(self, config):
        self.selected_option = 1
        self.config = config

        selection = self.get_selection()
        if selection == self.option_count:
            curses.endwin()
            return

        profiles_roles = sorted(self.config.data['key_pairs'].keys())
        profiles_roles += sorted(self.config.data['assumed_roles'].keys())

        profile_name = profiles_roles[selection - 1]
        self.config.data['default_profile_name'] = profile_name

        if profile_name in self.config.data['key_pairs'].keys():
            self.config.data['default_profile_type'] = 'key_pair'
        else:
            self.config.data['default_profile_type'] = 'assumed_role'

        self.config.save()
        self.msg_box(5, 8, 32, [
            [10, 'SUCCESS'],
            [1, ''],
            [1, 'Press any key to continue']
        ], 2)
        curses.endwin()

    def get_selection(self):
        input_key = None

        while input_key not in [ord('\n'), curses.KEY_RIGHT]:
            self.menu_init()
            pos = 1
            self.option_count = 0

            # Write title and message
            self.screen.addstr(pos, 2, 'awspm > Set default key pair/assumed role', curses.A_BOLD)
            pos += 1
            self.screen.addstr(pos, 2, '=========================================', curses.A_BOLD)
            pos += 2
            self.screen.addstr(pos, 2, 'Select a key pair/role:')
            pos += 1
            self.screen.addstr(pos, 2, '-----------------------')
            pos += 2

            for key in sorted(self.config.data['key_pairs'].keys()):
                self.option_count += 1
                color = curses.color_pair(1) if self.selected_option == self.option_count else curses.A_NORMAL
                self.screen.addstr(pos, 2, '{0:s}'.format(key), color)
                pos += 1

            for role in sorted(self.config.data['assumed_roles'].keys()):
                self.option_count += 1
                color = curses.color_pair(1) if self.selected_option == self.option_count else curses.A_NORMAL
                self.screen.addstr(pos, 2, '{0:s} (Role)'.format(role), color)
                pos += 1

            pos += 1
            self.option_count += 1
            color = curses.color_pair(1) if self.selected_option == self.option_count else curses.A_NORMAL
            self.screen.addstr(pos, 2, '< Back to main menu', color)
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
