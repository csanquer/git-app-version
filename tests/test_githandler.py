# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from datetime import datetime

import pytest
import pytz
from mock import patch

from git_app_version.githandler import GitHandler
from test_helpers import git_utils


@pytest.fixture()
def git_repo(tmpdir_factory):
    cwd = os.getcwd()
    new_cwd = tmpdir_factory.mktemp('git_repo')
    new_cwd_path = str(new_cwd)
    os.chdir(new_cwd_path)
    repo = git_utils.init(repo_dir=new_cwd_path)
    yield repo
    os.chdir(cwd)


@pytest.fixture()
def git_repo_remote(tmpdir_factory):
    cwd = os.getcwd()
    new_cwd = tmpdir_factory.mktemp('git_repo_remote')
    new_cwd_path = str(new_cwd)
    os.chdir(new_cwd_path)

    name = 'Paul Dupond'
    email = 'paul.dupond@example.com'

    author_tz = 'Europe/Paris'
    tz = pytz.timezone(author_tz)

    author_dt1 = datetime(2016, 12, 10, 0, 33, 33)
    author_dt2 = datetime(2016, 12, 12, 2, 33, 33)
    author_dt3 = datetime(2016, 12, 17, 6, 40, 21)

    repo = git_utils.init(repo_dir=new_cwd_path)
    git_utils.commit(repo, message='commit 1',
                                   author='{} <{}>'.format(name, email),
                                   date=tz.localize(author_dt1).isoformat())
    git_utils.commit(repo, message='commit 2',
                                   author='{} <{}>'.format(name, email),
                                   date=tz.localize(author_dt2).isoformat())
    git_utils.tag(repo, 'v0.1.2')
    git_utils.branch(repo, 'release', 'master')
    git_utils.commit(repo, message='commit 3',
                                   author='{} <{}>'.format(name, email),
                                   date=tz.localize(author_dt3).isoformat())
    git_utils.branch(repo, 'feature/my_feature', 'master')

    yield repo
    os.chdir(cwd)


@pytest.fixture()
def git_repo_local(tmpdir_factory, git_repo_remote):
    cwd = os.getcwd()
    new_cwd = tmpdir_factory.mktemp('git_repo_local')
    new_cwd_path = str(new_cwd)
    os.chdir(new_cwd_path)
    repo = git_utils.clone(git_repo_remote, new_cwd_path)
    yield repo
    os.chdir(cwd)


@pytest.fixture()
def handler(git_repo):
    return GitHandler(git_repo.working_dir)


@pytest.fixture()
def handler_local(git_repo_local):
    return GitHandler(git_repo_local.working_dir)


def test_not_git_repository(tmpdir):
    not_git_dir = tmpdir.mkdir('not_git')

    with pytest.raises(ValueError):
        GitHandler(str(not_git_dir))


@patch('git_app_version.helper.date.datetime')
@pytest.mark.parametrize("mock_dt_now,expected", [
    (datetime(2015, 12, 21, 11, 33, 45), datetime(2015, 12, 21, 11, 33, 45)),
])
def test_get_deploy_date(mock_dt, mock_dt_now, expected, handler):
    tz = pytz.utc

    expectedDate = tz.localize(expected)
    mock_dt.now.return_value = tz.localize(mock_dt_now)

    assert expectedDate == handler.get_deploy_date()


def test_getters(git_repo_local, handler_local):
    name = 'Paul Dupond'
    email = 'paul.dupond@example.com'

    author_dt = datetime(2016, 12, 17, 6, 40, 21)
    author_tz = 'Europe/Paris'
    tz = pytz.timezone(author_tz)
    author_dt_tz = tz.localize(author_dt)

    commit = git_repo_local.commit('HEAD')

    assert handler_local.get_full_commit() == commit.hexsha
    assert handler_local.get_abbrev_commit() == commit.hexsha[0:7]
    assert handler_local.get_version() == 'v0.1.2-1-g' + commit.hexsha[0:7]

    assert handler_local.get_message() == commit.message.strip()

    assert handler_local.get_author_name() == name
    assert handler_local.get_author_email() == email

    assert handler_local.get_committer_name() == 'User Test'
    assert handler_local.get_committer_email() == 'user@example.com'

    assert handler_local.get_author_date() == author_dt_tz
    assert handler_local.get_commit_date() == author_dt_tz


def test_get_version_no_commit(handler):
    default = '8fa82b6'
    assert handler.get_version() == ''
    assert handler.get_version(default=default) == default


def test_get_version_no_tags(git_repo, handler):
    default = '8fa82b6'
    commit = git_utils.commit(repo=git_repo, message='test 1')

    assert handler.get_version(default=default) == commit.hexsha[0:7]


def test_get_version_on_tag(git_repo, handler):
    default = '8fa82b6'
    git_utils.commit(repo=git_repo, message='test 1')
    git_utils.tag(repo=git_repo, version='v0.1.3')

    assert handler.get_version(default=default) == 'v0.1.3'


def test_get_version_after_tag(git_repo, handler):
    default = '8fa82b6'
    git_utils.commit(repo=git_repo, message='test 1')
    git_utils.tag(repo=git_repo, version='v0.1.3')
    commit = git_utils.commit(repo=git_repo, message='test 2')

    assert handler.get_version(
        default=default) == 'v0.1.3-1-g' + commit.hexsha[0:7]


def test_get_branches(git_repo_local, handler_local):
    expected = ['origin/feature/my_feature', 'origin/master']
    assert handler_local.get_branches() == expected


def test_get_top_branches(git_repo_local, handler_local):
    branches = ['origin/feature/my_feature', 'origin/release', 'origin/master']
    expected = ['origin/feature/my_feature', 'origin/master']
    abbrev_commit = git_repo_local.commit('HEAD').hexsha[0:7]

    assert handler_local.get_top_branches(
        branches=branches,
        abbrev_commit=abbrev_commit) == expected


@pytest.mark.parametrize("branches,expected", [
    (['origin/master', 'origin/feature/my_feature'],
     ['master', 'feature/my_feature']),
])
def test_remove_remote_prefix(branches, expected, handler):
    assert handler.remove_remote_prefix(branches=branches) == expected


@patch('git_app_version.helper.date.datetime')
def test_get_infos(mock_dt, git_repo_local, handler_local):
    commit = git_repo_local.commit('HEAD')
    now = datetime(2016, 12, 20, 11, 33, 45)

    tz = pytz.utc
    now_tz = tz.localize(now)
    mock_dt.now.return_value = now_tz
    mock_dt.side_effect = lambda *args, **kw: datetime(*args, **kw)

    expected = {
        'message': 'commit 3',
        'abbrev_commit': commit.hexsha[0:7],
        'author_date': '2016-12-17T06:40:21+0100',
        'author_email': 'paul.dupond@example.com',
        'author_name': 'Paul Dupond',
        'author_timestamp': '1481953221',
        'branches': ['feature/my_feature', 'master'],
        'commit_date': '2016-12-17T06:40:21+0100',
        'commit_timestamp': '1481953221',
        'committer_email': 'user@example.com',
        'committer_name': 'User Test',
        'deploy_date': now_tz.strftime('%Y-%m-%dT%H:%M:%S%z'),
        'deploy_timestamp': '1482233625',
        'full_commit': commit.hexsha,
        'top_branches': ['feature/my_feature', 'master'],
        'version': 'v0.1.2-1-g' + commit.hexsha[0:7]
    }

    assert handler_local.get_infos() == expected
