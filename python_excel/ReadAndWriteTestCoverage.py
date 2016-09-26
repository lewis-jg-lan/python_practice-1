import xlrd,xlwt,re
from  collections import Counter
#step 1
#read all data from testcoverage

#step 2
#summery all data to find all values
def ReadAndParsedata(filePath):
    book = xlrd.open_workbook(filePath)
    print(book)
    sheets = book.sheet_names()
    def keeped(x):
        if 'Color' in x or 'ChangeNote' in x:
            return False
        else:
            return True
    sheets = [x for x in sheets if keeped(x)]
    print(sheets)
    listTestItems = []
    listTestItemNames = []
    for x in sheets:
        table = book.sheet_by_name(x)
        test_items_sheet = table.col_values(1,3)
        test_items_sheet1 = [x for x in test_items_sheet if x != '']
        test_items_sheet1 = [x for  x in test_items_sheet1 if x != ' ']
        for items in test_items_sheet1:
            listTestItemNames.append(items)
        dict_sheet = {}
        for y in test_items_sheet1:
           dict_sheet[y]=x
        listTestItems.append(dict_sheet)
    print(listTestItemNames)
    ModifiedListTestitems = sorted(set(listTestItemNames))
    print(ModifiedListTestitems)

    print(len(listTestItems))

    dict_finallResult = {}
    for x in range(0,len(listTestItems)):
        dict1 = listTestItems[x]
        dict_combine = {}
        dict1_copy = dict1.copy()
        for k in dict1_copy:
            if k in dict_finallResult.keys():
                value = dict1[k]
                value2 = dict_finallResult[k]
                if isinstance(value2,set):
                    print(value)
                    value2.add(value)
                    print('same item is %s and vlaue is %s' % (k,value2))
                    dict_combine[k] = value2
                else:
                    same_testItem = set([value,value2])
                    dict_combine[k] =same_testItem
                dict1.pop(k)
        dict_finallResult.update(dict_combine)
        dict_finallResult.update(dict1)
    log = ''
    for k, v in dict_finallResult.items():
        log = log + 'key is>> %s << \n value is %s\n'% (k, v)
    print(log)
    with open('/Users/allenliu/Desktop/result1.txt','w') as f:
        f.write(log)
    print(dict_finallResult)
    return ModifiedListTestitems, dict_finallResult

#step 3
#write data to new sheet
def WriteSummeryIntoSheet(targetFilePath):
    pass

if __name__ == '__main__':
    alldata = ReadAndParsedata('/Users/allenliu/Desktop/D10_MP_QTx TestCoverage.xls')
    print('alldata 0 is %s' % alldata[0])
    print('alldata 1 is %s' % alldata[1])
    if WriteSummeryIntoSheet('/Users/allenliu/Desktop/D10_MP_QTx TestCoverage_Summery.xls'):
        print('Write File to target , PASSS!')

    else:
        print('There is something wrong')
