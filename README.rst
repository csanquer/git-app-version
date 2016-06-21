===============
Git App Version
===============

.. image:: https://badge.fury.io/py/git-app-version.svg
   :target: https://badge.fury.io/py/git-app-version
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

Help result ::

    usage: git-app-version [-h] [-V] [-v] [-q] [-o path] [-f format]
                           [-n namespace]
                           [path] [commit]

    Get Git commit informations and store them in a INI/XML/YAML/JSON file.

    positional arguments:
      path                  git repository path. Default is the current directory.
      commit                git commit to check. Default is HEAD.

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         display tool version
      -v, --verbose         increase verbosity : use -v or -vv
      -q, --quiet           silent mode
      -o path, --output path
                            output file path (without extension). Default is
                            '<repository-path>/version'.
      -f format, --format format
                            output file format and extension (ini/xml/yml/json).
                            Default is json.
      -n namespace, --namespace namespace
                            namespace like notation in version file, use dot
                            separator to segment namespaces e.g.: 'foo.bar.git'.
                            Default is 'app_version' for XML and INI and no
                            namespace for JSON and YAML.



Get Commit Informations
^^^^^^^^^^^^^^^^^^^^^^^

To store git commit informations into a json file ::

    # git-app-version -o <output-file-without-extension> -f <file-format> <my-git-repository>

    git-app-version -o version -f json

This will generate a version.json file in the current directory (if this directory is a git repository).

Commit informations
^^^^^^^^^^^^^^^^^^^

* **full_commit** : Git SHA1 commit hash,

  *e.g.: 40aaf83894b98898895d478f8b7cc4a866b1d62c*

* **abbrev_commit** : Git SHA1 commit hash abbrev notation (x significant first characters),

  *e.g.: 40aaf83*

* **version** : result of the command ``git describe --tags --always``, see `git-describe <https://git-scm.com/docs/git-describe>`_,
  if no version is found, the abbrev commit will be used per default

  *e.g.: v1.1.0-3-g439e52*

* **commit_date** : Git commit date in `iso8601 <https://en.wikipedia.org/wiki/ISO_8601>`_ format,

  *e.g.: 2016-03-01T09:33:33+0000*

* **commit_timestamp** : Git commit date in timestamp format,

  *e.g.: 1456824813*

* **author_date** : Git author date in `iso8601 <https://en.wikipedia.org/wiki/ISO_8601>`_ format,

  *e.g.: 2016-03-02T11:33:45+0000*

* **author_timestamp** : Git author date in timestamp format,

  *e.g.: 1456918425*

* **deploy_date** : current date (when running the tool) in `iso8601 <https://en.wikipedia.org/wiki/ISO_8601>`_ format,

  *e.g.: 2016-03-02T11:33:45+0000*

* **deploy_timestamp** : current date (when running the tool) in timestamp format,

  *e.g.: 1456918425*

* **branches** : branches which the commit belongs,

  *e.g.: ['master', 'develop']*

* **top_branches** : branches where the commit is the HEAD commit,

  *e.g.: ['master']*

* **branches** : branches which the commit belongs,

  *e.g.: ['master', 'develop']*

* **committer_name** : Git committer name,

  *e.g.: Paul Durand*

* **committer_email** : Git committer email,

  *e.g.: paul.durand@example.com*

* **author_name** : Git author name,

  *e.g.: Paul Durand*

* **author_email** : Git author email,

  *e.g.: paul.durand@example.com*

File formats
^^^^^^^^^^^^

* json

  without namespace ::

        git-app-version -f json

  result ::

        {
          "version": "v1.1.0-3-g439e52",
          "full_commit": "40aaf83894b98898895d478f8b7cc4a866b1d62c",
          "abbrev_commit": "40aaf83",
          "branches": [
            "develop",
            "master"
          ],
          "top_branches": [
            "master"
          ],
          "committer_email": "paul.durand@example.com",
          "committer_name": "Paul Durand",
          "author_name": "Paul Durand",
          "author_email": "paul.durand@example.com",
          "commit_date": "2015-09-05T16:14:16+0000",
          "commit_timestamp": "1441469656",
          "author_date": "2015-09-05T16:14:16+0000",
          "author_timestamp": "1441469656",
          "deploy_date": "2016-06-21T09:33:01+0000",
          "deploy_timestamp": "1466501581"
        }

  with namespace ::

        git-app-version -f json -n git.infos

  result ::

        {
          "git": {
            "infos": {
              "version": "v1.1.0-3-g439e52",
              "full_commit": "40aaf83894b98898895d478f8b7cc4a866b1d62c",
              "abbrev_commit": "40aaf83",
              "branches": [
                "develop",
                "master"
              ],
              "top_branches": [
                "master"
              ],
              "committer_email": "paul.durand@example.com",
              "committer_name": "Paul Durand",
              "author_name": "Paul Durand",
              "author_email": "paul.durand@example.com",
              "commit_date": "2015-09-05T16:14:16+0000",
              "commit_timestamp": "1441469656",
              "author_date": "2015-09-05T16:14:16+0000",
              "author_timestamp": "1441469656",
              "deploy_date": "2016-06-21T09:33:01+0000",
              "deploy_timestamp": "1466501581"
            }
          }
        }

