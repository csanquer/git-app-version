# -*- coding: utf-8 -*-

"""
    Helper functions to run shell commands
"""

import subprocess

from git_app_version.helper.pyversion import PY3

try:
    from subprocess import DEVNULL  # py3k
except ImportError:
    import os
    DEVNULL = open(os.devnull, 'wb')


def output_command(args, cwd=None):
    """
        run a shell command and return its output
    """
    try:
        output = subprocess.check_output(
            args,
            cwd=cwd,
            universal_newlines=True,
            stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        output = ''

    if PY3:
        return output
    else:
        return output.decode('utf-8')


def call_command(args, cwd=None):
    """
        run a shell command and return its exit code
    """
    return subprocess.call(args, cwd=cwd, stderr=DEVNULL)
