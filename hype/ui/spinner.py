#                   Copyright (c) 2021, Serum Studio
#   Copyright (c) Sindre Sorhus <sindresorhus@gmail.com> (sindresorhus.com)

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

#: Spinner frames are https://github.com/sindresorhus

import itertools
import sys
import time
from typing import Optional
from typing import Any
from .constants import SpinnerType
from hype.cursor import hide as hide_cursor
from hype.cursor import show as show_cursor
import threading
from hype.constants import COLOR_SUPPORTED
from hype.constants import rule_colors


class SpinnerNotFound(Exception):
    pass


class SpinnerError(Exception):
    pass


class Spinner:
    """
    A spinner animation based on https://github.com/sindresorhus Spinner Frames.

    Parameters:
    ---

        text (str):
            The text that is printed next to the spinner

        type (str):
            Spinner type. see documentation for more info. or check out `hype.ui.constants`

        cursor (bool):
            Set if the cursor is hidden or shown


    Example:
    ---

        >>> from hype.ui import Spinner
        >>> with Spinner('Loading', type='arc') as spinner:
        >>>     spinner.start() # Start the spinner


    """

    #: Set the stop event to None
    __stop_event = None

    #: Set the stop event to None
    __thread = None

    #: Set the stop event to None
    __thread_id = None

    def __init__(
        self,
        text: Optional[Any] = "",
        type: Optional[str] = "dots",
        cursor: Optional[bool] = False,
        color: Optional[str] = None,
    ):

        self.text = text
        self.type = type
        self.stream = sys.stdout
        self.color = color

        if self.color and COLOR_SUPPORTED == False:
            raise SpinnerError(
                "Colors are not supported. Install using `pip install hypecli[color]`"
            )

        if cursor == False:
            hide_cursor()

    def render(self):
        """
        Render the spinner to the terminal
        """
        if self.type not in SpinnerType.keys():
            raise SpinnerNotFound("%s is not supported." % (self.type))

        frames = SpinnerType[self.type]["frames"]
        interval = 0.001 * SpinnerType[self.type]["interval"]
        spinner = itertools.cycle(frames)

        while not self.__stop_event.set():

            if self.color:
                output = "\r{0}{1}{2} {3}".format(
                    rule_colors[self.color],
                    next(spinner),
                    rule_colors["reset"],
                    self.text,
                )
            else:
                output = "\r{0} {1}".format(next(spinner), self.text)

            self.stream.write(output)
            self.stream.write("\033[K")  #: Clear line
            self.stream.flush()
            self.stream.write("\b")
            time.sleep(interval)

        return self

    @property
    def id(self):
        """
        Get the thread id. For some purposes..
        """
        return self.__thread_id

    @id.setter
    def id(self, value):
        return value

    def start(self):

        self.__thread = threading.Thread(target=self.render)
        self.__stop_event = threading.Event()
        self.__thread_id = self.__thread.name
        self.__thread.setDaemon(True)
        self.__thread.start()

        return self

    def stop(self):
        """Stop the thread on running"""

        if self.__thread and self.__thread.is_alive():
            self.__stop_event.set()

        self.stream.write("\r")
        self.stream.write("\033[K")  #: Clear line
        self.id = None
        show_cursor()
        return self

    def __enter__(self):
        """When the `with` statement opens."""

        return self.start()

    def __exit__(self, type, value, tracerback):
        """When the `with` statement ends"""

        return self.stop()
