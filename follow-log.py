#!/usr/bin/env python

"""
Follows the process of log.txt (or any specified filename)
containing the output of ./naive.py, and shows what file
each process is currently working on.

Slow files will be marked with "!", and files that might
be permanently stuck are marked with "!!".

(Except at the end, when all processes will be marked with !!,
since there's no signal in the log file that a process has
finished all the files it was asked to do.)
"""

import argparse
import curses
import re
import time
from typing import Tuple

import nicer

STUCK_ITERS = 20  # how many display iterations before we declare a file stuck"
SLOW_ITERS = 8  # how many display iterations before we declare a file slow
SECONDS_PER_ITERATION = 1
REFRESH_INTERVAL = 60   # completely redraw the screen every this many iterations


def display_loop(stdscr, fd):
    "Display the most recent input files for each ./naive.py process"

    # keep track of the number of times the display has been updated.
    # (files that haven't changed after many display updates are possibly
    # stuck, and worth noting.)
    display_iter = 0

    # mapping from PIDs (as strings) to the texes input file they are working
    # on *and* the number of display updates when the file was first
    # encountered.
    worklog: dict[str, Tuple[str, int]] = {}

    maxy, maxx = stdscr.getmaxyx()

    while True:
        # Read the next line of the file
        line: str = fd.readline()
        if line:
            # A process has started a new file if we find a line
            # that contains just a number and a filename (with whitespace)
            m = re.fullmatch(r"\s*(\d{1,5})\s+(.*?)\s*", line)
            if m:
                # Process is working on a new file; update the worklog
                pid = m.group(1)
                file = m.group(2)
                worklog[pid] = (file, display_iter)
        else:
            if curses.is_term_resized(maxy, maxx):
                stdscr.clear()
                maxy, maxx = stdscr.getmaxyx()
                curses.resizeterm(maxy, maxx)
                resized_term = True
            else:
                resized_term = False
            # We've reached the end of the log file (for the moment!)
            # so it's a good time to update the display.
            row = 2
            for pid, (current_file, n) in sorted(worklog.items()):
                # To facilitate copying-and-pasting filenames while the
                # screen is updating, only redraw the lines that have
                # changed since the last updated (or if we're redrawing
                # everything)
                updated_line = (resized_term or
                    display_iter % REFRESH_INTERVAL == 0)
                flag = "  "
                if display_iter - n == 0:
                    # new file for this process
                    # flag = "  "
                    updated_line = True
                elif display_iter - n == SLOW_ITERS:
                    # mark process as slow
                    flag = "! "
                    updated_line = True
                elif display_iter - n == STUCK_ITERS:
                    # mark process as (potentially) stuck
                    flag = "!!"
                    updated_line = True

                if updated_line and row < maxy:
                    # Update this line
                    stdscr.addstr(row, 2, f"{flag} {pid:5} {current_file}")
                    # In case this filename is shorter than the previous
                    # filename, clear the rest of the line
                    stdscr.clrtoeol()
                row += 1

            # Drawing the border also helps facilitate copying-and-pasting
            #   (because all screen lines have basically the same length
            #    due to the left and right borders).
            # We redraw the border every interval because clrtoeol()
            #   tends to erase the right border of changed lines.
            stdscr.border()
            # Display the updated list of files to the user.
            stdscr.refresh()
            display_iter += 1
            # If we wait a bit, perhaps more lines will appear in our log file.
            time.sleep(SECONDS_PER_ITERATION)


if __name__ == "__main__":
    # This program shouldn't be putting a noticeable load on Ark,
    # but make sure it's Ark-friendly just in case.
    nicer.make_nice()

    # By default we display output from log.txt, but the user
    # can choose to specify a different filename.
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="?", default="log.txt")
    args = parser.parse_args()

    with open(args.file, "r") as fd:
        # initialize the text-display functionality,
        # and call display_loop with a handle to the
        # terminal window and the log-file handle.
        curses.wrapper(display_loop, fd)
