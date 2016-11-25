# Task 分解变量
p = (4, 5)
num1, num2 = p
print(num1)
print(num2)

strTest = 'I am allen'
str1, *str2, str3 = strTest
print(str1)
print(str2)
print(str3)

records = [
    ('foo', '1', '2'),
    ('bar', 'hello'),
    ('foo', 4, 5),
]


def do_foo(x, y):
    print('foo', x, y)


def do_bar(x):
    print('bar', x)


for tag, *args in records:
    if tag == 'foo':
        do_foo(*args)
    elif tag == 'bar':
        do_bar(*args)

line = 'nobody:*:2:-2:unprivileged User:/var/root:/usr/bin'
name, *feilds, dir, sh = line.split(':')
print(dir)

lines = 'allen\nliu\n'
for line in lines:
    print(line)


def sum(item):
    head, *tail = item
    return head + sum(tail) if tail else head


print(sum('items'))

# TASK 保存最后N个记录
from collections import deque


def search(lines, pattern, histroy=5):
    # deque(maxlen=x) 的意思是创建一个固定长度的队列,当有新纪录加入的时候,自动将最老的记录移除。
    previous_lines = deque(maxlen=histroy)
    for line in lines:
        if pattern in line:
            yield line, previous_lines
        previous_lines.append(line)


if __name__ == '__main__':

    # /Users/allenliu/Desktop/rsync.txt
    try:
        with open('/Users/allenliu/Desktop/TEST.txt') as f:
            for line, previous_line in search(f, 'root'):
                for pline in previous_line:
                    print('preLine is ', pline, end='')
                print('the line is ', line, end='')
                print('-' * 100)
    except FileNotFoundError:
        with open('/Users/allen/Desktop/old/rsync.txt') as f:
            for line, previous_line in search(f, 'root'):
                for pline in previous_line:
                    print('preLine is ', pline, end='')
                print('the line is ', line, end='')
                print('-' * 100)
    finally:
        print('end')


# Q: 为何遍历的时候会是以行为元素,不是一个char 一个char?
# deque 是一个队列元素,从两段插入队列或者弹出元素的复杂度都是O(1),而列表从头部插入或者移除元素的复杂度是O(N)


# TASK
# 从某个集合中找出最大或者最小的元素
import heapq

portfolio = [
    {'name': 'IBM', 'share': 100, 'price': 91.1},
    {'name': 'Apple', 'share': 1110, 'price': 90.1},
    {'name': 'Google', 'share': 2000, 'price': 89.1},
]

cheap = heapq.nsmallest(2, portfolio, key=lambda s: s['price'])
print(cheap)
expensive = heapq.nlargest(2, portfolio, key=lambda s: s['share'])
print(expensive)

# 堆 最重要的一个特性是heap[0]永远是最小的元素
num = [1, 4.2, 567, 8, 83, 23]
heap = list(num)
heapq.heapify(heap)
print(heap)
print(heapq.heappop(heap))
print(heapq.heappop(heap))
print(heapq.heappop(heap))


# 实现一个优先级序列

class PriorityQ:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]


class Item:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Item ({!r})'.format(self.name)
'''
str()一般是将数值转成字符串。
repr()是将一个对象转成字符串显示，注意只是显示用，有些对象转成字符串没有直接的意思
如list,dict使用str()是无效的，但使用repr可以，这是为了看它们都有哪些值，为了显示之用。
'''



q = PriorityQ()
q.push(Item('foo'), 1)
q.push(Item('bar'), 5)

print(q.pop())
print(q.pop())

# todo multidict 用来实现字典的一对多,我们可以用list 跟 set 来表示多值。取值则可以用二维方式来取出。
# 使用collection 中的 defaultdict 模块


from  collections import defaultdict
from  collections import OrderedDict

d = defaultdict(list)
d['a'].append(1)
d['a'].append(2)
d['b'].append(4)

print(d['a'][0])

s = defaultdict(set)
s['a'].add(1)
s['b'].add(2)
s['a'].add(4)
print(s)

# 需要注意的是这个 OrderDict 中维护着一个根据建插入的顺序排序的双向链表,当有新元素插入的时候,他会放到链表的尾部

d = OrderedDict()
d['allen'] = 'liu'
d['Elva'] = 'wang'

for key in d:
    print(key, d[key])

# 记录归类问题
# 你有一个字典或者实例的序列,然后想根据某个特定的字段来分组迭代

'''
groupby 函数主要是扫描整个序列,并且查找连续相同的元素序列。
每一次迭代,都会返回一个值跟迭代器对象。
不过前提是要对待分组的对象排序。
'''
from  operator import itemgetter
from  itertools import groupby

