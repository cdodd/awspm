# Python standard library modules
import curses


class BaseMenu(object):
    def menu_init(self):
        self.screen = curses.initscr()
        self.screen.erase()
        self.screen.keypad(1)
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.curs_set(0)
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

    def msg_box(self, pos_x, pos_y, width, message_list, colour):
        box = curses.newwin(len(message_list) + 4, width, pos_x, pos_y)
        box.box()

        for i in [1, len(message_list) + 2]:
            box.addstr(i, 1, '|', curses.color_pair(colour))
            box.addstr(i, width - 2, '|', curses.color_pair(colour))

        for i, message in enumerate(message_list):
            box.addstr(i + 2, 1, '|', curses.color_pair(colour))
            box.addstr(i + 2, width - 2, '|', curses.color_pair(colour))
            box.addstr(i + 2, message[0] + 3, message[1])

        curses.echo(0)
        curses.curs_set(0)
        box.refresh()
        box.getch(1, 1)
        box.erase()
        box.refresh()
