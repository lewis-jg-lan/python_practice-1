import csv
import os
import re
import threading
from collections import OrderedDict


QCR_WEBSITE = 'http://17.239.228.36/cgi-bin/WebObjects/QCR.woa/default'

class ModulePART(object):

    def __init__(self, csvPath):
        self.csvPath= csvPath
        self.csvData =[]
        self.QcrAccount = 'tina_huang'
        self.QcrPassword = 'Ats@123'
        self.FailBasicInfo = OrderedDict()
        self.SNs = []


    def parseCsv(self):
        self.csvData=[]
        with open(self.csvPath) as csvPath:
            self.csvData = list(csv.reader(csvPath))
        print(self.csvData)
        for x in range(1, len(self.csvData)-1):
            self.SNs.append(self.csvData[x])

        return self.csvData

    def async_Download(self):
        pass

    def parse_FailLog(self, logpath):
        print(threading.current_thread())
        theListofFiles = os.listdir(os.path.abspath(logpath))
        for file in theListofFiles:
            thefilePath = os.path.join(os.path.abspath(logpath), file)
            if '.csv' in file:
                print(file)
                csvData = list(csv.reader(open(thefilePath)))
                for x in csvData:
                    if x[1] is '1':
                        self.FailBasicInfo['Item_(%s)' % csvData.index(x)] = x[0]
                        self.FailBasicInfo['Value_(%s)' % csvData.index(x)] = x[2]
                        self.FailBasicInfo['Spec_(%s)' % csvData.index(x)] = '[%s , %s]' % (x[3],x[4])
                        print(self.FailBasicInfo)
            elif 'Uart' in file:
                print(thefilePath)
                with open(thefilePath) as UartFile:
                    UartData = UartFile.read()
                if self.FailBasicInfo is None:
                    print('There is no Fail need to check')
                else:
                    ListFailItem = list(self.FailBasicInfo.items())
                    for x in range(0, len(ListFailItem), 3):
                        SingalFailItem = ListFailItem[x: x+3]
                        for (key, value) in SingalFailItem:
                            if 'Item' in key:
                                ItemName = value
                            elif 'Value' in key:
                                ItemValue = value
                            else:
                                ItemSpec = value
                    strRegex = r'START TEST %s .* ' % ItemName.upper()
                    print(strRegex)
                    regexForFailLog = re.compile(strRegex)
                    # result = regexForFailLog.search(UartData)
                    result = regexForFailLog.search(UartData,endpos=len(UartData))
                    print(result.group(0))



                    # regax = re.compile('')
                    # FailString = re.match(r'', UartData)
            else:
                print(file)

    def async_parseFailLog(self, logPath):
        self.thread = threading.Thread(target=self.parse_FailLog, name='ParseFailLog', args=(logPath,))
        self.thread.start()

    def generate_FailReport(self):
        pass


if __name__ == '__main__':
    md = ModulePART('/Users/allen/PycharmProjects/QCR downloder/App/example.csv')
    md.parseCsv()




