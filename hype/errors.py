class HypeException(Exception):
    def __init__(self, msg=None):
        if msg == None:
            msg = "Something went wrong with the Hype CLI"

        super().__init__(msg)


class OptionError(HypeException):
    def __init__(self, msg="There is something went wrong on the option"):
        super().__init__(msg)


class TooMuchArguments(HypeException):
    def __init__(self, msg="You passed too much arguments"):
        super().__init__(msg)


class PluginError(HypeException):
    def __init__(self, msg="Plugin not installed"):
        super().__init__(msg)


class ColorNotFound(HypeException):
    def __init__(self, msg="The color used is not found"):
        super().__init__(msg)


class TagNotFound(HypeException):
    """
    Used for parsing colors in `hype.colors`
    """

    def __init__(self, msg="Tag is not defined"):
        super().__init__(msg)
