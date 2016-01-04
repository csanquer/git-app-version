# -*- coding: utf-8 -*-

from mock import patch
import pytest

from git_app_version.helper.date import *
from datetime import datetime
# import iso8601
import pytz

from pprint import pprint,pformat

@patch('git_app_version.helper.date.datetime')
@pytest.mark.parametrize("mockInput,expected", [
    (datetime(2015, 12, 21, 11, 33, 45), datetime(2015, 12, 21, 11, 33, 45)),
])
def test_utcnow(mockDt, mockInput, expected):
    tz = pytz.utc

    expectedDate = tz.localize(expected)
    mockDt.now.return_value = tz.localize(mockInput)

    assert expectedDate == utcnow()

@pytest.mark.parametrize("input,expected", [
    ("2015-12-21T11:33:45+0100", datetime(2015, 12, 21, 10, 33, 45)),
    ("2015-12-21T09:33:45+0000", datetime(2015, 12, 21, 9, 33, 45)),
    ("2015-12-21T09:33:45Z", datetime(2015, 12, 21, 9, 33, 45)),
])
def test_dateTimeFromIso8601(input, expected):
    tz = pytz.utc
    expectedDate = tz.localize(expected)
    assert expectedDate == dateTimeFromIso8601(input)

@pytest.mark.parametrize("input,inputTZ,expected", [
    (datetime(2015, 12, 21, 11, 33, 45), 'Europe/Paris', "2015-12-21T11:33:45+0100"),
    (datetime(2015, 12, 21, 10, 33, 45), 'UTC', "2015-12-21T10:33:45+0000"),
    (None, None, ''),
])
def test_iso8601FromDateTime(input, inputTZ, expected):
    if isinstance(input, datetime):
        tz = pytz.timezone(inputTZ)
        input = tz.localize(input)

    assert expected == iso8601FromDateTime(input)

@pytest.mark.parametrize("input,expected", [
    (datetime(2015, 12, 21, 10, 33, 45), '1450690425'),
    (None, ''),
])
def test_timestampFromDateTime(input, expected):
    if isinstance(input, datetime):
        tz = pytz.utc
        input = tz.localize(input)

    assert expected == timestampFromDateTime(input)
