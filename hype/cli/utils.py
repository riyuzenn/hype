
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

from typing import Optional
from typing import Any
from typing import Callable

class CommandDict:
    def __init__(self, *, name: Optional[str] = None, params: Optional[list] = None, 
            desc: Optional[str] = None, type: Optional[Any] = None,
            default: Optional[Any] = None, required: Optional[bool] = False,
            func: Callable[..., Any], deprecated: Optional[bool] = False):

        self.name = name
        self.desc = desc
        self.params = params
        self.default = default
        self.func = func
        self.type = type
        self.req = required
        self.deprecated = deprecated

    def dict(self):
        return { 
            
            self.name: {
                "params": self.params, "desc": self.desc, 
                "default": self.default, "func": self.func, "required": self.req,
                "type": self.type, "deprecated": self.deprecated
            }

        }