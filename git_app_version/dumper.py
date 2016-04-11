# -*- coding: utf-8 -*-

import os
import json
import xmltodict

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import yaml
try:
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper

class Dumper(object):

    def dump(self, data = {}, format = 'json', target = None, cwd=None, namespace=''):
        target = self.__checkTarget(target, cwd)
        if format == 'yaml' or format == 'yml':
            return self.dumpYaml(data, target, namespace)
        elif format == 'xml':
            return self.dumpXml(data, target, namespace)
        elif format == 'ini':
            return self.dumpIni(data, target, namespace)
        else:
            return self.dumpJson(data, target, namespace)

    def __checkTarget(self, target, cwd=None):
        if not os.path.isabs(target):
            if cwd is None or not os.path.exists(cwd):
                cwd = os.getcwd()

            target = cwd+'/'+target

        self.__makeParentDir(target)

        return target

    def __makeParentDir(self, target):
        parentDir = os.path.dirname(target)
        if not os.path.exists(parentDir):
            os.makedirs(parentDir, 493) # 493 in decimal as 755 in octal

    def __createInfosToDump(self, infos, namespace=None):
        toDump = infos
        if namespace is not None and namespace != '' :
            namespaces = namespace.split('.')
            namespaces.reverse()
            for name in namespaces :
                toDump = { name: toDump }

        return toDump

    def dumpIni(self, data, target, namespace=None):
        target = target+'.ini'
        namespace = 'app_version' if namespace is None or namespace == '' else namespace

        ini = configparser.RawConfigParser()
        ini.add_section(namespace)
        for key,val in data.items():
            ini.set(namespace, key, val)

        with open(target, 'w') as f:
            ini.write(f)

        return target

    def dumpXml(self, data, target, namespace=None):
        target = target+'.xml'
        namespace = 'app_version' if namespace is None or namespace == '' else namespace

        with open(target, 'w') as f:
            xml = xmltodict.unparse(self.__createInfosToDump(data, namespace), encoding='utf-8', pretty=True, indent='  ')
            f.write(xml)

            return target

    def dumpJson(self, data, target, namespace=None):
        target = target+'.json'

        data1 = self.__createInfosToDump(data, namespace)

        with open(target, 'w') as f:
            json.dump(data1, f, indent=2)

        return target

    def dumpYaml(self, data, target, namespace=None):
        target = target+'.yml'

        with open(target, 'w') as f:
            if not data :
                f.write("---\n")
            else :
                yaml.dump(
                    self.__createInfosToDump(data, namespace),
                    f,
                    default_flow_style=False,
                    explicit_start=True,
                    allow_unicode=True,
                    default_style='\'' # force quoting to prevent abbrev_commit to be read as a float
                )

        return target
