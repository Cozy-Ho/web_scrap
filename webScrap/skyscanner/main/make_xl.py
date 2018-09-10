import openpyxl

'''
저장한 txt데이터를 날짜별로 나눠 엑셀파일로 저장하는 파일.
'result1.xlsx'와 'result2.xlsx'로 저장했다.
'''

wb = openpyxl.Workbook()
sheet = wb.get_sheet_by_name('Sheet')

result_1 = open("result_1.txt","r")

data = result_1.read().split("\n")

Row = 1
count = 1
Column =1

for i in data:
    if count % 5 == 0:
        Column = 1
        Row += 1
    else:
        sheet.cell(row=Row, column=Column).value = i
        Column += 1
    count += 1

result_1.close()
wb.save('./result1.xlsx')
