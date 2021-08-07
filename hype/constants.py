from hype.errors import PluginError
from .style import Background, Color
from .style import Style

try:
    import hype.color

    COLOR_SUPPORTED = True
except PluginError:
    COLOR_SUPPORTED = False

rule_colors = {
    "red": Color.RED,
    "blue": Color.BLUE,
    "green": Color.GREEN,
    "black": Color.BLACK,
    "cyan": Color.CYAN,
    "magenta": Color.MAGENTA,
    "yellow": Color.YELLOW,
    "white": Color.WHITE,
    "reset": Color.RESET,
}

bg_colors = {
    "red": Background.RED,
    "blue": Background.BLUE,
    "green": Background.GREEN,
    "black": Background.BLACK,
    "cyan": Background.CYAN,
    "magenta": Background.MAGENTA,
    "yellow": Background.YELLOW,
    "white": Background.WHITE,
    "reset": Background.RESET,
}

rule_styles = {
    "bold": Style.BOLD,
    "italic": Style.ITALIC,
    "underline": Style.UNDERLINE,
    # ALiases
    "b": Style.BOLD,
    "i": Style.ITALIC,
    "u": Style.UNDERLINE,
}

all_tags = [
    #: colors
    "red",
    "blue",
    "green",
    "black",
    "cyan",
    "magenta",
    "yellow",
    "white",
    "reset",
    #: background
    "bg",
    #: styles
    "i",
    "italic",
    "b",
    "bold",
    "u",
    "underline",
]
