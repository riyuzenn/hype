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

    def __init__(
        self,
        name: str,
        usage: Optional[str] = None,
        aliases: Optional[Tuple[Any]] = None,
        help: Optional[str] = "",
    ):

        self.name = name
        self.usage = usage
        self.aliases = aliases
        self.help = help if help != "" else "This command accept a positional arguments"
        self.parser = optparse.OptionParser()

        if self.usage:
            self.parser.usage = self.usage

    def add_option(self, *args, **kwargs):
        return self.parser.add_option(*args, **kwargs)
