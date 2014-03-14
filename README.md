# Lua5 with optimized interpreter dispatch

Lua5 uses switch-based dispatch which is slow but compatible with the widest range of compilers.
This patch adds support for indirect threading which is faster but requires a non-standard feature in C: labels as values.

Support for subroutine threading, which is faster than indirect threading, is planned.


## Requirements

- Tested on OS X 10.9.2, may work on Linux.
- Requires [Cog](https://pypi.python.org/pypi/cogapp) for Python


## Original Release Notes

This is Lua 5.2.3, released on 11 Nov 2013.

For installation instructions, license details, and
further information about Lua, see doc/readme.html.


