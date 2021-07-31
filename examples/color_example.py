#                    Copyright (c) 2021 Serum Studio

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

#: A simple greet command with color support. Make sure to install color plugins.
#: `pip install hypecli[color]` or `pip isntall hypecli[standard]` 
#: Check installation documentation: https://hype.serum.studio/

from hype import Hype

app = Hype()

@app.command()
def greet(name):
    """
    Greet the user.
    """
    app.print("Hello, [green]%s[/green]" % (name))
    

@app.command()
def goodbye(name: str):
    """
    Say Goodbye to the user.
    """
    app.print("Goodbye, [red]%s[/red]" % (name))


if __name__ == "__main__":
    app.run()


