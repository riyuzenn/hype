
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
from typing import Optional
from typing import Callable
from typing import List
from typing import Any
from optparse import OptionParser
from .errors import HypeException
from .errors import TooMuchArguments

class OptionParser(OptionParser):
    """
    Option Parser that is used on decorator 
    @app.option().
    """

    pass

    
class HelpCommand:
    """
    A default help command for Hype CLI.   
    """

    def __init__(self, commands: dict = None, 
                banner: Optional[str] = None):

        self.banner = banner
        self.commands = commands


    def __call__(self):
        
        if self.banner:
            print(self.banner)
        
        print("\nUsage {} [COMMANDS] ".format(sys.argv[0]))
        print("\nAll commands available:")
        print("-" * 50)
        for command in self.commands.keys():
            print(f"{command} - {self.commands[command]['desc']}", end="\n")

        print("")
        

class HypeParser:
    """
    A argument parser for Hype CLI This is only used for non-dashed command
    and can be only used by decorator `@app.command`.

    

    """

    __args = {}
    __sys_args = sys.argv

    def __init__(self, usage: Optional[str] = None,
            help_command: Callable[..., Any] = None ):


        #: Simple usage format for the parser. 
        #: Default Value: None
        self.usage = usage

        #: You may define your own help command. by creating a help command class.
        #: Default value: HelpCommand `:class:`
        self.help_command = help_command or HelpCommand()
        

    def add_argument(self, args: str, 
                description: Optional[str] = None, value: Optional[Any] = None, 
                type: Optional[Any] = None, svalue: Optional[int] = 1, required: Optional[bool] = False,
                deprecated: Optional[bool] = False):
        
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
            >>> parser.add_argument('greet', type=str, required=True)
            >>> ...
        """
        
        if required and description != None:
            description = description + " (*required)"


        if description == None:
            #: Create own description

            _required = f"(*required)" if required else ""
            description = "This command accepts a positional arguments. %s" %(_required) 

        
        self.__args.update({
            args: { 
                "desc": description, "svalue": svalue,
                "type": type, "value": value, "required": required, 
                "deprecated": deprecated
            } 
        })



    def __check_value(self, command: str, params: List[str] = [], keys: dict = {}):
        
        try:

            if len(params) == 1:
                value = params[0]
        
            else:
                #: Multiple value
                value = params
                

        except IndexError:
            raise ValueError("%s needs a value. " % (command))
 
        new_value = []
        if command in keys:
        

            if type(self.__args[command]['type']) == list:
                if len(value) != len(self.__args[command]['type']):
                    pass

            #: Check if the command is deprecated.
            if self.__args[command]['deprecated']:
                raise DeprecationWarning("%s is deprecated." % (command))


            if type(value) != list:
                #: Check if the value is none and default value is required.
                
                if self.__args[command]['value'] and value == None:
                    value = self.__args[command]['value']

            else:
                raise ValueError("Your passing a default value on a multiple value")


            # get the param
            # convert the value to the type given if not none

            if type(value) != list and self.__args[command]['type']:
                if len(self.__args[command]['type']) != len(value):
                    try:
                        new_value = self.__args[command]['type'][0](value)
                    except TypeError:
                        #: If the type is None
                        pass

            elif type(value) == list and type(self.__args[command]['type']) == list:
                
                for i in range(0, len(value)):
                    try:

                        new_value.append(self.__args[command]['type'][i](value[i]))
                    
                    except IndexError:
                        #: This error is when you pass to much arguments
                        raise TooMuchArguments()

                    except TypeError:
                        #: This error is probably when the type is None.
                        pass

                    except ValueError:
                        raise TypeError('it looks like %s accept %s positional arguments' % (value[i], self.__args[command]['type'][i]))
            
            if new_value:
                return { command: new_value }
            
            else:
                return { command: value }

    def parse_args(self):
        self.help_command.commands = self.__args
        params = []
        possible_args = []


        if len(self.__sys_args) <= 1:
            self.help_command()
            sys.exit()

        for i in range(1, len(self.__sys_args)):
            params.append(self.__sys_args[i])
        
        for i in range(1, len(params)):
            possible_args.append(params[i])

        command = params[0]

        if len(possible_args) > self.__args[command]['svalue']:
            raise TooMuchArguments()


        return self.__check_value(command, possible_args, self.__args.keys())
