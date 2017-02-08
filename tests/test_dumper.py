# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import os
import re
import shutil
from builtins import open

import pytest
import xmltodict
import yaml
from backports import configparser, csv

from git_app_version.dumper import FileDumper as AppDumper

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


@pytest.fixture
def output_dir():
    cwd = os.path.realpath(os.path.dirname(__file__))
    path = cwd + '/output'
    if os.path.exists(path):
        shutil.rmtree(path)
    # os.makedirs(path, 493)

    return path


def get_file_content(path, section=None, fileFormat=None,
                     csv_delimiter=',', csv_quote='"', csv_eol='lf'):
    if fileFormat == 'yml' or fileFormat == 'yaml':
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.load(f)
    elif fileFormat == 'xml':
        with open(path, 'r', encoding='utf-8') as f:
            return xmltodict.parse(f.read(), dict_constructor=dict)
    elif fileFormat == 'ini':
        config = configparser.RawConfigParser()
        config.read(path)

        data = {}
        if not section:
            section = 'app_version'

        if config.has_section(section):
            for k, v in config.items(section):
                data[k] = v

        return data
    elif fileFormat == 'csv':
        data = {}

        eol = '\r\n' if csv_eol == 'crlf' or csv_eol == '\r\n' else '\n'

        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.reader(
                f,
                delimiter=csv_delimiter,
                quotechar=csv_quote,
                lineterminator=eol,
                quoting=csv.QUOTE_MINIMAL)
            for row in reader:
                data[row[0]] = row[1]

        return data
    elif fileFormat == 'sh':
        data = {}
        pattern = re.compile(r'^([^=]+)="(.*)"$')
        with open(path, 'r', encoding='utf8') as f:
            for line in f:
                match = pattern.match(line)
                if match:
                    data[match.group(1)] = match.group(2)

        return data
    elif fileFormat == 'json':
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()