test1 = [1, 2, 3]
key = itemgetter(2)
print(key)

rows = [
    {'address': '5412 N CLARK', 'date': '07/01/2012'},
    {'address': '5148 N CLARK', 'date': '07/04/2012'},
    {'address': '5800 E 58TH', 'date': '07/02/2012'},
    {'address': '2122 N CLARK', 'date': '07/03/2012'},
    {'address': '5645 N RAVENSWOOD', 'date': '07/02/2012'},
    {'address': '1060 W ADDISON', 'date': '07/02/2012'},
    {'address': '4801 N BROADWAY', 'date': '07/01/2012'},
    {'address': '1039 W GRANVILLE', 'date': '07/04/2012'},
]
rows.sort(key=itemgetter('date'))
for date, items in groupby(rows, key=itemgetter('date')):
    print(date, ':')
    for i in items:
        print('', i)

# 删除序列相同元素并保持顺序


# def dedupe(items, key =None):
#     seen = set()
#     for item in items:
#         val = item if key is None else key(item)
#         if val not in seen:
#             yield item
#             seen.add(val)
#
# # a = [ {'x':1, 'y':2}, {'x':1, 'y':3}, {'x':1, 'y':2}, {'x':2, 'y':4}]
# # print(list(dedupe(a, key= lambda d: (d['x'],d['y']))))
#
#
# strTest = ''
# with open('/Users/allenliu/Desktop/TEST.txt','r') as f:
#     for line in dedupe(f):
#         print('return line is ',line)
#         strTest = strTest + line
#
# with open('/Users/allenliu/Desktop/TEST_result.txt','w') as fw:
#     fw.write(strTest)

# 切片命名
# 这个更多是编码的一个规范。
record = '....................100 .......513.25 ..........'
Shares = slice(20, 23)
Price = slice(31, 37, 2)
print(str(record[Price]))
print(Price.start, 'end', Price.stop, 'Step', Price.step)
cost = int(record[Shares]) * float(record[Price])
print(cost)

# 怎样找出一个序列中出现次数最多的元素呢？
# 我的逻辑: 先排序,再遍历排序后的元素,每一个跟之后的比,一样的话计数加一
# python
'''
Counter 对象在几乎所有需要制表或者计数数据的场合是非常有用的工具。
在解决这类问题的时候你应该优先选择它，而不是手动的利用字典去实现。
'''

words = [
    'look', 'into', 'my', 'eyes', 'look', 'into', 'my', 'eyes',
    'the', 'eyes', 'the', 'eyes', 'the', 'eyes', 'not', 'around', 'the',
    'eyes', "don't", 'look', 'around', 'the', 'eyes', 'look', 'into',
    'my', 'eyes', "you're", 'under'
]

sortWords = sorted(words)
dictWord = {}
wordNum = 1
for index in range(0, len(sortWords) - 1):
    nextIndex = index + 1
    theItem = sortWords[index]
    if theItem == sortWords[nextIndex]:
        wordNum += 1
    else:
        print(wordNum)
        dictWord[theItem] = wordNum
        wordNum = 1

print(dictWord)

from collections import Counter

word_counts = Counter(words)

top_three = word_counts.most_common(3)
print(top_three)
print(word_counts['look'])
print(Counter(words))


#对于字典列表

rows = [
    {'fname': 'Brian', 'lname': 'Jones', 'uid': 1003},
    {'fname': 'David', 'lname': 'Beazley', 'uid': 1002},
    {'fname': 'John', 'lname': 'Cleese', 'uid': 1001},
    {'fname': 'Big', 'lname': 'Jones', 'uid': 1004}
]

sorwRows = sorted(rows, key= itemgetter('fname'))
sorwRows1 = sorted(rows, key= itemgetter('uid'))
print('sorted ROWS :%s' % sorwRows)
print('sorted ROWS :%s' % sorwRows1)

#过滤元素
mylist = [1, 4, -5, 10, -7, 2, 3, -1, 'NA']

print([n if isinstance(n,int) else 0 for n in mylist])

values = ['1', '2', '-3', '-', '4', 'N/A', '5']
def is_int(val):
    try:
        x = int(val)
        return True
    except ValueError:
        return False
FiltorValues = list(filter(is_int, mylist))
print(FiltorValues)

#从字典中提取子集
prices = {
    'ACME': 45.23,
    'AAPL': 612.78,
    'IBM': 205.55,
    'HPQ': 37.20,
    'FB': 10.75
}

#但是，字典推导方式表意更清晰，
# 并且实际上也会运行的更快些 (在这个例子中，实际测试几乎比 dcit() 函数方式快整整一倍)。

p1 = {key:value for key, value in prices.items() if value > 200}
print(p1)




