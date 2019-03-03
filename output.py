#!/usr/bin/env python3

from json import dumps

def pretty_print(obj):
    print(dumps(obj, indent=4))

