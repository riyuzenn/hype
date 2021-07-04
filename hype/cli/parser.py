
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

from optparse import Option, OptionParser
import sys
from typing import Iterable, Optional
from typing import Callable
from typing import List
from typing import Any


class HelpCommand:
    """
    A default help command for Hype CLI.   
    """

class HypeParser:
    """
    A argument parser for Hype CLI.

    """

    __args = {}

    def __init__(self, usage: Optional[str] = None,
            help_command: Callable[..., Any] = HelpCommand ):


        #: Simple usage format for the parser. 
        #: Default Value: None
        self.usage = usage

        #: You may define your own help command. by creating a help command class.
        #: Default value: HelpCommand `:class:`
        self.help_command = help_command


    def add_argument(self, args_name, full_args_name: Optional[str] = None, 
                description: Optional[str] = None, value: Option[Any] = None, 
                type: Optional[Any] = None, required: Optional[bool] = False, 
                deprecated: Optional[bool] = False, hidden: Optional[bool] = False):
        
        """
        Add the single argument to be parsed to.
        It can be Any type of argument.

        Parameters:
            args_name (str):
                The name of the argument. It can be single character or a full string
            
            full_args_name (str):
                The full argument name. You can define this if the arg name is single char


            description (str):
                The description for the command. 

            value (Any):
                Set the default value of the command.

            type (Any):
                Set the type of the argument to be parsed.

            required (bool):
                Set if the argument is required. Default Value: False

            deprecated (bool):
                Set if the argument is deprecated. Default Value: False

            hidden (bool):
                Set if the argument is hidden to the help command. Default Value: False
        
        Example:

            >>> parser = HypeParser(...)
            >>> ...
            >>> parser.add_argument('g', 'greet', type=str, required=True)
            >>> ...
        """

        if full_args_name != None:
            self.__args.update({
                args_name: { 
                    "full_args_name": full_args_name, "desc": description,
                    "type": type, "value": value, "required": required, 
                    "deprecated": deprecated, "hidden": hidden
                } 
            })

        else:
            self.__args.update({
                args_name: { 
                    "desc": description,
                    "type": type, "value": value, "required": required, 
                    "deprecated": deprecated, "hidden": hidden
                } 
            })
        
        
    