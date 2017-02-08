# -*- coding: utf-8 -*-
'''
Data dumper to files with several format
'''
from __future__ import unicode_literals

import json
from builtins import open

import xmltodict
import yaml
from backports import configparser, csv

import git_app_version.helper.tools as tools


class FileDumper(object):
    '''
    Main dumper
    '''

    def dump(self,
             data=None,
             fileformat='json',
             target=None,
             cwd=None,
             namespace='',
             csv_delimiter=',',
             csv_quote='"',
             csv_eol='lf'):
        '''
        Agnostic main dump function
        '''

        target = tools.create_parent_dirs(target, cwd)
        if fileformat == 'yaml' or fileformat == 'yml':
            return self.__dump_yaml(data, target, namespace)
        elif fileformat == 'xml':
            return self.__dump_xml(data, target, namespace)
        elif fileformat == 'ini':
            return self.__dump_ini(data, target, namespace)
        elif fileformat == 'sh':
            return self.__dump_sh(data, target)
        elif fileformat == 'csv':
            return self.__dump_csv(data, target, delimiter=csv_delimiter,
                                   quotechar=csv_quote, eol=csv_eol)
        else:
            return self.__dump_json(data, target, namespace)

    def __create_infos_to_dump(self, infos, namespace=None):
        '''
        reorganize data with a namespace if necessary
        '''

        to_dump = infos
        if namespace is not None and namespace != '':
            namespaces = namespace.split('.')
            namespaces.reverse()
            for name in namespaces:
                to_dump = {name: to_dump}

        return to_dump

    def __dump_sh(self, data, target):
        '''
        dump to Shell variables file
        '''

        target = target + '.sh'

        with open(target, 'w', encoding='utf-8') as fpt:
            for key, val in data.items():
                fpt.write("{}=\"{}\"\n".format(key, tools.flatten(val)))

        return target

    def __dump_csv(self, data, target, delimiter=',', quotechar='"', eol='lf'):
        '''
        dump to CSV file (comma separated values)
        '''

        target = target + '.csv'

        eol = '\r\n' if eol == 'crlf' or eol == '\r\n' else '\n'

        with open(target, 'w', encoding='utf-8') as fpt:
            writer = csv.writer(fpt,
                                delimiter=delimiter,
                                lineterminator=eol,
                                quotechar=quotechar,
                                quoting=csv.QUOTE_MINIMAL)
            for key, val in data.items():
                writer.writerow((key, tools.flatten(val)))

        return target

    def __dump_ini(self, data, target, namespace=None):
        '''
        dump to INI file
        '''

        target = target + '.ini'

        if namespace is None or namespace == '':
            namespace = 'app_version'

        ini = configparser.RawConfigParser()
        ini.add_section(namespace)

        for key, val in data.items():
            ini.set(namespace, key, tools.flatten(val))

        with open(target, 'w', encoding='utf-8') as fpt:
            ini.write(fpt)

        return target

    def __dump_xml(self, data, target, namespace=None):
        '''
        dump to XML file
        '''

        target = target + '.xml'
        if namespace is None or namespace == '':
            namespace = 'app_version'

        with open(target, 'w', encoding='utf-8') as fpt:
            xml = xmltodict.unparse(
                self.__create_infos_to_dump(data, namespace),
                encoding='utf-8',
                pretty=True,
                indent='  ')

            fpt.write(xml)

            return target

    def __dump_json(self, data, target, namespace=None):
        '''
        dump to JSON file
        '''

        target = target + '.json'

        data1 = self.__create_infos_to_dump(data, namespace)

        with open(target, 'w', encoding='utf-8') as fpt:
            fpt.write(json.dumps(data1, indent=2, ensure_ascii=False))

        return target

    def __dump_yaml(self, data, target, namespace=None):
        '''
        dump to YAML file
        '''

        target = target + '.yml'

        with open(target, 'w', encoding='utf-8') as fpt:
            if not data:
                fpt.write("---\n")
            else:
                yaml.safe_dump(
                    self.__create_infos_to_dump(data, namespace),
                    fpt,
                    default_flow_style=False,
                    explicit_start=True,
                    allow_unicode=True,
                    # force quoting
                    # to prevent abbrev_commit to be read as a float
                    default_style='\''
                )

        return target
