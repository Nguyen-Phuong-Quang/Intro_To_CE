import matplotlib.pyplot as plt
import numpy as np
from math import pi

# <<<<<<<<<<<<<<<<<<<< FSK Modulation and Demodulation >>>>>>>>>>>>>>>>>>>>

# ******************* Digital/Binary input information ********************

x = np.random.randint(2, size=100)
# x = [0, 0, 1, 1, 0, 1, 0, 0, 0, 1]
N = len(x)
Tb = 0.000001  # Data rate = 1MHz i.e., bit period (second)
# print('Binary Input Information at Transmitter: ')
# print(x)

# ************* Represent input information as digital signal *************
nb = 99   # Digital signal per bit
digit = []
for i in range(0, N):
    if x[i] == 1:
        sig = [1 for g in range(nb)]
    elif x[i] == 0:
        sig = [0 for g in range(nb)]
    digit.extend(sig)


t1 = np.arange(0, nb*N*(Tb/nb), Tb/nb)   # Time period
plt.subplot(3, 1, 2)
plt.plot(t1, digit, linewidth=2)
plt.grid()
plt.axis([0, Tb*N, -0.5, 1.5])
plt.ylabel('Amplitude(volt)')
plt.xlabel('Time(sec)')
plt.title('Transmitting information as digital signal')
plt.show()

# **************************** FSK Modulation *****************************

Ac = 10        # Carrier amplitude for binary input
br = 1/Tb      # Bit rate
Fc1 = br*10    # Carrier frequency for binary input '1'
Fc2 = br*2    # Carrier frequency for binary input '0'
t2 = np.arange(0, Tb, Tb/nb)   # Signal time

mod = []
cr1 = []
cr2 = []
for i in range(0, N):
    cr1.extend(Ac * np.cos(2*pi*Fc1*t2))
    cr2.extend(Ac * np.cos(2*pi*Fc2*t2))
    
    if x[i] == 1:
        # Modulation signal with carrier signal 1
        y = Ac * np.cos(2*pi*Fc1*t2)
    else:
        # Modulation signal with carrier signal 2
        y = Ac * np.cos(2*pi*Fc2*t2)
    mod.extend(y)

t3 = np.arange(0, Tb * N, Tb/nb);   # Time period
plt.subplot(3, 1, 1)
plt.plot(t3, cr1)
plt.axis([0, Tb*N, -10.5, 10.5])
plt.xlabel('Time(Sec)')
plt.ylabel('Amplitude(Volts)')
plt.title('Carrier signal 1')
plt.tight_layout()

plt.subplot(3, 1, 2)
plt.plot(t3, cr2)
plt.axis([0, Tb*N, -10.5, 10.5])
plt.xlabel('Time(Sec)')
plt.ylabel('Amplitude(Volts)')
plt.title('Carrier signal 2')
plt.tight_layout()

plt.subplot(3, 1, 3)
plt.plot(t3, mod)
plt.axis([0, Tb*N, -10.5, 10.5])
plt.xlabel('Time(Sec)')
plt.ylabel('Amplitude(Volts)')
plt.title('ASK Modulated Signal')
plt.tight_layout()
plt.show()

# ********************* Transmitted signal x ******************************

Ts = mod

# ********************* Channel model h and w *****************************

h = 1   # Signal fading
w = np.random.normal(loc=0, scale=10, size=(N * nb))  # Noise

# ********************* Received signal y *********************************

y = np.add(np.multiply(h, Ts), w)  # Convolution

# *************************** FSK Demodulation ****************************
s = len(t2)
demod = []

for n in range(0, len(y), s):
    t4 = np.arange(0, Tb, Tb/nb)  # Time period
    c1 = np.cos(2*pi*Fc1*t4)      # carrier signal for binary value '1'
    c2 = np.cos(2*pi*Fc2*t4)      # carrier siignal for binary value '0'
    mc1 = np.multiply(c1, y[n:n+s])             # Convolution
    mc2 = np.multiply(c2, y[n:n+s])             # Convolution
    t5 = np.arange(0, Tb, Tb/nb)
    z1 = np.trapz(t5, mc1)                      # Intregation
    z2 = np.trapz(t5, mc2)                      # Intregation
    rz1 = round(2*z1/Tb)
    rz2 = round(2*z2/Tb)
    if rz1 < rz2:                               # Logical condition
        a = 1
    else:
        a = 0
    demod.append(a)
    

# print('Demodulated Binary Information at Receiver: ')
# print(demod)

# ********** Represent demodulated information as digital signal **********

bit = []
for n in range(0, len(demod)):
    if demod[n] == 1:
        se = [1 for i in range(nb)]
    elif demod[n] == 0:
        se = [0 for i in range(nb)]
    bit.extend(se)

t4 = np.arange(0, nb*len(demod)*(Tb/nb), Tb/nb)    # Time period
plt.subplot(3, 1, 2)
plt.plot(t4, bit, linewidth=2)
plt.grid()
plt.axis([0, Tb*len(demod), -0.5, 1.5])
plt.ylabel('Amplitude(volt)')
plt.xlabel('Time(sec)')
plt.title('Recived information as digital signal after binary ASK demodulation')
plt.tight_layout()

count_error = 0
print("Bit error at:")
for i in range(0, N):
    if x[i] != demod[i]:
        print(i + 1)
        count_error += 1

print("Bit error probability:", count_error/len(x)*100, "%")
plt.show()

# ************************** End of the program ***************************
