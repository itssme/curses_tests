"""
Repository: https://github.com/itssme/python_curses_examples
Desc: Waits for the user to type in 10 Characters and then displays them on the screen.
Author: https://github.com/itssme
"""

import curses


def main():
    stdscr = curses.initscr()

    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)

    key = "".join([chr(stdscr.getch()) for i in range(0, 10)])

    stdscr.addstr(key)

    stdscr.getch()

    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()


if __name__ == '__main__':
    main()