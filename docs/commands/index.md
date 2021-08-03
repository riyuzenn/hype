# How Commands work?
---

!!! note ""
    **Total Reading Time**: 1 min and 37 seconds

**Hype**'s main feature was creating commands and options. It can be access by the `hype.app.command` decorator. 

By understanding how a basic decorator works, you can now use **Hype** with ease.

Here are some sneak peak example 👀 on the **Hype** core command decorator:

```py
@app.command()
def greet(name: str):
    app.echo('Hello, {}'.format(name))

```

The structure of the command is simple. The app has a command which define using the `command` 
decorator and it accept options based on the function parameters.


### Command Structure
---

On the other hand, this structure below show how it works. 

```python

app = Hype()

@app.command()
def greet(name: str):
    """
    Greet the user
    """
    app.echo('Hello, {}'.format(name))

@app.command()
def goodbye(name: str, formal: bool=False):
    """
    Goodbye the user.
    """

    if formal:
        app.echo('Goodbye, Mr/Ms {}!'.format(name))

    else:
        app.echo('Goodbye {}'.format(name))
    
```


```console

Hype Application
-------
    |
    |
    | - commands

        | - help
        |   | - The help command is built in. It shows all commands registered
        |
        | - greet # This is a command defined by the greet function
        |   | - --name # The option name is defined on the function parameter
        |
        | - goodbye # This is a command defined by the goodby function
        |   | - --name # The option name is defined on the function parameter
        |   | - --format # The formal option is defined on the function parameter.
        |
        |
```

!!! tip
    Did you know that the `help` description for the command can be automatically
    define by creating a docstring on a function?

    ```py
    @app.command()
    def greet(name: str):
        """
        Greet the user
        """ # -> This is a docstring

        app.echo("Hello, {}".format(name))
    
    ```