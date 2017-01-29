# -*- coding: utf-8 -*-
'''
    Main module
'''
import argparse
import os
import sys

import git_app_version.version
from git_app_version.dumper import FileDumper
from git_app_version.git import Git

__version__ = git_app_version.version.__version__
__DESCRIPTION__ = 'Get Git commit informations'
' and store them in a INI/XML/YAML/JSON file.'


def main(args=None):
    '''
        Main CLI function
    '''
    parser = argparse.ArgumentParser(
        prog='git-app-version',
        description=__DESCRIPTION__)
    parser.add_argument(
        '-V',
        '--version',
        action='version',
        version='%(prog)s ' +
        __version__,
        help='display tool version')
    parser.add_argument('-v', '--verbose', action='count',
                        help='increase verbosity : use -v or -vv')
    parser.add_argument(
        '-q',
        '--quiet',
        action='store_true',
        help='silent mode')
    parser.add_argument(
        'repository',
        nargs='?',
        metavar='path',
        type=str,
        help='git repository path. Default is the current directory.',
        default=os.getcwd())
    parser.add_argument(
        'commit',
        nargs='?',
        type=str,
        help='git commit to check. Default is HEAD.',
        default='HEAD')
    parser.add_argument(
        '-o',
        '--output',
        metavar='path',
        type=str,
        help='output file path (without extension).'
        ' Default is \'<repository-path>/version\'.',
        default='version')
    parser.add_argument(
        '-f',
        '--format',
        metavar='format',
        type=str,
        help='output file format and extension (ini/xml/yml/json).'
        ' Default is json.',
        default='json')
    parser.add_argument(
        '-n',
        '--namespace',
        metavar='namespace',
        type=str,
        help='namespace like notation in version file,'
        ' use dot separator to segment namespaces e.g.: \'foo.bar.git\'.'
        ' Default is \'app_version\' for XML and INI'
        ' and no namespace for JSON and YAML.',
        default='')

    options = parser.parse_args(sys.argv[1:] if args is None else args)

    try:
        vcs = Git()

        if not vcs.is_git_repo(options.repository):
            raise ValueError(
                'The directory \'' +
                options.repository +
                '\' is not a git repository.')

        data = vcs.get_infos(commit=options.commit, cwd=options.repository)

        if (not options.quiet and options.verbose is not None and
                options.verbose >= 1):

            print('Git commit :')
            keys = sorted(data.keys())
            for key in keys:
                try:
                    print(key + ' = ' + data[key])
                except TypeError:
                    print(key + ' = ' + ' '.join(data[key]))

        dumper = FileDumper()
        dest = dumper.dump(
            data=data,
            fileformat=options.format,
            target=options.output,
            cwd=options.repository,
            namespace=options.namespace)
        if not options.quiet:
            print("Git commit informations stored in " + dest)

        return 0

    except (RuntimeError, ValueError, TypeError) as exc:
        print("Error Writing version config file : " + str(exc))

        return 1


if __name__ == '__main__':
    sys.exit(main())
