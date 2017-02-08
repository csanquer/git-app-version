# -*- coding: utf-8 -*-
"""
    various tool helpers
"""
from __future__ import unicode_literals

import os


def create_parent_dirs(path, cwd=None, mode=493):
    '''
    create parent directories tree for a path

    mode : 493 in decimal = 0755 in octal
    '''

    if not os.path.isabs(path):
        cwd = cwd if cwd else os.getcwd()
        path = cwd + '/' + path

    parent_dir = os.path.dirname(path)
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir, mode)

    return path


def flatten(items):
    '''
    transform a list to a string representation
    '''

    if isinstance(items, list):
        flattened_list = ''
        if len(items):
            flattened_list = "'{}'".format("', '".join(items))
        return "[{}]".format(flattened_list)
    else:
        return items
