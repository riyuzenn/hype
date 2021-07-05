

class HypeException(Exception):
    def __init__(self, msg=None):
        if msg == None:
            msg = "Something went wrong with the Hype CLI"

        super().__init__(msg)


class TooMuchArguments(HypeException):
    def __init__(self):
        super().__init__("You passed too much arguments.")


