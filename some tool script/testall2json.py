import plistlib
import os
import json
from collections import OrderedDict, Counter
import warnings
import re
import threading


class testall_Item_Structure(object):
	def __init__(self, basic_structure):
		self.command = basic_structure['Command']
		self.catch = basic_structure['Catch']
		self.judge = basic_structure['Judge']
	def generate_total_item(self, regax, spec, *commands):
		item = []
		if commands is not None:
			for each_command in commands:
				for x in self.command:

# parse the plist raw_data
class raw_data(object):
	def __init__(self, path):
		self.stationsPlstRawData = {}
		self.stationsJSONRawData = {}
		self.ItemIndex = OrderedDict()
		self.path = path
		self.paser_target_path()

	def paser_target_path(self):
		dir_jsons = []
		dir_testall = []
		for root, dir, file in os.walk(self.path):
			print('root is ' + root)
			print('file is %s' % file[0])
			for x in file:
				if x.endswith('.json') and root.endswith('Live json'):
					dir_jsons.append(os.path.join(root, x))
				if x.endswith('.plist') and root.endswith('test-all'):
					dir_testall.append(os.path.join(root, x))
		print(dir_testall)
		print(dir_jsons)
		for x in dir_testall:
			station_name = os.path.basename(x).split('_TESTALL')[0]
			print(station_name)
			Content = plistlib.readPlist(x)
			if isinstance(Content, dict):
				try:
					self.stationsPlstRawData[station_name] = Content
				except KeyError:
					warnings.warn('this is a key error')
			else:
				warnings.warn('this is not a dictionary , load error')
			for y in dir_jsons:
				if station_name in y:
					jsonData = open(y)
					JSON_Content = json.load(jsonData)
					print(JSON_Content)
					if isinstance(JSON_Content, dict):
						self.stationsJSONRawData[station_name] = JSON_Content
			self.generate_itemindex(station_name,
			                        plistdata=self.stationsPlstRawData[station_name]['Main_TestItems'],
			                        jsonData=self.stationsJSONRawData[station_name]['data']['tests'])
		print(len(self.ItemIndex))

	def generate_itemindex(self, stationName, plistdata=None, jsonData=None):
		ItemIndexTmp = OrderedDict()
		print(stationName)
		for indexP in range(0, len(plistdata) - 1):
			item = list(plistdata[indexP].keys())
			ItemIndexTmp['%s_plist' % item[0]] = indexP
		for indexJ in range(0, len(jsonData) - 1):
			item = dict(jsonData[indexJ])['Name']['main']
			ItemIndexTmp['%s_json' % item] = indexJ
		print(ItemIndexTmp)
		self.ItemIndex[stationName] = ItemIndexTmp


# todo define the add, delete, modify operation
def add(newItemData, station_raw_Data, stationName):
	for item in newItemData:
		print(item)
		before_item = item['before']
		tmp = generate_addItem(item)
		addJsonItem = tmp[0]
		addTestallItem = tmp[1]
		print('add item in testall is  %s' % addTestallItem )
		print('add item is %s' % addJsonItem)
		if isinstance(station_raw_Data, raw_data):
			PlistData = station_raw_Data.stationsPlstRawData[stationName]
			JSONData = station_raw_Data.stationsJSONRawData[stationName]
			ItemIndex = station_raw_Data.ItemIndex[stationName]
			tmpItemP = '%s_plist' % item
			tmpItemJ = '%s_json' % item

def generate_addItem(item):
	pass

def delete(deletedItemData, station_raw_Data, stationName):
	for item in deletedItemData:
		print('delted item data is ' + item)
		if isinstance(station_raw_Data, raw_data):
			PlistData = station_raw_Data.stationsPlstRawData[stationName]
			JSONData = station_raw_Data.stationsJSONRawData[stationName]
			ItemIndex = station_raw_Data.ItemIndex[stationName]
			tmpItemP = '%s_plist' % item
			tmpItemJ = '%s_json' % item
			if tmpItemP in ItemIndex:
				PlistData['Main_TestItems'].pop(ItemIndex[tmpItemP])
				station_raw_Data.stationsPlstRawData[stationName] = PlistData
				if tmpItemJ in ItemIndex:
					JSONData['data']['tests'].pop(ItemIndex[tmpItemJ])
					station_raw_Data.stationsJSONRawData[stationName] = JSONData
				station_raw_Data.generate_itemindex(
					stationName,
					plistdata=station_raw_Data.stationsPlstRawData[stationName]['Main_TestItems'],
					jsonData=station_raw_Data.stationsJSONRawData[stationName]['data']['tests'])
			else:
				warnings.warn('there is no item %s in the plist' % item)
	return station_raw_Data



def modify(modifyItemData, station_raw_Data):
	pass


class dailywork(object):
	def __init__(self, path):
		self.path = path
		self.gitpath = ''
		self.stations = {}
		self.load_data()

	def load_data(self):
		dailywork = plistlib.readPlist(self.path)
		self.gitpath = dailywork['GitPath']
		self.stations = OrderedDict(dailywork['Stations'])
		self.basicStruct = dailywork['Basic_Item_Structure']
		print(self.stations.keys())


if __name__ == '__main__':
	dw = dailywork(os.path.join(os.getcwd(), 'daily_work.plist'))
	ParseRawData = raw_data(dw.gitpath)
	ItemStructure = testall_Item_Structure(dw.basicStruct)
	print(dw.stations.items())
	for station, operation in dw.stations.items():
		print(station)
		print(operation)
		if operation['add'] is not None:
			# todo add operation
					ParseRawData = add(operation['add'], ParseRawData, station)

		if operation['delete'] is not None:
			deleteData = operation['delete']
			if isinstance(deleteData, list):
				ParseRawData = delete(deleteData, ParseRawData, station)
			else:
				warnings.warn('type error')
		if operation['modify'] is not None:
			pass
		plistlib.writePlist(ParseRawData.stationsPlstRawData[station],
		                    '/Users/allenliu/Desktop/%s_TESTALL.plist' % station)
	plistlib.writePlist(ParseRawData.ItemIndex, os.path.join(os.getcwd(), 'index.plist'))
