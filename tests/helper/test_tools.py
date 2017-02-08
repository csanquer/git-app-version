# -*- coding: utf-8 -*-

import os
import shutil
import sys

import pytest

import git_app_version.helper.tools as tools_helper


@pytest.fixture
def output_dir():
    cwd = os.path.realpath(os.path.dirname(__file__))
    path = cwd + '/output'
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path, 493)

    return path


@pytest.mark.parametrize("path,mode,abs_path", [
    ('foo/bar', 493, False),
    ('foo/bar', 493, True),
])
def test_create_parent_dirs(output_dir, path, mode, abs_path):
    if abs_path:
        path = os.path.join(output_dir, path)

    expected_path = os.path.join(output_dir, path)
    assert expected_path == tools_helper.create_parent_dirs(path,
                                                            output_dir,
                                                            mode)
    assert os.path.exists(os.path.dirname(expected_path))


@pytest.mark.skipif(sys.version_info > (3,),
                    reason="python version >= 3.0")
@pytest.mark.parametrize("text,encoding,expected", [
    (u'Se\u0301bastien', 'utf-8', 'Se\xcc\x81bastien'),
    ('Sébastien', 'utf-8', 'S\xc3\xa9bastien'),
])
def test_encode(text, encoding, expected):
    assert expected == tools_helper.encode(text, encoding=encoding)


@pytest.mark.parametrize("items,expected", [
    (['master', 'release'], "['master', 'release']"),
])
def test_flatten(items, expected):
    assert expected == tools_helper.flatten(items)
