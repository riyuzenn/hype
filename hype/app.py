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
from typing import Optional
from typing import Any
from typing import Callable
from typing import Tuple
from typing import get_type_hints
from .command import HypeCommand
from .parser import HypeParser
from .utils import CommandDict
from .utils import ParamOption
from .utils import convert_param_to_option
from .utils import convert_option_to_string


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
        
        #: The parser object to be used
        self.__parser = HypeParser
    
    
    @property
    def commands(self):
        """
        All command registered. Return by it's name.
        """
        command_list = []
        for k in self.__commands.keys():
            command_list.append(self.__commands[k]['name'])

        return command_list


    def command(self, name: str = None, 
                usage: Optional[str] = None,
                aliases: Optional[Tuple[Any]] = (),
                help: Optional[str] = '', 
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
            _help = help
                        
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
            
            self.__commands[_name] = CommandDict(_name, _usage, _help, _aliases, params, func).to_dict 

            return func

        
        return deco(func) if func else deco
        

    def run(self):
        """
        Run the application.

        Parameters:
        ---
            it takes no params yet

        Example: 
        `(More example at the examples folder located on github repo.)`

        >>> ...

        """


        commands = []
        required_commands = []
        
        for k in self.__commands.keys():
                        
            _command = HypeCommand(self.__commands[k]['name'], 
                    self.__commands[k]['usage'], self.__commands[k]['aliases'],
                    self.__commands[k]['help']
            )

            if self.__commands[k]['options']:
                for _option in self.__commands[k]['options']:
                    
                    if _option['required']:
                        required_commands.append(
                            (self.__commands[k]['name'], convert_option_to_string(_option['name']))
                        )

                    _command.parser.add_option(
                                _option['name'],  
                                default=_option['default'], 
                                type=_option['type']
                            )

            commands.append(_command)
        
        parser = self.__parser(commands)
        option, command, command_opt, command_args, = parser.parse_args()
        params = []

        for _k, v in vars(command_opt).items():                
            if (command.name, _k) in required_commands and v == None:
                parser.error("Option: {} is required.".format(_k))
                parser.exit()

            params.append(v)

        if command.name in self.__commands:
            self.__commands[command.name]['func'](*params)
            