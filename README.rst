===============
Git App Version
===============

.. image:: https://travis-ci.org/csanquer/git-app-version.svg?branch=master
    :target: https://travis-ci.org/csanquer/git-app-version

A CLI tool written in Python to fetch Git commit informations and store them in an INI/XML/YAML/JSON file.

Typical usecase : when deploying, run this command and import the git version config file.


Requirements
------------

* Python 2.7 or >= 3.3
* python pip package tool

Installation
------------

Just run ::

    pip install git-app-version


Usage
-----

Help
^^^^

To get help ::

    git-app-version -h

Get Commit Informations
^^^^^^^^^^^^^^^^^^^^^^^

To store git commit informations into a json file ::

    cd <my-git-repository>
    # git-app-version -o <output-file-without-extension> -f <file-format>

    git-app-version -o version -f json

This will generate a version.json file in the current directory.

File formats
^^^^^^^^^^^^

* json ::

    {
        "commit_date": "2016-03-01T09:33:33+0000",
        "full_commit": "40aaf83894b98898895d478f8b7cc4a866b1d62c",
        "version": "v1.1.0-3-g439e52",
        "commit_timestamp": "1456824813",
        "deploy_date": "2016-03-02T11:33:45+0000",
        "deploy_timestamp": "1456918425",
        "abbrev_commit": "40aaf83"
    }

* ini ::

    [app_version]
    commit_date = 2016-03-01T09:33:33+0000
    full_commit = 40aaf83894b98898895d478f8b7cc4a866b1d62c
    version = v1.1.0-3-g439e52
    commit_timestamp = 1456824813
    deploy_date = 2016-03-02T11:33:45+0000
    deploy_timestamp = 1456918425
    abbrev_commit = 40aaf83

* xml ::

    <?xml version='1.0' encoding='UTF-8'?>
    <app_version>
      <full_commit>40aaf83894b98898895d478f8b7cc4a866b1d62c</full_commit>
      <commit_timestamp>1456824813</commit_timestamp>
      <abbrev_commit>40aaf83</abbrev_commit>
      <version>v1.1.0-3-g439e52</version>
      <deploy_timestamp>1456918425</deploy_timestamp>
      <commit_date>2016-03-01T09:33:33+0000</commit_date>
      <deploy_date>2016-03-02T11:33:45+0000</deploy_date>
    </app_version>

* yml ::

    ---
    'abbrev_commit': '40aaf83'
    'commit_date': '2016-03-01T09:33:33+0000'
    'commit_timestamp': '1456824813'
    'deploy_date': '2016-03-02T11:33:45+0000'
    'deploy_timestamp': '1456918425'
    'full_commit': '40aaf83894b98898895d478f8b7cc4a866b1d62c'
    'version': 'v1.1.0-3-g439e52'


Licensing
---------

Project under MIT License

Copyright (C) 2016 Charles Sanquer
