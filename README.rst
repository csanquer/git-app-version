===============
Git App Version
===============

.. image:: https://badge.fury.io/py/git-app-version.svg
    :target: https://badge.fury.io/py/git-app-version
.. image:: https://travis-ci.org/csanquer/git-app-version.svg?branch=master
    :target: https://travis-ci.org/csanquer/git-app-version
.. image:: https://scrutinizer-ci.com/g/csanquer/git-app-version/badges/quality-score.png?b=master
    :target: https://scrutinizer-ci.com/g/csanquer/git-app-version/?branch=master
.. image:: https://scrutinizer-ci.com/g/csanquer/git-app-version/badges/coverage.png?b=master
    :target: https://scrutinizer-ci.com/g/csanquer/git-app-version/?branch=master

A CLI tool written in Python to fetch Git commit informations and store them in a config file.

supported formats :

* JSON
* YAML
* XML
* INI
* CSV
* Shell script variables

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

To get help

.. code:: shell

    git-app-version -h

Help result

.. code:: shell

    Usage: git-app-version [OPTIONS] [REPOSITORY] [COMMIT]

      Get Git commit informations and store them in a config file

      REPOSITORY git repository path, Default is the current directory.
      COMMIT     git commit to check, Default is HEAD.

    Options:
      -V, --version
      -q, --quiet                     silent mode
      -o, --output TEXT               output file path (without extension).
                                      Default is '<repository-path>/version'.
      -f, --format [json|yml|xml|ini|csv|sh]
                                      output file format and extension, Default is
                                      json.
      -n, --namespace TEXT            namespace like notation in version file, use
                                      dot separator to segment namespaces e.g.:
                                      'foo.bar.git'. Default is 'app_version' for
                                      XML and INI and no namespace for JSON and
                                      YAML. Never used for Shell file.
      -m, --meta METADATA             meta data to add, format = "<key>=<value>"
      -d, --csv-delimiter TEXT        CSV delimiter, default=","
      -e, --csv-eol [lf|crlf]         CSV end of line, lf = Unix new line, crlf =
                                      windows new line, default=lf
      -u, --csv-quote TEXT            CSV quoting character, default='"'
      -h, --help                      Show this message and exit.



Get Commit Informations
^^^^^^^^^^^^^^^^^^^^^^^

To store git commit informations into a json file

.. code:: shell

    # git-app-version -o <output-file-without-extension> -f <file-format> <my-git-repository>

    git-app-version -o version -f json


output :

.. code:: shell

    Git commit :
    ----------------  ----------------------------------------
    abbrev_commit     40aaf83
    author_date       2015-09-05T16:14:16+0000
    author_email      paul.durand@example.com
    author_name       Paul Durand
    author_timestamp  1441469656
    branches          master develop
    commit_date       2015-09-05T16:14:16+0000
    commit_timestamp  1441469656
    committer_email   paul.durand@example.com
    committer_name    Paul Durand
    deploy_date       2016-06-21T09:33:01+0000
    deploy_timestamp  1466501581
    full_commit       40aaf83894b98898895d478f8b7cc4a866b1d62c
    message           new feature
    top_branches      master
    version           v1.1.0-3-g439e52
    ----------------  ----------------------------------------
    written to :
    <my-git-repository>/version.json

This will generate a version.json file in the current directory (if this directory is a git repository).

You can generate several format at once :

.. code:: shell

    git-app-version -o version -f json -f yml -f xml -f ini -f sh


Metadata : adding custom fields
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can add custom metadata fields with the `--meta` / `-m` option (can be used several times) :

.. code:: shell

    git-app-version -m foo=bar -m custom_key=custom_value

output :

.. code:: shell

    Git commit :
    ----------------  ----------------------------------------
    abbrev_commit     40aaf83
    author_date       2015-09-05T16:14:16+0000
    author_email      paul.durand@example.com
    author_name       Paul Durand
    author_timestamp  1441469656
    branches          master develop
    commit_date       2015-09-05T16:14:16+0000
    commit_timestamp  1441469656
    committer_email   paul.durand@example.com
    committer_name    Paul Durand
    custom_key        custom_value
    deploy_date       2016-06-21T09:33:01+0000
    deploy_timestamp  1466501581
    foo               bar
    full_commit       40aaf83894b98898895d478f8b7cc4a866b1d62c
    message           new feature
    top_branches      master
    version           v1.1.0-3-g439e52
    ----------------  ----------------------------------------
    written to :
    <my-git-repository>/version.json


