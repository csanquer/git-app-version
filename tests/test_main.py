# -*- coding: utf-8 -*-

import os
import re

import pytest

import git_app_version.version
from git_app_version.__main__ import main as git_app_version_main
from test_helpers import git_utils


@pytest.fixture()
def tmpdir(tmpdir_factory):
    cwd = os.getcwd()
    new_cwd = tmpdir_factory.mktemp('git_repo')
    new_cwd_path = str(new_cwd)
    os.chdir(new_cwd_path)
    yield new_cwd_path
    os.chdir(cwd)


def test_version(capsys):
    arg = ['-V']
    with pytest.raises(SystemExit):
        git_app_version_main((arg))

    out, err = capsys.readouterr()
    expected = 'git-app-version ' + git_app_version.version.__version__ + "\n"
    assert out == expected or err == expected


def test_not_git_repository(tmpdir, capsys):
    arg = []
    assert git_app_version_main((arg)) == 1
    out, err = capsys.readouterr()
    assert err == ""
    expected = ("Error Writing version config file :"
                " The directory '{}' is not a git repository.\n")
    assert out == expected.format(tmpdir)


def test_quiet(tmpdir, capsys):
    arg = ['-q']

    git_utils.default_init()
    capsys.readouterr()

    exit_code = git_app_version_main((arg))
    output_path = os.path.join(tmpdir, 'version.json')

    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert exit_code == 0

    assert os.path.exists(output_path)


def test_verbose(tmpdir, capsys):
    arg = ['-v']

    git_utils.default_init()
    capsys.readouterr()

    exit_code = git_app_version_main((arg))
    output_path = os.path.join(tmpdir, 'version.json')

    out, err = capsys.readouterr()
    assert err == ''
    assert out.find('Git commit :') != -1
    assert out.find('version = 0.1.2') != -1
    assert re.search(
        "Git commit informations stored in {}\n".format(output_path), out)

    assert os.path.exists(output_path)
    assert exit_code == 0


def test_json(tmpdir, capsys):
    arg = []

    git_utils.default_init()
    capsys.readouterr()

    exit_code = git_app_version_main((arg))
    output_path = os.path.join(tmpdir, 'version.json')

    out, err = capsys.readouterr()
    assert err == ''
    assert out == "Git commit informations stored in {}\n".format(output_path)

    assert os.path.exists(output_path)
    assert exit_code == 0
