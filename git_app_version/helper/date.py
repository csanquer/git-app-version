# -*- coding: utf-8 -*-
"""
    Date time helpers

    to convert easily date to ISO format and timestamp
"""
from __future__ import unicode_literals

from datetime import datetime

import iso8601
import pytz


def utcnow():
    """
        return current UTC date
    """
    return datetime.now(pytz.utc)


def datetime_from_iso8601(isodate, utc=False):
    """
        convert ISO 8601 date string to datetime
    """
    try:
        date = iso8601.parse_date(isodate)
        if utc:
            return date.astimezone(pytz.utc)

        return date
    except (AttributeError, iso8601.ParseError):
        return None


def iso8601_from_datetime(date):
    """
        convert datetime to ISO 8601 date string
    """
    try:
        return date.strftime('%Y-%m-%dT%H:%M:%S%z')
    except (AttributeError, iso8601.ParseError):
        return ''


def timestamp_from_datetime(date):
    """
        convert datetime to timestamp (UTC)
    """
    try:
        utc_date = date.replace(tzinfo=None) - date.utcoffset()
        return str(int((utc_date - datetime(1970, 1, 1)).total_seconds()))
    except (AttributeError, iso8601.ParseError):
        return ''
