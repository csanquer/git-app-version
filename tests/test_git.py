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
@pytest.mark.parametrize("cmdResults,expected", [
    (('v1.1.0-3-g439e52', '40aaf83'), 'v1.1.0-3-g439e52'),
    (('','40aaf83'), '40aaf83'),
])
def test_getVersion(mockSubProcess, cmdResults, expected):
    git = Git()
    mockSubProcess.check_output.side_effect = cmdResults

    assert git.getVersion() == expected

@patch('git_app_version.helper.date.datetime')
@patch('git_app_version.helper.process.subprocess')
@pytest.mark.parametrize("cmdResults,now,expected", [
    (
        (
            '2016-03-01 10:33:33 +0100',
            'v1.1.0-3-g439e52',
            '40aaf83',
            '40aaf83894b98898895d478f8b7cc4a866b1d62c'
        ),
        datetime(2016, 3, 2, 11, 33, 45),
        {
            'version': 'v1.1.0-3-g439e52',
            'abbrev_commit': '40aaf83',
            'full_commit': '40aaf83894b98898895d478f8b7cc4a866b1d62c',
            'commit_date': '2016-03-01T09:33:33+0000',
            'commit_timestamp': '1456824813',
            'deploy_date': '2016-03-02T11:33:45+0000',
            'deploy_timestamp': '1456918425',
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
