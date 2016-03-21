# -*- coding: utf-8 -*-

import os
import argparse
from git_app_version.git import Git
from git_app_version.dumper import Dumper

__version__ = '0.3.1'
__DESCRIPTION__ = 'Get Git commit informations and store them in a INI/XML/YAML/JSON file.'

def main():
    parser = argparse.ArgumentParser(prog='git-app-version', description=__DESCRIPTION__)
    parser.add_argument('-v', '--version', action='version', version='%(prog)s '+__version__)
    parser.add_argument('repository', nargs='?', metavar='path', type=str, help='git repository path', default=os.getcwd())
    parser.add_argument('commit', nargs='?', type=str, help='git commit to check', default='HEAD')
    parser.add_argument('-o', '--output', metavar='path', type=str, help='output file path (without extension)', default='version')
    parser.add_argument('--format', metavar='format', type=str, help='output file format and extension (ini/xml/yml/json)', default='json')
    parser.add_argument('--section', metavar='root', type=str, help='section name in INI file or root tag in XML file', default='app_version')

    args = parser.parse_args()

    try:
        vcs = Git()

        if not vcs.isGitRepository(args.repository):
            raise Exception('The directory \''+args.repository+'\' is not a git repository.')

        data = vcs.getInfos(commit = args.commit, cwd = args.repository)

        print('Git commit :')
        for key,val in data.items():
            print (key+' = '+val)

        dumper = Dumper()
        dest = dumper.dump(data = data, format = args.format, target = args.output, cwd = args.repository, section=args.section)
        print("Git commit informations stored in "+dest)

    except Exception as exc:
        print("Error Writing version config file : ", exc)
        exit(1)

if __name__ == '__main__':
    main()
