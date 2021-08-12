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


from hype.errors import PluginError
from hype.prompt.getkey import getkey
from hype.prompt.getkey import keys

from hype.constants import rule_colors
from hype.constants import COLOR_SUPPORTED

from hype.prompt.error import error

from hype.cursor import hide as _hide_cursor
from hype.cursor import show as _show_cursor
from typing import Optional
from typing import TextIO

import sys


class Confirm:
    """
    A simple confirm prompt that return True or False.

    Parameters:
    ---

        prompt (str):
            Set the prompt text.


        default (Optional[bool]):
            Set the default value.


        hide_cursor (Optional[bool]):
            Set if the cursor is hidden or shown. Default Value: False

        stream (TextIO):
            Set the stream. Usually sys.stdout

        **options:
            prompt_color (str): Set the color of the prompt
            color (str): Set the response color. Default Value: cyan

    Example:
    ---

        >>> value = Confirm()
        >>> print(value.response) #: or #: print(value())

    """

    #: Set the user response
    __res = None

    #: Set the returned value for the confirm
    __yes_no = {True: "Yes", False: "No"}

    def __init__(
        self,
        prompt: str,
        default: Optional[bool] = None,
        hide_cursor: Optional[bool] = False,
        stream: TextIO = sys.stdout,
        **options,
    ):

        self.prompt = "{}? {}[y/n]{}: ".format(
            prompt, rule_colors["magenta"], rule_colors["reset"]
        )
        self.default = default
        self.stream = stream

        self.prompt_color = options.get("prompt_color") or None
        self.color = options.get("res_color") or "cyan"

        if hide_cursor:
            _hide_cursor()
        else:
            _show_cursor()

        #: Render the output after the initialization.
        self.render()

    def __color_output(self, text: str, color: str):
        return f"{rule_colors[color]}{text}{rule_colors['reset']}"

    @property
    def response(self):
        """
        Get the response from the value
        """
        return self.__res

    @property
    def answer(self):
        """
        Same as response, just change the name
        """
        return self.__res

    def render(self):
        """
        Render the output to the terminal.

        Parameter:
        ---
            It takes no param

        Example:
        ---

            >>> value = Confirm()
            >>> value.render()

        """

        self.stream.write(self.prompt)
        self.stream.flush()

        while True:
            key = getkey()
            if key == keys.ENTER:

                if self.default:
                    self.__res = self.default
                    self.stream.write(
                        self.__color_output(self.__yes_no[self.__res], self.color)
                    )
                    self.stream.write("\n")
                    break

                else:
                    error("Please enter Yes or No only.")
                    continue

            elif key.lower() == "y":
                self.__res = True
                self.stream.write(
                    self.__color_output(self.__yes_no[self.__res], self.color)
                )

                self.stream.write("\n")
                break

            elif key.lower() == "n":
                self.__res = False
                self.stream.write(
                    self.__color_output(self.__yes_no[self.__res], self.color)
                )
                self.stream.write("\n")
                break

            elif key == keys.CTRL_C:
                self.stream.write("\n")
                raise KeyboardInterrupt

            else:
                continue

        return self.__res

    def __call__(self):
        """
        Return the response of the user.

        Example:
        ---
            >>> value = Confirm('Would you like to quit')
            >>> value(value())

        """

        return self.response
