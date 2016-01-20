__author__ = 'alpiii'


class Line:

    def __init__(self, max_price, min_price, color):
        """
        :param max_price: Max price of line
        :param min_price: Min price of line
        :param color: Increase: G (Green), Decrease: R (Red)
        """
        self.max_price = max_price
        self.min_price = min_price
        self.color = color


class ThreeLineBreakAnalysis:
    """
    For more detailed information about
    TLB (Three Line Break) technical analysis method :
    http://www.metastock.com/Customer/Resources/TAAZ/?c=3&p=108
    """

    def __init__(self, data_set, line_break_count, start_day):
        """
        :param data_set: An array of rates sorted by date ascending order.
        :param line_break_count: Day count to change color
        :param start_day: Starting date of analysis.
        """
        self.data_set = data_set
        self.start_index = 0
        self.line_break_count = line_break_count
        # Array consists of rates that is older then start day.
        # Finding the index of start day.
        while data_set[self.start_index + 1].rate_date < start_day:
            self.start_index += 1
        self.end_index = len(data_set) - 1

    def determine_first_line(self):
        """
        Determines and creates the first line of the chart.
        If start date's price is lower than previous,
        than it is a decrease (red)
        otherwise it is increase (green).
        :return: First line of the chart.
        """
        if self.data_set[self.start_index].price < \
                self.data_set[self.start_index - 1].price:
            return Line(self.data_set[self.start_index - 1].price,
                        self.data_set[self.start_index].price, 'R')
        else:
            return Line(self.data_set[self.start_index].price,
                        self.data_set[self.start_index - 1].price, 'G')
        return line

    def analyse(self):
        """
        Analyses the data for each day between start and end dates.
        :return: An array of Line class instances
        contains TLB result values.
        """
        i = self.start_index
        result = []
        # firstly finding the first line and adding it to the result list
        result.append(self.determine_first_line())
        j = 1
        control_index = 0
        while i <= self.end_index:
            # finding the index to be compared
            control_index = j - self.line_break_count
            if control_index < 0:
                control_index = 0
            if result[j - 1].color == 'R':
                if self.data_set[i].price > result[control_index].max_price:
                    # when current flow is Red, to change it to the Green
                    # new price should be higher than price of
                    # control_index's max price
                    result.append(Line(self.data_set[i].price,
                                       result[j - 1].max_price, 'G'))
                    j += 1
                elif self.data_set[i].price < result[j - 1].min_price:
                    # when current flow is Red and new price is lower than
                    # price of previous index's min price,
                    # new Red line is added
                    result.append(Line(result[j - 1].min_price,
                                       self.data_set[i].price, 'R'))
                    j += 1
                else:
                    None
            else:  # result[j - 1].color == 'G'
                if self.data_set[i].price < result[control_index].min_price:
                    # when current flow is Green, to change it to the Red
                    # new price should be lower than price of
                    # control_index's min price
                    result.append(Line(result[j - 1].min_price,
                                       self.data_set[i].price, 'R'))
                    j += 1
                elif self.data_set[i].price > result[j - 1].max_price:
                    # when current flow is Green and new price is higher than
                    # price of previous index's max price,
                    # new Green line is added
                    result.append(Line(self.data_set[i].price,
                                       result[j - 1].max_price, 'G'))
                    j += 1
                else:
                    None

            i += 1
        return result
