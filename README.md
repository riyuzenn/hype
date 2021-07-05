<h1 align="center">
  <img src="https://raw.githubusercontent.com/serumstudio/hype.cli/main/images/hypecli.png" height="150" alt="hypecli">
</h1>

<h4 align="center">⚙ A lightweight command line interface library for creating cli commands.</h4>

<p align="center">
  <a href="#about">About</a> | 
  <a href="#installation">Installation</a> | 
  <a href="#usage">Usage</a> | 
  <a href="#features">Features</a> | 
  <a href="#contributors">Contributors</a> |
  <a href="#license">License</a>
</p>

# About

> **Next**: [Installation](https://github.com/serumstudio/anglo#installation) 

**Hype CLI** is an *open source* framework use for building command line applications easirer <br>
for cli applications that required different type of commands.

It also comes with alot of different [features](https://github.com/serumstudio/hype.cli#features) that you may want to check out. Hype CLI was mainly <br>
built for [Anglo](https://github.com/serumstudio/anglo) *( a modern lightweight web framework for python 3. )*. Because of Hype CLI's capability <br>
it becomes easier to build command-line application.

| [Learn More](https://serum.studio/hypecli)|
|-------|


<div align="right" id="installation">
  <h1> Installation </h1>
</div>

# Usage
You can read the [documentation]() for more info and [examples]() for more examples.
Hyper CLI comes with a starter project template as well. After the installation, run 
```bash
$ hyper create demoproject
```

Or you can create your own project by looking on this simple example.

```py

#: Import the main class of the module
from hype.cli import HyperCLI

#: create a `app` instance of HyperCLI `:class:`
app = HyperCLI()

#: Declare a command decorator.
@app.command(description="Greet the given user")
def greet(name: str):

  #: print the name that user define.
  print("Hello", name)
 
if __name__ == "__main__":
  #: Run the application
  app.run()

# Output:
# python test.py greet Zenqi
# Hello Zenqi
```

<div align="right" id="features">
  <h1> Features </h1>
</div>

# Contributors

<div align="right" id="license">
  <h1> License </h1>
  <p> Hype is license under <a href="https://github.com/serumstudio/anglo/blob/main/LICENSE">MIT</a> </p>
</div>
