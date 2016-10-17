#!/usr/bin/python
from HTMLParser import HTMLParser
import urllib2
import re
import datetime
import json
import os

dir_path = os.path.dirname(os.path.realpath(__file__)) + '/'

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def __init__(self):
        self.td = False
        #self.a = False
        self.count = 0
        self.table_count = 0
        self.table_level = 0
        self.result = {}
        HTMLParser.__init__(self)
    def handle_starttag(self, tag, attrs):
        if tag == 'table' and self.table_count <= 2:
            self.table_level += 1
            self.table_count += 1
        if tag == 'td' and self.table_level == 1 and self.table_count <= 2: 
            self.td = True
            self.data = ''
        #if tag == 'a':
        #    self.a = True
    def handle_endtag(self, tag):
        if tag == 'table' and self.table_count <= 2:
            self.table_level -= 1
        if tag == 'td' and self.table_level == 1 and self.table_count <= 2: 
            self.td = False
            if not self.data.strip():
                self.data = 'Null'
            res = re.sub(r"\s+", " ", self.data)
            self.result[self.count] = res
            self.count += 1
        #if tag == 'a':
        #    self.a = False
    def handle_data(self, data):
        #if self.td and self.table_level == 1 and self.table_count <= 2 and not self.a :
        if self.td and self.table_level == 1 and self.table_count <= 2 :
            data = data.decode('big5').encode('utf-8').strip()
            self.data += data
    def getData(self):
        return self.data
    def getResult(self):
        return self.result
# instantiate the parser and fed it some HTML
parser = MyHTMLParser()
url = 'http://www.avi.com.tw/single_lens/price-single-lens-canonef.htm'
html = urllib2.urlopen(url).read()
html = re.sub(r"<!.>", "", html)
parser.feed(html)
new_data = parser.getResult()

now = datetime.datetime.now()
today = str(now.month) + "/" + str(now.day)

# need change to old data
#result = {}
#result['dates'] = []
#result['dates'].append(today)
#result['data'] = {}

with open(dir_path + 'result.json', 'r') as f:
    input_data = f.read().decode("utf-8")
    input_data = json.loads(input_data, encoding='utf-8');
    #print json.dumps(input_data, ensure_ascii=False)
    old_dates = input_data['dates']
    old_data = input_data['data']
    #print json.dumps(old_dates, ensure_ascii=False)
    #print json.dumps(old_data, ensure_ascii=False)    
f.close()

if today not in old_dates:
    old_dates.append(today)

i = 6
while i < len(new_data) - 5: 
    name = new_data[i].replace('\xe8\xa9\xb3', '').strip().decode('utf-8')
    if name in old_data:
        old_price = old_data[name]['price']
        if today not in old_price:
            old_price[today] = new_data[i+5].decode('utf-8')
        old_water_price = old_data[name]['water_price']
        if today not in old_water_price:
            old_water_price[today] = new_data[i+4].decode('utf-8')

    else:
        item = {} 
        item['name'] = name
        item['detail'] = new_data[i+1].decode('utf-8')
        item['hood'] = new_data[i+2].decode('utf-8')
        item['caliber'] = new_data[i+3].decode('utf-8')
        item['water_price'] = {}
        item['water_price'][today] = new_data[i+4].decode('utf-8')
        item['price'] = {}
        item['price'][today] = new_data[i+5].decode('utf-8')
        old_data[name] = item 
    i += 6

result = {}
result['dates'] = old_dates
result['data'] = old_data

result = json.dumps(result, ensure_ascii=False).encode('utf-8')

#print result
# write uptated data to result.json
with open(dir_path + 'result.json', 'w') as f:
    f.write(result)
f.close()
