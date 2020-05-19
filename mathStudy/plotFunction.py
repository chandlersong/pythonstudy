import matplotlib.pyplot as plt
import numpy as np

import mathStudy


def teo_function(d):
    return 2 * mathStudy.pi * mathStudy.sqrt(((1 ** 2) / (12 + d ** 2)) / 9.81 * d)


vecfunc = np.vectorize(teo_function) #关键是这个函数

d = np.arange(0.0, 100.0, 0.01)
T = vecfunc(d)
plt.plot(d, T, 'bo', d, T, 'k')
plt.show()
