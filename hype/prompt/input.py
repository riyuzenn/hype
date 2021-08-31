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
from hype.prompt.error import error

from hype.constants import rule_colors
from hype.constants import COLOR_SUPPORTED

from hype.cursor import hide as _hide_cursor
from hype.cursor import show as _show_cursor
from typing import Callable, Optional
from typing import TextIO
from typing import Any

import ast
import sys


class Input:
    """
    A simple input prompt that has color response and validator
    When defining `validator` make sure the `validator_msg` is defined.

    Parameters:
    ---

        prompt (str):
            Set the prompt text.


        hide_cursor (Optional[bool]):
            Set if the cursor is hidden or shown. Default Value: False

        stream (TextIO):
            Set the stream. Usually sys.stdout

        validator (Function):
            The validator function that accept the response text

        validator_msg (str):
            The message when the validator fails

        **options:
            res (str): The color while the input is running
            prompt_color (str): Set the color of the prompt
            res_color (str): Set the response color after pressing enter

    Example:
    ---

        >>> name = Input('What is your name')
        >>> print(name.response) #: or #: print(name())

    """

    #: Set the buffer
    text = ""
    _validator = None
    _is_valid = True
    _validator_msg = None

    def __init__(
        self,
        prompt: str,
        hide_cursor: Optional[bool] = False,
        stream: TextIO = sys.stdout,
        validator: Callable[..., Any] = None,
        validator_msg: Optional[str] = None,
        **options,
    ):

        self.prompt = "{}: ".format(prompt)
        self.stream = stream

        self.prompt_color = options.get("prompt_color", None)
        self.res_color = options.get("res_color", 'magenta') 
        self.res = options.get('res', None)

        if self.prompt_color:
            self.prompt = (
                f"{rule_colors[self.prompt_color]}{self.prompt}{rule_colors['reset']}"
            )

        if hide_cursor:
            _hide_cursor()
        else:
            _show_cursor()

        if validator and not validator_msg:
            raise ValueError('Validator msg is not define')
        
        self._validator = validator
        self._validator_msg = validator_msg
        
        #: Render the output after the initialization.
        self.render()

    @property
    def response(self):
        """
        Get the response from the input
        """
        return self.text

    @property
    def answer(self):
        """
        Same as response, just change the name
        """
        return self.text


    def render(self):
        """
        Render the output to the terminal.

        Parameter:
        ---
            It takes no param

        Example:
        ---

            >>> input = Input()
            >>> input.render()

        """

        self.stream.write(self.prompt)
        self.stream.flush()

        while True:
        
            key = getkey()
            
            if key == keys.ENTER:
                if self._validator:
                    self._is_valid = self._validator(self.text)
                    if not isinstance(self._is_valid, bool):
                        raise ValueError(
                            'The validator `%s` should return True or False' % 
                            (self._validator.__name__)
                        )

                if not self._is_valid:
                    error(msg=self._validator_msg, duration=1)
                    continue

                self.stream.write(
                    f"\r{self.prompt}{rule_colors[self.res_color]}{self.text}{rule_colors['reset']}"
                )

                self.stream.write("\n")
                break

            elif key == keys.BACKSPACE:
                self.text = self.text[:-1]
                self.stream.write(
                    f'\r{(len(self.prompt)+len(self.text)+1)*" "}\r{self.prompt}{self.text[:len(self.text)]}'
                )
                self.stream.flush()

            elif key == keys.CTRL_C:
                self.stream.write("\n")
                raise KeyboardInterrupt

            else:
                self.text += key
                if self.res:
                    self.stream.write(
                        f"{rule_colors[self.res]}{key}{rule_colors['reset']}"
                    )
                else:
                    self.stream.write(key)

                self.stream.flush()

        return self.text

    def __call__(self):
        """
        Return the response of the user.

        Example:
        ---
            >>> input = Input()
            >>> print(input())

        """

        return self.response
