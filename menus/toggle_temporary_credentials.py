# Python standard library modules
import curses

# Local application modules
import menus.base_menu


class Menu(menus.base_menu.BaseMenu):
    def __init__(self, config):
        self.selected_option = 1
        self.config = config

        selection = self.get_selection()

        key_pair_names = sorted(self.config.data['key_pairs'].keys())

        # Exit if "< Back to previous menu" was selected
        if selection == len(key_pair_names) + 1:
            curses.endwin()
            return

        key_pair_name = key_pair_names[selection - 1]

        if self.config.data['key_pairs'][key_pair_name]['use_temporary_credentials']:
            self.config.data['key_pairs'][key_pair_name]['use_temporary_credentials'] = False
        else:
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
            self.screen.addstr(pos, 2, 'awspm > ... > Enable/disable temporary credentials', curses.A_BOLD)
            pos += 1
            self.screen.addstr(pos, 2, '==================================================', curses.A_BOLD)
            pos += 2
            self.screen.addstr(pos, 2, 'Select a key pair:')
            pos += 1
            self.screen.addstr(pos, 2, '----------------------------')
            pos += 2

            for i, key in enumerate(sorted(self.config.data['key_pairs'].keys())):
                color = curses.color_pair(1) if self.selected_option == i + 1 else curses.A_NORMAL
                self.screen.addstr(pos, 2, '{0:s} ({1:s}) [{2:s}]'.format(
                    key,
                    self.config.data['key_pairs'][key]['iam_username'],
                    'Enabled' if self.config.data['key_pairs'][key]['use_temporary_credentials'] else 'Disabled',
                ), color)
                option_count += 1
                pos += 1

            pos += 1
            color = curses.color_pair(1) if self.selected_option == len(self.config.data['key_pairs'].keys()) + 1 else curses.A_NORMAL
            self.screen.addstr(pos, 2, '< Back to previous menu', color)
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
