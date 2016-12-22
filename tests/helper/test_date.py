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
def test_utcnow(mock_dt, mockInput, expected):
    tz = pytz.utc

    expected_date = tz.localize(expected)
    mock_dt.now.return_value = tz.localize(mockInput)

    assert expected_date == utcnow()

@pytest.mark.parametrize("isodate,utc,expected,expected_tz", [
    ("2015-12-21T11:33:45+0100", False, datetime(2015, 12, 21, 11, 33, 45), 'Europe/Paris'),
    ("2015-12-21T11:33:45+0100", True, datetime(2015, 12, 21, 10, 33, 45), 'UTC'),
    ("2015-12-21T09:33:45+0000", False, datetime(2015, 12, 21, 9, 33, 45), 'UTC'),
    ("2015-12-21T09:33:45Z", False, datetime(2015, 12, 21, 9, 33, 45), 'UTC'),
])
def test_datetime_from_iso8601(isodate, utc, expected, expected_tz):
    tz = pytz.timezone(expected_tz)
    expected_date = tz.localize(expected)

    assert expected_date == datetime_from_iso8601(isodate, utc)

@pytest.mark.parametrize("input,input_tz,expected", [
    (datetime(2015, 12, 21, 11, 33, 45), 'Europe/Paris', "2015-12-21T11:33:45+0100"),
    (datetime(2015, 12, 21, 10, 33, 45), 'UTC', "2015-12-21T10:33:45+0000"),
    (None, None, ''),
])
def test_iso8601_from_datetime(input, input_tz, expected):
    if isinstance(input, datetime):
        tz = pytz.timezone(input_tz)
        input = tz.localize(input)

    assert expected == iso8601_from_datetime(input)

@pytest.mark.parametrize("dt,input_tz,expected", [
    (datetime(2015, 12, 21, 10, 33, 45), 'UTC',          '1450694025'),
    (datetime(2015, 12, 21, 11, 33, 45), 'Europe/Paris', '1450694025'),
    (None, None, ''),
])
def test_timestamp_from_datetime(dt, input_tz, expected):
    if isinstance(dt, datetime):
        tz = pytz.timezone(input_tz)
        dt = tz.localize(dt)

    assert expected == timestamp_from_datetime(dt)
