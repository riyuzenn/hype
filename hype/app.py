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


import functools
import inspect
import sys

from typing import Optional
from typing import Any
from typing import Callable
from typing import Tuple
from typing import get_type_hints

from .command import HypeCommand
from .parser import HypeParser
from .print import print as _print

from .constants import rule_colors
from .constants import bg_colors
from .style import Background

from .utils import CommandDict
from .utils import ParamOption
from .utils import OptionDict
from .utils import create_bool_option
from .utils import convert_param_to_option
from .utils import convert_option_to_string

from .errors import ColorNotFound


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
    __required_commands = []
    __commands_function = {}
    __registered_args = {}

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
            command_list.append({self.__commands[k]["name"]: self.__commands[k]['help']})

        return command_list

    def echo(self, text: str = "", **options):
        """
        A format wrapper for the hype.print. It can print
        text with colors and styles. using the tag [%tagname%][/]

        Parameters:
        ---
            text (object):
                The value to be printed.

            **options(dict):
                A kwarg of options.

        Available Options:
        ---

        - style
        - foreground
        - color

        Available Color Tags:
        ---

        > For more info check the constant dictionary `hype.constants.rule_colors`

        - blue
        - red
        - yellow
        - magenta
        - green
        - black
        - cyan

        Example:
        ---

            >>> app = Hype()
            >>> app.echo('[red]This is a red color![/]')

        """

        background = options.get("background") or None

        if background in bg_colors:
            _print("%s%s%s" % (bg_colors[background], text, bg_colors["reset"]))

        elif background not in bg_colors and background != None:
            raise ColorNotFound("%s is not yet supported." % (background))

        else:
            _print(text)

    def command(
        self,
        name: str = None,
        usage: Optional[str] = None,
        aliases: Optional[Tuple[Any]] = (),
        help: Optional[str] = "",
    ):

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

        Example:

            >>> @app.command()
            >>> def greet(name: str):
            >>>     \"\"\"
            >>>     Greet the user
            >>>     \"\"\"
            >>>     app.echo(f'Hello {name}')

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
            _help = help or 'This command accept a positional arguments'

            #: The signature of the function
            signature = inspect.signature(func)

            #: Type hints of the function
            type_hints = func.__annotations__

            #: Set the params to none dict. It should contain the param of the function
            #: and the type hints of the parameters
            params = []

            for param in signature.parameters.values():
                #: The annotation of the function.
                #: For example: def func(name: str) -> str is the annotaiton
                annotation = param.annotation
                
                if param.name in type_hints:
                    annotation = type_hints[param.name]

                if param.name not in self.__registered_args.keys():
                    required = True if param.default is inspect.Parameter.empty else False
                    default = (
                        param.default
                        if param.default is not inspect.Parameter.empty
                        else None
                    )
                    anon = annotation if annotation is not inspect.Parameter.empty else None

                    optionparam = ParamOption(
                        convert_param_to_option(param.name),
                        required,
                        default,
                        anon,
                        param.name,
                    )
                    params.append(optionparam.to_dict)

            self.__commands[_name] = CommandDict(
                _name, _usage, _help, _aliases, params, func
            ).to_dict
            self.__commands_function[func] = {"name": _name}

            return func

        return deco

    def argument(self, name: str, type: Optional[Any] = None):
        """
        A argument decorator for registering arguments. 
        Please take note that when you define argument, make sure
        the name of the argument is on the first parameter of the 
        function.
        
        Parameters:
        ---
            name (str):
                The name of the argument.
            
            type (Optional[Any]):
                The type of the argument.

        Examples:
        ---
            >>> @app.command()
            >>> @app.argument('option')
            >>> def upload(option, debug: bool=False):
            >>>     ...
            >>>     #: Make sure the option argument always on the first one.
            >>>     app.echo(option)

        """
        def deco(func):
            self.__registered_args[name] = {'type': type}
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs) 

            return wrapper
        return deco

    def exit(self):
        """
        Exit the all application instance without using standard `sys.exit()`

        Parameters:
        ---
            It takes no params yet

        Example:
        ---
            >>> import os
            >>> ...
            >>> @app.command()
            >>> def upload(path: str):
            >>>     if os.path.exists(path):
            >>>         app.echo(f'Path: {path} doesnt exist')
            >>>         app.exit()
            >>>     ...
            >>>     app.echo(f'File Uploaded: {path}')

        """

        try:
            self.__parser.exit()
        except Exception:
            pass

        sys.exit()

    def run(self):
        """
        Run the application.

        Parameters:
        ---
            it takes no params yet

        Example:
        `(More example at the examples folder located on github repo.)`


            >>> from hype import Hype
            >>> app = Hype()
            >>> ...
            >>> @app.command()
            >>> def greet(name: str):
            >>>     app.echo(f'Hello, {name}')
            >>> ...
            >>> @app.command()
            >>> def goodbye(name: str):
            >>>     app.echo(f'Goodbye, {name}')

            >>> if __name__ = "__main__":
            >>>     app.run()

        """

        commands = []
        boolean_options = []

        for k in self.__commands.keys():

            self.__command_parser = HypeCommand(
                self.__commands[k]["name"],
                self.__commands[k]["usage"],
                self.__commands[k]["aliases"],
                self.__commands[k]["help"],
            )

            if self.__commands[k]["options"]:
                for _option in self.__commands[k]["options"]:

                    if _option["required"]:

                        self.__required_commands.append(
                            (
                                self.__commands[k]["name"],
                                convert_option_to_string(_option["name"]),
                            )
                        )

                    name = _option["name"]

                    if _option["action"]:

                        bool_name = create_bool_option(_option["name"])
                        for bname in bool_name:

                            if bname == _option["name"]:
                                self.__command_parser.parser.add_option(
                                    _option["name"],
                                    default=_option["default"],
                                    dest=_option["dest"],
                                    action=_option["action"],
                                    metavar=_option["metavar"],
                                )
                            else:
                                self.__command_parser.parser.add_option(
                                    bname,
                                    default=_option["default"],
                                    dest=_option["dest"],
                                    action="store_false",
                                    metavar=_option["metavar"],
                                )

                    else:
                        if isinstance(name, str):

                            self.__command_parser.parser.add_option(
                                name,
                                default=_option["default"],
                                type=_option["type"],
                                dest=_option["dest"],
                                metavar=_option["metavar"],
                            )

                        else:
                            self.__command_parser.parser.add_option(
                                *name,
                                default=_option["default"],
                                type=_option["type"],
                                dest=_option["dest"],
                                metavar=_option["metavar"]
                            )

            commands.append(self.__command_parser)

        parser = self.__parser(commands)

        (
            option,
            command,
            command_opt,
            command_args,
        ) = parser.parse_args()

        params = []

        for i in boolean_options:
            self.__command_parser.parser.add_option(
                i["name"], default=i["default"], type=i["type"], action=i["action"]
            )

        if command_args:
            for i in range(len(self.__registered_args)):
                for k in self.__registered_args.keys():
                    if self.__registered_args[k]['type']:
                        self.__registered_args[k]['type'](command_args[i])
                        # del self.__registered_args[k]['type']

                    self.__registered_args[k] = command_args[i]

                params.append(command_args[i])   

        for _k, v in vars(command_opt).items():
            if (command.name, _k) in self.__required_commands and v == None:
                parser.error("Option: {} is required.".format(_k))
                parser.exit()

            
            params.append(v)

        if command.name in self.__commands:
            self.__commands[command.name]["func"](*params)
