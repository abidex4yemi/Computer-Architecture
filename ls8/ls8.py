#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

if len(sys.argv) != 2:
    print("Usage: ls8.py <filename>", file=sys.stderr)
else:
    print(sys.argv)
    cpu.load(sys.argv[1])
    cpu.run()
