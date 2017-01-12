import threading
import csv
import re
import requests
from bs4 import BeautifulSoup
import datetime
import random
import zipfile

#start
class Down_Tianya(threading.Thread):
    """多线程下载"""
    def __init__(self,csvinfos):
        threading.Thread.__init__(self)
        # self.url = url
        # self.num = num
        self.csv_list = csvinfos
    def run(self):
        global dictSN
        dictSN={}
        res = requests.get('http://17.239.228.36/cgi-bin/WebObjects/QCR.woa/default')
        parsehtml = res.text
        regex = re.compile(r'action=\"(.*?)\">')
        fetchURL = regex.search(parsehtml).group(1)
        print(fetchURL)
        regex1 = re.compile(r'.*/(.*?)/.*')
        wosid = regex1.search(fetchURL).group(1)
        print(wosid)
        post_url = 'http://17.239.228.36%s' % fetchURL
        print(post_url)
        post_data = {'Password': 'Ats@123', '3.7.5.13.y': 5, 'wosid': wosid, 'UserName': 'tina3_huang',
                     '3.7.5.13.x': 22}
        p = requests.post(post_url, data=post_data)
        for x in range(1,len(self.csv_list)):
            SN = self.csv_list[x][0]
            print('current thread %s' % threading.current_thread().name)
            print('downling from %s' % SN)
            StationName = self.csv_list[x][1]
            print(StationName)
            result = self.csv_list[x][2]
            print(result)
            number=self.csv_list[x][3]
            print(number)
            searchhtml = p.text
            regexsearch = re.compile('form name="f_1_5_5_29".*?action=\"(.*?)\">')
            searchurl = regexsearch.search(searchhtml).group(1)
            print(searchurl)
            post_data1 = {'1.5.5.29.1': SN, '1.5.5.29.3': 'Search', 'wosid': wosid}
            post_url1 = 'http://17.239.228.36/%s' % searchurl
            p1 = requests.post(post_url1, data=post_data1)
            # print(p1.text)
            downloadhtml = p1.text
            #   parse the html and choose the station and log informations
            # def parseHtml(downloadhtml,StationName,SN):
            soup = BeautifulSoup(downloadhtml, 'html.parser')
            formAtts = soup.find_all('form')
            # for a in range(0,len(formAtts)):
            #     oneform=formAtts[a]
            #     for b in oneform:
            #         if b['name']=="f_13_1_5_13_1_3_0_1":
            #             myForm=oneform
            myForm = formAtts[2]
            theDownloadUrl = 'http://17.239.228.36' + myForm['action']
            print('下载的url为:%s' % theDownloadUrl)
            infos = myForm.select('tr')
            cell_list = []
            content_list = []
            lognumber = 0
            for index in range(1, len(infos)):
                contents = infos[index].select('td')
                stationname = contents[0].text.strip()
                if stationname == StationName:
                    lognumber += 1
                    for td in contents:
                        cell_list.append(td.text.strip())
                    cell_list.pop()
                    # print(cell_list)
                    loactionInfo = contents[19].select('input')
                    for s in loactionInfo:
                        location = s['name']
                        cell_list.append(location)
                    print(cell_list)
                    content_list.append(cell_list)
                    cell_list = []
                else:
                    print(stationname)
            if lognumber == 0:
                print('%s目前没有%s的Log.' % (SN, StationName))
            print(content_list)
            print(theDownloadUrl)
            print(lognumber)
            # all_infos=(content_list,theDownloadUrl,lognumber)
            # print(all_infos)
            # return all_infos
            # pass
            # get sn and station from csv
            # examplefile=open('/Users/Belle_Li/Desktop/example.csv')
            # exampleread=csv.reader(examplefile)
            # exampledata=list(exampleread)
            # get sns and stations from the csv.
            #     for index in range(1,len(exampledata)):
            #     data=exampledata[index]
            #     SN =data[0]

            if number == '':
                number = 1
            # downloadhtml=serchPage(SN)
            # print(downloadhtml)
            # all_infos=parseHtml(downloadhtml,StationName,SN)
            # station_list=all_infos[0]
            # post_url2=all_infos[1]
            # totalnumber=all_infos[2]
            pass_list = []
            fail_list = []
            final_list=[]
            # if the result is pass,will choose the pass log
            if result.lower() == 'pass':
                for list in content_list:
                    if list[3] == 'PASS':
                        pass_list.append(list)
                    final_list = pass_list
            elif result.lower() == 'fail':
                for list in content_list:
                    if list[3] == 'FAIL' or list[3] == 'OVERRODE':
                        fail_list.append(list)
                    final_list = fail_list
            else:
                final_list = content_list
            if (len(final_list)) == 0:
                continue
            if int(number) > len(final_list):
                print('QCR中只有%s个Log。' % len(final_list))
                number = len(final_list)
            print(number)
            print(final_list)
            i = 0
            for n in range(int(number)):
                mmm = final_list[n]
                length = len(mmm)
                # 有种情况就是没有下载的标志,需要考虑一下
                if length == 19:
                    mn = int(number) + i
                    if mn >= int(number):
                        continue
                    mmm = final_list[mn]
                    xxxx = mmm[19]
                    time = mmm[16]
                    time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
                    time = time.strftime('%Y-%m-%d %H-%M-%S')
                    i = i + 1
                # number=number+1
                # n=n+1
                else:
                    xxxx = mmm[19]
                    time = mmm[16]
                    time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
                    time = time.strftime('%Y-%m-%d %H-%M-%S')
                    print(xxxx)
                x = xxxx + '.x'
                y = xxxx + '.y'
                theDownloadData = {}
                theDownloadData[x] = random.randrange(0, 10)
                theDownloadData[y] = random.randrange(0, 10)
                theDownloadData['wosid'] = wosid
                p2 = requests.post(theDownloadUrl, data=theDownloadData)
                if p2.status_code == requests.codes.ok:
                    print('Current thread %s download success' % threading.current_thread().name)
                else:
                    print('Current thread %s download fail' % threading.current_thread().name)
                with open('/Users/Belle_Li/Desktop/downloadlog/%s_%s_%s_%s.zip' % (
                        result.upper(), SN, time, StationName), 'wb') as f:
                    f.write(p2.content)
                # if the result is fail, will analysis the fail log
                # result = 'FAIL'
                # SN = 'C7CSN00BHQT9'
                # time = "2016-11-06 03-04-50"
                # StationName = 'QT0'
                result = result.upper()
                if result == 'FAIL':
                    # decompress the zip file and write the file to the new file.
                    filename = '/Users/Belle_Li/Desktop/downloadlog/%s_%s_%s_%s.zip' % (
                        result, SN, time, StationName)
                    print(filename)
                    filedir = '/Users/Belle_Li/Desktop/downloadlog/%s_%s/' % (SN, time)
                    r = zipfile.is_zipfile(filename)
                    if r:
                        fz = zipfile.ZipFile(filename, 'r')
                        for file in fz.namelist():
                            print(file)
                            fz.extract(file, filedir)
                    else:
                        print('This file is not zip file')
                    # define some parameter
                    failitem = []
                    baseinfo = [['TestName', 'Value', 'Limit']]
                    uartinfo = []
                    commandinfo = []
                    debuginfo = []
                    # analysis the csv file.
                    csvname = '%s_%s_%s_CSV.csv' % (result, SN, time)
                    csvpath = filedir + csvname
                    csvfile = open(csvpath, 'r')
                    reader = csv.reader(csvfile)
                    for row in reader:
                        if row[1] == '1':
                            # print(row[0])
                            failitem.append(row[0])
                            TestName = row[0]
                            Value = row[2]
                            Downlimit = row[3]
                            Uplimit = row[4]
                            if Downlimit == Uplimit:
                                limit = Downlimit
                            else:
                                limit = [Downlimit, Uplimit]
                            baseinfo.append([TestName, Value, limit])
                    print(failitem)
                    print(baseinfo)
                    #     analysis the uart log
                    uartname = '%s_%s_%s_Uart.txt' % (result, SN, time)
                    uartpath = filedir + uartname
                    uartfile = open(uartpath, 'r')
                    uartlog = uartfile.read()
                    uartlist = uartlog.split('====== START TEST')
                    del uartlist[0]
                    for list in uartlist:
                        regex = re.compile(r'Item Name:(.*?),')
                        failitemname = regex.search(list).group(1)
                        for item in failitem:
                            if item == failitemname:
                                uartinfo.append("Fail item:%s \n=============== START TEST%s" % (item, list))
                                commandlist = list.split(':-)')
                                for command in commandlist:
                                    if 'ERROR' in command or 'Fail' in command:
                                        failcommand = re.findall(r'\(TX ==> \[MOBILE\]\):(.*?)\n', command)
                                        commandinfo.append(failcommand[0])
                    print(uartinfo)
                    print(commandinfo)
                    #     analysis the debug log
                    debugname = '%s_%s_%s_DEBUG.txt' % (result, SN, time)
                    debugpath = filedir + debugname
                    debugfile = open(debugpath, 'r')
                    debuglog = debugfile.read()
                    debuglist = debuglog.split('====== START TEST')
                    del debuglist[0]
                    for lists in debuglist:
                        # regex1=re.compile(r'===== END TEST (.*?) ')
                        # itemname=regex1.search(lists).group(1)
                        itemname = re.findall(r'Item Name:(.*?),', lists)
                        # print(itemname[0])
                        for item in failitem:
                            if itemname[0] == item:
                                print(item)
                                debugcommand = lists.split('++++\n')
                                for debug in debugcommand:
                                    # print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
                                    # print(debug)
                                    if 'TestResult : FAIL ;' in debug:
                                        debuginfo.append([item, debug])
                    print(debuginfo)
                    dictinfo = {'FailItem': failitem, 'BaseInfo': baseinfo, 'FailCommand': commandinfo,
                                'UartInfo': uartinfo, 'DebugInfo': debuginfo}
                    SNn='%s_%s' % (SN,n)
                    dictSN = {SNn: dictinfo}
                    # print(dictSN)
                    # print(dictSN[SNn])
                print(dictSN)


threads=[]
csvinfos=[]
"""根据页数构造urls进行多线程下载"""
examplefile=open('/Users/Belle_Li/Desktop/example.csv')
exampleread=csv.reader(examplefile)
exampledata=list(exampleread)
print(exampledata)
# tup=[['qwe',1,3],['qaz',1,4],['wrr',34,5],['sdf',4,5],['wwe',5,7],['qsx',7,9],['ffgg',4,7]]
for x in range(1,len(exampledata),2):
    for y in range(0,2):
        if x+y>=len(exampledata):
            continue
        csvinfos.append(exampledata[x+y])
    print(csvinfos)
    downlist = Down_Tianya(csvinfos)
    downlist.start()
    threads.append(downlist)
    csvinfos=[]



