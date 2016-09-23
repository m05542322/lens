import openpyxl

wb = openpyxl.Workbook()

wb.get_sheet_names()

sheet = wb.active

sheet.title = 'Spam Bacon Eggs Sheet'

print wb.get_sheet_names()
