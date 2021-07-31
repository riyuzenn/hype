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
from .constants import rule_colors


logger = logging.getLogger(__name__)

try:

    import colorama
    colorama.init()

except ModuleNotFoundError:
    logger.warning('Colors are not supported..')


def check_for_color(string: str=None):
    pass

def print(

    *value: Any,
    sep: Optional[str] = " ",
    end: Optional[str] = "\n",
    file: Optional[IO[str]] = None,
    flush: Optional[bool] = False,
    **options
):

    background = options.get('background') or None
    color = options.get('color') or None
    background = options.get('style') or None

    