__author__ = 'alpiii'


class RSIResult:

    def __init__(self, day, value, price):
        """
        :param day: Date of value
        :param value: Calculated RSI value
        :param price: Real end-day price
        """
        self.day = day
        self.value = value
        self.price = price


class RSIAnalysis:
    """
    For more detailed information about
    RSI (Relative Strength Index) technical analysis method :
    https://en.wikipedia.org/wiki/Relative_strength_index
    """

    def __init__(self, number_of_days, data_set, start_day):
        """
        :param number_of_days: Number of days, used in calculations
        :param data_set: An array of rates sorted by date
        ascending order.
        :param start_day: Starting date of analysis.
        """
        self.number_of_days = number_of_days
        self.data_set = data_set
        self.start_index = 0
        # Array consists of rates that is older then start day.
        # Finding the index of start day.
        while data_set[self.start_index + 1].rate_date < start_day:
            self.start_index += 1
        self.end_index = len(data_set) - 1
        self.gains = 0
        self.loses = 0

    def calculate_averages(self, index):
        """
        Calculates the average values of gains and loses.
        :param index: Index value of the day to be analysed.
        """
        self.gains = 0
        gain_count = 0
        self.loses = 0
        lose_count = 0
        i = self.number_of_days - 1
        while i >= 0:
            # if price of today is higher and yesterday's, it is a gain
            if self.data_set[index - i].price > \
                    self.data_set[index - i - 1].price:
                self.gains = self.gains + self.data_set[index - i].price - \
                             self.data_set[index - i - 1].price
                gain_count += 1
            # if price of today is lower then yesterday's, it is a loss
            elif self.data_set[index - i].price < \
                    self.data_set[index - i - 1].price:
                self.loses = self.loses + \
                             self.data_set[index - i - 1].price - \
                             self.data_set[index - i].price
                lose_count += 1
            else:
                None
            i -= 1
        if gain_count == 0:
            self.gains = 0
        else:
            self.gains /= gain_count
        if lose_count == 0:
            self.loses = 1
        else:
            self.loses /= lose_count

    def calculate_rsi_value(self):
        """
        Calculates the RSI value of the day.
        :return: RSI Value between 0-100
        """
        return 100 - (100 / (1 + (self.gains / self.loses)))

    def analyse(self):
        """
        Analyses the data for each day between start and end dates.
        Firstly calculates averages of gains and losses.
        Then with these average values, calculating the RSI values.
        :return: An array of RSIResult class instances
        contains RSI result values.
        """
        i = self.start_index
        result = []
        while i <= self.end_index:
            self.calculate_averages(i)
            # creating the RSIResult instance for each day
            result.append(RSIResult(
                self.data_set[i].rate_date,
                self.calculate_rsi_value(),
                self.data_set[i].price))
            i += 1
        return result
