# -*- coding: utf-8 -*-

import os
import json
from lxml import etree

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
            return self.dumpYaml(data, target)
        elif format == 'xml':
            return self.dumpXml(data, target, root=section)
        elif format == 'ini':
            return self.dumpIni(data, target, section=section)
        else:
            return self.dumpJson(data, target)

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

        rootNode = etree.Element(root)

        for key,val in data.items():
            node = etree.SubElement(rootNode, key)
            node.text = val

        tree = etree.ElementTree(rootNode)
        tree.write(target,  encoding="UTF-8", xml_declaration=True, pretty_print=True)

        return target

    def dumpJson(self, data, target):
        target = target+'.json'

        with open(target, 'w') as f:
            json.dump(data, f, indent=4)

        return target

    def dumpYaml(self, data, target):
        target = target+'.yml'

        with open(target, 'w') as f:
            if not data :
                f.write("---\n")
            else :
                yaml.dump(
                    data,
                    f,
                    default_flow_style=False,
                    explicit_start=True,
                    allow_unicode=True,
                    default_style='\'' # force quoting to prevent abbrev_commit to be read as a float
                )

        return target
