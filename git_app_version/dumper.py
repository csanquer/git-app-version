# -*- coding: utf-8 -*-
'''
Data dumper to files with several format
'''
import csv
import json

import xmltodict
import yaml

import git_app_version.helper.tools as tools
from git_app_version.helper.pyversion import PY3

try:
    import ConfigParser as configparser
except ImportError:
    import configparser


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

        with open(target, 'w') as fpt:
            for key, val in data.items():
                if not PY3:
                    val = tools.encode(tools.flatten(val))
                fpt.write("{}=\"{}\"\n".format(key, val))

        return target

    def __dump_csv(self, data, target, delimiter=',', quotechar='"', eol='lf'):
        '''
        dump to CSV file (comma separated values)
        '''

        target = target + '.csv'

        eol = "\r\n" if eol == 'crlf' or eol == "\r\n" else "\n"

        csv.register_dialect('custom', delimiter=str(delimiter),
                             lineterminator=str(eol), quotechar=str(quotechar),
                             quoting=csv.QUOTE_MINIMAL)

        if PY3:
            with open(target, 'w', encoding='utf-8') as fpt:
                writer = csv.writer(fpt, dialect='custom')
                for key, val in data.items():
                    writer.writerow((key, val))
        else:
            with open(target, 'wb') as fpt:
                writer = csv.writer(fpt, dialect='custom')
                for key, val in data.items():
                    val = tools.encode(tools.flatten(val))
                    writer.writerow((key, val))

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
            if not PY3:
                val = tools.encode(tools.flatten(val))

            ini.set(namespace, key, val)

        with open(target, 'w') as fpt:
            ini.write(fpt)

        return target

    def __dump_xml(self, data, target, namespace=None):
        '''
        dump to XML file
        '''

        target = target + '.xml'
        if namespace is None or namespace == '':
            namespace = 'app_version'

        with open(target, 'w') as fpt:
            xml = xmltodict.unparse(
                self.__create_infos_to_dump(
                    data,
                    namespace),
                encoding='utf-8',
                pretty=True,
                indent='  ')
            if not PY3:
                xml = xml.encode('utf-8')

            fpt.write(xml)

            return target

    def __dump_json(self, data, target, namespace=None):
        '''
        dump to JSON file
        '''

        target = target + '.json'

        data1 = self.__create_infos_to_dump(data, namespace)

        with open(target, 'w') as fpt:
            json.dump(data1, fpt, indent=2)

        return target

    def __dump_yaml(self, data, target, namespace=None):
        '''
        dump to YAML file
        '''

        target = target + '.yml'

        with open(target, 'w') as fpt:
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
