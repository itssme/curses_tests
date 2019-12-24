"""
Repository: https://github.com/itssme/python_curses_examples
Desc: Lets the user move a character around in the terminal.
      if called with '--draw' the user can draw characters in the terminal.
Author: https://github.com/itssme
"""

import curses
from sys import argv


def setup():
    stdscr = curses.initscr()

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


def main():
    stdscr = setup()
    curses.curs_set(0)

    MAX_X, MAX_Y = stdscr.getmaxyx()

    main_window = curses.newwin(MAX_X, MAX_Y, 0, 0)
    main_window.keypad(1)

    player = [MAX_X//2, MAX_Y//2]
    alive = True

    draw_letter = "+"
    main_window.addch(player[0], player[1], draw_letter)

    while alive:
        key = main_window.getch()

        if key == curses.KEY_UP:
            player[0] -= 1
        elif key == curses.KEY_DOWN:
            player[0] += 1
        elif key == curses.KEY_LEFT:
            player[1] -= 1
        elif key == curses.KEY_RIGHT:
            player[1] += 1
        else:
            draw_letter = chr(key if 0 <= key < 256 else ord(draw_letter))

        if player[0] in [0, MAX_X] or player[1] in [0, MAX_Y]:
            alive = False
        else:
            if "--draw" not in argv:
                main_window.erase()
            main_window.addch(player[0], player[1], draw_letter)

    teardown(stdscr)


if __name__ == '__main__':
    main()
