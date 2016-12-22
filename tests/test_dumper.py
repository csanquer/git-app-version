# -*- coding: utf-8 -*-

from mock import patch
import pytest
import os
import shutil
from pprint import pprint

from git_app_version.helper.pyversion import PY3
from git_app_version.dumper import FileDumper as AppDumper
import json
import xmltodict

# import configparser

# from backports import configparser
#
try:
    import ConfigParser as configparser
except ImportError:
    import configparser

import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader,Dumper

@pytest.fixture
def output_dir():
    cwd = os.path.realpath(os.path.dirname(__file__))
    path = cwd+'/output'
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path, 493)

    return path

def get_file_content(path, section=None, fileFormat=None):
    if fileFormat == 'yml' or fileFormat == 'yaml':
        with open(path, 'r') as f:
            return yaml.load(f)
    elif fileFormat == 'xml':
        with open(path, 'r') as f:
            return xmltodict.parse(f.read(), dict_constructor=dict)
    elif fileFormat == 'ini':
        config = configparser.RawConfigParser()
        config.read(path)

        data = {}
        if config.has_section(section):
            for k,v in config.items(section):
                if PY3:
                    data[k] = v
                else:
                    data[k] = v.decode('utf-8')

        return data
    elif fileFormat == 'json':
        with open(path, 'r') as f:
            return json.load(f)
    else:
        with open(path, 'r') as f:
            return f.read()

@pytest.mark.parametrize("data,data_format,target,section,expected_target,expected_data", [
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
        'ini',
        'version',
        'app_version',
        'version.ini',
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
        'ini',
        'version',
        'parameters.git',
        'version.ini',
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
        'json',
        'version',
        '',
        'version.json',
        {
            'version': 'v1.1.0-3-g439e52',
            'abbrev_commit': '40aaf83',
            'full_commit': '40aaf83894b98898895d478f8b7cc4a866b1d62c',
            'commit_date': '2016-03-01T09:33:33+0000',
            'commit_timestamp': '1456824813',
            'deploy_date': '2016-03-02T11:33:45+0000',
            'deploy_timestamp': '1456918425',
        },
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
        'json',
        'version',
        'parameters.git',
        'version.json',
        {
            'parameters': {
                'git': {
                    'version': 'v1.1.0-3-g439e52',
                    'abbrev_commit': '40aaf83',
                    'full_commit': '40aaf83894b98898895d478f8b7cc4a866b1d62c',
                    'author_name': u'Se\u0301bastien Dupond',
                    'commit_date': '2016-03-01T09:33:33+0000',
                    'commit_timestamp': '1456824813',
                    'deploy_date': '2016-03-02T11:33:45+0000',
                    'deploy_timestamp': '1456918425',
                }
            }
        }
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
                    'full_commit': '40aaf83894b98898895d478f8b7cc4a866b1d62c',
                    'author_name': u'Se\u0301bastien Dupond',
                    'commit_date': '2016-03-01T09:33:33+0000',
                    'commit_timestamp': '1456824813',
                    'deploy_date': '2016-03-02T11:33:45+0000',
                    'deploy_timestamp': '1456918425',
                }
            }
        },
    ),
    (
        {},
        'yml',
        'version',
        '',
        'version.yml',
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
                    'full_commit': '40aaf83894b98898895d478f8b7cc4a866b1d62c',
                    'author_name': u'Se\u0301bastien Dupond',
                    'commit_date': '2016-03-01T09:33:33+0000',
                    'commit_timestamp': '1456824813',
                    'deploy_date': '2016-03-02T11:33:45+0000',
                    'deploy_timestamp': '1456918425',
                }
            }
        },
    )
])
def test_dump(output_dir, data, data_format, target, section, expected_target, expected_data):
    appdumper = AppDumper()

    cwd = os.path.realpath(os.path.dirname(__file__))
    resultTarget = appdumper.dump(data, data_format, target, output_dir, section)

    assert output_dir+'/'+expected_target == resultTarget
    assert expected_data == get_file_content(output_dir+'/'+expected_target, section, data_format)
