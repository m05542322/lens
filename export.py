import openpyxl
import json

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

sheet.title = 'Sheet1'

row = 1
# ord('A') = 65, chr(65) = 'A'
col = 65

for date in dates:
    offset = chr(col) + str(row)
    sheet[offset] = date
    col = col + 1

wb.save('result.xlsx')
