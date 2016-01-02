__author__ = 'alpiii'

import pymongo as mongo
from datetime import datetime, timedelta
from Exchange import Rate


class MongoConnector:

    def mongo_insert_rates(self, values):
        """
        Inserts the rates to MongoDB
        :param values: Array of rates
        """
        client = mongo.MongoClient()
        db = client.test
        i = 0

        for exc_day in values:
            for exc in exc_day.rates:
                db.exchangeRates.insert(
                    {
                        "excDate": datetime.strptime(exc_day.exc_date,
                                                     "%Y-%m-%d"),
                        "currCode": exc.curr_code,
                        "price": exc.price
                    }
                )
            i += 1
            print 'Inserted ' + str(i) + '/' + str(len(values))
        client.close()

    def mongo_delete_rates(self):
        """
        Removes all rates from MongoDB
        """
        client = mongo.MongoClient()
        db = client.test
        db.exchangeRates.remove({})
        print 'Deleted all documents'
        client.close()

    def mongo_get_rates(self,
                        currency_code,
                        start_date,
                        end_date,
                        number_of_days):
        """
        Reads all rates from MongoDB that suits with parameters
        :param currency_code: Currency code of rates
        :param start_date: Start date inclusive
        :param end_date: End date inclusive
        :param number_of_days: Necessary for analysis that needs older values
        :return: An array of Rate class instances sorted by date
        in ascending order.
        """
        client = mongo.MongoClient()
        db = client.test
        values = db.exchangeRates.find(
            {'currCode': currency_code,
             'excDate': {'$lte': end_date,
                         '$gte': start_date + timedelta(
                                     days=- number_of_days * 2
                                 )}}
        ).sort('excDate', mongo.ASCENDING)
        client.close()
        # creating the rate class array
        rates = []
        for value in values:
            rates.append(Rate(value['excDate'],
                              value['currCode'],
                              value['price']))
        return rates
