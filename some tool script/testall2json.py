import plistlib
import os
import json
from collections import OrderedDict
class raw_data(object):
	def __init__(self, path):
		self.ItemIndex = OrderedDict()
		if os.path.basename(path).endswith('.plist'):
			self.rawPlistdata = plistlib.readPlist(path)
			self.generate_itemindex(plistdata=self.rawPlistdata)
			self.plistItem = self.rawPlistdata["Main_TestItems"]
		if os.path.basename(path).endswith('.json'):
			with open(path) as jsonFile:
				jsonData = jsonFile.read()
			self.rawJSONdata = json.loads(jsonData)
			self.generate_itemindex(jsonData=self.rawJSONdata)
			self.jsonItems = self.rawJSONdata['tests']

	def generate_itemindex(self, plistdata = None, jsonData = None):
		if plistdata is not None:
			itemData =  plistdata['Main_TestItems']
			for index in range(0, len(itemData)-1):
				item = list(itemData[index].keys())
				print(type(item[0]))
				self.ItemIndex['%s_plist' % item[0]] = index
		if jsonData is not None:
			itemData = jsonData['tests']
			for index in range(0, len(itemData)-1):
				item = dict(itemData[index])['name']
				print(item)
				self.ItemIndex['%s_json' % item] = index

def add(*add_items , **kwargs):
	for x in add_items:
		print('add item is %s' % x)
		#todo get the add item info
		#todo insert item into plist
		#todo inser item into JSON

def delete(*delete_items):
	print('delete Item is %s' % delete_items)
	   #todo get the delete basic info
	   #todo delete the item in plist
	   #todo delete the item in json

def modify(*modify_items):
	print('modify items is %s' % modify_items)
	#todo get the modification item
	#todo check old and new info in plist
	#todo do modicication
	#todo check old and new info in json
	#todo do modication

def do_dailyWork(dailywork_path, stationfilesPath):
	def get_stationPath(originalpath, station):
		jsonDir = os.path.join(originalpath, 'Live json', '%s.json' % station)
		jsonDir = jsonDir if os.path.isfile(jsonDir) else None
		plistDir = os.path.join(originalpath, 'test-all', '%s_TESTALL.plist' % station)
		plistDir = plistDir if os.path.isfile(plistDir) else None
		return {'json': jsonDir, 'plist': plistDir}

	if os.path.isfile(dailywork_path):
		theContent = plistlib.readPlist(dailywork_path)
		print(theContent)
		stations = []
		operations = []
		for (station_name, value) in theContent['Station'].items():
			print(station_name)
			#todo get the station Path
			path = get_stationPath(theContent['GitPath'], station_name)
			if path['plist'] is not None:
				M_plistData = raw_data(path['plist'])
				print(M_plistData.plistItem)
				print(M_plistData.ItemIndex)
			if path['json'] is not None:
				M_jsonData = raw_data(path['json'])
				print(M_jsonData.rawJSONdata)

			print(type(value))
			for (ope_name, items) in value.items():
				print(ope_name)
				opeItems = list(items)
				if ope_name == 'add':
					add(*opeItems)
				elif ope_name == 'delete':
					delete(*opeItems)
				elif ope_name == 'modify':
					modify(*opeItems)
				else:
					print('there is no mapping operation about this %s' % ope_name)

	else:
		print(dailywork_path + stationfilesPath)






def main():
	dailywork_path = os.path.join(os.getcwd(), 'daily_work.plist')
	print(dailywork_path)
	dir_files = os.walk(os.getcwd())
	stationPath = os.path.join(os.getcwd(), 'INSTALL_TESTALL.plist')
	do_dailyWork(dailywork_path, stationPath)


if __name__ == '__main__':
    main()
