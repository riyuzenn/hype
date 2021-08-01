
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

from typing import List
from hype.command import HypeCommand
import optparse
from optparse import HelpFormatter
import sys
import textwrap

class HypeParser(optparse.OptionParser):
    """
    A command parser for Hype CLI that was built on the top of 
    `optparse.OptionParser` This parser is pretty simmilar with 
    OptionParser, the only difference is the commands. 
    

    Parameters:

        commands (list):
            A list of all HypeCommands
        
        **options (dict):
            A dictionary of kwargs

    Example:

        >>> greet = HypeCommand('greet', help="%prog [OPTIONS]")
        >>> greet.add_option('--name', type=str)
        >>> ...
        >>> goodbye = HypeCommand('goodbye', help="%prog [OPTIONS]")
        >>> goodbye.add_option('--name', type=str)
        >>> ...
        >>> parser = HypeParser( commands=(greet, goodbye) )
        >>> options, commands, command_opt, args = parser.parse_args()

    """
    _HelpCommand = HypeCommand('help', help="All details about the commands", aliases=('?'))

    def __init__(
        self, 
        commands: List[HypeCommand] = [], 
        *args, 
        **options
    ):
        
        self.commands = commands
        self.commands.append(self._HelpCommand)
        self.options = options

        if 'usage' not in self.options:
            self.options['usage'] = "%prog COMMAND [ARGS..]\n%prog help COMMAND"

        super(HypeParser, self).__init__(*args, **options)

        for command in self.commands:
            command.parser.prog = "%s %s" % (self.get_prog_name(), command.name)

        self.disable_interspersed_args()

    def add_command(self, cmd: HypeCommand):
        """
        Add a command. 
        
        Parameters
        ---
            cmd (HypeCommand):
                The command to be add.

        Example:

            >>> goodbye = HypeCommand(..)
            >>> parser = HyperParser(...)
            >>> ...
            >>> parser.add_command(goodbye)

        """
        if not isinstance(cmd, HypeCommand):
            raise TypeError('{} is not a instance of HypeCommand'.format(cmd))

        self.commands.append(cmd)


    def format_help(self, formatter=None) -> str:
        out = optparse.OptionParser.format_help(self, formatter)
        
        if formatter == None:
            formatter = self.formatter

        #: HEADER for the Help command
        result = ['\n']
        result.append(formatter.format_heading('Commands'))
        formatter.indent()

        display_names = []
        help_position = 0

        for command in self.commands:
            name = command.name
            if command.aliases:
                #: Add aliases of the command
                name += ' (%s)' % (', '.join(command.aliases))

            display_names.append(name)

            #: Set the help position based on the max width.
            proposed_help_position = len(name) + formatter.current_indent + 2
            if proposed_help_position <= formatter.max_help_position:
                help_position = max(help_position, proposed_help_position)  
    
        #: Add the command to the output
        for command, name in zip(self.commands, display_names):
            #: From optparse.py

            name_width = help_position - formatter.current_indent - 2

            if len(name) > name_width:
                name = "%*s%s\n" % (formatter.current_indent, "", name)
                indent_first = help_position

            else:
                name = "%*s%-*s  " % (formatter.current_indent, "",
                                      name_width, name)
                indent_first = 0

            result.append(name)
            help_width = formatter.width - help_position
            help_lines = textwrap.wrap(command.help, help_width)
            result.append("%*s%s\n" % (indent_first, "", help_lines[0]))
            result.extend(["%*s%s\n" % (help_position, "", line)
                           for line in help_lines[1:]])

        formatter.dedent()

        # Concatenate the original help message with the command list.
        return out + "".join(result)

    def __command_for_name(self, name):
        """
            Return the command in self.commands matching the
        given name. The name may either be the name of a subcommand or
        an alias. If no subcommand matches, returns None.
        
        Parameters:
            name (str):
                The name of the command to be matched.

        """ 

        _command = None

        for command in self.commands: 
            try:
            
                if name == command.name or name in command.aliases:
                    _command = command
            
            except TypeError:
                pass

        return _command

    def parse_args(self, _args=None, _value=None):
        """
        Just like the `parse_args` from OptionParser but add some more value.
        
        Added Value:
        ---

        - options: The option passed to the root parser
        - command: the command object that was invoked
        - command_opt: The option parsed to the command parser
        - command_args: The positional arguments passed to the sub command
        
        Parameters:
        ---

            _args (any):
                inherited from `optparse.OptionParser.parse_args`

            _value (any):
                inherited from `optparse.OptionParser.parse_args`

        Example:
        ---

            >>> parser = HypeParser(...)
            >>> parser.add_option(...)
            >>> ...
            >>> options, command, \ 
            ...    command_opt, command_args = parser.parse_args()
    
        """ 
        options, args = optparse.OptionParser.parse_args(self, _args, _value)

        if not args:
            # No command given, show the help message
            self.print_help()
            self.exit()

        else:
            command_name = args.pop(0)
            command = self.__command_for_name(command_name)

            if not command:
                self.error('Unknown Command: {}'.format(command_name))

        command_opt, command_args = command.parser.parse_args(args)

        if command is self._HelpCommand:
            if command_args:

                command_name = command_args[0]

                #: Check for the help command on the command arguments.
                helpcommand = self.__command_for_name(command_name)
                helpcommand.parser.print_help()
                self.exit()

            else:
                self.print_help()
                self.exit()

        
        return options, command, command_opt, command_args