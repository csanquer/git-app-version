# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
import os
import re

import click
import pytest
from click.testing import CliRunner

import git_app_version.version
from git_app_version.__main__ import dump as git_app_version_main
from test_helpers import git_utils


@pytest.fixture(params=['git_empty', 'téléchargement'])
def tmpdir(tmpdir_factory, request):
    cwd = os.getcwd()
    new_cwd = tmpdir_factory.mktemp(request.param)
    new_cwd_path = str(new_cwd)
    os.chdir(new_cwd_path)
    yield new_cwd_path
    os.chdir(cwd)


@pytest.fixture()
def git_repo(tmpdir_factory):
    cwd = os.getcwd()
    new_cwd = tmpdir_factory.mktemp('git_repo')
    new_cwd_path = str(new_cwd)
    os.chdir(new_cwd_path)
    repo = git_utils.init(repo_dir=new_cwd_path)
    git_utils.commit(repo, message='commit 1',)
    git_utils.tag(repo, version='0.1.2',)
    yield repo
    os.chdir(cwd)


def test_version():
    runner = CliRunner()

    arg = ['--version']
    expected = 'git-app-version ' + git_app_version.version.__version__ + "\n"

    result = runner.invoke(git_app_version_main, arg)
    assert result.exit_code == 0
    assert result.output == expected


def test_not_git_repository(tmpdir):
    runner = CliRunner()

    arg = [tmpdir]
    expected = (u"The directory '{}' is not a git repository.\n")

    result = runner.invoke(git_app_version_main, arg)

    assert result.exit_code == 1
    assert result.output == expected.format(click.format_filename(tmpdir))


def test_quiet(git_repo):
    runner = CliRunner()

    arg = ['-q', git_repo.working_tree_dir]
    output_path = os.path.join(git_repo.working_tree_dir, 'version.json')

    result = runner.invoke(git_app_version_main, arg)

    assert result.exit_code == 0
    assert os.path.exists(output_path)


def test_json(git_repo):
    runner = CliRunner()

    arg = [git_repo.working_tree_dir]
    output_path = os.path.join(git_repo.working_tree_dir, 'version.json')

    result = runner.invoke(git_app_version_main, arg)

    assert result.output.find('Git commit :') != -1
    assert re.search(r"version\s+0.1.2", result.output)
    assert result.output.find('written to :') != -1
    assert result.output.find(output_path) != -1

    assert os.path.exists(output_path)
    assert result.exit_code == 0


def test_all(git_repo):
    runner = CliRunner()

    arg = ['-f', 'all', git_repo.working_tree_dir]
    output_path = os.path.join(git_repo.working_tree_dir, 'version')

    result = runner.invoke(git_app_version_main, arg)

    assert result.output.find('Git commit :') != -1
    assert re.search(r"version\s+0.1.2", result.output)
    assert result.output.find('written to :') != -1
    assert result.output.find(output_path + '.json') != -1
    assert result.output.find(output_path + '.yml') != -1
    assert result.output.find(output_path + '.xml') != -1
    assert result.output.find(output_path + '.sh') != -1
    assert result.output.find(output_path + '.ini') != -1
    assert result.output.find(output_path + '.csv') != -1

    assert os.path.exists(output_path + '.json')
    assert os.path.exists(output_path + '.yml')
    assert os.path.exists(output_path + '.xml')
    assert os.path.exists(output_path + '.sh')
    assert os.path.exists(output_path + '.ini')
    assert os.path.exists(output_path + '.csv')

    assert result.exit_code == 0


def test_metadata(git_repo):
    runner = CliRunner()

    arg = ['-m', 'foo=bar', '-m', 'desc=custom', git_repo.working_tree_dir]
    output_path = os.path.join(git_repo.working_tree_dir, 'version.json')

    result = runner.invoke(git_app_version_main, arg)

    assert result.output.find('Git commit :') != -1
    assert re.search(r"version\s+0.1.2", result.output)
    assert re.search(r"foo\s+bar", result.output)
    assert re.search(r"desc\s+custom", result.output)
    assert result.output.find(output_path) != -1

    assert os.path.exists(output_path)
    assert result.exit_code == 0


def test_metadata_reserved_key(git_repo):
    runner = CliRunner()

    bad_key = 'deploy_date'
    arg = ['-m', bad_key + '=foo', git_repo.working_tree_dir]

    expected = (
        "Error: Invalid value for \"--meta\" / \"-m\": {} is a reserved key\n")

    result = runner.invoke(git_app_version_main, arg)
    assert result.exit_code == 2
    assert result.output.find(expected.format(bad_key)) != -1


def test_metadata_invalid_format(git_repo):
    runner = CliRunner()

    bad_key = 'foo'
    arg = ['-m', bad_key, git_repo.working_tree_dir]

    expected = u"Error: Invalid value for \"--meta\" / \"-m\":"
    " {} is not a valid meta data string e.g. : <key>=<value>\n"

    result = runner.invoke(git_app_version_main, arg)
    assert result.exit_code == 2
    assert result.output.find(expected.format(bad_key)) != -1
