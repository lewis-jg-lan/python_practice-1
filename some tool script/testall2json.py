import plistlib
import os
import json
from collections import OrderedDict
import warnings


class operation_functions(object):
    def __init__(self, **kwargs):
        self.send_command = {"SEND_COMMAND:": {"STRING": kwargs['commands'],
                                               "TARGET": kwargs['target']}}
        self.catch_value = {"CATCH_VALUE:RETURN_VALUE:": {"REGEX": kwargs['regax']}}


class raw_data(object):
    def __init__(self, path):
        self.station_raw_data = {}
        self.ItemIndex = {}
        self.path = path

    def paser_target_path(self):
        dir_jsons = []
        dir_testall = []
        for root,dir, file in os.walk(self.path):
            print('root is '+root)
            print('file is %s' % file[0])
            for x in file:
                if x.endswith('.json') and root.endswith('Live json'):
                    dir_jsons.append(os.path.join(root, x))
                if x.endswith('.plist') and root.endswith('test-all'):
                    dir_testall.append(os.path.join(root,x))
        print(dir_testall)
        print(dir_jsons)
        for x in dir_testall:
            station_name = os.path.basename(x).split('_TESTALL')[0]
            print(station_name)
            Content = plistlib.readPlist(x)
            if isinstance(Content, dict):
                try:
                    JSON_Version = Content['JSON Version']
                    Testall_Version = Content['Testall Version']
                    ItemControl = Content['ITEMSCONTROL']
                    MainItems = Content['Main_TestItems']
                    print(Content)
                except KeyError:
                    warnings.warn('this is a key error')
            else:
                warnings.warn('this is not a dictionary , load error')


    def generate_itemindex(self, plistdata=None, jsonData=None):
        if plistdata is not None:
            itemData = plistdata['Main_TestItems']
            for index in range(0, len(itemData) - 1):
                item = list(itemData[index].keys())
                print(type(item[0]))
                self.ItemIndex['%s_plist' % item[0]] = index
        if jsonData is not None:
            itemData = jsonData['tests']
            for index in range(0, len(itemData) - 1):
                item = dict(itemData[index])['name']
                print(item)
                self.ItemIndex['%s_json' % item] = index


if __name__ == '__main__':
    ParseRawData = raw_data(os.getcwd())
    ParseRawData.paser_target_path()
