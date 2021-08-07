#                   Copyright (c) 2021, Serum Studio

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

#: The parser was inspired at pyskcode. Thanks to https://github.com/TamiaLab/PySkCode

import string
from .constants import rule_colors
from .constants import rule_styles
from .constants import bg_colors
from .constants import all_tags
from typing import Optional
from typing import IO
from .errors import PluginError
from .errors import TagNotFound

__all__ = ["print_color", "parsed_color"]

try:

    import colorama

    colorama.init()
    COLOR_SUPPORTED = True

except ModuleNotFoundError:
    COLOR_SUPPORTED = False


# Character charsets
WHITESPACE_CHARSET = frozenset(string.whitespace)
IDENTIFIER_CHARSET = frozenset(string.ascii_letters + string.digits + "_*")

# Token types
TOKEN_DATA = 0
TOKEN_NEWLINE = 1
TOKEN_OPEN_TAG = 2
TOKEN_CLOSE_TAG = 3
TOKEN_SELF_CLOSE_TAG = 4


def skip_whitespaces(text: str, offset: int):
    """
    Skip any whitespaces.
    :param text: The input text.
    :param offset: The current offset in the input text.
    :return The new offset in the input text.
    """
    while text[offset] in WHITESPACE_CHARSET:
        offset += 1
    return offset


def get_identifier(text: str, offset: int):
    """
    Get the identifier string starting in the text at the given offset.
    :param text: The input text.
    :param offset: The current offset in the input text.
    :return The identifier normalized as lowercase and the new offset in the input text.
    """
    identifier = ""

    # Get any identifier char
    while text[offset] in IDENTIFIER_CHARSET:
        identifier += text[offset]

        # Process the next char
        offset += 1

    # Normalize the identifier and return new values
    return identifier.lower(), offset


def get_attribute_value(
    text: str, offset: int, opening_tag_ch: str, closing_tag_ch: str
):
    """
    Get the attribute value starting in the text at the given offset.
    :param text: The input text.
    :param offset: The current offset in the input text.
    :param opening_tag_ch: The opening tag char (must be one char long).
    :param closing_tag_ch: The closing tag char (must be one char long).
    :return The attribute value with trailing whitespaces removed and the new offset in the input text.
    """
    attribute_value = ""

    # Handle quoted and unquoted value
    if text[offset] == "'" or text[offset] == '"':
        quoting_ch = text[offset]

        # Process the next char
        offset += 1

        # Get attribute value
        while text[offset] != quoting_ch:

            # Handle escape sequences
            if text[offset] == "\\":

                # Process the next char
                offset += 1

                # Only the quoting char and the backslash char can be escaped
                if text[offset] != quoting_ch and text[offset] != "\\":
                    attribute_value += "\\"

            # Store the char
            attribute_value += text[offset]

            # Process the next char
            offset += 1

        # Skip last quoting sign
        offset += 1

    else:

        # Get raw attribute value
        ch = text[offset]
        while (
            ch != closing_tag_ch
            and ch != opening_tag_ch
            and ch not in WHITESPACE_CHARSET
        ):
            attribute_value += ch

            # Process the next char
            offset += 1
            ch = text[offset]

    # Check format
    if text[offset] != closing_tag_ch and text[offset] not in WHITESPACE_CHARSET:
        raise ValueError(
            "A whitespace is mandatory after the attribute "
            "value if not followed by the closing tag char"
        )

    # Strip the attribute value and return new values
    return attribute_value.strip(), offset


