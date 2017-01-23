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
		pass
	def paser_target_path(self, path):
		for root, file in os.walk(path):

		testallFiles_path = [os.path.join(root, file) for root, file in os.walk(os.path.join(path, 'test-all'))]
		testallFiles = [f for f in os.listdir(os.path.join(path, 'test-all')) if f.endswith('.plist')]
		jsonFiles = [f for f in os.listdir(os.path.join(path, 'Live json')) if f.endswith('.json')]
		for x in testallFiles:
			print(x)
			station_name = x.split('_TESTALL')[0]
			Content = plistlib.readPlist(x)
			if isinstance(Content, dict):
				try:
					JSON_Version = Content['JSON Version']
					Testall_Version = Content['Testall Version']
					ItemControl = Content['ITEMSCONTROL']
					MainItems = Content['Main_TestItems']
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
	main()
