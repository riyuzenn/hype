# Handling Commands
---

> Handling commands with **Hype** is easier, thanks to modern Python.
Currently, nested commands are not yet supported.

In this section, we are discussing all parameters that `hype.app.command` have.
Let's now dive in on `hype.app.command`!

### Command Parameter
---
`@command()` is based on `hype.command.HypeCommand`. And it takes a few parameters

- `name (str)`: 

    The name of the command. If the name is not define, it returns the function name.

- `usage (str)`:

    The usage format for the command. 
    Like for example:
    ```py
    @app.command(usage='%prog [OPTIONS]')
    ...
    ```

    This shows the usage when the option `--help` for the command is triggered:

    ```console
    Usage: python test.py [OPTIONS]
    ...
    ```

- `help (str)`:
    
    The help description for the command. You can set this by defining the function docstring


- `aliases (tuple)`:

    Set the aliases for the command. The alias is another keyword for executing commands.
    Here is the example:
    ```py
    @app.command(aliases=('g', 'greet'))
    ```
