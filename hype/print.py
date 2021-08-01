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

#: This source file is responsibble for printing output with styles and colors.

from typing import IO
from typing import Optional
from builtins import print as _print
from .errors import PluginError

try:
    from .color import print_color
except PluginError:
    print_color = None


def print(
    value: str = "",
    sep: Optional[str] = " ",
    end: Optional[str] = "\n",
    file: Optional[IO[str]] = None,
    flush: Optional[bool] = False,
):

    """
    A wrapper for both color printing from `hype.color.print_color`
    and a standart print function.

    Parameters:
    ---
        Same as print().

    Example:
    ---

        >>> from hype import print
        >>> print('[red]This is red[/]') # Hype Color should be supported.
        >>> print('No Color, standart print function') # No color installed.

    """

    try:

        print_color(value, sep=sep, end=end, file=file, flush=flush)

    except AttributeError:

        _print(value, sep=sep, end=end, file=file, flush=flush)
