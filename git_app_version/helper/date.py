# -*- coding: utf-8 -*-

from datetime import datetime
import iso8601
import pytz

def utcnow():
    return datetime.now(pytz.utc)

def dateTimeFromIso8601(isodate, utc=False):
    dt = iso8601.parse_date(isodate)
    if utc:
        return dt.astimezone(pytz.utc)

    return dt

def iso8601FromDateTime(dt):
    try:
        return dt.strftime('%Y-%m-%dT%H:%M:%S%z')
    except Exception as exc:
        return ''

def timestampFromDateTime(dt):
    try:
        utcDt  = dt.replace(tzinfo=None) - dt.utcoffset()
        return str(int((utcDt - datetime(1970, 1, 1)).total_seconds()))
    except Exception as exc:
        return ''
