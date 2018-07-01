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

    def __init__(self, parent_window, nlines, ncols, begin_y, begin_x, text=""):
        self.window = parent_window.subwin(nlines, ncols, begin_y, begin_x)
        self.MAX_X, self.MAX_Y = self.window.getmaxyx()
        self.window.border()
        self.checkbox = self.window.subwin(1, 1, 1, 1)
        self.__fit_text(str(self.MAX_Y))

    def __fit_text(self, text):
        self.window.addstr(self.MAX_X/2, self.MAX_Y-len(text) - 1, text)

    def check(self):
        pass


def main():
    stdscr = setup()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.color_pair(1)

    MAX_X, MAX_Y = stdscr.getmaxyx()

    main_window = curses.newwin(MAX_X, MAX_Y, 0, 0)
    main_window.keypad(1)

    main_window.border()
    main_window.subwin(10, 10, 10, 10).subwin(1, 1, 1, 1).border()
    #option_1 = Option(main_window, 3, 20, MAX_X/2, MAX_Y/2, "hallo")

    main_window.getch()

    teardown(stdscr)


if __name__ == '__main__':
    main()
