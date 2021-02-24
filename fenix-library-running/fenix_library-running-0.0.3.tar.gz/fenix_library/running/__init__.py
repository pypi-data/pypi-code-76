# Fenix Library
# Please refer to the file `LICENSE` in the main directory for license information. 
# For a high level documentation, please visit https://gitlab.com/rebornos-team/fenix/libraries

# AUTHORS
# 1. Shivanand Pattanshetti (shivanand.pattanshetti@gmail.com)
# 2. 

# IMPORTS
from .running import * # since this package (running) contains a single module (running.py), flatten the module so that users can access items within the module running.py by using just the package name (fenix_library.running.item) instead of having to add the module name too (fenix_library.running.running.item)
