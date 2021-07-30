import re

s = "[red] hello [/]"
m = re.findall(r"(?<=\[).+?(?=\])", s)
print(m)

"""
Hello, I just want to ask simple regex question.
I'm new to regex and i want to try out something.

So basically I have a string:

```py
text = "[greet] Hello [/]"
```

What I wanted is how to split everything and make a tuple of tokens
like for example:

```py
[('TAG', 'greet'), ('VALUE', 'Hello'), ('CLOSING_TAG', '/')]
```

I tried a simple find all:
But it prints: the string inside a []
Ex: ['greet', '/']

```py
text = "[greet] Hello [/]"
m = re.findall(r"(?<=\[).+?(?=\])", s)
print(m)
```

"""