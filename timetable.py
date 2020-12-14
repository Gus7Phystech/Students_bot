import xlrd

# Constants
fl = 0 # Shows if the group found in the table

column_of_day = 0  # In the final version can be found in function find_sth
column_of_time = 1
line_of_head = 4

#Dictionary of tables

Tables = dict()

Tables['Б0'] = 'timetables\\1-kurs-osen-2020.xls'
Tables['Б0Д'] = 'timetables\\1-kurs-osen-2020-_-do.xls'

Tables['Б9'] = 'timetables\\2-kurs-osen-2020.xls'
Tables['Б9Д'] = 'timetables\\2-kurs-osen-2020-do.xls'

Tables['Б8'] = 'timetables\\3-kurs-osen-2020.xls'
Tables['Б8Д'] = 'timetables\\3-kurs-osen-2020-do.xls'

Tables['Б7'] = 'timetables\\4-kurs-osen-2020.xls'

Tables['М0'] = 'timetables\\5-kurs-osen-2020.xls'

#Dictionary of days

Day = dict()

Day['1'] = 'Понедельник'
Day['2'] = 'Вторник'
Day['3'] = 'Среда'
Day['4'] = 'Четверг'
Day['5'] = 'Пятница'
Day['6'] = 'Суббота'

#Returns value from merged cells

def unmergedValue(rowx, colx, thesheet):
    for crange in thesheet.merged_cells:
        rlo, rhi, clo, chi = crange
        if rowx in range(rlo, rhi):
            if colx in range(clo, chi):
                return thesheet.cell_value(rlo, clo)
    #if you reached this point, it's not in any merged cells
    return thesheet.cell_value(rowx, colx)


#Searches by string

def find_column_of_sth(name_of_sth, line, thesheet):
    i = -1
    cell = thesheet.cell(line, 0)
    while cell.value != name_of_sth:
        i += 1
        cell = thesheet.cell(line, i)
        if cell.value == name_of_sth:
            global fl
            fl = 1
        if i > 100:
            break
    if i == - 1:
        i = 0
    return i

#Searches by column

def find_string_of_sth(name_of_sth, column, thesheet):
    i = -1
    cell = thesheet.cell(0, column)
    while cell.value != name_of_sth:
        i += 1
        cell = thesheet.cell(i, column)
        if i > 100:
            break
    if i == - 1:
        i = 0
    return i


def start_timetable(name_of_group, name_of_day):

    list_timetable = []

    name_of_day = Day[name_of_day]

    #Define a key for Tables[]

    Key = ''
    if name_of_group[0] == 'Б' or name_of_group[0] == 'С' or name_of_group[0] == 'б' or name_of_group[0] == 'с':
        Key += 'Б'
        Key += name_of_group[4]
    elif name_of_group[0] == 'М' or name_of_group[0] == 'м':
        Key += 'М'
        Key += name_of_group[4]

    #For debug (will be deleted in the final version)
    #print(Key)
    #print(Tables[Key])

    #open files
    book = xlrd.open_workbook(Tables[Key], formatting_info = True)
    sheet = book.sheet_by_index(0)

    column_of_group = find_column_of_sth(name_of_group, line_of_head, sheet)


    if fl == 0:
        #Shows that all bad
        list_timetable.append('А все, раньше надо было...')
    else:
        #print(column_of_group)

        string_of_day = find_string_of_sth(name_of_day, 0, sheet)

        #print(string_of_day)

        cell = unmergedValue(string_of_day, column_of_day, sheet)

        list_timetable.append(name_of_day + ':')
        list_timetable.append('')

        count_classes = 0
        count_output_classes = 0
        prev_time = '' #previous time

        #Determine the count of days (if final version will be replaced by function)

        while cell == name_of_day:
            if unmergedValue(string_of_day, column_of_time, sheet) != prev_time:
                if unmergedValue(string_of_day, column_of_group, sheet) != '':
                    count_classes += 1
            prev_time = unmergedValue(string_of_day, column_of_time, sheet)
            string_of_day += 1
            cell = unmergedValue(string_of_day, column_of_day, sheet)

        string_of_day = find_string_of_sth(name_of_day, 0, sheet)
        cell = unmergedValue(string_of_day, 0, sheet)

        #Data output (if final version will be replaced by function)

        while cell == name_of_day and count_output_classes < count_classes:
            if unmergedValue(string_of_day, column_of_time, sheet) != prev_time:
                s = unmergedValue(string_of_day, column_of_time, sheet)
                s = s[:-2] + ':' + s[-2:]
                s = s[:-10] + ':' + s[-10:]
                s = s + ' - ' + unmergedValue(string_of_day, column_of_group, sheet)
                if unmergedValue(string_of_day, column_of_group, sheet) != '':
                    count_output_classes += 1
                list_timetable.append(s)
            prev_time = unmergedValue(string_of_day, column_of_time, sheet)
            string_of_day += 1
            cell = unmergedValue(string_of_day, column_of_day, sheet)

    return list_timetable