from libraries import *

def main(stock, years=1, month=0):  # function to get data from Yahoo Finance
    end = dt.datetime.today().strftime('%Y-%m-%d')  # today as the end date
    start = (dt.datetime.today() - dt.timedelta(days=365*years+30*month)).strftime('%Y-%m-%d')  # 1 year ago as start
    df = data.DataReader(stock, 'yahoo', start, end)

    return df, start, end


def company_name(stock):  # function to get the company's name from the stock
    url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(stock)  # source
    company_name = requests.get(url).json()['ResultSet']['Result'][0]['name']   # saving the name as 'company'

    return company_name


def plot(id, df, stock_name, start, end):
        dates = df.index.tolist()
        close_prices = df.Close.tolist()
        register_matplotlib_converters()

        plt.plot(dates, close_prices)
        plt.title(company_name(stock_name) + " c {} по {}".format(start, end))
        plt.xlabel('Date')
        plt.ylabel('Close price (USD)')
        plt.gcf().autofmt_xdate()

        plt.savefig('files_to_send\\{}_{}.png'.format(id, stock_name))

        plt.close()

        return str(round(close_prices[-1], 2)) + " " + "USD — цена на " + str(dates[-1])
