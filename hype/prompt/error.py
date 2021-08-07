#                   Copyright (c) 2021, Serum Studio

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


from hype.cursor import hide as hide_cursor
from hype.cursor import show as show_cursor

from hype.constants import COLOR_SUPPORTED
from hype.constants import bg_colors
from typing import Optional

import time
import os
import sys


def pprint(x: int, y: int, text: str):
    """
    A printing function that requires a postiion where the text
    is printed.

    PPrint stand for "Positional Printing"

    Parameters:
    ---
        x (int):
            The x position

        y (int):
            The y position

        text (str):
            The text to be printed.

    """

    sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x, y, text))
    sys.stdout.flush()


def error(
    msg: Optional[str] = "An error occured.",
    duration: Optional[int] = 3,
    height: Optional[int] = os.get_terminal_size().lines,
    width: Optional[int] = os.get_terminal_size().columns,
):

    """

    A function for printing error on a bottom part of the terminal.
    That vanish on a given duration.

    Parameters:
    ---
        msg (str):
            The error message to display.

        duration (int):
            The duration of the error.

        height: (Optional[int]):
            The height of the terminal

        width: (Optional[int]):
            The width of the terminal.

    """

    msg = bg_colors["red"] + msg.ljust(width - 10, " ") + bg_colors["reset"]
    invisible_msg = " " * len(msg)  #: Blank msg replacing the error for disappearing.

    for i in range(duration):
        hide_cursor()

        pprint(height - 1, 5, msg)
        time.sleep(duration)
        pprint(height - 1, 5, invisible_msg.ljust(width - 10, " "))

    show_cursor()
