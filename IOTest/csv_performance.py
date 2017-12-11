import csv

import numpy as np
import pandas as pd
from datetime import datetime

csv_delimiter = ','


def open_with_python_csv(filename):
    '''
    https://docs.python.org/2/library/csv.html
    '''
    data = []
    with open(filename, 'rt') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=csv_delimiter, quotechar='|')
        for row in csvreader:
            data.append(row)


def open_with_pandas(filename):
    '''
    https://docs.python.org/2/library/csv.html
    '''
    data = []
    df = pd.read_csv(filename)

    for row in df.values:
        data.append(row)

def parsetime(v):
    return np.datetime64(
       datetime.strptime(v.decode("utf-8"), '%Y-%m-%d %H:%M:%S')
    )


def open_with_numpy_loadtxt(filename):
    '''
    http://stackoverflow.com/questions/4315506/load-csv-into-2d-matrix-with-numpy-for-plotting
    '''
    result = []
    data = np.loadtxt(open(filename, 'rb'), delimiter=csv_delimiter, skiprows=1,
                      dtype={'names': (
                          'Date', 'Open', 'Low', 'High', 'Close', 'Volume', 'Amount'),
                          'formats':('|S19',np.float, np.float, np.float, np.float, np.float, np.float)})
    for row in data:
        result.append(row)
    return result


def timeit_test(solution, file_name="csv_15m.csv", times=10):
    import timeit
    name = solution.__name__
    executeMethod = "{0}('{1}')".format(name, file_name)
    result = timeit.timeit(executeMethod, setup="from __main__ import {0}".format(name), number=times)
    print("{0} takes {1} per loop,loop times:{2},file:{3}".format(name, result / times, times, file_name))
    return result


if __name__ == '__main__':
    timeit_test(open_with_numpy_loadtxt)
    timeit_test(open_with_pandas)
    timeit_test(open_with_python_csv)
