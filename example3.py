"""
Repository: https://github.com/itssme/python_curses_examples
Desc: If the user presses 'ENTER' the Option window will be checked.
Author: https://github.com/itssme
"""

# TODO: make a menu with options

import curses


def setup():
    stdscr = curses.initscr()
    curses.start_color()
    curses.use_default_colors()

    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)
    curses.curs_set(0)

    return stdscr


def teardown(stdscr):
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.curs_set(1)
    curses.endwin()


class Option:

    def __init__(self, parent_window, nlines, ncols, begin_y, begin_x, title="", text=""):
        self.window = parent_window.subwin(nlines, ncols, begin_y, begin_x)
        self.MAX_X, self.MAX_Y = self.window.getmaxyx()
        self.title = title
        self.__fit_text(text)

    def __fit_text(self, text, mode=None):
        self.window.erase()
        self.window.border()
        self.window.addstr(0, 1, self.title)
        if mode is None:
            self.window.addstr(self.MAX_X/2, self.MAX_Y-len(text) - 1, text)
        else:
            self.window.addstr(self.MAX_X/2, self.MAX_Y-len(text) - 1, text, mode)
        self.text = text

    def check(self):
        self.window.erase()
        self.__fit_text(self.text, curses.A_REVERSE)


def main():
    stdscr = setup()

    MAX_X, MAX_Y = stdscr.getmaxyx()

    main_window = curses.newwin(MAX_X, MAX_Y, 0, 0)

    option_1 = Option(main_window, 3, 20, MAX_X/2, MAX_Y/2, title="hello window", text="hello")

    option_1.window.getch()

    option_1.check()
    main_window.refresh()

    option_1.window.getch()
    teardown(stdscr)


if __name__ == '__main__':
    main()
