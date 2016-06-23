# -*- coding: utf-8 -*-

import subprocess

from git_app_version.helper.pyversion import PY3

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

    if PY3:
        return output
    else:
        return output.decode('utf-8')

def callCommand(args, cwd=None):
    return subprocess.call(args, cwd=cwd, stderr=DEVNULL)
