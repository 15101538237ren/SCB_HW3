# coding: utf-8

# ### HW 1 A). Simulate a single kinesin-type motor stepping along a microtubule (MT)

import random,time, os, pickle
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


def simulation(n, time_step, step_length, p_step_forward, p_fall_off):
    max_distances = []
    for i in range(1, n + 1):
        loc = 0.0  # current location of motor
        t = 0.0  # current time
        while True:
            t = t + time_step  # update simulation time
            r1 = random.random()  # generate a random number to decide whether step forward, drop off, or stay
            if r1 < p_step_forward:
                loc = loc + step_length
            elif r1 < (p_step_forward + p_fall_off):
                break
        max_distances.append(loc)
    return max_distances

def two_moter_simulation(n_sim, time_step, step_length, p_step_forward, p_fall_off, p_rebind):
    max_distances = []
    for i in range(1, n_sim + 1):
        loc = 0.0  # current location of motor
        t = 0.0  # current time

        a_off = False # whether motor A is fall off
        b_off = False

        while True:
            t = t + time_step  # update simulation time
            r1 = random.random()  # generate a random number to decide whether motor A step forward, drop off, or stay
            if a_off and b_off:
                break
            elif a_off == False and b_off == False:
                if r1 <= 2 * p_step_forward:
                    loc = loc + step_length
                elif 2 * p_step_forward < r1 < 2 * p_step_forward + p_fall_off:
                    a_off = True
                elif  2 * p_step_forward + p_fall_off < r1 < 2 * (p_step_forward + p_fall_off):
                    b_off = True
            elif a_off:
                if r1 <= p_rebind:
                    a_off = False
                elif p_rebind < r1 < p_rebind + p_fall_off:
                    #b_off = True
                    break
            elif b_off:
                if r1 <= p_rebind:
                    b_off = False
                elif p_rebind < r1 < p_rebind + p_fall_off:
                    #a_off = True
                    break
        max_distances.append(loc)
    return max_distances


# ### HW 1 B). Simulate different numbers of trials and plot the histograms

time_step = 1./10000
step_length = 8.
p_step_forwards = [1./200, 1./400, 1./800, 1./1600] #corresponding to 800nm/sec, 400nm/sec, 200nm/sec, 100nm/sec
p_fall_off = 1./10000
p_rebind = 1./5000
n = 1000

for p_step_forward in p_step_forwards:
    dists = np.array(two_moter_simulation(n, time_step, step_length, p_step_forward, p_fall_off, p_rebind))
    mean_d = dists.mean()  # left and right confidence interval and mean
    hist = plt.hist(dists, bins=50, color='g')
    plt.axvline(x=mean_d, color='r', linewidth=2, linestyle='dashed')
    plt.title("Histogram of " + str(n))
    plt.xlabel("Max Distance")
    plt.ylabel("Number of Runs")
    plt.show()

