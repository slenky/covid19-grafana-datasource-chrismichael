from datetime import datetime
from functools import partial, reduce
from time import mktime
import json
from operator import concat, is_not
import os
import requests
import objectpath

class Covid19:

    DATA_URL = "https://covid19-server.chrismichael.now.sh/api/v1/AllReports"

    def __init__(self):
        if "ENVIRONMENT" in os.environ and os.environ["ENVIRONMENT"] == 'test':
            with open('src/example-data/allreports.min.json', 'rb') as file:
                self.data = json.load(file)
        else:
            response = requests.get(self.DATA_URL)
            all_data = response.json()
            self.data = all_data["reports"][0]["table"][0]

    def countries(self):
        table = objectpath.Tree(self.data)
        return sorted(tuple(table.execute('$.Country')))

    def metrics(self):
        metrics = list(map(lambda country: [
            country + ":TotalCases",
            country + ":NewCases",
            country + ":TotalDeaths",
            country + ":NewDeaths",
            country + ":TotalRecovered", 
            country + ":ActiveCases",
            country + ":TotalTests",
            country + ":Deaths_1M_pop",
            country + ":Tests_1M_Pop",
            country + ":TotCases_1M_Pop"
        ], self.countries()))
        return reduce(concat, metrics)

    def timeseries(self, target, from_date, to_date):
        country, group = target.split(":")
        country_data = self.data[country]
        from_date_dt, to_date_dt = self.convert_input_dates(from_date, to_date)
        series = list(map(
            lambda datapoint: self.filter_datapoint(datapoint, group, from_date_dt, to_date_dt), country_data
        ))

        return list(filter(partial(is_not, None), series))

    @staticmethod
    def filter_datapoint(datapoint, group, from_date_dt, to_date_dt):
        datapoint_dt = mktime(datetime.strptime(datapoint["date"], "%Y-%m-%d").timetuple())
        if from_date_dt <= datapoint_dt <= to_date_dt:
            try:
                return [float(datapoint[group]), int(datapoint_dt * 1000)]
            except (KeyError, TypeError):
                return [0, int(datapoint_dt * 1000)]
        else:
            return None

    @staticmethod
    def convert_input_dates(from_date, to_date):
        date_format = '%Y-%m-%dT%H:%M:%S.%fZ'
        return [
            mktime(datetime.strptime(from_date, date_format).timetuple()),
            mktime(datetime.strptime(to_date, date_format).timetuple())
        ]
