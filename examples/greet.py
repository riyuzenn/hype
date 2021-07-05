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


from hype.cli import HypeCLI

app = HypeCLI(banner="""\noooo                                         \n`888                                         \n 888 .oo.   oooo    ooo oo.ooooo.   .ooooo.  \n 888P"Y88b   `88.  .8'   888' `88b d88' `88b \n 888   888    `88..8'    888   888 888ooo888 \n 888   888     `888'     888   888 888    .o \no888o o888o     .8'      888bod8P' `Y8bod8P' \n            .o..P'       888                 \n            `Y8P'       o888o\n""")

@app.command("greet", description="Greet the given user")
def greet(name: str):
  print("Hello, {}!".format(name))
 

if __name__ == "__main__":
  app.run()