Commit informations fields
^^^^^^^^^^^^^^^^^^^^^^^^^^

* **full_commit** : Git SHA1 commit hash,

  *e.g.: 40aaf83894b98898895d478f8b7cc4a866b1d62c*

* **abbrev_commit** : Git SHA1 commit hash abbrev notation (x significant first characters),

  *e.g.: 40aaf83*

* **version** : result of the command ``git describe --tags --always``, see `git-describe <https://git-scm.com/docs/git-describe>`_,
  if no version is found, the abbrev commit will be used per default

  *e.g.: v1.1.0-3-g439e52*

* **message** : Git commit message

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

  without namespace

  .. code:: shell

      git-app-version -f json

  result

  .. code:: json

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
        "deploy_timestamp": "1466501581",
        "message": "new feature"

      }

  with namespace

  .. code:: shell

      git-app-version -f json -n git.infos

  result

  .. code:: json

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
            "deploy_timestamp": "1466501581",
            "message": "new feature"
          }
        }
      }

* yml

  without namespace

  .. code:: shell

      git-app-version -f yml

  result

  .. code:: yaml

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
      'message': 'new feature'
      'branches':
      - 'develop'
      - 'master'
      'top_branches':
      - 'master'

  with namespace

  .. code:: shell

      git-app-version -f yml -n git.infos

  result

  .. code:: yaml

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
          'message': 'new feature'
          'branches':
          - 'develop'
          - 'master'
          'top_branches':
          - 'master'
* xml

  with default namespace

  .. code:: shell

      git-app-version -f xml

  result

  .. code:: xml

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
        <message>new feature</message>
        <branches>develop</branches>
        <branches>master</branches>
        <top_branches>master</top_branches>
      </app_version>

  with namespace

  .. code:: shell

      git-app-version -f xml -n git.infos

  result

  .. code:: xml

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
          <message>new feature</message>
          <branches>develop</branches>
          <branches>master</branches>
          <top_branches>master</top_branches>
        </infos>
      </git>

* ini

  with default namespace

  .. code:: shell

      git-app-version -f ini

  result

  .. code:: ini

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
      message = new feature
      author_name = Paul Durand
      author_email = paul.durand@example.com
      committer_name = Paul Durand
      committer_email = paul.durand@example.com
      top_branches = ['master']
      branches = ['master','develop']


  with namespace

  .. code:: shell

      git-app-version -f ini -n git.infos

  result

  .. code:: ini

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
      message = new feature
      author_name = Paul Durand
      author_email = paul.durand@example.com
      committer_name = Paul Durand
      committer_email = paul.durand@example.com
      top_branches = ['master']
      branches = ['master','develop']

* csv

  you can configure CSV format with the option `--csv-delimiter` , `--csv-eol` and `--csv-quote`

  .. code:: shell

      git-app-version -f csv --csv-delimiter ',' --csv-eol lf --csv-quote '"'


  result

  .. code:: csv

      version,v1.1.0-3-g439e52
      full_commit,40aaf83894b98898895d478f8b7cc4a866b1d62c
      abbrev_commit,40aaf83
      commit_date,2016-03-01T09:33:33+0000
      commit_timestamp,1456824813
      author_date,2016-03-01T09:33:33+0000
      author_timestamp,1456824813
      deploy_date,2016-03-02T11:33:45+0000
      deploy_timestamp,1456918425
      message,new feature
      author_name,Paul Durand
      author_email,paul.durand@example.com
      committer_name,Paul Durand
      committer_email,paul.durand@example.com
      top_branches,"['master']"
      branches,"['master','develop']"


* sh (shell script variables)

  .. code:: shell

      git-app-version -f sh

  result

  .. code:: shell

      version="v1.1.0-3-g439e52"
      full_commit="40aaf83894b98898895d478f8b7cc4a866b1d62c"
      abbrev_commit="40aaf83"
      commit_date="2016-03-01T09:33:33+0000"
      commit_timestamp="1456824813"
      author_date="2016-03-01T09:33:33+0000"
      author_timestamp="1456824813"
      deploy_date="2016-03-02T11:33:45+0000"
      deploy_timestamp="1456918425"
      message="new feature"
      author_name="Paul Durand"
      author_email="paul.durand@example.com"
      committer_name="Paul Durand"
      committer_email="paul.durand@example.com"
      top_branches="['master']"
      branches="['master','develop']"


Licensing
---------

Project under GPL v3 License

Copyright (C) 2016 Charles Sanquer
