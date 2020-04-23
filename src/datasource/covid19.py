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

    def timeseries(self, target):
        country, group = target.split(":")
        country_data = [b for b in self.data if b[0] == country]
        series = list(map(
            country_data[group]
        ))

        return list(filter(partial(is_not, None), series))
