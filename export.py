import openpyxl
import json
import collections

with open('result.json', 'r') as f:
    input_data = f.read().decode("utf-8")
    input_data = json.loads(input_data, encoding='utf-8');
    #print json.dumps(input_data, ensure_ascii=False)
    dates = input_data['dates']
    data = input_data['data']
    #print json.dumps(old_dates, ensure_ascii=False)
    #print json.dumps(old_data, ensure_ascii=False)
f.close()

wb = openpyxl.Workbook()

sheet = wb.active

sheet.title = 'Canon'

sheet['A1'] = 'Name'
sheet['B1'] = 'Detail'

row = 1
# ord('C') = 67, chr(67) = 'C'
col = 67

# header
for date in dates:
    offset = chr(col) + str(row)
    sheet[offset] = date
    col = col + 1

row = 2
col = 65

col_num = len(dates) + 2

# body
for item in data:
    #print item
    each_data = data[item]
    for i in range(col_num):
        offset = chr(col+i) + str(row)
        if i == 0:
            sheet[offset] = each_data['name']
        elif i == 1:
            sheet[offset] = each_data['detail']
        else:
            prices = each_data['price']
            sorted_prices = collections.OrderedDict(sorted(prices.items()))
            for price_date in sorted_prices:
                if price_date in dates:
                    sheet[offset] = sorted_prices[price_date]
    
    row = row + 1
        

wb.save('result.xlsx')
