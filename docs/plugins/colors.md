# Handling Colors
---

Colors with **Hype** are powered by <a href="https://github.com/tartley/colorama" class="external-link"><b>colorama</b></a>. 

In this page, you will learn how to print colored output with the builtin `ColorParser`
of **Hype**.


## Parsing Color
---

Parsing color is pretty similar to `bbcode`. If you don't know what bbcode is, it's ok.
It is just a lightweight markup language similar to html. However bbcode uses `[]` brakets.

For more understanding, here is an example:

```python
from hype import print
print('[red]This is red[/red]')
```

As you can see we imported the `print` function from `hype.print`. It is a wrapper for
standard printing or colored printing.

## Color Tags
---
How convinient is that right? You don't need to format manually with ANSI Codes.

Speaking of ANSI Codes, here are some list of supported colors:

- `red`: 

    Color Red

- `blue`: 

    Color Blue

- `green`: 

    Color Green

- `black`: 

    Greyish Color

- `cyan`: 

    Color Cyan

- `magenta`: 

    Color Magenta

- `yellow`: 

    Color Yellow

- `white`: 

    Color White

- `reset`: 

    Reset the color You dont need to define reset. It is already define when closing the tag.

## Styles
---

Of course, we support style tag as well.

- `bold or b`
    Set the text to bold

- `italic or i`
    Set the text to italic

- `underline or u`
    Set the text to underline

Example:

```python
from hype import print
print('[red][b]This is bold red[/b][/red]')
```

## Background
---

Setting up text background is not same as setting the color of the text.
The background uses `bg` tag and it takes 1 attribute, the `color` tag.

Example:

```python
from hype import print
print('[bg color=red]This is background is color red[/bg]')
```

!!! tip
    Did you know that nested colors are supported?
    ```python
    from hype import print #: Import the print wrapper for color printing.
    print('[red]This [green](green inside the red)[/green] is red[/red]')
    ```
