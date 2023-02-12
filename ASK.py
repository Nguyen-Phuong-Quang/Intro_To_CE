import matplotlib.pyplot as plt
import numpy as np
from math import pi

# <<<<<<<<<<<<<<<<<<<< ASK Modulation and Demodulation >>>>>>>>>>>>>>>>>>>>

# ******************* Digital/Binary input information ********************

x = np.random.randint(2, size=100)
# x = [0, 0, 1, 1, 0, 1, 0, 0, 0, 1]
N = len(x)
Tb = 0.000001  # Data rate = 1MHz i.e., bit period (second)
# print('Binary Input Information at Transmitter: ');
# print(x);


# ************* Represent input information as digital signal *************
nb = 99   # Digital signal per bit
digit = []
for i in range(0, N):
    if x[i] == 1:
        sig = [1 for g in range(nb)]
    elif x[i] == 0:
        sig = [0 for g in range(nb)]
    digit.extend(sig)


t1 = np.arange(Tb/nb, nb*N*(Tb/nb) + Tb/nb, Tb/nb)   # Time period
plt.subplot(3, 1, 2)
plt.plot(t1, digit, linewidth=2)
plt.grid()
plt.axis([0, Tb*N, -0.5, 1.5])
plt.ylabel('Amplitude(volt)')
plt.xlabel('Time(sec)')
plt.title('Transmitting information as digital signal')
plt.show()

# **************************** ASK Modulation *****************************

Ac1 = 10     # Carrier amplitude for binary input '1'
Ac2 = 5      # Carrier amplitude for binary input '0'
br = 1/Tb    # Bit rate
Fc = br*10   # Carrier frequency
t2 = np.arange(Tb/nb, Tb + Tb/nb, Tb/nb)   # Signal time

cr1 = []
cr2 = []


mod = []
for i in range(0, N):
    cr1.extend(Ac1 * np.cos(2*pi*Fc*t2))
    cr2.extend(Ac2 * np.cos(2*pi*Fc*t2))

    if x[i] == 1:
        # Modulation signal with carrier signal 1
        y = Ac1 * np.cos(2*pi*Fc*t2)
    else:
        # Modulation signal with carrier signal 2
        y = Ac2 * np.cos(2*pi*Fc*t2)
    mod.extend(y)

t3 = np.arange(Tb/nb, Tb * N + Tb/nb, Tb/nb)   # Time period

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
w = np.random.normal(loc=0, scale=1, size=(N * nb))


# ********************* Received signal y *********************************

y = np.add(np.multiply(h, Ts), w)  # Convolution

# *************************** ASK Demodulation ****************************
s = len(t2)
demod = []
Ac = ((Ac1 + Ac2)/2)                      # Average of carrier amplitudes

for n in range(0, len(y), s):
    t4 = np.arange(Tb/nb, Tb + Tb/nb, Tb/nb)  # Time period
    c = np.cos(2*pi*Fc*t4)                    # Carrier signal
    mm = np.multiply(c, y[n:n+s])             # Convolution
    t5 = np.arange(Tb/nb, Tb + Tb/nb, Tb/nb)
    z = np.trapz(t5, mm)                      # Intregation
    rz = round((2*z/Tb))
    if rz > Ac:                               # Logical condition
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

print(f'Bit error probability {count_error/len(x)*100}%')
plt.show()

# ************************** End of the program ***************************
