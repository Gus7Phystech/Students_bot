import xlrd

Tables = dict()

Tables['Б0'] = 'recieved\\1-kurs-osen-2020.xls'
Tables['Б0Д'] = 'recieved\\1-kurs-osen-2020-_-do.xls'

Tables['Б9'] = 'recieved\\2-kurs-osen-2020.xls'
Tables['Б9Д'] = 'recieved\\2-kurs-osen-2020-do.xls'

Tables['Б8'] = 'recieved\\3-kurs-osen-2020.xls'
Tables['Б8Д'] = 'recieved\\3-kurs-osen-2020-do.xls'

Tables['Б7'] = 'recieved\\4-kurs-osen-2020.xls'

Tables['М0'] = 'recieved\\5-kurs-osen-2020.xls'

Day = dict()

Day['1'] = 'Понедельник'
Day['2'] = 'Вторник'
Day['3'] = 'Среда'
Day['4'] = 'Четверг'
Day['5'] = 'Пятница'
Day['6'] = 'Суббота'

name_of_group = input()
name_of_day = input()
name_of_day = Day[name_of_day]

line_of_head = 4

Key = ''
if name_of_group[0] == 'Б' or name_of_group[0] == 'С' or name_of_group[0] == 'б' or name_of_group[0] == 'с':
    Key += 'Б'
    Key += name_of_group[4]
elif name_of_group[0] == 'М' or name_of_group[0] == 'м':
    Key += 'М'
    Key += name_of_group[4]

#print(Key)
#print(Tables[Key])

book = xlrd.open_workbook(Tables[Key], formatting_info = True)
sheet = book.sheet_by_index(0)
fl = 0
column_of_day = 0
column_of_time = 1

def unmergedValue(rowx, colx):
    for crange in sheet.merged_cells:
        rlo, rhi, clo, chi = crange
        if rowx in range(rlo, rhi):
            if colx in range(clo, chi):
                return sheet.cell_value(rlo, clo)
    #if you reached this point, it's not in any merged cells
    return sheet.cell_value(rowx, colx)

def find_column_of_sth(name_of_sth, line):
    i = -1
    cell = sheet.cell(line, 0)
    while cell.value != name_of_sth:
        i += 1
        cell = sheet.cell(line, i)
        if cell.value == name_of_sth:
            global fl
            fl = 1
        if i > 100:
            break
    if i == - 1:
        i = 0
    return i

def find_string_of_sth(name_of_sth, column):
    i = -1
    cell = sheet.cell(0, column)
    while cell.value != name_of_sth:
        i += 1
        cell = sheet.cell(i, column)
        if i > 100:
            break
    if i == - 1:
        i = 0
    return i


column_of_group = find_column_of_sth(name_of_group, line_of_head)

if fl == 0:
    print('А все, раньше надо было...')
else:
    pass
    #print(column_of_group)

string_of_day = find_string_of_sth(name_of_day, 0)
#print(string_of_day)
cell = unmergedValue(string_of_day, column_of_day)
print(name_of_day + ':')
print('')
count_classes = 0
count_output_classes = 0
prev_time = ''

while cell == name_of_day:
    if unmergedValue(string_of_day, column_of_time) != prev_time:
        if unmergedValue(string_of_day, column_of_group) != '':
            count_classes += 1
    prev_time = unmergedValue(string_of_day, column_of_time)
    string_of_day += 1
    cell = unmergedValue(string_of_day, column_of_day)

string_of_day = find_string_of_sth(name_of_day, 0)
cell = unmergedValue(string_of_day, 0)

while cell == name_of_day and count_output_classes < count_classes:
    if unmergedValue(string_of_day, column_of_time) != prev_time:
        s = unmergedValue(string_of_day, column_of_time)
        s = s[:-2] + ':' + s[-2:]
        s = s[:-10] + ':' + s[-10:]
        s = s + ' - ' + unmergedValue(string_of_day, column_of_group)
        if unmergedValue(string_of_day, column_of_group) != '':
            count_output_classes += 1
        print(s)
    prev_time = unmergedValue(string_of_day, column_of_time)
    string_of_day += 1
    cell = unmergedValue(string_of_day, column_of_day)