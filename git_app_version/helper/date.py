# -*- coding: utf-8 -*-

from datetime import datetime
import iso8601
# import tzlocal
import pytz

def utcnow():
    return datetime.now(pytz.utc)

def dateTimeFromIso8601(isodate):
    return iso8601.parse_date(isodate).astimezone(pytz.utc)

def iso8601FromDateTime(dt):
    try:
        return dt.strftime('%Y-%m-%dT%H:%M:%S%z')
    except Exception as exc:
        return ''

def timestampFromDateTime(dt):
    try:
        return dt.strftime('%s')
    except Exception as exc:
        return ''
