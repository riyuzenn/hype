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

from hype.errors import PluginError
from typing import Any, Optional
from typing import List

try:
    from hype.color import parse_color
except PluginError:
    parse_color = None
try:
    from tabulate import tabulate

except ModuleNotFoundError:
    tabulate = None


class Table:
    """
    A table wrapper for `tabulate`

    Parameters:
    ---

        headers (List[str]):
            A list of header string. You can set it as None since there
            is a function `add_header` for adding header.

        rows (List[str]):
            A list of row to be added. You can set it as None since there
            is a function called `add_row` for adding row individually.

        type (str):
            A table type to be rendered. See the docs for more information.

    Functions:
    ---

        add_header (List[str]):
            Add a list of header (str) to the data.

        add_row (List[str]):
            Add a list of row (str) to the data.



    Example:
    ---
        >>> table = Table(headers=['Name', 'Age', 'Hobby'])
        >>> table.add_row(['Zenqi', '5', 'Programming'])
        >>> print(table.render()) #: or print(table())

    """

    #: Initialize empty header list
    __headers = []

    #: Initialize empty row list
    __rows = []

    #: Initialize empty type
    __type = None

    def __init__(
        self,
        headers: Optional[List[str]] = None,
        rows: Optional[List[str]] = None,
        type: Optional[str] = "fancy_grid",
    ):

        self.__headers = headers
        self.__rows = rows or []
        self.__type = type

    def add_row(self, row: Any):
        """
        Add a list row to the table data.

        Parameters:
        ---

            row (Any):
                Add a row to the data. It can be a list or a single string.

        """

        if parse_color:
            try:
                for i in range(len(row)):
                    row[i] = parse_color(row[i])
            except Exception:
                row = row

        self.__rows.append(row)

    def add_header(self, header: Any):
        """
        Add a list row to the table data.

        Parameters:
        ---

            header (Any):
                Add a header to the data. It can be a list or a single string.

        """

        if parse_color:
            try:
                for i in range(len(header)):
                    header[i] = parse_color(header[i])
            except Exception:
                header = header

        self.__headers.append(header)

    def render(self, background_color: Optional[str] = None):
        """
        Render the table. It return a string of table.

        Parameter:
        ---

            background_color (str):
                Set the background color of the table. Color plugin should be installed.

        """

        if parse_color and background_color:
            try:
                table = parse_color(
                    "[bg color={0}]{1}[/bg]".format(
                        background_color,
                        tabulate(
                            self.__rows, headers=self.__headers, tablefmt=self.__type
                        ),
                    )
                )

            except AttributeError:
                raise PluginError(
                    "Table plugin is not supported. Read the docs for more info"
                )

        elif parse_color == None and background_color:
            raise PluginError("Colors are not supported. Read the docs for more info.")

        else:
            try:
                table = tabulate(
                    self.__rows, headers=self.__headers, tablefmt=self.__type
                )
            except AttributeError:
                raise PluginError(
                    "Table plugin is not supported. Read the docs for more info"
                )

        return table

    def __call__(self, background_color: Optional[str] = None):
        """
        Render the table. It return a string of table.

        Parameter:
        ---

            background_color (str):
                Set the background color of the table. Color plugin should be installed.

        """

        return self.render(background_color)
