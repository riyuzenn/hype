#: A maintain project from https://github.com/kcsaff/getkey.
#: Since it hasn't maintain for years now and alot of issues
#: when installing on windows


import sys
from .platforms import platform, PlatformError, PlatformInvalid

try:
    __platform = platform()
except PlatformError as err:
    print(
        "Error initializing standard platform: {}".format(err.args[0]), file=sys.stderr
    )
    __platform = PlatformInvalid()

getkey = __platform.getkey
keys = __platform.keys
key = keys  # alias
bang = __platform.bang

__version__ = "0.6.6"
