from HTMLParser import HTMLParser
import urllib2
import re
import datetime
import json

# test
# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def __init__(self):
        self.td = False
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
            #print "Encountered a start tag:", tag
    def handle_endtag(self, tag):
        if tag == 'table' and self.table_count <= 2:
            self.table_level = self.table_level - 1
        if tag == 'td' and self.table_level == 1 and self.table_count <= 2: 
            self.td = False
            if not self.data.strip():
                self.data = "Null"
            res = re.sub(r"\s+", " ", self.data)
            self.result[self.count] = res
            self.count = self.count + 1
            #print res
            #print "Encountered an end tag :", tag
    def handle_data(self, data):
        if self.td and self.table_level == 1 and self.table_count <= 2:
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
#print  html.reaid()

html = html.replace('<!######1>', '')
html = html.replace('<!######2>', '')

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
for key,value in data.iteritems(): 
    if key % 6 == 0:
        item = {}
        name = data[key]
        item['name'] = data[key]
    elif key % 6 == 1:
        item['detail'] = data[key]
    elif key % 6 == 2:
        item['hood'] = data[key]
    elif key % 6 == 3:
        item['caliber'] = data[key]
    elif key % 6 == 4:
        item['water_price'] = {}
        item['water_price'][today] = data[key]
    elif key % 6 == 5:
        item['price'] = {}
        item['price'][today] = data[key]
    result['data'][name] = item
    #raw_input()

print json.dumps(result, ensure_ascii=False)

