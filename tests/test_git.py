# -*- coding: utf-8 -*-

from datetime import datetime

import pytest
import pytz
from mock import patch

from git_app_version.git import Git


@patch('git_app_version.helper.process.subprocess')
@pytest.mark.parametrize("cmd_result,expected", [
    (0, True),
    (1, False),
])
def test_is_git_repo(mock_sub_process, cmd_result, expected):
    git = Git()
    mock_sub_process.call.return_value = cmd_result

    assert git.is_git_repo(None) == expected


@patch('git_app_version.helper.date.datetime')
@pytest.mark.parametrize("mock_dt_now,expected", [
    (datetime(2015, 12, 21, 11, 33, 45), datetime(2015, 12, 21, 11, 33, 45)),
])
def test_get_deploy_date(mock_dt, mock_dt_now, expected):
    git = Git()
    tz = pytz.utc

    expectedDate = tz.localize(expected)
    mock_dt.now.return_value = tz.localize(mock_dt_now)

    assert expectedDate == git.get_deploy_date()


@patch('git_app_version.helper.process.subprocess')
@pytest.mark.parametrize("cmd_result,expected", [
    ('40aaf83', '40aaf83'),
    ('', ''),
])
def test_get_abbrev_commit(mock_sub_process, cmd_result, expected):
    git = Git()
    mock_sub_process.check_output.return_value = cmd_result

    assert git.get_abbrev_commit() == expected


@patch('git_app_version.helper.process.subprocess')
@pytest.mark.parametrize("cmd_result,expected", [
    ('40aaf83894b98898895d478f8b7cc4a866b1d62c',
     '40aaf83894b98898895d478f8b7cc4a866b1d62c'),
    ('', ''),
])
def test_get_full_commit(mock_sub_process, cmd_result, expected):
    git = Git()
    mock_sub_process.check_output.return_value = cmd_result

    assert git.get_full_commit() == expected


@patch('git_app_version.helper.process.subprocess')
@pytest.mark.parametrize("cmd_result,expected", [
    ('Paul Dupond', 'Paul Dupond'),
    ('', ''),
])
def test_get_committer_name(mock_sub_process, cmd_result, expected):
    git = Git()
    mock_sub_process.check_output.return_value = cmd_result
    assert git.get_committer_name() == expected


@patch('git_app_version.helper.process.subprocess')
@pytest.mark.parametrize("cmd_result,expected", [
    ('paul.dupond@example.com', 'paul.dupond@example.com'),
    ('', ''),
])
def test_get_committer_email(mock_sub_process, cmd_result, expected):
    git = Git()
    mock_sub_process.check_output.return_value = cmd_result
    assert git.get_committer_email() == expected


@patch('git_app_version.helper.process.subprocess')
@pytest.mark.parametrize("cmd_result,expected", [
    ('Paul Dupond', 'Paul Dupond'),
    ('', ''),
])
def test_get_author_name(mock_sub_process, cmd_result, expected):
    git = Git()
    mock_sub_process.check_output.return_value = cmd_result
    assert git.get_author_name() == expected


@patch('git_app_version.helper.process.subprocess')
@pytest.mark.parametrize("cmd_result,expected", [
    ('paul.dupond@example.com', 'paul.dupond@example.com'),
    ('', ''),
])
def test_get_author_email(mock_sub_process, cmd_result, expected):
    git = Git()
    mock_sub_process.check_output.return_value = cmd_result
    assert git.get_author_email() == expected


@patch('git_app_version.helper.process.subprocess')
@pytest.mark.parametrize("cmd_result,expected,expectedTZ", [
    ('2016-01-01 00:33:33 +0100', datetime(2016, 1, 1, 0, 33, 33),
     'Europe/Paris'),
    ('', None, None),
])
def test_get_commit_date(mock_sub_process, cmd_result, expected, expectedTZ):
    git = Git()
    mock_sub_process.check_output.return_value = cmd_result

    if isinstance(expected, datetime):
        tz = pytz.timezone(expectedTZ)
        expected = tz.localize(expected)

    assert git.get_commit_date() == expected


