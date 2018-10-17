#!/usr/bin/env python3
import curses
from curses import wrapper

def main(stdscr):
	# Clear screen
	stdscr.clear()

	message_box = curses.newwin(5, 40, 7, 20)

	# This raises ZeroDivisionError when i == 10.
	for i in range(0, 11):
		# print(i)
	 #    # v = i-10
		stdscr.addstr('hello')

	stdscr.refresh()
	stdscr.getkey()



wrapper(main)