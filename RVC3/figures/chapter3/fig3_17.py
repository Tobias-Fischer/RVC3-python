import numpy as np
import matplotlib.pyplot as plt
from math import pi, sqrt
from numpy.core.shape_base import block
from numpy.lib.function_base import blackman

import sys
from spatialmath.base import *
from spatialmath.base import sym
from spatialmath import SE3, SO2, SO3, UnitQuaternion
from rvcprint import rvcprint

# load the simulation data
from imu_data import IMU
true, imu = IMU()
t = imu.t
attitude = UnitQuaternion()
for i, w in enumerate(imu.gyro[:-1]):
   attitude.append(attitude[-1] * UnitQuaternion.EulerVec(w * imu.dt))

# plt.clf()
# plt.plot(attitude.rpy())
# plt.title('naive')
# plt.figure()
# plt.plot(true.attitude.rpy())
# plt.title('true')
# plt.figure()
# plt.plot(t, attitude.angdist(true.attitude, metric=0), 'r' )
# plt.show(block=True)

kI = 0.2
kP = 1

bias = np.zeros(imu.gyro.shape)  # initial bias
attitude_ECF = UnitQuaternion()

for k, (wm, am, mm) in enumerate(zip(imu.gyro[:-1], imu.accel[:-1], imu.magno[:-1])):
   invq = attitude_ECF[-1].inv()
   sigmaR = np.cross(am, invq * true.g) + np.cross(mm, invq * true.B)
   wp = wm - bias[k,:] + kP * sigmaR
   attitude_ECF.append(attitude_ECF[k] * UnitQuaternion.EulerVec(wp * imu.dt))
   bias[k+1,:] = bias[k,:] - kI * sigmaR * imu.dt

ax = plt.subplot(211)
plt.plot(t, attitude.angdist(true.attitude), 'r' )
plt.plot(t, attitude_ECF.angdist(true.attitude), 'b')

ax.set_xlim(0, 20)
plt.ylabel('Orientation error (rad)')
plt.legend(['Simple integration', 'Explicit complementary filter'], loc='upper left')
plt.grid(True)

ax = plt.subplot(212)

plt.plot(t, bias)
ax.set_xlim(0, 20)
plt.xlabel('Time (s)')
plt.ylabel('Estimated gyro bias (rad/s)')
plt.legend(['$b_x$', '$b_y$', '$b_z$'], loc='center right')
plt.grid(True)

q1=UnitQuaternion.Rx(pi/2) 
q2=UnitQuaternion()
print(q1.angdist(q2, metric=2))

rvcprint()