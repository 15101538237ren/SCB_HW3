import random
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

def simulation(n, time_step, step_length, p_step_forward, p_fall_off):
    max_distances =[]
    for i in range(1, n+1):
        loc = 0.0 #current location of motor
        t = 0.0 #current time
        while True:
            t = t + time_step # update simulation time
            r1 = random.random() # generate a random number to decide whether step forward, drop off, or stay
            if r1 < p_step_forward:
                loc = loc + step_length
            elif r1 < (p_step_forward + p_fall_off):
                break
        max_distances.append(loc)
    return max_distances

def mean_confidence_interval(data, confidence=0.95):
    n = len(data)
    mean = np.mean(data)
    std_dev = stats.sem(data)
    h = std_dev * stats.t.ppf((1 + confidence) / 2., n - 1)
    return mean-h, mean, mean+h

for n in [10, 40, 160, 320, 1000, 5000]:
    dists = np.array(simulation(n, 1./10000, 8., 1./100, 1./10000))
    lci, mean, rci = mean_confidence_interval(dists) # left and right confidence interval and mean
