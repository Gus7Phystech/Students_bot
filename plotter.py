from libraries import *


def _to_bool(x):
    res = False
    if x == 'Y' or x == 'y':
        res = True

    return res

def open_xl_sheet(name='ex.xlsx', sheet_ind=0):
    """
    gets filename name - str, index of sheet in book - int
    prints test values
    returns sheet
    """
    book = xlrd.open_workbook(name)
    sheet = book.sheet_by_index(sheet_ind)
    return sheet


def collect_data_from_sheet(sheet, graphic_pos):
    x = []
    y = []
    approx = False
    deg = 0
    zero = False
    i = 0
    #print(sheet.cell(5 + i, graphic_pos).value)
    #print(sheet.cell(5 + i, graphic_pos + 1).value)
    while i < sheet.nrows - 6:
        if type(sheet.cell(5 + i + 1, graphic_pos).value) != str and type(sheet.cell(5 + i + 1, graphic_pos + 1).value) != str:
            x.append(sheet.cell(5 + i + 1, graphic_pos).value)
            y.append(sheet.cell(5 + i + 1, graphic_pos + 1).value)
        i += 1

    approx = _to_bool(sheet.cell(1, graphic_pos).value)
    if approx:
        deg = sheet.cell(2, graphic_pos).value
        zero = _to_bool(sheet.cell(3, graphic_pos).value)

    return x, y, approx, deg, zero


def preparing_figure(fig_title, x_label, y_label):
    fig, ax = plt.subplots()
    font = {'fontname': 'Times New Roman'}
    ax.set_title(fig_title)

    # Подписи:
    ax.set_xlabel(x_label, **font)
    ax.set_ylabel(y_label, **font)

    # Сетка:
    ax.minorticks_on()
    ax.grid(which='major', axis='both')
    ax.grid(which='minor', axis='both', linestyle=':')

    fig.set_figheight(7)
    fig.set_figwidth(10)
    # Легенда:
    # matplotlib.rcParams["legend.framealpha"] = 1
    return fig, ax


def error_on_plot(x_set, y_set, x_error=0, y_error=0):
    # Погрешность + точки:
    plt.errorbar(x_set, y_set, fmt='.k', ecolor='gray', xerr=x_error, yerr=y_error)
    # plt.errorbar(x, y, fmt='.k', ecolor='gray', xerr = error, yerr = error, label=u'эксп. изм.')


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
    print("read xlsx\n")
    types_of_dots = [
        '.',
        'o',
        'x',
        'v',
        '>'
    ]
    sheet = []
    fl = True
    while fl:
        file_name = 'example.xlsx'

        try:
            num_sheet = 0  # number of sheet
            sheet = open_xl_sheet(file_name, num_sheet)
            fl = False
        except:
            break

    print("read comm. info\n")
    title = sheet.cell(0, 1).value
    n_graph = int(sheet.cell(3, 1).value)
    x_label = sheet.cell(1, 1).value
    y_label = sheet.cell(2, 1).value
    fig, ax = preparing_figure(title, x_label, y_label)

    print("read graph info\n")
    '''
    for i in range(1, n_graph + 1):
        x, y = collect_data_from_sheet(sheet, i)
        zero = False  # FIXME - meaning must be collected from sheet
        error_on_plot(x, y, sheet.cell(1, 4 + 4 * (i - 1)).value,
                      sheet.cell(1, 6 + 4 * (i - 1)).value)  # FIXME - make the func work normally

        if sheet.cell(i + 3, 1).value == 'y':
            deg = sheet.cell(i + 3, 2).value

            p = fitting(x, y, deg, zero)
            print(p)
            if zero:
                xp = np.linspace(0, max(x))  # FIXME +10% to max to have padding
            else:
                xp = np.linspace(min(x), max(x))  # FIXME \pm 10% to meanings to have paddings

            plt.plot(xp, p(xp), label=sheet.cell(i + 3, 0).value, )
        else:
            plt.plot(x, y, types_of_dots[i - 1], label=sheet.cell(i + 3, 0).value)
    '''
    for i in range(1, n_graph + 1):
        i = 2
        j = 2 + 3 * (i - 1) + 1
        x, y, approx, deg, zero = collect_data_from_sheet(sheet, j)

        if approx:
            p = fitting(x, y, deg, zero)

            if zero:
                x_p = np.linspace(0, int(max(x) * 1.1))
            else:
                dist = max(x) - min(x)

                x_p = np.linspace(np.floor(min(x) - 0.05 * dist),
                                  np.ceil(max(x) + 0.05 * dist))

            ax.plot(x_p, p(x_p), 'r-')
        else:
            ax.plot(x, y, 'r-')

        print("plotting\n")
        # plotting
        ax.plot(x, y, 'r' + types_of_dots[1])

    # plt.legend(loc='best')

    plt.show()

    fig.savefig('foo.png', dpi=500)
    fig.savefig('foo.pdf', dpi=500)


def create_plot(src):
    return True


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

# TODO
# zero - half-done
# errors
# ticks on figure
# saving figure after all
