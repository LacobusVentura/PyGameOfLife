################################################################################################
#	MIT License
#
#	Copyright (c) 2023 Tiago Ventura
#
#	Permission is hereby granted, free of charge, to any person obtaining a copy
#	of this software and associated documentation files (the "Software"), to deal
#	in the Software without restriction, including without limitation the rights
#	to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#	copies of the Software, and to permit persons to whom the Software is
#	furnished to do so, subject to the following conditions:
#
#	The above copyright notice and this permission notice shall be included in all
#	copies or substantial portions of the Software.
#
#	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#	IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#	AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#	LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#	OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#	SOFTWARE.
################################################################################################

import random
import time
import curses as _curses

FPS = 10
ALIVE = 10

def screen_initialize():
	stdscr = _curses.initscr()
	_curses.noecho()
	_curses.cbreak()
	_curses.curs_set(False)
	if _curses.has_colors():
		_curses.start_color()
	stdscr.keypad(True)
	return stdscr, _curses

def screen_finish(stdscr):
	stdscr.keypad(False)
	_curses.endwin()

def fishtank_create(ncols, nlines, population):
	random.seed(time.time())
	return [[random.randint(0, 100) < population
		for _ in range(ncols)]
			for _ in range(nlines)]

def fishtank_read(fishtank, nline, ncol):
	nlines, ncols = len(fishtank), len(fishtank[0])
	if(nline >= nlines):
		nline = 0
	if(nline < 0):
		nline = nlines - 1
	if(ncol >= ncols):
		ncol = 0
	if(ncol < 0):
		ncol = ncols - 1
	return fishtank[nline][ncol]

def fishtank_write(fishtank, nline, ncol, value):
	nlines, ncols = len(fishtank), len(fishtank[0])
	if(nline >= nlines):
		nline = 0
	if(nline < 0):
		nline = nlines - 1
	if(ncol >= ncols):
		ncol = 0
	if(ncol < 0):
		ncol = ncols - 1
	fishtank[nline][ncol] = value

def fishtank_iterate(fishtank):
	next_fishtank = [line[:] for line in fishtank]
	nlines, ncols = len(fishtank), len(fishtank[0])
	for nline in range(nlines):
		for ncol in range(ncols):
			try:
				neighboard = 0

				if fishtank_read(fishtank, nline + 1, ncol + 1):
					neighboard += 1

				if fishtank_read(fishtank, nline + 1, ncol):
					neighboard += 1

				if fishtank_read(fishtank, nline, ncol + 1):
					neighboard += 1

				if fishtank_read(fishtank, nline - 1, ncol + 1):
					neighboard += 1

				if fishtank_read(fishtank, nline + 1, ncol - 1):
					neighboard += 1

				if fishtank_read(fishtank, nline - 1, ncol - 1):
					neighboard += 1

				if fishtank_read(fishtank, nline - 1, ncol):
					neighboard += 1

				if fishtank_read(fishtank, nline, ncol - 1):
					neighboard += 1

				if fishtank_read(fishtank, nline, ncol):
					fishtank_write(next_fishtank, nline, ncol, neighboard in (2, 3))
				else:
					fishtank_write(next_fishtank, nline, ncol, neighboard == 3)

			except IndexError as e:
				pass

	return next_fishtank


def fishtank_refresh(stdscr, fishtank):
	for nline, lines in enumerate(fishtank):
		for ncol, col in enumerate(lines):
			try:
				stdscr.addstr(ncol, nline, '★' if col else ' ')
			except Exception as e:
				pass
	stdscr.refresh()

def main():
	stdscr, curses = screen_initialize()
	fishtank = fishtank_create(curses.LINES, curses.COLS, ALIVE)

	try:
		while True:
			fishtank_refresh(stdscr, fishtank)
			time.sleep(1 / FPS)
			fishtank = fishtank_iterate(fishtank)
	except KeyboardInterrupt as e:
		pass

	screen_finish(stdscr)

if __name__ == "__main__":
	main()

# eof #
