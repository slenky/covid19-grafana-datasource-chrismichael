![](https://travis-ci.com/twei55/covid19-grafana-datasource.svg?branch=master)

## Covid-19 JSON API
This repository is just a pure reimplementation of twei55's code for consuming API from [ChrisMichael](https://github.com/ChrisMichaelPerezSantiago/covid19) 
in Grafana. Data in that API is not time-serialized but useful thou :(

Visualize Covid-19 data in [Grafana](https://grafana.com/grafana/) using the [JSON Datasource plugin](https://grafana.com/grafana/plugins/simpod-json-datasource).

### API Endpoint

This API is running at [https://covid19-grafana-chrismichael.herokuapp.com/](https://covid19-grafana-michael.herokuapp.com/). Just add the API Endpoint to the URL field of your datasource to visualize the data in Grafana.

### Data

The API endpoint uses data provided by [https://github.com/ChrisMichaelPerezSantiago/covid19](https://github.com/ChrisMichaelPerezSantiago/covid19).

### Develop and run locally

#### Install dependencies

```
pipenv install --dev
```

#### Run application

```
ENVIRONMENT=development FLASK_DEBUG=true FLASK_APP=src/app pipenv run flask run
```

#### Test application

```
PYTHONPATH=src ENVIRONMENT=test pipenv run mamba src/tests
```
