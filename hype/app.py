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


import sys
import inspect
from typing import Optional, TypeVar
from typing import Any
from typing import Callable
from typing import Tuple
from typing import TYPE_CHECKING
from typing import get_type_hints
from .command import HypeCommand
from .utils import CommandDict, ParamOption
from .utils import convert_param_to_option


class Hype:
    """
    The main application for the CLI.

    Parameters:
        -
    
    Example:
        
        >>> app = HypeCLI()
        >>> @app.command()
        >>> def greet(name: str):
        >>>     print("hello, {}".format(name))
        >>> ...
        >>> if __name__ == "__main__":
        >>>     app.run()
    
    """

    __commands = {}

    def __init__(self):
        pass


    def command(self, name: str = None, 
                usage: Optional[str] = None,
                aliases: Optional[Tuple[Any]] = None,
                help: Optional[str] = None, 
                func: Callable[..., Any] = None,):

        """
        A command decorator for HypeCommand.

        Parameters:
            name (str): 
                The name of the command, if None return the function name

            usage (str):
                The usage format of the command.

            aliases (tuple):
                A tuple of aliases of the command.
            
            help (str):
                The help format of the command.

        """
 

        #: set the usage of the command
        _usage = usage

        #: Set the aliases of the command
        _aliases = aliases


        def deco(func): 
            
            #: Set the name of the command.
            #: If the name is none, return the name of the function
            _name = name if name else func.__name__
            
            #: Set the help of the command
            _help = help if help else func.__doc__

            #: The signature of the function
            signature = inspect.signature(func)

            #: Type hints of the function
            type_hints = get_type_hints(func)
            
            #: Set the params to none dict. It should contain the param of the function
            #: and the type hints of the parameters 
            params = []

            for param in signature.parameters.values():
                #: The annotation of the function.
                #: For example: def func(name: str) -> str is the annotaiton
                annotation = param.annotation
                
                if param.name in type_hints:
                    annotation = type_hints[param.name]

                required = True if param.default is inspect.Parameter.empty else False
                default = param.default if param.default is not inspect.Parameter.empty else None
                anon = annotation if annotation is not inspect.Parameter.empty else None
                

                optionparam = ParamOption(convert_param_to_option(param.name), required, default, anon)
                params.append(optionparam.to_dict)
                
            self.__commands[func] = CommandDict(_name, _usage, _help, _aliases, params).to_dict 

            return func

        
        return deco(func) if func else deco
        


    def run(self):
        print(self.__commands)

