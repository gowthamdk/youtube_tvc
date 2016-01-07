#!/usr/bin/python
###########################################################
#
# This python script is used for clean file name for unix/linux compatibility 
# using python re module.
#
# Written by : Gowtham D
# Email : gowthamdk@outlook.com
# GitHub: https://github.com/gowthamdk/
#
###########################################################

# Import required python libraries

import re
import os

path = os.getcwd()
filenames = os.listdir(path)

for f in filenames:
    result = re.sub(r'[#|&|@|:|-|(|)|?|$|.|!]',r'_',f)
    print result
