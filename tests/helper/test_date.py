# -*- coding: utf-8 -*-

from mock import patch
import pytest

from git_app_version.helper.date import *
from datetime import datetime
# import iso8601
import pytz

# from pprint import pprint,pformat

@patch('git_app_version.helper.date.datetime')
@pytest.mark.parametrize("mockInput,expected", [
    (datetime(2015, 12, 21, 11, 33, 45), datetime(2015, 12, 21, 11, 33, 45)),
])
def test_utcnow(mockDt, mockInput, expected):
    tz = pytz.utc

    expectedDate = tz.localize(expected)
    mockDt.now.return_value = tz.localize(mockInput)

    assert expectedDate == utcnow()

@pytest.mark.parametrize("isodate,utc,expected,expectedTZ", [
    ("2015-12-21T11:33:45+0100", False, datetime(2015, 12, 21, 11, 33, 45), 'Europe/Paris'),
    ("2015-12-21T11:33:45+0100", True, datetime(2015, 12, 21, 10, 33, 45), 'UTC'),
    ("2015-12-21T09:33:45+0000", False, datetime(2015, 12, 21, 9, 33, 45), 'UTC'),
    ("2015-12-21T09:33:45Z", False, datetime(2015, 12, 21, 9, 33, 45), 'UTC'),
])
def test_dateTimeFromIso8601(isodate, utc, expected, expectedTZ):
    tz = pytz.timezone(expectedTZ)
    expectedDate = tz.localize(expected)

    assert expectedDate == dateTimeFromIso8601(isodate, utc)

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

@pytest.mark.parametrize("dt,inputTZ,expected", [
    (datetime(2015, 12, 21, 10, 33, 45), 'UTC',          '1450694025'),
    (datetime(2015, 12, 21, 11, 33, 45), 'Europe/Paris', '1450694025'),
    (None, None, ''),
])
def test_timestampFromDateTime(dt, inputTZ, expected):
    if isinstance(dt, datetime):
        tz = pytz.timezone(inputTZ)
        dt = tz.localize(dt)

    assert expected == timestampFromDateTime(dt)
