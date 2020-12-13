from libraries import *


def _to_bool(x):
    res = False
    if x == 'Y' or x == 'y':
        res = True

    return res


def create_plot(src='example.xlsx', user_id='123'):

    interphase(src, user_id)

    return True


def open_xl_sheet(name='example.xlsx', sheet_ind=0):
    """
    gets filename name - str, index of sheet in book - int
    prints test values
    returns sheet
    """
    book = xlrd.open_workbook(name)
    sheet = book.sheet_by_index(sheet_ind)
    return sheet


def collect_data_from_sheet(sheet, graphic_pos):
    x, y = [], []
    approx = False
    deg = 0
    zero = False
    i = 0
    x_err, y_err = 0, 0
    curve_name = 'Curve_' + str(graphic_pos // 3)
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

    x_err = float(sheet.cell(4, graphic_pos).value)
    y_err = float(sheet.cell(4, graphic_pos + 1).value)

    curve_name = sheet.cell(0, graphic_pos - 1).value

    return x, y, approx, deg, zero, x_err, y_err, curve_name


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


def interphase(name='example.xlsx', user_id='123'):
    #print("read xlsx\n")
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
        file_name = name

        try:
            num_sheet = 0  # number of sheet
            sheet = open_xl_sheet(file_name, num_sheet)
            fl = False
        except:
            break

    #print("read comm. info\n")
    title = sheet.cell(0, 1).value
    n_graph = int(sheet.cell(3, 1).value)
    x_label = sheet.cell(1, 1).value
    y_label = sheet.cell(2, 1).value
    fig, ax = preparing_figure(title, x_label, y_label)

    #print("read graph info\n")
    for i in range(1, n_graph + 1):
        #i = 1
        j = 2 + 3 * (i - 1) + 1
        x, y, approx, deg, zero, x_err, y_err, curve_name = collect_data_from_sheet(sheet, j)
        #print(curve_name)
        if approx:
            p = fitting(x, y, deg, zero)

            if zero:
                x_p = np.linspace(0, int(max(x) * 1.1))
                if n_graph == 1:
                    plt.xlim(0, int(max(x) * 1.1))
                    plt.ylim(0, p(int(max(x) * 1.1)))
            else:
                dist = max(x) - min(x)

                x_p = np.linspace(np.floor(min(x) - 0.05 * dist),
                                  np.ceil(max(x) + 0.05 * dist))
                if n_graph == 1:
                    plt.xlim(np.floor(min(x) - 0.05 * dist),
                             np.ceil(max(x) + 0.05 * dist))
                    plt.ylim(p(np.floor(min(x) - 0.05 * dist)),
                             p(np.ceil(max(x) + 0.05 * dist)))

            ax.plot(x_p, p(x_p), 'r-', label=curve_name)
        else:
            ax.plot(x, y, 'r-', label=curve_name)


        #print("plotting\n")
        # plotting
        ax.plot(x, y, 'r' + types_of_dots[1])
        ax.errorbar(x, y, xerr=x_err, yerr=y_err, fmt='.')

    plt.legend(loc='best')

    plt.show()

    fig.savefig('files_to_send\\' + str(user_id) + '.png', dpi=500)
    fig.savefig('files_to_send\\' + str(user_id) + '.pdf', dpi=500)


#create_plot()

# TODO
# zero - done
# errors
# ticks on figure
# saving figure after all - done
