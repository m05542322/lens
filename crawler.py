from HTMLParser import HTMLParser
import urllib2
import re
import datetime
import json

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
            self.table_level = self.table_level + 1
            self.table_count = self.table_count + 1
        if tag == 'td' and self.table_level == 1 and self.table_count <= 2: 
            self.td = True
            self.data = ''
        #if tag == 'a':
        #    self.a = True
    def handle_endtag(self, tag):
        if tag == 'table' and self.table_count <= 2:
            self.table_level = self.table_level - 1
        if tag == 'td' and self.table_level == 1 and self.table_count <= 2: 
            self.td = False
            if not self.data.strip():
                self.data = 'Null'
            res = re.sub(r"\s+", " ", self.data)
            self.result[self.count] = res
            self.count = self.count + 1
        #if tag == 'a':
        #    self.a = False
    def handle_data(self, data):
        #if self.td and self.table_level == 1 and self.table_count <= 2 and not self.a :
        if self.td and self.table_level == 1 and self.table_count <= 2 :
            data = data.decode('big5').encode('utf-8').strip()
            self.data = self.data + data
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
data = parser.getResult()

now = datetime.datetime.now()
today = str(now.month) + "/" + str(now.day)

result = {}
result['dates'] = ''
if result['dates']:
    result['dates'] = result['dates'] + "," + today
else:
    result['dates'] = today

result['data'] = {}
my_key = 6
while my_key < len(data) - 5: 
    item = {}
    
    name = data[my_key].replace('\xe8\xa9\xb3', '').strip()
    item['name'] = name
    item['detail'] = data[my_key+1]
    item['hood'] = data[my_key+2]
    item['caliber'] = data[my_key+3]
    item['water_price'] = {}
    item['water_price'][today] = data[my_key+4]
    item['price'] = {}
    item['price'][today] = data[my_key+5]
   
    result['data'][name] = item
    my_key = my_key + 6

#print json.dumps(result, ensure_ascii=False)

#raw_input()

with open('result.json', 'r') as f:
    input_data = f.read();   
    input_data = json.loads(input_data);
    old_dates = input_data['dates']
    old_data = input_data['data']
f.close()

print old_dates

#print json.dumps(old_data, ensure_ascii=False)

for key, value in old_data.iteritems():
    if key == 'LCA1124':
        print old_data[key]

'''
with open('result.json', 'w') as f:
    f.write(json.dumps(result, ensure_ascii=False))
f.close()
'''
