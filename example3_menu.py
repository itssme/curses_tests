"""
Repository: https://github.com/itssme/python_curses_examples
Desc: A simple menu with options. The user can check options by pressing the space bar. When the user presses the
      enter key the callback function of the checked options is called.
Author: https://github.com/itssme
"""

import curses
from time import sleep, time


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


class Menu:
    def __init__(self, parent_window, begin_y, begin_x, options, title=""):
        nlines = len(options) + 3
        ncols = len(options[0][0])
        for i in range(1, len(options)):
            ncols = len(options[i][0]) if ncols <= len(options[i][0]) else ncols

        ncols = len(title) if ncols < len(title) else ncols

        ncols = ncols + 6

        self.title = title
        self.window = parent_window.subwin(nlines, ncols, begin_y, begin_x)
        self.window.keypad(1)
        self.MAX_X, self.MAX_Y = self.window.getmaxyx()

        self.options = []
        for i in range(0, len(options)):
            self.options.append(self.__Option(self.window, options[i][0], i + 2, 1, ncols, options[i][1]))

        self.window.border()
        if self.title != "":
            self.window.addstr(0, 1, " {} ".format(self.title))

        self.option_index = 0
        self.__last_blink = 0

    def up(self):
        self.option_index -= 1 if self.option_index - 1 >= 0 else 0
        self.check_blink()
        if self.title != "":
            self.window.addstr(0, 1, " {} ".format(self.title))

    def down(self):
        self.option_index += 1 if self.option_index + 1 < len(self.options) else 0
        self.check_blink()
        if self.title != "":
            self.window.addstr(0, 1, " {} ".format(self.title))

    def check(self):
        if self.options[self.option_index].is_checked:
            self.options[self.option_index].uncheck()
        else:
            self.options[self.option_index].check()

        self.window.border()
        if self.title != "":
            self.window.addstr(0, 1, " {} ".format(self.title))

    def check_blink(self):
        for i in range(0, len(self.options)):
            if i != self.option_index:
                if self.options[i].is_reversed:
                    self.options[i].blink()
                    self.window.border()

    def blink(self):
        if time() - self.__last_blink > 0.2:
            self.options[self.option_index].blink()
            self.window.border()
            if self.title != "":
                self.window.addstr(0, 1, " {} ".format(self.title))
            self.__last_blink = time()

    def refresh(self):
        self.window.refresh()
        for option in self.options:
            option.window.refresh()

    def execute(self):
        for option in self.options:
            if option.callback is not None and option.is_checked:
                option.callback()

    class __Option:

        def __init__(self, parent_window, text, begin_y, begin_x, length, callback=None):
            self.length = length
            self.window = parent_window.subwin(1, length, begin_y, begin_x)
            self.text = text
            self.callback = callback
            self.is_checked = False
            self.is_reversed = False
            self.fit_text(self.text)

        def fit_text(self, text, mode=None):
            self.window.erase()
            if mode is None:
                self.window.addstr(0, self.length - len(text) - 1, text)
            else:
                self.window.addstr(0, self.length - len(text) - 1, text, mode)

            if self.is_checked:
                self.window.addch(0, 1, '[')
                self.window.addch(0, 2, ' ', curses.A_REVERSE)
                self.window.addch(0, 3, ']')
            else:
                self.window.addstr(0, 1, "[ ]")

            self.text = text

        def blink(self):
            if self.is_reversed:
                self.window.erase()
                self.fit_text(self.text)
                self.is_reversed = False
            else:
                self.window.erase()
                self.fit_text(self.text, curses.A_REVERSE)
                self.is_reversed = True

        def check(self):
            self.window.erase()
            self.is_checked = True
            self.fit_text(self.text)

        def uncheck(self):
            self.window.erase()
            self.is_checked = False
            self.fit_text(self.text)


def example_callback1():
    print("one")


def example_callback2():
    print("two")


def main():
    stdscr = setup()

    MAX_X, MAX_Y = stdscr.getmaxyx()

    main_window = curses.newwin(MAX_X, MAX_Y, 0, 0)
    main_window.keypad(1)
    main_window.timeout(100)

    menu = Menu(main_window, 1, 1, [("one1", example_callback1), ("two2", example_callback2)], "Menu")
    menu.refresh()
    key = -1

    while key != 10:
        key = main_window.getch()
        menu.refresh()

        menu.blink()

        if key == 32:
            menu.check()
        elif key == curses.KEY_UP:
            menu.up()
        elif key == curses.KEY_DOWN:
            menu.down()

    teardown(stdscr)

    menu.execute()


if __name__ == '__main__':
    main()
