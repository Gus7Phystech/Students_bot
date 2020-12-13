from libraries import *


def main(stock, years=1, month=0):  # function to get data from Yahoo Finance
    '''
    :param stock: ticker
    :param years: how many years of history to find
    :param month: how many months of history to find above found years
    :return: found data, period limits
    '''
    end = dt.datetime.today().strftime('%Y-%m-%d')  # today as the end date
    start = (dt.datetime.today() - dt.timedelta(days=365*years+30*month)).strftime('%Y-%m-%d')  # 1 year ago as start
    df = data.DataReader(stock, 'yahoo', start, end)

    return df, start, end


def company_name(stock):  # function to get the company's name from the stock
    '''
    :param stock: ticker
    :return: company name
    '''
    url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(stock)  # source
    company_name = requests.get(url).json()['ResultSet']['Result'][0]['name']   # saving the name as 'company'

    return company_name


def plot(id, df, stock_name, start, end): # making a plot of the stock's dynamics
    '''
    :param id: user id
    :param df: data of the stock
    :param stock_name: ticker
    :param start: start date
    :param end: end date
    :return: current info, makes a plot
    '''

    dates = df.index.tolist() # making list of dates
    close_prices = df.Close.tolist() # saving close prices as a list
    register_matplotlib_converters() # This function modifies the global matplotlib.units.registry dictionary

    plt.plot(dates, close_prices) # adding points

    # adding titles
    plt.title(company_name(stock_name) + " c {} по {}".format(start, end))
    plt.xlabel('Date')
    plt.ylabel('Close price (USD)')

    plt.gcf().autofmt_xdate() # fitting points

    plt.savefig('files_to_send\\{}_{}.png'.format(id, stock_name)) #saving figure locally in files_to_send

    plt.close() #closing matplotlib

    # returning current price
    return str(round(close_prices[-1], 2)) + " " + "USD — цена на " + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


def moving_mean(id, df, stock_name):
    dates = df.index.tolist()  # making list of dates
    close_prices = df.Close.tolist()  # saving close prices as a list
    
    days_required = 60 # constant to account moving mean of this number
    moving_means = []
    for i in range(days_required):
        moving_means.append(np.mean(close_prices[-days_required+i-2:i-days_required]))

    register_matplotlib_converters()  # This function modifies the global matplotlib.units.registry dictionary

    plt.plot(dates[-days_required:], close_prices[-days_required:])  # adding points close price
    plt.plot(dates[-days_required:], moving_means, label='Скользящее среднее')  # adding points moving mean
    plt.legend(loc='best')

    # adding titles
    plt.title(company_name(stock_name) + " со скользящим средним")
    plt.xlabel('Date')
    plt.ylabel('USD')

    plt.gcf().autofmt_xdate()  # fitting points

    plt.savefig('files_to_send\\{}_{}_mm.png'.format(id, stock_name))  # saving figure locally in files_to_send

    plt.close()  # closing matplotlib