@pytest.mark.parametrize(
    'data,data_format,target,section,expected_target,expected_data,'
    'csv_delimiter,csv_quote,csv_eol',
    [
        (
            {
                'version': 'v1.1.0-3-g439e52',
                'abbrev_commit': '40aaf83',
                'full_commit': '40aaf83894b98898895d478f8b7cc4a866b1d62c',
                'author_name': u'Sébastien Dupond',
                'commit_date': '2016-03-01T09:33:33+0000',
                'commit_timestamp': '1456824813',
                'deploy_date': '2016-03-02T11:33:45+0000',
                'deploy_timestamp': '1456918425',
                'branches': ['master', 'feature/my_feature']
            },
            'sh',
            'version',
            '',
            'version.sh',
            {
                'version': 'v1.1.0-3-g439e52',
                'abbrev_commit': '40aaf83',
                'full_commit': '40aaf83894b98898895d478f8b7cc4a866b1d62c',
                'author_name': u'Sébastien Dupond',
                'commit_date': '2016-03-01T09:33:33+0000',
                'commit_timestamp': '1456824813',
                'deploy_date': '2016-03-02T11:33:45+0000',
                'deploy_timestamp': '1456918425',
                'branches': "['master', 'feature/my_feature']"
            },
            None,
            None,
            None,
        ),
        (
            {
                'version': 'v1.1.0-3-g439e52',
                'abbrev_commit': '40aaf83',
                'full_commit': '40aaf83894b98898895d478f8b7cc4a866b1d62c',
                'author_name': u'Se\u0301bastien Dupond',
                'commit_date': '2016-03-01T09:33:33+0000',
                'commit_timestamp': '1456824813',
                'deploy_date': '2016-03-02T11:33:45+0000',
                'deploy_timestamp': '1456918425',
                'branches': ['master', 'feature/my_feature']
            },
            'csv',
            'version',
            '',
            'version.csv',
            {
                'version': 'v1.1.0-3-g439e52',
                'abbrev_commit': '40aaf83',
                'full_commit': '40aaf83894b98898895d478f8b7cc4a866b1d62c',
                'author_name': u'Se\u0301bastien Dupond',
                'commit_date': '2016-03-01T09:33:33+0000',
                'commit_timestamp': '1456824813',
                'deploy_date': '2016-03-02T11:33:45+0000',
                'deploy_timestamp': '1456918425',
                'branches': "['master', 'feature/my_feature']"
            },
            ',',
            '"',
            'lf',
        ),
        (
            {
                'version': 'v1.1.0-3-g439e52',
                'abbrev_commit': '40aaf83',
                'full_commit': '40aaf83894b98898895d478f8b7cc4a866b1d62c',
                'author_name': u'Se\u0301bastien Dupond',
                'commit_date': '2016-03-01T09:33:33+0000',
                'commit_timestamp': '1456824813',
                'deploy_date': '2016-03-02T11:33:45+0000',
                'deploy_timestamp': '1456918425',
                'branches': ['master', 'feature/my_feature']
            },
            'csv',
            'version',
            '',
            'version.csv',
            {
                'version': 'v1.1.0-3-g439e52',
                'abbrev_commit': '40aaf83',
                'full_commit': '40aaf83894b98898895d478f8b7cc4a866b1d62c',
                'author_name': u'Se\u0301bastien Dupond',
                'commit_date': '2016-03-01T09:33:33+0000',
                'commit_timestamp': '1456824813',
                'deploy_date': '2016-03-02T11:33:45+0000',
                'deploy_timestamp': '1456918425',
                'branches': "['master', 'feature/my_feature']"
            },
            ';',
            '\'',
            'crlf',
        ),
        (
            {
                'version': 'v1.1.0-3-g439e52',
                'abbrev_commit': '40aaf83',
                'full_commit': '40aaf83894b98898895d478f8b7cc4a866b1d62c',
                'author_name': u'Sébastien Dupond',
                'commit_date': '2016-03-01T09:33:33+0000',
                'commit_timestamp': '1456824813',
                'deploy_date': '2016-03-02T11:33:45+0000',
                'deploy_timestamp': '1456918425',
                'branches': ['master', 'feature/my_feature']
            },
            'ini',
            'version',
            '',
            'version.ini',
            {
                'version': 'v1.1.0-3-g439e52',
                'abbrev_commit': '40aaf83',
                'full_commit': '40aaf83894b98898895d478f8b7cc4a866b1d62c',
                'author_name': u'Sébastien Dupond',
                'commit_date': '2016-03-01T09:33:33+0000',
                'commit_timestamp': '1456824813',
                'deploy_date': '2016-03-02T11:33:45+0000',
                'deploy_timestamp': '1456918425',
                'branches': "['master', 'feature/my_feature']"
            },
            None,
            None,
            None,
        ),
        (
            {
                'version': 'v1.1.0-3-g439e52',
                'abbrev_commit': '40aaf83',
                'full_commit': '40aaf83894b98898895d478f8b7cc4a866b1d62c',
                'author_name': u'Sébastien Dupond',
                'commit_date': '2016-03-01T09:33:33+0000',
                'commit_timestamp': '1456824813',
                'deploy_date': '2016-03-02T11:33:45+0000',
                'deploy_timestamp': '1456918425',
            },
            'ini',
            'version',
            'parameters.git',
            'version.ini',
            {
                'version': 'v1.1.0-3-g439e52',
                'abbrev_commit': '40aaf83',
                'full_commit': '40aaf83894b98898895d478f8b7cc4a866b1d62c',
                'author_name': u'Sébastien Dupond',
                'commit_date': '2016-03-01T09:33:33+0000',
                'commit_timestamp': '1456824813',
                'deploy_date': '2016-03-02T11:33:45+0000',
                'deploy_timestamp': '1456918425',
            },
            None,
            None,
            None,
        ),
        (
            {
                'version': 'v1.1.0-3-g439e52',
                'abbrev_commit': '40aaf83',
                'full_commit': '40aaf83894b98898895d478f8b7cc4a866b1d62c',
                'author_name': u'Sébastien Dupond',
                'commit_date': '2016-03-01T09:33:33+0000',
                'commit_timestamp': '1456824813',
                'deploy_date': '2016-03-02T11:33:45+0000',
                'deploy_timestamp': '1456918425',
            },
            'json',
            'version',
            '',
            'version.json',
            {
                'version': 'v1.1.0-3-g439e52',
                'abbrev_commit': '40aaf83',
                'full_commit': '40aaf83894b98898895d478f8b7cc4a866b1d62c',
                'author_name': u'Sébastien Dupond',
                'commit_date': '2016-03-01T09:33:33+0000',
                'commit_timestamp': '1456824813',
                'deploy_date': '2016-03-02T11:33:45+0000',
                'deploy_timestamp': '1456918425',
            },
            None,
            None,
            None,
        ),
        (
            {
                'version': 'v1.1.0-3-g439e52',
                'abbrev_commit': '40aaf83',
                'full_commit': '40aaf83894b98898895d478f8b7cc4a866b1d62c',
                'author_name': u'Sébastien Dupond',
                'commit_date': '2016-03-01T09:33:33+0000',
                'commit_timestamp': '1456824813',
                'deploy_date': '2016-03-02T11:33:45+0000',
                'deploy_timestamp': '1456918425',
            },
            'json',
            'version',
            'parameters.git',
            'version.json',
            {
                'parameters': {
                    'git': {
                        'version': 'v1.1.0-3-g439e52',
                        'abbrev_commit': '40aaf83',
                        'full_commit':
                            '40aaf83894b98898895d478f8b7cc4a866b1d62c',
                        'author_name': u'Sébastien Dupond',
                        'commit_date': '2016-03-01T09:33:33+0000',
                        'commit_timestamp': '1456824813',
                        'deploy_date': '2016-03-02T11:33:45+0000',
                        'deploy_timestamp': '1456918425',
                    }
                }
            },
            None,
            None,
            None,
        ),
        (
            {
                'version': 'v1.1.0-3-g439e52',
                'abbrev_commit': '40aaf83',
                'full_commit': '40aaf83894b98898895d478f8b7cc4a866b1d62c',
                'commit_date': '2016-03-01T09:33:33+0000',
                'commit_timestamp': '1456824813',
                'deploy_date': '2016-03-02T11:33:45+0000',
                'deploy_timestamp': '1456918425',
            },
            'yml',
            'version',
            '',
            'version.yml',
            {
                'version': 'v1.1.0-3-g439e52',
                'abbrev_commit': '40aaf83',
                'full_commit': '40aaf83894b98898895d478f8b7cc4a866b1d62c',
                'commit_date': '2016-03-01T09:33:33+0000',
                'commit_timestamp': '1456824813',
                'deploy_date': '2016-03-02T11:33:45+0000',
                'deploy_timestamp': '1456918425',
            },
            None,
            None,
            None,
        ),
        (
            {
                'version': 'v1.1.0-3-g439e52',
                'abbrev_commit': '40aaf83',
                'full_commit': '40aaf83894b98898895d478f8b7cc4a866b1d62c',
                'author_name': u'Se\u0301bastien Dupond',
                'commit_date': '2016-03-01T09:33:33+0000',
                'commit_timestamp': '1456824813',
                'deploy_date': '2016-03-02T11:33:45+0000',
                'deploy_timestamp': '1456918425',
            },
            'yml',
            'version',
            'parameters.git',
            'version.yml',
            {
                'parameters': {
                    'git': {
                        'version': 'v1.1.0-3-g439e52',
                        'abbrev_commit': '40aaf83',
                        'full_commit':
                            '40aaf83894b98898895d478f8b7cc4a866b1d62c',
                        'author_name': u'Se\u0301bastien Dupond',
                        'commit_date': '2016-03-01T09:33:33+0000',
                        'commit_timestamp': '1456824813',
                        'deploy_date': '2016-03-02T11:33:45+0000',
                        'deploy_timestamp': '1456918425',
                    }
                }
            },
            None,
            None,
            None,
        ),
        (
            {},
            'yml',
            'version',
            '',
            'version.yml',
            None,
            None,
            None,
            None,
        ),
        (
            {
                'version': 'v1.1.0-3-g439e52',
                'abbrev_commit': '40aaf83',
                'full_commit': '40aaf83894b98898895d478f8b7cc4a866b1d62c',
                'commit_date': '2016-03-01T09:33:33+0000',
                'commit_timestamp': '1456824813',
                'deploy_date': '2016-03-02T11:33:45+0000',
                'deploy_timestamp': '1456918425',
            },
            'xml',
            'version',
            '',
            'version.xml',
            {
                'app_version': {
                    'version': 'v1.1.0-3-g439e52',
                    'abbrev_commit': '40aaf83',
                    'full_commit': '40aaf83894b98898895d478f8b7cc4a866b1d62c',
                    'commit_date': '2016-03-01T09:33:33+0000',
                    'commit_timestamp': '1456824813',
                    'deploy_date': '2016-03-02T11:33:45+0000',
                    'deploy_timestamp': '1456918425',
                }
            },
            None,
            None,
            None,
        ),
        (
            {
                'version': 'v1.1.0-3-g439e52',
                'abbrev_commit': '40aaf83',
                'full_commit': '40aaf83894b98898895d478f8b7cc4a866b1d62c',
                'author_name': u'Se\u0301bastien Dupond',
                'commit_date': '2016-03-01T09:33:33+0000',
                'commit_timestamp': '1456824813',
                'deploy_date': '2016-03-02T11:33:45+0000',
                'deploy_timestamp': '1456918425',
            },
            'xml',
            'version',
            'parameters.git',
            'version.xml',
            {
                'parameters': {
                    'git': {
                        'version': 'v1.1.0-3-g439e52',
                        'abbrev_commit': '40aaf83',
                        'full_commit':
                            '40aaf83894b98898895d478f8b7cc4a866b1d62c',
                        'author_name': u'Se\u0301bastien Dupond',
                        'commit_date': '2016-03-01T09:33:33+0000',
                        'commit_timestamp': '1456824813',
                        'deploy_date': '2016-03-02T11:33:45+0000',
                        'deploy_timestamp': '1456918425',
                    }
                }
            },
            None,
            None,
            None,
        )
    ]
)
def test_dump(output_dir, data, data_format, target,
              section, expected_target, expected_data,
              csv_delimiter, csv_quote, csv_eol):
    appdumper = AppDumper()

    resultTarget = appdumper.dump(
        data=data,
        fileformat=data_format,
        target=target,
        cwd=output_dir,
        namespace=section,
        csv_delimiter=csv_delimiter,
        csv_quote=csv_quote,
        csv_eol=csv_eol)

    assert output_dir + '/' + expected_target == resultTarget
    assert expected_data == get_file_content(
        output_dir + '/' + expected_target, section, data_format,
        csv_delimiter=csv_delimiter, csv_quote=csv_quote, csv_eol=csv_eol)
