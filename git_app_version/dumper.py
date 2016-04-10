# -*- coding: utf-8 -*-

import os
import json
import xmltodict
from pprint import pprint

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

    def dump(self, data = {}, format = 'json', target = None, cwd=None, section='app_version'):
        target = self.__checkTarget(target, cwd)
        if format == 'yaml' or format == 'yml':
            return self.dumpYaml(data, target, section=section)
        elif format == 'xml':
            return self.dumpXml(data, target, root=section)
        elif format == 'ini':
            return self.dumpIni(data, target, section=section)
        else:
            return self.dumpJson(data, target, section=section)

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

    def __createInfosToDump(self, infos, section=None):
        toDump = infos
        if section is not None and section != '' :
            sections = section.split('.')
            sections.reverse()
            for sec in sections :
                toDump = { sec: toDump }

        return toDump

    def dumpIni(self, data, target, section='app_version'):
        target = target+'.ini'

        ini = configparser.RawConfigParser()
        ini.add_section(section)
        for key,val in data.items():
            ini.set(section, key, val)

        with open(target, 'w') as f:
            ini.write(f)

        return target

    def dumpXml(self, data, target, root='app_version'):
        target = target+'.xml'

        with open(target, 'w') as f:
            xml = xmltodict.unparse(self.__createInfosToDump(data, root), encoding='utf-8', pretty=True, indent='  ')
            f.write(xml)

            return target

    def dumpJson(self, data, target, section=None):
        target = target+'.json'

        data1 = self.__createInfosToDump(data, section)

        with open(target, 'w') as f:
            json.dump(data1, f, indent=2)

        return target

    def dumpYaml(self, data, target, section=None):
        target = target+'.yml'

        with open(target, 'w') as f:
            if not data :
                f.write("---\n")
            else :
                yaml.dump(
                    self.__createInfosToDump(data, section),
                    f,
                    default_flow_style=False,
                    explicit_start=True,
                    allow_unicode=True,
                    default_style='\'' # force quoting to prevent abbrev_commit to be read as a float
                )

        return target
