# -*- coding: utf-8 -*-

import subprocess
try:
    from subprocess import DEVNULL # py3k
except ImportError:
    import os
    DEVNULL = open(os.devnull, 'wb')

def outputCommand(args, cwd=None):
    try:
        output = subprocess.check_output(args, cwd=cwd, universal_newlines=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as exc :
        output = ''

    return output

def callCommand(args, cwd=None):
    return subprocess.call(args, cwd=cwd, stderr=DEVNULL)
