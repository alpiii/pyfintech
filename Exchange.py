__author__ = 'alpiii'


class Exchange:

    def __init__(self, exc_date, rates):
        """
        :param exc_date: Date of rates.
        :param rates: Array of rates. Consists of Rate class instances.
        """
        self.exc_date = exc_date
        self.rates = rates

    def print_all(self):
        """
        Prints all of the rate details to console
        """
        for rate in self.rates:
            print('****************' + self.exc_date + '******************')
            print 'CURRCODE : ' + rate.curr_code
            print 'PRICE : ' + str(rate.price)


class Rate:

    def __init__(self, rate_date, curr_code, price):
        """
        :param rate_date: Date of the rate
        :param curr_code: Currency code of rate value
        :param price: End-day price.
        """
        self.curr_code = curr_code
        self.price = price
        self.rate_date = rate_date
