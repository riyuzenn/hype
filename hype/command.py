
import optparse
from typing import Any, Optional, Tuple

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
    __parser = optparse.OptionParser()
    
    def __init__(self, name: str, usage: Optional[str] = None, 
                aliases: Optional[Tuple[Any]] = None, help: Optional[str] = None):

        self.name = name
        self.usage = usage
        self.aliases = aliases
        self.help = help

        if self.usage:
            self.__parser.usage = self.usage

    @property
    def parser(self):
        return self.__parser
        
    def add_option(self, *args, **kwargs):
        return self.__parser.add_option(*args, **kwargs)
    
        