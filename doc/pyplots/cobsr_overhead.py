
from matplotlib import pyplot as plt
import numpy as np
from cobs import cobs
from cobs import cobsr


def cobsr_overhead_calc(num_bytes):
    return 257./256 - (255./256)**num_bytes

def cobsr_overhead_measure(num_bytes):
    # TODO: review value
    NUM_TESTS = 10000
    overhead = 0
    for _i in xrange(NUM_TESTS):
        output = cobsr.encode(np.random.bytes(num_bytes))
        overhead += (len(output) - num_bytes)
    return overhead / float(NUM_TESTS)

def cobs_overhead_measure(num_bytes):
    # TODO: review value
    NUM_TESTS = 10000
    overhead = 0
    for _i in xrange(NUM_TESTS):
        output = cobs.encode(np.random.bytes(num_bytes))
        overhead += (len(output) - num_bytes)
    return overhead / float(NUM_TESTS)

fig = plt.figure()
ax1 = fig.add_subplot(111)

# x-range for plot
num_bytes_list = np.arange(1, 30)

# Calculate values and plot

# Measured values for COBS
#cobs_measured_overhead = [ cobs_overhead_measure(num_bytes) for num_bytes in num_bytes_list ]
#ax1.plot(num_bytes_list, cobs_measured_overhead, 'g.')

# Measured values for COBS/R
cobsr_measured_overhead = [ cobsr_overhead_measure(num_bytes) for num_bytes in num_bytes_list ]
ax1.plot(num_bytes_list, cobsr_measured_overhead, 'r.')

# Calculated values for COBS/R
cobsr_calc_overhead = [ cobsr_overhead_calc(num_bytes) for num_bytes in num_bytes_list ]
ax1.plot(num_bytes_list, cobsr_calc_overhead, 'b.')

ax1.set_xlabel('message length (bytes)')
ax1.set_xlim(min(num_bytes_list), max(num_bytes_list))

# Make the y-axis label and tick labels match the line color.
ax1.set_ylabel('encoding overhead (bytes)')
if 0:
    ax1.set_ylabel('encoding overhead (bytes)', color='b')
    for tl in ax1.get_yticklabels():
        tl.set_color('b')

plt.show()
