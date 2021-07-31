
from .style import Color
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



rule_style = {
    
    'bold':      Style.BOLD,
    'italic':    Style.ITALIC,
    'underline': Style.UNDERLINE,

    # ALiases
    'b': Style.BOLD,
    'i': Style.ITALIC,
    'u': Style.UNDERLINE,
}