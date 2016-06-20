# -*- coding: utf-8 -*-

import os
import argparse
from git_app_version.git import Git
from git_app_version.dumper import Dumper

__version__ = '0.5.0'
__DESCRIPTION__ = 'Get Git commit informations and store them in a INI/XML/YAML/JSON file.'

def main():
    parser = argparse.ArgumentParser(prog='git-app-version', description=__DESCRIPTION__)
    parser.add_argument('-V', '--version', action='version', version='%(prog)s '+__version__, help='display tool version')
    parser.add_argument('-v', '--verbose', action='count', help='increase verbosity : use -v or -vv')
    parser.add_argument('-q', '--quiet', action='store_true', help='silent mode')
    parser.add_argument('repository', nargs='?', metavar='path', type=str, help='git repository path. Default is the current directory.', default=os.getcwd())
    parser.add_argument('commit', nargs='?', type=str, help='git commit to check. Default is HEAD.', default='HEAD')
    parser.add_argument('-o', '--output', metavar='path', type=str, help='output file path (without extension). Default is \'<repository-path>/version\'.', default='version')
    parser.add_argument('-f', '--format', metavar='format', type=str, help='output file format and extension (ini/xml/yml/json). Default is json.', default='json')
    parser.add_argument('-n', '--namespace', metavar='namespace', type=str, help='namespace like notation in version file, use dot separator to segment namespaces e.g.: \'foo.bar.git\'. Default is \'app_version\' for XML and INI and no namespace for JSON and YAML.', default='')

    args = parser.parse_args()

    try:
        vcs = Git()

        if not vcs.isGitRepository(args.repository):
            raise Exception('The directory \''+args.repository+'\' is not a git repository.')

        data = vcs.getInfos(commit = args.commit, cwd = args.repository)

        if args.verbose > 1 and not args.quiet :
            print('Git commit :')
            keys = data.keys()
            keys.sort()
            for key in keys:
                try:
                    print (key+' = '+data[key])
                except TypeError:
                    print (key+' = '+' '.join(data[key]))

        dumper = Dumper()
        dest = dumper.dump(data = data, format = args.format, target = args.output, cwd = args.repository, namespace=args.namespace)
        if not args.quiet :
            print("Git commit informations stored in "+dest)

    except Exception as exc:
        print("Error Writing version config file : ", exc)
        exit(1)

if __name__ == '__main__':
    main()
