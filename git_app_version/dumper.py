# -*- coding: utf-8 -*-

import json
import os

import xmltodict
import yaml

from git_app_version.helper.pyversion import PY3

try:
    import ConfigParser as configparser
except ImportError:
    import configparser


class FileDumper(object):

    def dump(
            self,
            data=None,
            fileformat='json',
            target=None,
            cwd=None,
            namespace=''):
        target = self.__check_target(target, cwd)
        if fileformat == 'yaml' or fileformat == 'yml':
            return self.dump_yaml(data, target, namespace)
        elif fileformat == 'xml':
            return self.dump_xml(data, target, namespace)
        elif fileformat == 'ini':
            return self.dump_ini(data, target, namespace)
        else:
            return self.dump_json(data, target, namespace)

    def __check_target(self, target, cwd=None):
        if not os.path.isabs(target):
            cwd = cwd if cwd else os.getcwd()
            target = cwd + '/' + target

        self.__make_parent_dir(target)

        return target

    def __make_parent_dir(self, target):
        parent_dir = os.path.dirname(target)
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir, 493)  # 493 in decimal as 755 in octal

    def __create_infos_to_dump(self, infos, namespace=None):
        to_dump = infos
        if namespace is not None and namespace != '':
            namespaces = namespace.split('.')
            namespaces.reverse()
            for name in namespaces:
                to_dump = {name: to_dump}

        return to_dump

    def __encode(self, item, encoding='utf-8'):
        if isinstance(item, unicode):
            return item.encode(encoding)
        else:
            return item

    def __flatten(self, item):
        if isinstance(item, list):
            flattened_list = ''
            if len(item):
                flattened_list = "'{}'".format("', '".join(item))
            return "[{}]".format(flattened_list)
        else:
            return item

    def dump_ini(self, data, target, namespace=None):
        target = target + '.ini'

        if namespace is None or namespace == '':
            namespace = 'app_version'

        ini = configparser.RawConfigParser()
        ini.add_section(namespace)

        for key, val in data.items():
            if not PY3:
                val = self.__encode(self.__flatten(val))

            ini.set(namespace, key, val)

        with open(target, 'w') as fp:
            ini.write(fp)

        return target

    def dump_xml(self, data, target, namespace=None):
        target = target + '.xml'
        if namespace is None or namespace == '':
            namespace = 'app_version'

        with open(target, 'w') as fp:
            xml = xmltodict.unparse(
                self.__create_infos_to_dump(
                    data,
                    namespace),
                encoding='utf-8',
                pretty=True,
                indent='  ')
            if not PY3:
                xml = xml.encode('utf-8')

            fp.write(xml)

            return target

    def dump_json(self, data, target, namespace=None):
        target = target + '.json'

        data1 = self.__create_infos_to_dump(data, namespace)

        with open(target, 'w') as fp:
            json.dump(data1, fp, indent=2)

        return target

    def dump_yaml(self, data, target, namespace=None):
        target = target + '.yml'

        with open(target, 'w') as fp:
            if not data:
                fp.write("---\n")
            else:
                yaml.safe_dump(
                    self.__create_infos_to_dump(data, namespace),
                    fp,
                    default_flow_style=False,
                    explicit_start=True,
                    allow_unicode=True,
                    # force quoting
                    # to prevent abbrev_commit to be read as a float
                    default_style='\''
                )

        return target
