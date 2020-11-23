from libraries import *

def create_plot(id):
    return True


def open_xl_sheet(name = 'ex.xlsx', sheet_ind = 0):
    '''
    gets filename name - str, index of sheet in book - int
    prints test values
    returns sheet
    '''
    book = xlrd.open_workbook(name)
    sheet = book.sheet_by_index(sheet_ind)
    print(sheet.cell(1,1).value) # test cell: (x, y) x - строка, y - столбец
    print(sheet.nrows, sheet.ncols) # число строк и столбцов
    return sheet

def collect_data_from_sheet(sheet, graphic_pos = 1):
    x = []
    y = []
    i = 0
    print(sheet.cell(i+1, 1+4*(graphic_pos - 1)).value, type(sheet.cell(1, 1).value))
    print(sheet.cell(i+1, 3+4*(graphic_pos - 1)).value)
    while i < sheet.nrows-1:
        if type(sheet.cell(i+1, 3+4*(graphic_pos - 1)).value) != str:
            x.append(sheet.cell(i+1, 3+4*(graphic_pos - 1)).value)
            y.append(sheet.cell(i+1, 5+4*(graphic_pos - 1)).value)
        i+=1
    return x, y

def preparing_figure(fig_title, x_label, y_label):
    fig, ax = plt.subplots()
    font = {'fontname': 'Times New Roman'}
    ax.set_title(fig_title)

    # Подписи:
    ax.set_xlabel(x_label, **font)
    ax.set_ylabel(y_label, **font)

    # Сетка:
    ax.minorticks_on()
    ax.grid(True)
    ax.grid(which='minor', linestyle = ':')
    ax.grid(which='minor', linestyle = ':')

    # Легенда:
    #matplotlib.rcParams["legend.framealpha"] = 1


def error_on_plot(x_set, y_set, x_error = 0, y_error = 0):
    # Погрешность + точки:
    plt.errorbar(x_set, y_set, fmt='.k', ecolor='gray', xerr = x_error, yerr = y_error)
    #plt.errorbar(x, y, fmt='.k', ecolor='gray', xerr = error, yerr = error, label=u'эксп. изм.')


def fitting(x, y, deg, zero=False):
    if zero:
        def fit_poly_through_origin(x, y, n=1):
            a = x[:, np.newaxis] ** np.arange(1, n + 1)
            coeff = np.linalg.lstsq(a, y)[0]
            return np.concatenate(([0], coeff))

        z = fit_poly_through_origin(x, y, deg)

        p = np.polynomial.Polynomial(z)
    else:
        z = np.polyfit(x, y, deg)
        p = np.poly1d(z)
    return p


def interphase():
    fl = True
    while fl:
        file_name = 'ex.xlsx'

        try:
            num_sheet = 0 #number of sheet
            sheet = open_xl_sheet(file_name, num_sheet)
            fl = False
        except:
            break

    title = sheet.cell(0, 0).value
    n_graph = int(sheet.cell(1, 0).value)
    x_label = sheet.cell(2, 0).value
    y_label = sheet.cell(3, 0).value
    preparing_figure(title, x_label, y_label)
    types_of_dots = [
        '.',
        'x',
        'v',
        '>']
    for i in range(1, n_graph+1):
        x, y = collect_data_from_sheet(sheet, i)
        zero = False #FIXME - meaning must be collected from sheet
        error_on_plot(x, y, sheet.cell(1, 4+4*(i - 1)).value, sheet.cell(1, 6+4*(i - 1)).value) #FIXME - make the func work normally

        if sheet.cell(i+3, 1).value == 'y':
            deg = sheet.cell(i+3, 2).value
            

            p = fitting(x, y, deg, zero)
            print(p)
            if zero:
                xp = np.linspace(0, max(x)) #FIXME +10% to max to have padding
            else:
                xp = np.linspace(min(x), max(x)) #FIXME \pm 10% to meanings to have paddings
    
            plt.plot(xp, p(xp), label=sheet.cell(i+3, 0).value, )
        else:
            plt.plot(x, y, types_of_dots[i-1], label=sheet.cell(i+3, 0).value)

    # plotting


    plt.legend(loc='best')

    #plt.xticks([i for i in range(0, 451, 50)]) #FIXME - may be necessary
    #plt.yticks([i/1000 for i in range(0, 36, 5)])
    plt.show()
    plt.savefig('foo.png')
    plt.savefig('foo.pdf')

interphase()
'''    
z = np.polyfit(x, y, 1)
p = np.poly1d(z)
'''
'''
#plotting
xp = np.linspace(-1, 6)
plt.plot(x, y, 'x', label = r'AC режим' )
plt.plot(x, y, '.', label = r'DC режим' )
plt.legend(loc='best')

plt.show()
'''

#TODO
#zero - done
#errors
#ticks on figure
#saving figure after all