@patch('git_app_version.helper.process.subprocess')
@pytest.mark.parametrize("cmd_result,expected,expectedTZ", [
    ('2016-01-01 00:33:33 +0100', datetime(2016, 1, 1, 0, 33, 33),
     'Europe/Paris'),
    ('', None, None),
])
def test_get_author_date(mock_sub_process, cmd_result, expected, expectedTZ):
    git = Git()
    mock_sub_process.check_output.return_value = cmd_result

    if isinstance(expected, datetime):
        tz = pytz.timezone(expectedTZ)
        expected = tz.localize(expected)

    assert git.get_author_date() == expected


@patch('git_app_version.helper.process.subprocess')
@pytest.mark.parametrize("cmd_results,default,expected", [
    (('v1.1.0-3-g439e52', '40aaf83'), None, 'v1.1.0-3-g439e52'),
    (('', '40aaf83'), None, '40aaf83'),
    (('', '40aaf83'), '8fa82b6', '8fa82b6'),
])
def test_get_version(mock_sub_process, cmd_results, default, expected):
    git = Git()
    mock_sub_process.check_output.side_effect = cmd_results

    assert git.get_version(default=default) == expected


@patch('git_app_version.helper.process.subprocess')
@pytest.mark.parametrize("cmd_result,commit,expected", [
    ('', 'HEAD', []),
    ("  origin/HEAD -> origin/master\n  origin/master\n"
     "  origin/feature/my_feature\n",
     'HEAD', ['origin/master', 'origin/feature/my_feature'])
])
def test_get_branches(mock_sub_process, cmd_result, commit, expected):
    git = Git()
    mock_sub_process.check_output.return_value = cmd_result

    assert git.get_branches(commit=commit) == expected


@patch('git_app_version.helper.process.subprocess')
@pytest.mark.parametrize("cmd_results,branches,abbrevCommit,expected", [
    (('40aaf83', 'a7b5290'), [
     'origin/master', 'origin/feature/my_feature'],
     '40aaf83', ['origin/master']),
    (('40aaf83'), [], '', []),
])
def test_get_top_branches(mock_sub_process, cmd_results,
                          branches, abbrevCommit, expected):
    git = Git()
    mock_sub_process.check_output.side_effect = cmd_results

    assert git.get_top_branches(
        branches=branches,
        abbrev_commit=abbrevCommit) == expected


@pytest.mark.parametrize("branches,expected", [
    (['origin/master', 'origin/feature/my_feature'],
     ['master', 'feature/my_feature']),
])
def test_remove_remote_prefix(branches, expected):
    git = Git()

    assert git.remove_remote_prefix(branches=branches) == expected


@patch('git_app_version.helper.date.datetime')
@patch('git_app_version.helper.process.subprocess')
@pytest.mark.parametrize("cmd_results,now,expected", [
    (
        (
            '40aaf83',
            '2016-03-01 10:33:33 +0100',
            '2016-03-02 14:10:48 +0100',
            "  origin/HEAD -> origin/master\n  origin/master\n"
            "  origin/feature/my_feature\n",
            '40aaf83',
            '83bc5f1',
            'v1.1.0-3-g439e52',
            '40aaf83894b98898895d478f8b7cc4a866b1d62c',
            'Martin Durand',
            'martin.durand@example.fr',
            'Paul Dupont',
            'paul.dupont@example.fr'
        ),
        datetime(2016, 3, 2, 11, 33, 45),
        {
            'version': 'v1.1.0-3-g439e52',
            'abbrev_commit': '40aaf83',
            'full_commit': '40aaf83894b98898895d478f8b7cc4a866b1d62c',
            'author_name': 'Martin Durand',
            'author_email': 'martin.durand@example.fr',
            'committer_name': 'Paul Dupont',
            'committer_email': 'paul.dupont@example.fr',
            'branches': ['master', 'feature/my_feature'],
            'top_branches': ['master'],
            'commit_date': '2016-03-01T09:33:33+0000',
            'commit_timestamp': '1456824813',
            'author_date': '2016-03-02T13:10:48+0000',
            'author_timestamp': '1456924248',
            'deploy_date': '2016-03-02T11:33:45+0000',
            'deploy_timestamp': '1456918425'
        }
    )
])
def test_get_infos(mock_sub_process, mock_dt, now, cmd_results, expected):
    git = Git()

    tz = pytz.utc
    mock_dt.now.return_value = tz.localize(now)
    mock_dt.side_effect = lambda *args, **kw: datetime(*args, **kw)

    mock_sub_process.check_output.side_effect = cmd_results

    assert git.get_infos() == expected
