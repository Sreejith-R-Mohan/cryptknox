#! /usr/bin/python

from lib.Arguments import Arguments
import sys

class Cli:
    @staticmethod
    def help():
        print("Usage: cryptknox --operation store --master-password Mysecretpassword --service gmail --password mygmailpassword")

    def __init__(self,args):
        self.args = Arguments(args)

        
        
        
    