def parse_tag(
    text: str,
    start_offset: int,
    opening_tag_ch="[",
    closing_tag_ch="]",
    allow_tagvalue_attr=True,
    allow_self_closing_tags=True,
):
    """
    Parse the text starting at ``start_offset`` to extract a valid tag, if any.
    Return the tag name, the ``is_closing_tag`` and ``is_self_closing_tag`` flags,
    the tag attributes (as a dictionary) and the offset just after the end of the tag.

    If something goes wrong (malformed tag, unexpected end-of-file, etc.) an exception
    of type``IndexError`` (unexpected end-of-file) or ``ValueError`` (malformed tag) is raised.

    :param text: The input text.
    :param start_offset: The offset in the input text to start with.
    :param opening_tag_ch: The opening tag char (must be one char long, default '[').
    :param closing_tag_ch: The closing tag char (must be one char long, default ']').
    :param allow_tagvalue_attr: Set to ``True`` to allow the BBcode ``tagname=tagvalue`` syntax shortcut

    (default is ``True``).

    :param allow_self_closing_tags: Set to ``True`` to allow the self closing tags syntax (default is ``True``).

    :return A tuple ``(tag_name, is_closing_tag, is_self_closing_tag, tag_attrs, offset + 1)`` on success, or an
    exception on error (see possible exception in the docstring above).
    """
    assert text, "No text input given (mandatory)."
    assert start_offset >= 0, "Starting offset must be greater or equal to zero."
    assert start_offset < len(
        text
    ), "Starting offset must be lower than the size of the text."
    assert (
        len(opening_tag_ch) == 1
    ), "Opening tag character must be one char long exactly."
    assert (
        len(closing_tag_ch) == 1
    ), "Closing tag character must be one char long exactly."
    assert (
        text[start_offset] == opening_tag_ch
    ), "Unexpected call to parse_tag, no opening tag char at starting offset."

    # Init tag variables
    tag_attrs = {}
    is_closing_tag = is_self_closing_tag = False

    # Skip the opening char and whitespaces
    offset = skip_whitespaces(text, start_offset + 1)

    # Check for closing tag
    if text[offset] == "/":

        # Look like a closing tag for me
        is_closing_tag = True

        # Skip slash and whitespaces
        offset = skip_whitespaces(text, offset + 1)

    # Get the tag name
    tag_name, offset = get_identifier(text, offset)

    # Detect invalid tag early
    if not tag_name:
        raise ValueError("Invalid tag format: no tag name found")

    # Skip whitespaces
    offset = skip_whitespaces(text, offset)

    # Check for closing char if is_closing_tag is set (closing tags have no attribute)
    if is_closing_tag and text[offset] != closing_tag_ch:
        raise ValueError("Invalid tag format: closing tags cannot have attribute")

    # Check for tag value
    if text[offset] == "=":

        # Check for support
        if not allow_tagvalue_attr:
            raise ValueError(
                "Invalid tag format: tagname=tagvalue shortcut support disabled by caller."
            )

        # Skip equal sign and whitespaces
        offset = skip_whitespaces(text, offset + 1)

        # Get the tag value
        tag_value, offset = get_attribute_value(
            text, offset, opening_tag_ch, closing_tag_ch
        )

        # Store the tag value
        tag_attrs[tag_name] = tag_value

        # Skip whitespaces
        offset = skip_whitespaces(text, offset)

    # Named attributes handling
    while text[offset] != closing_tag_ch and text[offset] != "/":

        # Get the attribute name
        attr_name, offset = get_identifier(text, offset)

        # Detect erroneous attribute name
        if not attr_name:
            raise ValueError(
                "Invalid tag format: no attribute name found or invalid character found"
            )

        # Skip whitespaces
        offset = skip_whitespaces(text, offset)

        # Check for attr value
        if text[offset] == "=":

            # Skip equal sign and whitespaces
            offset = skip_whitespaces(text, offset + 1)

            # Get the attribute value
            attr_value, offset = get_attribute_value(
                text, offset, opening_tag_ch, closing_tag_ch
            )

            # Store the tag value
            tag_attrs[attr_name] = attr_value

            # Skip whitespaces
            offset = skip_whitespaces(text, offset)

        else:

            # Attribute without value
            tag_attrs[attr_name] = ""

    # Handle self closing tag
    if text[offset] == "/":

        # Check for support
        if not allow_self_closing_tags:
            raise ValueError(
                "Invalid tag format: self closing tags support disabled by caller."
            )

        # Look like a self closing tag for me
        is_self_closing_tag = True

        # Skip slash and whitespaces
        offset = skip_whitespaces(text, offset + 1)

    # Assert end of tag
    if text[offset] != closing_tag_ch:
        raise ValueError("Invalid tag format: malformed end of tag")

    # Emit the tag
    return tag_name, is_closing_tag, is_self_closing_tag, tag_attrs, offset + 1


def tokenize_newline(data: str):
    """
    Given a string that does not contain any tags, this function will
    yield a list of ``TOKEN_NEWLINE`` and ``TOKEN_DATA`` tokens in such way
    that if you concatenate their data, you will have the original string.
    N.B. Newline must have been normalized to ``\n`` before calling this function.
    :param data: Input data string to be tokenize.
    """
    lines = data.split("\n")
    last_line = lines.pop()
    for line in lines:
        if line:
            yield TOKEN_DATA, None, None, line
        yield TOKEN_NEWLINE, None, None, "\n"

    if last_line:
        yield TOKEN_DATA, None, None, last_line


