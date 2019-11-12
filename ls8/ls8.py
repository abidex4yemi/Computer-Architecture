#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

file_name = "print8.ls8"

cpu.load(f"examples/{file_name}")
cpu.run()
