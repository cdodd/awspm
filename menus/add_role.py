# Python standard library modules
import curses

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

        role_name_box = curses.newwin(5, 42, 5, 8)
        role_name_box.box()
        role_name_box.addstr(1, 1, 'Enter role name (leave blank to cancel):')
        curses.echo()
        curses.curs_set(1)
        role_name_box.refresh()
        role_name = role_name_box.getstr(3, 2).decode('utf-8')
        role_name_box.erase()
        role_name_box.refresh()
        if role_name.strip() == '':
            return

        role_arn_box = curses.newwin(5, 42, 5, 8)
        role_arn_box.box()
        role_arn_box.addstr(1, 1, 'Enter role ARN (leave blank to cancel):')
        curses.echo()
        curses.curs_set(1)
        role_arn_box.refresh()
        role_arn = role_arn_box.getstr(3, 2).decode('utf-8')
        role_arn_box.erase()
        role_arn_box.refresh()
        if role_arn.strip() == '':
            return

        self.config.data['key_pairs'][key_pair_name]['roles'][role_name] = role_arn
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
            self.screen.addstr(pos, 2, 'awspm > ... > Add a Role', curses.A_BOLD)
            pos += 1
            self.screen.addstr(pos, 2, '========================', curses.A_BOLD)
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
