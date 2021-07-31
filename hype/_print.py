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

from typing import Any
from typing import IO
from typing import Optional
import logging
from .style import Color
from .style import Style
from .style import Background
from .style import Cursor
from .color import _print_color
from builtins import print as _print


logger = logging.getLogger(__name__)

try:

    import colorama

    colorama.init()

except ModuleNotFoundError:
    logger.warning("Colors are not supported..")


def print(
    *value: Any,
    sep: Optional[str] = " ",
    end: Optional[str] = "\n",
    file: Optional[IO[str]] = None,
    flush: Optional[bool] = False,
):

    try:

        _print_color(
            value, 
            sep=sep, 
            end=end, 
            file=file, 
            flush=flush
        )

    except AssertionError:
        _print(
            value, 
            sep=sep, 
            end=end, 
            file=file, 
            flush=flush
        )
