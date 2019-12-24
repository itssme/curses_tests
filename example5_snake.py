"""
Repository: https://github.com/itssme/python_curses_examples
Desc: Lets the user play Snake on the terminal
Author: https://github.com/itssme
"""

import curses
import time
import random


def setup():
    stdscr = curses.initscr()

    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)
    curses.curs_set(0)

    return stdscr


def teardown():
    curses.endwin()


def new_food(snake, MAX_X, MAX_Y):
    food = snake[0]

    while food in snake:
        food = [random.randint(2, MAX_X - 2), random.randint(2, MAX_Y - 2)]

    return food


def main():
    stdscr = setup()

    MAX_X, MAX_Y = stdscr.getmaxyx()
    main_window = curses.newwin(MAX_X, MAX_Y, 0, 0)

    main_window.nodelay(1)
    main_window.border()
    main_window.keypad(1)

    valid_keys = [
        curses.KEY_UP,
        curses.KEY_DOWN,
        curses.KEY_LEFT,
        curses.KEY_RIGHT
    ]
    alive = True
    snake = [
        (MAX_X // 2, MAX_Y // 2),
        (MAX_X // 2, (MAX_Y // 2) - 1),
        (MAX_X // 2, (MAX_Y // 2) - 2)
    ]
    food = new_food(snake, MAX_X, MAX_Y)
    main_window.addch(food[0], food[1], curses.ACS_DIAMOND)
    usr_input = curses.KEY_UP
    score = 0
    score_window = main_window.subwin(1, 0, 0, 0)
    score_window.addstr("Score: " + str(score))

    while alive:
        start_time = time.time()
        tmp_input = 0
        new_input = usr_input
        while tmp_input != -1:
            new_input = tmp_input
            tmp_input = main_window.getch()
        usr_input = new_input if new_input in valid_keys else usr_input

        score_window.refresh()
        main_window.addch(food[0], food[1], curses.ACS_DIAMOND)
        snake_head = [snake[0][0], snake[0][1]]

        if usr_input == curses.KEY_UP:
            snake_head[0] -= 1
        elif usr_input == curses.KEY_DOWN:
            snake_head[0] += 1
        elif usr_input == curses.KEY_LEFT:
            snake_head[1] -= 1
        elif usr_input == curses.KEY_RIGHT:
            snake_head[1] += 1

        snake.insert(0, snake_head)

        if snake[0][0] in [0, MAX_X - 1] or snake[0][1] in [0, MAX_Y - 1] or snake[0] in snake[1:]:
            alive = False
        else:
            if snake[0] == food:
                food = new_food(snake, MAX_X, MAX_Y)
                main_window.addch(food[0], food[1], curses.ACS_DIAMOND)
                score += round(1 + score * 0.2, 2)
                score_window.erase()
                main_window.border()
                score_window.addstr("Score: " + str(score))
            else:
                tail = snake.pop()
                main_window.addch(tail[0], tail[1], " ")

            main_window.addch(snake[0][0], snake[0][1], " ", curses.A_REVERSE)
        end_time = time.time()

        try:
            time.sleep(0.1 - (end_time - start_time))
        except IOError:
            pass

    for i in range(0, 2):
        curses.flash()
        time.sleep(random.randint(1, 200) / 600.0)

    score_str = "Your Score is: " + str(score)
    end_win_len = MAX_Y // 6
    if end_win_len < len(score_str):
        end_win_len += (len(score_str)-(end_win_len)) + 2
    end_win_height = MAX_X // 6
    if end_win_height < 3:
        end_win_height = 3
    end_screen = main_window.subwin(end_win_height, end_win_len,
                                    (MAX_X // 2) - end_win_height // 2,(MAX_Y // 2) - end_win_len // 2)
    end_screen.erase()
    MAX_X_END, MAX_Y_END = end_screen.getmaxyx()
    end_screen.border()
    end_screen.addstr(0, 1, "Game Over")
    end_screen.addstr(MAX_X_END // 2, (MAX_Y_END // 2) - len(score_str) // 2, score_str)
    end_screen.getch()

    teardown()


if __name__ == '__main__':
    main()
