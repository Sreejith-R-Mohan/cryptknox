#! /usr/bin/python

from lib.Arguments import Arguments
import sys

class Cli:
    print(sys.argv)
    a = Arguments(sys.argv)
