# -*- coding: utf-8 -*-

from mock import patch
import pytest
import tempfile
import os
import re

from git_app_version.__main__ import main as git_app_version_main
import git_app_version.version
from git_app_version.helper.pyversion import PY3

@pytest.fixture()
def tmpdir(tmpdir_factory):
    cwd = os.getcwd()
    new_cwd = tmpdir_factory.mktemp('git_repo')
    new_cwd_path = str(new_cwd)
    os.chdir(new_cwd_path)
    yield new_cwd_path
    os.chdir(cwd)

def _git_commit(message):
    os.system('git commit --allow-empty -m "{}"'.format(message))

def _git_tag(version):
    _git_commit("release: {}".format(version))
    os.system('git tag -am {0} {0}'.format(version))

def _git_init(version='0.1.2'):
    os.system('git init')
    os.system('git config user.email "user@example.com"')
    os.system('git config user.name "User Test"')

    _git_commit('initial commit')
    _git_tag(version)

def test_version(capsys):
    arg = ['-V']
    with pytest.raises(SystemExit):
        git_app_version_main((arg))

    out, err = capsys.readouterr()
    std_to_test = out if PY3 else err
    assert std_to_test == 'git-app-version '+git_app_version.version.__version__+"\n"

def test_not_git_repository(tmpdir, capsys):
    arg = []
    assert git_app_version_main((arg)) == 1
    out, err = capsys.readouterr()
    assert err == ""
    assert out == "Error Writing version config file : The directory '{}' is not a git repository.\n".format(tmpdir)

def test_quiet(tmpdir, capsys):
    arg = ['-q']

    _git_init()
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

    _git_init()
    capsys.readouterr()

    exit_code = git_app_version_main((arg))
    output_path = os.path.join(tmpdir, 'version.json')

    out, err = capsys.readouterr()
    assert err == ''
    assert out.find('Git commit :') != -1
    assert out.find('version = 0.1.2') != -1
    assert re.search("Git commit informations stored in {}\n".format(output_path), out)

    assert os.path.exists(output_path)
    assert exit_code == 0

def test_json(tmpdir, capsys):
    arg = []

    _git_init()
    capsys.readouterr()

    exit_code = git_app_version_main((arg))
    output_path = os.path.join(tmpdir, 'version.json')

    out, err = capsys.readouterr()
    assert err == ''
    assert out == "Git commit informations stored in {}\n".format(output_path)

    assert os.path.exists(output_path)
    assert exit_code == 0
