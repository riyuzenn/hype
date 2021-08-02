# Features
---

You probably heard other libraries that are simillar with **Hype**. Like for example,
<a class="external-link" href="https://github.com/tiangolo/typer" target="_blank"><b>Typer</b></a> developed by [@tiangolo](https://github.com/tiangolo){:target="_blank"} and <a class="external-link" href="https://github.com/pallets/click" target="_blank"><b>Click</b></a> developed
by [@pallets](https://github.com/pallets){:target="_blank"}. Yet this library was inspired by it.

Basically there is alot of differences regarding on the libraries' feature.
Here are some list of features from <a class="internal-link" href="https://hype.serum.studio"><b>Hype:</b></a>

#### 1. Easy to code.

Hype comes with simple and neat syntax. 

#### 2. Decorator based.

It is decorator base for easy understanding. You probably don't need to know alot of 
stuff with *python decorator* since **Hype** doesn't teach you about that. See this for more
simple explaination about <a class="external-link" href="https://www.programiz.com/python-programming/decorator"><b>Python Decorators</b></a>.


#### 3. Production Ready.

It not that Hype is built for testing and development. It was built for **Production** as well!

## Editor Friendly
---

If you are using a popular code editor that has a auto completion like <a href="https://code.visualstudio.com" target="_blanl" class="external-link">Visual Studio Code</a> or <a href="https://www.jetbrains.com/pycharm/" target="_blanl" class="external-link">PyCharm</a>
it becomes easier to code with **Hype** since it supports *type hints*.


## User Friendly Library
---

**Hype** is also user/developer friendly. It has a integrated features making it user friendly.

- **Automatic help command**: If you're not aware of it, Hype integrate and add a help command.
You can access it by typing the command `help`.

- **Basic command and option structures**: Hype was mainly built at the top of `optparse`, a standard python library for parsing typicall option. 
Since `optparse` doesn't require alot of features including command, Hype was here for you.

!!! tip 
    Did you know that you can set command alias for the command?
    You can achieve it by using the parameter **aliases**.

    Here are the example command.
    ```py
    @app.command(aliases=('g', 'greeting'))
    def greet(name: str):
        app.echo('Hello, {}'.format(name))

    # Example Command:
    # python greet.py g --name Zenqi
    # or 
    # python greet.py greeting --name Zenqi

    #: Output
    #: Hello, Zenqi
    
    ```