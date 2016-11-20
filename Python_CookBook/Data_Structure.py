#Task 分解变量
p = (4,5)
num1 , num2 = p
print(num1)
print(num2)

strTest = 'I am allen'
str1,*str2,str3 = strTest
print(str1)
print(str2)
print(str3)

records = [
    ('foo','1','2'),
    ('bar','hello'),
    ('foo',4,5),
]
def do_foo(x,y):
    print('foo',x,y)
def do_bar(x):
    print('bar',x)

for tag, *args in records:
    if tag == 'foo':
        do_foo(*args)
    elif tag == 'bar':
        do_bar(*args)


line = 'nobody:*:2:-2:unprivileged User:/var/root:/usr/bin'
name,*feilds,dir,sh = line.split(':')
print(dir)


lines = 'allen\nliu\n'
for line in lines:
    print(line)

def sum(item):
    head, *tail = item
    return head + sum(tail) if tail else head

print(sum('items'))

#TASK 保存最后N个记录
from collections import deque

def search(lines, pattern, histroy = 5):
#deque(maxlen=x) 的意思是创建一个固定长度的队列,当有新纪录加入的时候,自动将最老的记录移除。
    previous_lines = deque(maxlen=histroy)
    for line in lines:
        if pattern in line:
            yield line, previous_lines
        previous_lines.append(line)

if __name__ == '__main__':
    with open('/Users/allen/Desktop/rsync.txt') as f:
        for line, previous_line in search(f,'root'):
            for pline in previous_line:
                print('preLine is ',pline, end='')
            print('the line is ',line,end='')
            print('-'*100)
# Q: 为何遍历的时候会是以行为元素,不是一个char 一个char?
# deque 是一个队列元素,从两段插入队列或者弹出元素的复杂度都是O(1),而列表从头部插入或者移除元素的复杂度是O(N)


#TASK
#从某个集合中找出最大或者最小的元素
import heapq

portfolio = [
    {'name':'IBM','share':100, 'price':91.1},
    {'name': 'Apple', 'share': 1110, 'price': 90.1},
    {'name': 'Google', 'share': 2000, 'price': 89.1},
]

cheap = heapq.nsmallest(2,portfolio,key=lambda s:s['price'])
print(cheap)
expensive = heapq.nlargest(2,portfolio,key=lambda s:s['share'])
print(expensive)

#堆 最重要的一个特性是heap[0]永远是最小的元素
num = [1,4.2,567,8,83,23]
heap = list(num)
heapq.heapify(heap)
print(heap)
print(heapq.heappop(heap))
print(heapq.heappop(heap))
print(heapq.heappop(heap))


#实现一个优先级序列

class PriorityQ:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self,item,priority):
        heapq.heappush(self._queue, (-priority,self._index,item))
        self._index += 1

    def pop(self):
        return  heapq.heappop(self._queue)[-1]



