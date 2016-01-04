# -*- coding: utf-8 -*-

from mock import patch
import pytest
import os
import shutil

from git_app_version.dumper import Dumper as AppDumper
import json
from lxml import etree

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader,Dumper

from pprint import pprint,pformat

@pytest.fixture
def outputDir():
    cwd = os.path.realpath(os.path.dirname(__file__))
    path = cwd+'/output'
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path, 493)

    return path

def getFileContent(path, section=None, fileFormat=None):
    if fileFormat == 'yml' or fileFormat == 'yaml':
        with open(path, 'r') as f:
            return yaml.load(f)
    elif fileFormat == 'xml':
        with open(path, 'r') as f:
            tree = etree.parse(f)

            root = tree.getroot()

            data = {}
            if root.tag == section :
                for child in root:
                    data[child.tag] = child.text

            return data

        return ''
    elif fileFormat == 'ini':
        config = configparser.RawConfigParser()
        config.read(path)

        data = {}
        if config.has_section(section):
            for k,v in config.items(section):
                data[k] = v

        return data
    elif fileFormat == 'json':
        with open(path, 'r') as f:
            return json.load(f)
    else:
        with open(path, 'r') as f:
            return f.read()

@pytest.mark.parametrize("data,dataFormat,target,section,expectedTarget,expectedFile", [
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
        'ini',
        'version',
        'app_version',
        'version.ini',
        'data/version.ini'
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
        'app_version',
        'version.json',
        'data/version.json'
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
        'app_version',
        'version.yml',
        'data/version.yml'
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
        'app_version',
        'version.xml',
        'data/version.xml'
    ),
])
def test_dump(outputDir, data, dataFormat, target, section, expectedTarget, expectedFile):
    appdumper = AppDumper()

    cwd = os.path.realpath(os.path.dirname(__file__))

    resultTarget = appdumper.dump(data, dataFormat, target, outputDir, section)

    assert outputDir+'/'+expectedTarget == resultTarget
    assert data == getFileContent(cwd+'/'+expectedFile, section, dataFormat)
