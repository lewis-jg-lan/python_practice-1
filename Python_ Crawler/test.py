import urllib.request
import http.cookiejar
url = 'http://www.baidu.com'

response = urllib.request.urlopen(url)
print(response.getcode())
print(len(response.read()))


request = urllib.request.Request(url)
request.add_header('user-agent','Mozilla/5.0')
response1 = urllib.request.urlopen(request)
print(response1.getcode())
print(response1.read())

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
urllib.request.install_opener(opener)
response2 = urllib.request.urlopen(url)
print(response2.getcode())
print(response2.read())
print(cj)
str = response2.read()
print(str)