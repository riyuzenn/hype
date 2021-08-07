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

from hype.cursor import hide as _hide_cursor
from hype.cursor import show as _show_cursor
from typing import Optional
from typing import TextIO

import sys


class Password:
    """
    A simple password prompt that cover the input with '*'.

    Parameters:
    ---

        prompt (str):
            Set the prompt text. Default Value: 'Password'


        hide_cursor (Optional[bool]):
            Set if the cursor is hidden or shown. Default Value: False

        stream (TextIO):
            Set the stream. Usually sys.stdout

        **options:
            res (str): Default Value: *
            prompt_color (str): Set the color of the prompt
            res_color (str): Set the response color or the '*'

    Example:
    ---

        >>> pass = Password()
        >>> print(pass.response) #: or #: print(pass())

    """

    #: Set the buffer
    __buffer = ""

    def __init__(
        self,
        prompt: str = "Password",
        hide_cursor: Optional[bool] = False,
        stream: TextIO = sys.stdout,
        **options,
    ):

        self.prompt = "{}: ".format(prompt)
        self.stream = stream
        self.res = options.get("res") or "*"

        self.prompt_color = options.get("prompt_color") or None
        self.res_color = options.get("res_color") or None

        if self.prompt_color:
            self.prompt = (
                f"{rule_colors[self.prompt_color]}{self.prompt}{rule_colors['reset']}"
            )

        if self.res_color:
            self.res = f"{rule_colors[self.res_color]}{self.res}{rule_colors['reset']}"

        if hide_cursor:
            _hide_cursor()
        else:
            _show_cursor()

        #: Render the output after the initialization.
        self.render()

    @property
    def response(self):
        """
        Get the response from the password
        """
        return self.__buffer

    @property
    def answer(self):
        """
        Same as response, just change the name
        """
        return self.__buffer

    def render(self):
        """
        Render the output to the terminal.

        Parameter:
        ---
            It takes no param

        Example:
        ---

            >>> pass = Password()
            >>> pass.render()

        """

        self.stream.write(self.prompt)
        self.stream.flush()

        while True:
            key = getkey()
            if key == keys.ENTER:
                self.stream.write("\n")
                break

            elif key == keys.BACKSPACE:
                self.__buffer = self.__buffer[:-1]
                self.stream.write(
                    f'\r{(len(self.prompt)+len(self.__buffer)+1)*" "}\r{self.prompt}{"*" * len(self.__buffer)}'
                )
                self.stream.flush()

            elif key == keys.CTRL_C:
                self.stream.write("\n")
                raise KeyboardInterrupt

            else:
                self.__buffer += key
                self.stream.write(self.res)
                self.stream.flush()

        return self.__buffer

    def __call__(self):
        """
        Return the response of the user.

        Example:
        ---
            >>> pass = Password()
            >>> print(pass())

        """

        return self.response
