import openpyxl
import json
import collections
import os

dir_path = os.path.dirname(os.path.realpath(__file__)) + '/'

if not os.path.isfile(dir_path + 'one_day_record.json'):
    exit()

with open(dir_path + 'one_day_record.json', 'r') as f:
    input_data = f.read().decode("utf-8")
    input_data = json.loads(input_data, encoding='utf-8');
    #print json.dumps(input_data, ensure_ascii=False)
    dates = input_data['dates']
    #reverse dates make dates = ['10/17', '10/16', '10/15']
    #dates = dates[::-1]
    dates.reverse()
    data = input_data['data']
    #print json.dumps(old_dates, ensure_ascii=False)
    #print json.dumps(old_data, ensure_ascii=False)
f.close()

wb = openpyxl.Workbook()

sheet = wb.active

sheet.title = 'Canon'

# preserve two column for name and detail
col_num = len(dates) + 2

sheet['A1'] = 'Name'
sheet['B1'] = 'Detail'

row = 1
# ord('C') = 67, chr(67) = 'C'
col = 67

# header after first two column 'Name' and 'Detail'
for key, value in enumerate(dates):
    offset = chr(col+key) + str(row)
    sheet[offset] = value

row = 2
col = 65

# preserve two column for name and detail
col_num = len(dates) + 2

max_len_name = 0
max_len_detail = 0
max_len_price = 0

# body
for item in data:
    #print item
    each_data = data[item]
    for i in range(col_num):
        offset = chr(col+i) + str(row)
        if i == 0:
            sheet[offset] = each_data['name']
            max_len_name = len(each_data['name']) if len(each_data['name']) > max_len_name else max_len_name
        elif i == 1:
            sheet[offset] = each_data['detail']
            max_len_detail = len(each_data['detail']) if len(each_data['detail']) > max_len_detail else max_len_detail
        else:
            # shift left for 2 columns
            now_date = dates[i-2]
            prices = each_data['price']
            if now_date in prices:
                sheet[offset] = prices[now_date]
                max_len_price = len(prices[now_date]) if len(prices[now_date]) > max_len_price else max_len_price
            else:
                sheet[offset] = '0'
    row += 1


# adjusting column width 
for i in range(col_num):
    col_name = chr(col+i)
    if i == 0:
        sheet.column_dimensions[col_name].width = max_len_name * 1.5
    elif i == 1:
        sheet.column_dimensions[col_name].width = max_len_detail * 1.5
    else:
        sheet.column_dimensions[col_name].width = max_len_price * 1.5

wb.save(dir_path + 'one_day_change.xlsx')
