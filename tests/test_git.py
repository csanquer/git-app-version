# -*- coding: utf-8 -*-

from mock import patch
import pytest

from git_app_version.git import Git
from datetime import datetime
import pytz

from pprint import pprint,pformat

@patch('git_app_version.helper.process.subprocess')
@pytest.mark.parametrize("cmdResult,expected", [
    (0, True),
    (1, False),
])
def test_isGitRepository(mockSubProcess, cmdResult, expected):
    git = Git()
    mockSubProcess.call.return_value = cmdResult

    assert git.isGitRepository(None) == expected


@patch('git_app_version.helper.date.datetime')
@pytest.mark.parametrize("mockDtNow,expected", [
    (datetime(2015, 12, 21, 11, 33, 45), datetime(2015, 12, 21, 11, 33, 45)),
])
def test_getDeployDate(mockDt, mockDtNow, expected):
    git = Git()
    tz = pytz.utc

    expectedDate = tz.localize(expected)
    mockDt.now.return_value = tz.localize(mockDtNow)

    assert expectedDate == git.getDeployDate()

@patch('git_app_version.helper.process.subprocess')
@pytest.mark.parametrize("cmdResult,expected", [
    ('40aaf83', '40aaf83'),
    ('', ''),
])
def test_getAbbrevCommit(mockSubProcess, cmdResult, expected):
    git = Git()
    mockSubProcess.check_output.return_value = cmdResult

    assert git.getAbbrevCommit() == expected

@patch('git_app_version.helper.process.subprocess')
@pytest.mark.parametrize("cmdResult,expected", [
    ('40aaf83894b98898895d478f8b7cc4a866b1d62c', '40aaf83894b98898895d478f8b7cc4a866b1d62c'),
    ('', ''),
])
def test_getFullCommit(mockSubProcess, cmdResult, expected):
    git = Git()
    mockSubProcess.check_output.return_value = cmdResult

    assert git.getFullCommit() == expected


@patch('git_app_version.helper.process.subprocess')
@pytest.mark.parametrize("cmdResult,expected", [
    ('Paul Dupond', 'Paul Dupond'),
    ('', ''),
])
def test_getCommitterName(mockSubProcess, cmdResult, expected):
    git = Git()
    mockSubProcess.check_output.return_value = cmdResult
    assert git.getCommitterName() == expected

@patch('git_app_version.helper.process.subprocess')
@pytest.mark.parametrize("cmdResult,expected", [
    ('paul.dupond@example.com', 'paul.dupond@example.com'),
    ('', ''),
])
def test_getCommitterEmail(mockSubProcess, cmdResult, expected):
    git = Git()
    mockSubProcess.check_output.return_value = cmdResult
    assert git.getCommitterEmail() == expected

@patch('git_app_version.helper.process.subprocess')
@pytest.mark.parametrize("cmdResult,expected", [
    ('Paul Dupond', 'Paul Dupond'),
    ('', ''),
])
def test_getAuthorName(mockSubProcess, cmdResult, expected):
    git = Git()
    mockSubProcess.check_output.return_value = cmdResult
    assert git.getAuthorName() == expected

@patch('git_app_version.helper.process.subprocess')
@pytest.mark.parametrize("cmdResult,expected", [
    ('paul.dupond@example.com', 'paul.dupond@example.com'),
    ('', ''),
])
def test_getAuthorEmail(mockSubProcess, cmdResult, expected):
    git = Git()
    mockSubProcess.check_output.return_value = cmdResult
    assert git.getAuthorEmail() == expected

@patch('git_app_version.helper.process.subprocess')
@pytest.mark.parametrize("cmdResult,expected,expectedTZ", [
    ('2016-01-01 00:33:33 +0100', datetime(2016, 1, 1, 0, 33, 33), 'Europe/Paris'),
    ('', None, None),
])
def test_getCommitDate(mockSubProcess, cmdResult, expected, expectedTZ):
    git = Git()
    mockSubProcess.check_output.return_value = cmdResult

    if isinstance(expected, datetime):
        tz = pytz.timezone(expectedTZ)
        expected = tz.localize(expected)

    assert git.getCommitDate() == expected

@patch('git_app_version.helper.process.subprocess')
@pytest.mark.parametrize("cmdResult,expected,expectedTZ", [
    ('2016-01-01 00:33:33 +0100', datetime(2016, 1, 1, 0, 33, 33), 'Europe/Paris'),
    ('', None, None),
])
def test_getAuthorDate(mockSubProcess, cmdResult, expected, expectedTZ):
    git = Git()
    mockSubProcess.check_output.return_value = cmdResult

    if isinstance(expected, datetime):
        tz = pytz.timezone(expectedTZ)
        expected = tz.localize(expected)

    assert git.getAuthorDate() == expected

@patch('git_app_version.helper.process.subprocess')
@pytest.mark.parametrize("cmdResults,default,expected", [
    (('v1.1.0-3-g439e52', '40aaf83'), None, 'v1.1.0-3-g439e52'),
    (('','40aaf83'), None, '40aaf83'),
    (('','40aaf83'), '8fa82b6', '8fa82b6'),
])
def test_getVersion(mockSubProcess, cmdResults, default, expected):
    git = Git()
    mockSubProcess.check_output.side_effect = cmdResults

    assert git.getVersion(default=default) == expected

@patch('git_app_version.helper.process.subprocess')
@pytest.mark.parametrize("cmdResult,commit,expected", [
    ('', 'HEAD', []),
    ("  origin/HEAD -> origin/master\n  origin/master\n  origin/feature/my_feature\n", 'HEAD', ['origin/master', 'origin/feature/my_feature'])
])
def test_getBranches(mockSubProcess, cmdResult, commit, expected):
    git = Git()
    mockSubProcess.check_output.return_value = cmdResult

    assert git.getBranches(commit=commit) == expected

@patch('git_app_version.helper.process.subprocess')
@pytest.mark.parametrize("cmdResults,branches,abbrevCommit,expected", [
    (('40aaf83', 'a7b5290'), ['origin/master', 'origin/feature/my_feature'], '40aaf83', ['origin/master']),
])
def test_getTopBranches(mockSubProcess, cmdResults, branches, abbrevCommit, expected):
    git = Git()
    mockSubProcess.check_output.side_effect = cmdResults

    assert git.getTopBranches(branches=branches, abbrevCommit=abbrevCommit) == expected

@pytest.mark.parametrize("branches,expected", [
    (['origin/master', 'origin/feature/my_feature'], ['master', 'feature/my_feature']),
])
def test_removeRemotePrefix(branches, expected):
    git = Git()

    assert git.removeRemotePrefix(branches=branches) == expected


@patch('git_app_version.helper.date.datetime')
@patch('git_app_version.helper.process.subprocess')
@pytest.mark.parametrize("cmdResults,now,expected", [
    (
        (
            '40aaf83',
            '2016-03-01 10:33:33 +0100',
            '2016-03-02 14:10:48 +0100',
            "  origin/HEAD -> origin/master\n  origin/master\n  origin/feature/my_feature\n",
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
def test_getInfos(mockSubProcess, mockDt, now, cmdResults, expected):
    git = Git()

    tz = pytz.utc
    mockDt.now.return_value = tz.localize(now)
    mockDt.side_effect = lambda *args, **kw: datetime(*args, **kw)

    mockSubProcess.check_output.side_effect = cmdResults

    assert git.getInfos() == expected
