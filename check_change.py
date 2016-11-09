#!/usr/bin/python
from HTMLParser import HTMLParser
import urllib2
import re
import datetime
import json
import os

dir_path = os.path.dirname(os.path.realpath(__file__)) + '/'

# check the file all_records.json exist or not
if os.path.isfile(dir_path + 'all_records.json'):
    with open(dir_path + 'all_records.json', 'r') as f:
        input_data = f.read().decode("utf-8")
        input_data = json.loads(input_data, encoding='utf-8');
        dates = input_data['dates']
        data = input_data['data']
    f.close()
else:
    dates = []
    data = {}


dates = dates[-2:]
new_data = data.copy()

for item in data:
    price_1 = data[item]['price'][dates[0]]
    price_2 = data[item]['price'][dates[1]]
    if price_1 == price_2:
        del new_data[item]
    #print item
    #print price_1
    #print price_2
    #print "======================================================"

if new_data:
    result = {}
    result['dates'] = dates
    result['data'] = new_data

    result = json.dumps(result, ensure_ascii=False).encode('utf-8')

    #print result
    # write uptated data to all_records.json
    with open(dir_path + 'one_day_record.json', 'w') as f:
        f.write(result)
    f.close()

