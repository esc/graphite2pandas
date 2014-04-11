import pandas
import numpy
import requests
import json


def g2p(url):
    resp = requests.get(url)
    decoded_json = json.loads(resp.content)
    times =  []
    values = []
    labels = []
    for element in decoded_json:
        labels.append(element['target'])
        datapoints = zip(*element['datapoints'])
        values.append(datapoints[0])
        times.append(datapoints[1])
    return pandas.DataFrame(
            dict(((labels[i], values[i]) for i in range(len(values)))),
            index=(numpy.array(times[0],dtype='datetime64[s]')))

