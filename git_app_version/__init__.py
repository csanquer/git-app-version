# -*- coding: utf-8 -*-
import os
import sys

from ._version import get_versions

__version__ = ''

if getattr(sys, 'frozen', False):  # pragma: no cover
    # we are running in a bundle
    bundle_dir = sys._MEIPASS

    version_file = os.path.join(bundle_dir, 'version.txt')
    if os.path.exists(version_file):
        with open(version_file) as f:
            __version__ = f.read().strip("\n")
else:  # pragma: no cover
    # we are running in a normal Python environment
    from pkg_resources import resource_string, resource_exists  # noqa
    if resource_exists('git_app_version', 'version.txt'):
        __version__ = resource_string('git_app_version',
                                      'version.txt').strip("\n")

if not __version__:  # pragma: no cover
    __version__ = get_versions()['version']

del get_versions
