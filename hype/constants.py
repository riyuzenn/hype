
from .style import Background, Color
from .style import Style

rule_colors =  {

    'red':      Color.RED,
    'blue':     Color.BLUE,
    'green':    Color.GREEN,
    'black':    Color.BLACK,
    'cyan':     Color.CYAN,
    'magenta':  Color.MAGENTA,
    'yellow':   Color.YELLOW,
    'white':    Color.WHITE,
    '/':        Color.RESET,

}

bg_colors =  {
    
    'red':      Background.RED,
    'blue':     Background.BLUE,
    'green':    Background.GREEN,
    'black':    Background.BLACK,
    'cyan':     Background.CYAN,
    'magenta':  Background.MAGENTA,
    'yellow':   Background.YELLOW,
    'white':    Background.WHITE,
    'reset':    Background.RESET,

}

rule_bg_colors = {

    'bg red':       Background.RED,
    'bg blue':      Background.BLUE,
    'bg green':     Background.GREEN,
    'bg black':     Background.BLACK,
    'bg cyan':      Background.CYAN,
    'bg magenta':   Background.MAGENTA,
    'bg yellow':    Background.YELLOW,
    'bg white':     Background.WHITE,
    'bg reset':     Background.RESET,

}


rule_styles = {

    'bold':      Style.BOLD,
    'italic':    Style.ITALIC,
    'underline': Style.UNDERLINE,

    # ALiases
    'b': Style.BOLD,
    'i': Style.ITALIC,
    'u': Style.UNDERLINE,
}