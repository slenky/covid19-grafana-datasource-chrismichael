from functools import reduce
import time
import json
from operator import concat
import os
import locale
import requests
import requests_cache
import objectpath

class Covid19:
    requests_cache.install_cache('data_cache', backend='sqlite', expire_after=360)
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
        country_index = next((index for (index, d) in enumerate(self.data) if d["Country"] == country), None)
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        series = [[locale.atoi(self.data[country_index][group]), int(time.time())]]
        return series
