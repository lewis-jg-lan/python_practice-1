'''
正则表达式对于字符串的处理是极其有帮助的。
在python中的正则的库是 re

常用函数:
re.match: 从字符串的起始位置匹配一个pattern,如果没有就返回none
re.search: 扫描整个字符串,并返回第一个成功的匹配
re.sub(pattern, repl, string, count=0, flags=0): 用来替换字符串中的匹配项
re.split(): 用来更灵活的切割字符串
'''

import  re

line = 'asdf fjdk; afed, fjek,asdf, foo  allen;'

result = re.split(r'[;,\s]\s',line)
print(result)
'''
需要特别注意的是正则表达式中是否包含一个括号捕获分组。
如果使用了捕获分组，那么被匹配的文本也将出现在结果列表中。
'''
fields = re.split(r'(;|,|\s)\s*',line)
print(fields)
Values = fields[::2]
delimiters = fields[1::2]+['']
print(Values)
print(delimiters)
#S.join(iterable） ==> 将一个可迭代对象的每个元素拼接起来,用S分割
#zip ==> 返回一个可迭代对象
print('$'.join(v+d+s for v, d, s in zip(Values,delimiters,result)))

findallValue = re.compile(r'\s.{4};')
m = findallValue.findall(line)
print(m)
pattern = re.compile(r'(as.{2}).*(.{5})$')
s = pattern.match(line)
print(s.group(2))

replaceStr = re.sub(r'(.{5})$',r'Elva',line)
print(replaceStr)
'''
根据shell通配符去匹配字符串

from fnmatch import  fnmatch,fnmatchcase

fnmatch('foo.txt','*.txt')
'''
text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'
from calendar import month_abbr
def change_dataFor(m):
    mon_name = month_abbr[int(m.group(1))]
    return '{} {} {}'.format(m.group(2),mon_name,m.group(1))

datepat = re.compile(r'(\d+)/(\d+)/(\d+)')
print(datepat.sub(change_dataFor,text))

s = 'hello'
s = format(s,'=>20s')
print(s)