* yml ::

  without namespace ::

        git-app-version -f yml

  result ::

        ---
        'version': 'v1.1.0-3-g439e52'
        'full_commit': '40aaf83894b98898895d478f8b7cc4a866b1d62c'
        'abbrev_commit': '40aaf83'
        'committer_name': 'Paul Durand'
        'committer_email': 'paul.durand@example.com'
        'author_name': 'Paul Durand'
        'author_email': 'paul.durand@example.com'
        'commit_date': '2015-09-05T16:14:16+0000'
        'commit_timestamp': '1441469656'
        'author_date': '2015-09-05T16:14:16+0000'
        'author_timestamp': '1441469656'
        'deploy_date': '2016-06-21T09:32:57+0000'
        'deploy_timestamp': '1466501577'
        'branches':
        - 'develop'
        - 'master'
        'top_branches':
        - 'master'

  with namespace ::

        git-app-version -f yml -n git.infos

  result ::

        ---
        'git':
          'infos':
            'version': 'v1.1.0-3-g439e52'
            'full_commit': '40aaf83894b98898895d478f8b7cc4a866b1d62c'
            'abbrev_commit': '40aaf83'
            'committer_name': 'Paul Durand'
            'committer_email': 'paul.durand@example.com'
            'author_name': 'Paul Durand'
            'author_email': 'paul.durand@example.com'
            'commit_date': '2015-09-05T16:14:16+0000'
            'commit_timestamp': '1441469656'
            'author_date': '2015-09-05T16:14:16+0000'
            'author_timestamp': '1441469656'
            'deploy_date': '2016-06-21T09:32:57+0000'
            'deploy_timestamp': '1466501577'
            'branches':
            - 'develop'
            - 'master'
            'top_branches':
            - 'master'
* xml ::

  with default namespace ::

        git-app-version -f xml

  result ::

        <?xml version='1.0' encoding='UTF-8'?>
        <app_version>
          <version>v1.1.0-3-g439e52</version>
          <full_commit>40aaf83894b98898895d478f8b7cc4a866b1d62c</full_commit>
          <abbrev_commit>40aaf83</abbrev_commit>
          <commit_date>2015-09-05T16:14:16+0000</commit_date>
          <commit_timestamp>1441469656</commit_timestamp>
          <author_date>2015-09-05T16:14:16+0000</author_date>
          <author_timestamp>1441469656</author_timestamp>
          <deploy_date>2016-06-21T09:32:53+0000</deploy_date>
          <deploy_timestamp>1466501573</deploy_timestamp>
          <committer_name>Paul Durand</committer_name>
          <committer_email>paul.durand@example.com</committer_email>
          <author_name>Paul Durand</author_name>
          <author_email>paul.durand@example.com</author_email>
          <branches>develop</branches>
          <branches>master</branches>
          <top_branches>master</top_branches>
        </app_version>

  with namespace ::

        git-app-version -f xml -n git.infos

  result ::

        <?xml version='1.0' encoding='UTF-8'?>
        <git>
          <infos>
            <version>v1.1.0-3-g439e52</version>
            <full_commit>40aaf83894b98898895d478f8b7cc4a866b1d62c</full_commit>
            <abbrev_commit>40aaf83</abbrev_commit>
            <commit_date>2015-09-05T16:14:16+0000</commit_date>
            <commit_timestamp>1441469656</commit_timestamp>
            <author_date>2015-09-05T16:14:16+0000</author_date>
            <author_timestamp>1441469656</author_timestamp>
            <deploy_date>2016-06-21T09:32:53+0000</deploy_date>
            <deploy_timestamp>1466501573</deploy_timestamp>
            <committer_name>Paul Durand</committer_name>
            <committer_email>paul.durand@example.com</committer_email>
            <author_name>Paul Durand</author_name>
            <author_email>paul.durand@example.com</author_email>
            <branches>develop</branches>
            <branches>master</branches>
            <top_branches>master</top_branches>
          </infos>
        </git>


* ini ::

  with default namespace ::

        git-app-version -f ini

  result ::

        [app_version]
        version = v1.1.0-3-g439e52
        full_commit = 40aaf83894b98898895d478f8b7cc4a866b1d62c
        abbrev_commit = 40aaf83
        commit_date = 2016-03-01T09:33:33+0000
        commit_timestamp = 1456824813
        author_date = 2016-03-01T09:33:33+0000
        author_timestamp = 1456824813
        deploy_date = 2016-03-02T11:33:45+0000
        deploy_timestamp = 1456918425
        author_name = Paul Durand
        author_email = paul.durand@example.com
        committer_name = Paul Durand
        committer_email = paul.durand@example.com
        top_branches = ['master']
        branches = ['master','develop']


  with namespace ::

        git-app-version -f ini -n git.infos

  result ::

        [git.infos]
        version = v1.1.0-3-g439e52
        full_commit = 40aaf83894b98898895d478f8b7cc4a866b1d62c
        abbrev_commit = 40aaf83
        commit_date = 2016-03-01T09:33:33+0000
        commit_timestamp = 1456824813
        author_date = 2016-03-01T09:33:33+0000
        author_timestamp = 1456824813
        deploy_date = 2016-03-02T11:33:45+0000
        deploy_timestamp = 1456918425
        author_name = Paul Durand
        author_email = paul.durand@example.com
        committer_name = Paul Durand
        committer_email = paul.durand@example.com
        top_branches = ['master']
        branches = ['master','develop']

Licensing
---------

Project under GPL v3 License

Copyright (C) 2016 Charles Sanquer
