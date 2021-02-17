#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
import os, sys
sys.path.insert(1, "/Volumes/GitHub/Packages/fil3s/")
from fil3s.v1 import Files,Formats

array = Files.Array(path="array.json", load=False)
array.array = [1, 2, 3]
array.save()


quit()

