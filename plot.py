import json
import matplotlib.pyplot as plt
import numpy as np

data = {}

with open('action.log') as f:
    for l in f:
        a = json.loads(l)

        for x, y in a.items():
            if x not in data:
                data[x] = [y]
            else:
                data[x].append(y)

L, R = 0, 220000
theta = np.array(list(zip(*data['theta_smooth'])))
omega = np.array(list(zip(*data['omega'])))
action = np.array(list(zip(*data['action'])))
time = np.array(data['time'])
#plt.plot(time[L:R], theta[0][L:R], label='tx')
plt.plot(time[-100000:], theta[1][-100000:], label='ty')
#plt.plot(time[L:R], theta[2][L:R], label='tz')
#plt.plot(time[L:R], omega[1][L:R], label='tz')
plt.legend()
pl2 = plt.twinx()
pl2.plot(time[-100000:], action[0][-100000:]-action[2][-100000:], color='black', label='a2')
#pl2.legend()
plt.grid()
plt.show()
