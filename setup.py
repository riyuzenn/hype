
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


from setuptools import setup, find_packages
from hype import __license__, __author__, __version__, __desc__

BASE_URL = "https://github.com/serumstudio/hype"

def get_long_description():

    with open("README.md", encoding="utf-8") as f:
        readme = f.read()

    return readme

extras_require = {

    'color': ['colorama==0.4.4'], #: Color support
    'standard': ['colorama==0.4.4'], #: Standard installation with color support
    'progress': ['alive-progress==1.6.2'], #: With progressbar support
    'table': ['tabulate==0.8.9'] #: With Table support
}



setup(
    name = "hypecli",
    author = __author__,
    description =__desc__,
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    project_urls={
        'Documentation': 'https://hype.serum.studio',
        'Source': BASE_URL,
        'Tracker': "%s/issues" % (BASE_URL)
    },
    version = __version__,
    license = __license__,
    url=BASE_URL,
    keywords='cli,commandline-toolkit,command line toolkit,python cli,python 3'.split(','),
    packages = [p for p in find_packages() if 'hype.prompt' not in p and 'hype.prompt.getkey' not in p],
    extras_require = extras_require,
    classifiers = [
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development",
        "Typing :: Typed",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License"
    ],
)