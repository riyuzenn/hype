
# Running The Commands
---

!!! note ""
    **Estimated Reading Time**: 1 minute and 11 seconds

In **Hype** Application instance, you may run the code by executing the app function:
```py
if __name__ == "__main__":
    app.run()
```
This will run the entire application and look for the command arguments.
Now for running the cli application. Use the command `python <filename>.py help`
to show the help command. This will show every commands registered

## Brief Explaination
---

Lets say you have a simple app with command `greet` and `goodbye`. This command takes both 2
options. The `name` and `age`.

```py

from hype import Hype #: Import the Hype Application instance from `hype.app`

app = Hype() #: Create a Application instance

@app.command() #: Create a basic command
def greet(name: str, age: int): #: This command requires the name and age.
    app.echo('Hello, {0}. Your age is {1}'.format(name, age)) #: Print the output

@app.command() #: Create a basic command similar to `greet` but it goodbye the user
def goodbye(name: str, age: int): #: This command requires the name and age.
    app.echo('Bye, {0}. Your age is {1}'.format(name, age)) #: Print the output

if __name__ = "__main__":
    app.run() #: Running the command

```

Now you created a simple **Hype** applications. Congrats!
In order t orun the command, you need to run it via python. Lets suppose the
name of the file is `test.py`

```console
$ python test.py help
```

And then it shows all command registered. The output should look like this
```console
Usage: test.py COMMAND [ARGS..]
test.py help COMMAND

Options:
  -h, --help  show this help message and exit

Commands:
  greet     This command accept a positional arguments
  goodbye   This command accept a positional arguments
  help (?)  All details about the commands
```

Finally, you can run the command by passing the command name.
```console
$ python test.py greet --name Zenqi --age 5
```
And the final output should be 
`Hello, Zenqi. Your age is 5`

