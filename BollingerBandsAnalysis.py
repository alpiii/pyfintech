__author__ = 'alpiii'

import numpy


class BollingerResult:

    def __init__(self, day, lower_band, middle_band, upper_band, real_price):
        """
        :param day: Date of value
        :param lower_band: Calculated lower band value
        :param middle_band: Calculated middle band value
        :param upper_band: Calculated upper band value
        :param real_price: Real end-day price
        """
        self.day = day
        self.lower_band = lower_band
        self.middle_band = middle_band
        self.upper_band = upper_band
        self.real_price = real_price


class BollingerBandsAnalysis:
    """
    For more detailed information about
    Bollinger Bands technical analysis method :
    https://en.wikipedia.org/wiki/Bollinger_Bands
    """

    def __init__(self, number_of_days, count_of_std, data_set, start_day):
        """
        :param number_of_days: Number of days, used in calculations
        :param count_of_std: Standard deviation count
        :param data_set: An array of rates sorted by date
        ascending order.
        :param start_day: Starting date of analysis.
        """
        self.number_of_days = number_of_days
        self.count_of_std = count_of_std
        self.data_set = data_set
        self.start_index = 0
        # Array consists of rates that is older then start day.
        # Finding the index of start day.
        while data_set[self.start_index + 1].rate_date < start_day:
            self.start_index += 1
        self.end_index = len(data_set) - 1

    def calculate_middle_band(self, prices):
        """
        Calculates the average values of prices.
        Middle band values
        :param prices: Price list
        """
        return round(numpy.average(prices), 2)

    def calculate_upper_band(self, prices, middle_band):
        """
        Calculates the upper band value
        :param prices: Price list
        :param middle_band: Middle band value
        :return: Calculated upper band value
        """
        return middle_band + (round(numpy.std(prices), 2) * self.count_of_std)

    def calculate_lower_band(self, prices, middle_band):
        """
        Calculates the lower band value
        :param prices: Price list
        :param middle_band: Middle band value
        :return: Calculated lower band value
        """
        return middle_band - (round(numpy.std(prices), 2) * self.count_of_std)

    def analyse(self):
        """
        Analyses the data for each day between start and end dates.
        :return: An array of BollingerResult class instances
        contains Bollinger result values.
        """
        i = self.start_index
        result = []
        while i <= self.end_index:
            price_list = [x.price for x in
                          self.data_set[i - self.number_of_days:i]]

            middle_band = self.calculate_middle_band(price_list)

            # creating the BollingerResult instance for each day
            result.append(BollingerResult(
                self.data_set[i].rate_date,
                self.calculate_lower_band(price_list, middle_band),
                middle_band,
                self.calculate_upper_band(price_list, middle_band),
                self.data_set[i].price))

            i += 1
        return result
