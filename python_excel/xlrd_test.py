import xlrd
import xlwt

book =  xlrd.open_workbook(r'/Users/allenliu/Desktop/D10_MP_QTx TestCoverage.xls')
print(book)
sheetName = book.sheet_names()[0]
print(sheetName)
sheetName_qt0 = book.sheet_by_name('QT0')
print(sheetName_qt0)

#sheet rows and colomns

nrows = sheetName_qt0.nrows
ncol = sheetName_qt0.ncols
print(nrows, ncol)

row_data = sheetName_qt0.row_values(0)
print(row_data)
col_data = sheetName_qt0.col_values(4)
print(col_data)

cell_value = sheetName_qt0.cell_value(5,4)
print(cell_value)

cell_allInfo = sheetName_qt0.cell(2,0)
print(cell_allInfo)

from  datetime import date, datetime

def set_style(name,height,bold=False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.colour_index = 4
    font.height = height

    style.font = font
    return  style

def write_excel():
    f = xlwt.Workbook()

    sheet1 = f.add_sheet(u'sheet1',cell_overwrite_ok=True)
    row0 = [u'业务',u'状态',u'北京',u'shanghai',u'guangzhou',u'shenzheng',u'sum']
    column0 = [u'airport',u'board',u'train',u'car',u'other']
    status = [u'booking',u'out',u'withdraw',u'busuness SUM']

    for i in range(0,len(row0)):
        sheet1.write(0,i,row0[i],set_style('Times New Roman',220,True))

    i, j = 1, 0
    while i < 4 * len(column0) and j < len(column0):
        sheet1.write_merge(i, i + 3, 0, 0, column0[j], set_style('Arial', 220, True))  # 第一列
        sheet1.write_merge(i, i + 3, 7, 7)  # 最后一列"合计"
        i += 4
        j += 1

    sheet1.write_merge(21, 21, 0, 1, u'合计', set_style('Times New Roman', 220, True))

    i = 0
    while i < 4 * len(column0):
        for j in range(0, len(status)):
            sheet1.write(j + i + 1, 1, status[j])
        i += 4
    f.save('/Users/allenliu/Desktop/D10_MP_QTx_format.xls')

if __name__ == '__main__':
    write_excel()