def tokenize_tag(
    text: str,
    opening_tag_ch="[",
    closing_tag_ch="]",
    allow_tagvalue_attr=True,
    allow_self_closing_tags=True,
):
    """
    Split the given text into tokens (generator function).
    :param text: The input text to be tokenize.
    :param opening_tag_ch: The opening tag char (must be one char long, default '[').
    :param closing_tag_ch: The closing tag char (must be one char long, default ']').
    :param allow_tagvalue_attr: Set to ``True`` to allow the BBcode ``tagname=tagvalue`` syntax shortcut
    (default is ``True``).
    :param allow_self_closing_tags: Set to ``True`` to allow the self closing tags syntax (default is ``True``).
    """
    assert text, "No text input given (mandatory)."
    assert (
        len(opening_tag_ch) == 1
    ), "Opening tag character must be one char long exactly."
    assert (
        len(closing_tag_ch) == 1
    ), "Closing tag character must be one char long exactly."

    # Normalize newlines (fastest method)
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Search an opening tag
    start = text.find(opening_tag_ch)
    pos = 0

    # Process the whole text until no more tag can be found
    # N.B. string.find(s, beg) return -1 if beg >= len(string)
    while start >= 0:

        # Run the parser to get the tag
        try:
            tag = parse_tag(
                text,
                start,
                opening_tag_ch,
                closing_tag_ch,
                allow_tagvalue_attr,
                allow_self_closing_tags,
            )

        except (IndexError, ValueError):

            # Continue searching if not a valid tag
            start = text.find(opening_tag_ch, start + 1)
            continue

        # Get the text before the tag, if any
        if start > pos:
            text_before_tag = text[pos:start]
            yield from tokenize_newline(text_before_tag)

        # Unpack the tag structure
        tag_name, is_closing_tag, is_self_closing_tag, tag_attrs, offset = tag
        tag_source = text[start:offset]

        # Yield the tag token
        if is_self_closing_tag:
            yield TOKEN_SELF_CLOSE_TAG, tag_name, tag_attrs, tag_source
        elif is_closing_tag:
            yield TOKEN_CLOSE_TAG, tag_name, tag_attrs, tag_source
        else:
            yield TOKEN_OPEN_TAG, tag_name, tag_attrs, tag_source

        # Store the current position in text for next loop
        pos = offset

        # Search the next tag if any
        start = text.find(opening_tag_ch, offset)

    # Yield the remaining piece of text if any
    remaining_text = text[pos:]
    if remaining_text:
        yield from tokenize_newline(remaining_text)


def parse_color(text: str = ""):
    """
    Parsed the text of string that contains color tag into colored texts

    Parameters:
    ---
        text(str):
            The string to be parsed.

    Example:
    ---

        >>> string = parse_color('[red]This is red[/red]')
        >>> ...
        >>> #: You can use the parse_color to standard
        >>> #: printing or storing variables.
        >>> ...
        >>> print(string)

    """

    parsed_text = []
    tokens = tokenize_tag(text)

    for token in tokens:
        token_type, tag_name, tag_attr, token_source = token

        if token_type == TOKEN_OPEN_TAG:
            if tag_name not in all_tags:
                raise TagNotFound(
                    '\n\n"%s" is not found. check avaialble tags on the documentation:\nhttps://hype.serum.studio\n\n'
                    % (tag_name)
                )

            if tag_name in rule_colors:
                parsed_text.append(rule_colors[tag_name])

            if tag_name in rule_styles:
                parsed_text.append(rule_styles[tag_name])

            if tag_name == "bg":

                if "color" in tag_attr:
                    parsed_text.append(bg_colors[tag_attr.get("color")])

                else:
                    raise AttributeError(
                        "when defining background, color attribute must define."
                    )

        if token_type == TOKEN_CLOSE_TAG:
            parsed_text.append(rule_colors["reset"])

        if token_type == TOKEN_DATA:
            parsed_text.append(token_source)

        if token_type == TOKEN_NEWLINE:
            parsed_text.append(token_source)

    return "".join(parsed_text)


def print_color(
    text: str = "",
    sep: Optional[str] = " ",
    end: Optional[str] = "\n",
    file: Optional[IO[str]] = None,
    flush: Optional[bool] = False,
):

    """
    Simillar to built-in function, `print` but it prints a colored text
    from `parsed_color`

    Parameters:
    ---
        Similar to `print`

    Example:
    ---

        >>> print_color('[green]This is green[/green]')
        >>> #: Output This is green -> The output is colored in green.

    """

    if COLOR_SUPPORTED == False:
        raise PluginError(
            """

        -----------------------------------

        Plugin not installed properly:

        `color`: In order to install the `color` plugin,
        you may run the commmand `pip install hypecli[color]`
        or read the documentation.

        https://hype.serum.studio/
        
        -----------------------------------
        """
        )

    parsed_text = parse_color(text)

    print(parsed_text, sep=sep, end=end, file=file, flush=flush)
