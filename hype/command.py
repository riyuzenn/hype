import optparse
from os import name
from typing import Any, Dict
from typing import Optional
from typing import List
from typing import Tuple
import textwrap



class HypeArgument:
    """
    Base class for handling arguments.
    """
    __metavar_mapping = {
        str: "STRING",
        int: "INTEGER",
        float: "FLOAT",
        bool: "BOOLEAN",
        bytes: "BYTES",
        list: "LIST",
        dict: "DICTIONARY",
    }
    def __init__(
        self,
        name: str,
        help: str = None,
        type: Any = None
    ):

        self.name = name
        self.help = help
        self.type = self.__metavar_mapping[type] if type else None
        

class HypeOptionParser(optparse.OptionParser):
    """
    This is a parser inherited by `optparse.OptionParser`
    with some minor changes and adding arguments as well as 
    including help formatter.
    """
    __args = []
    def __init__(self, arguments: List[Any], *args, **options):
        super(HypeOptionParser, self).__init__(*args, **options)
        
        self.options = options
        self.arguments = arguments
        
        if self.arguments:
            self.usage = "%prog [ARGS] [OPTIONS]"
        else:
            self.usage = "%prog [OPTIONS]"

        self.disable_interspersed_args()

    def add_argument(self, argument):
        if not isinstance(argument, HypeArgument):
            raise ValueError('{} is not a instance of HypeArgument'.format(argument))
        
        return self.arguments.append(argument)

    def format_help(self, formatter=None):
        output = optparse.OptionParser.format_help(self, formatter)
        result = []
        display_names = []
        help_position = 0

        if formatter == None:
            formatter = self.formatter
        
        if self.arguments:
            result += ['\n']
            result += formatter.format_heading('Arguments')
            formatter.indent()

            for arg in self.arguments:
                name = arg.name
                if arg.type:
                    name = "{}={}".format(name, arg.type)
                display_names.append(name)

                #: Set the help position based on the max width.
                proposed_help_position = len(name) + formatter.current_indent + 2
                if proposed_help_position <= formatter.max_help_position:
                    help_position = max(help_position, proposed_help_position)  
                    
            
            for arg, name in zip(self.arguments, display_names):
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
                help_lines = textwrap.wrap(arg.help, help_width)
                result.append("%*s%s\n" % (indent_first, "", help_lines[0]))
                result.extend(["%*s%s\n" % (help_position, "", line)
                            for line in help_lines[1:]])
            
            
            formatter.dedent()

        result += ['\n']
        return output + ''.join(result)


class HypeCommand:
    """
    A command for Hype CLI. Commands are different with options.
    It act as a sub command argument that has different type of options


    Parameters:

        name (str):
            The name of the command

        usage (str):
            The usage format for the command

        help (str):
            The help for the command.


        aliases (tuple):
            Aliases of the command.


    Example:

        >>> greet = HypeCommand('greet', usage='%prog [OPTIONS]',
        ...      help="Greet the user", aliases=('g'))

        >>> greet.add_option('--name', type=str, required=True)

    """

    def __init__(
        self,
        name: str,
        usage: Optional[str] = None,
        aliases: Optional[Tuple[Any]] = None,
        help: Optional[str] = None,
        args: Optional[List[Any]] = None,
    ):
        self.name = name
        self.usage = usage
        self.aliases = aliases
        self.help = help or "This command accept a positional arguments"
        self.args = args
        self.parser = HypeOptionParser(self.args)
        

        if self.usage:
            self.parser.usage = self.usage

    def add_option(self, *args, **kwargs):
        return self.parser.add_option(*args, **kwargs)
