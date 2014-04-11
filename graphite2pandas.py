import pandas
import numpy
import requests
import json

""" Script to convert graphite response to Pandas DataFrame.

Author: Valentin Haenel <valentin@haenel.co>
Licence: WTFPL

Can be used to do fetch and load data for exploratory data analysis (EDA) and
for prototyping advanced algorithms on your local machine before hacking on
graphites `functions.py`.

Example
-------

>>> from graphite2pandas import g2p
>>> url = 'http://grp.example.com/render/?target=metric.data.foo&format=json&from=-31d'
>>> df = g2p(url)
>>> df.plot()

Notes
-----

* You need to request data as JSON using `format=json`
* You can specify a timezone using the `localize` parameter

"""

def _localize(index, tz):
    index = index.tz_localize('UTC')
    index = index.tz_convert('CET')
    return index

def g2p(url, localize='CET'):
    resp = requests.get(url)
    decoded_json = json.loads(resp.content)
    times, values, labels =  [], [], []
    for element in decoded_json:
        labels.append(element['target'])
        datapoints = zip(*element['datapoints'])
        values.append(datapoints[0])
        times.append(datapoints[1])
    index = pandas.DatetimeIndex((numpy.array(times[0],dtype='datetime64[s]')))
    if localize:
        index = _localize(localize)
    return pandas.DataFrame(
            dict(((labels[i], values[i]) for i in range(len(values)))),
            index=index)

