import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import scipy

# Get current workding directory
cwd = os.getcwd()

# Get relative path of src directory
src_path = cwd.split('/scripts')[0]

# Add relative path to system path
sys.path.insert(0, src_path)

# Import package modules
try:
    import utils.functions as fn
    from models.event import Event
except:
    print("Failed to import module packages. Check whether relative path to /src is correct:")
    print(src_path)

# Define important paths
repo_path = cwd.split('/src')[0]
lcd_path  = os.path.join(repo_path, 'lcd')
out_path  = os.path.join(repo_path, 'out')
plt_path  = os.path.join(repo_path, 'plt')


# ================
# Event analysis
# ================
"""
In the following example we will load an event just as in example1,
then do some analysis on it.
"""

# Define path to pdf
pdf_path      = os.path.join(out_path, 'example2.pdf')

# Initialise pdf
pdf           = PdfPages(pdf_path)

# Define path to specific run
dir_path      = 'Calib/Position'
run_path = os.path.join(lcd_path, dir_path)

# Define scope_config
scope_config  = [('dt-run15', 4)] #,('scope-2-run7', 4)]
"""
scope_config: each tuple specifies the scope name as given in the saved csv files
              and the corresponding number of active channels. 
"""

# Choose segment, or define it as system input
#segment       = 100
segment       = sys.argv[1]

# Define event object
myevent       = Event(run_path, segment, scope_config)

# Process event data and store in variable
myevent.get_data()
mydata = myevent.data     # waveform matrix of all channels
times  = myevent.times    # the x-axis time values, one array for each scope


# ==========
# Analysis
# ==========

t   = times[0]
wf1 = mydata[2]
wf2 = mydata[3]

min_idx = 625 # t=0ns
max_idx = 850 # t=90ns

# windowed
wf1_window = wf1[min_idx:max_idx]
wf2_window = wf2[min_idx:max_idx]

peaks1 = scipy.signal.find_peaks(wf1_window, height = 0.2, distance = 20, width = 4)[0] + min_idx
peaks2 = scipy.signal.find_peaks(wf2_window, height = 0.2, distance = 20, width = 4)[0] + min_idx

# Plot
fig, ax = plt.subplots(figsize=(7,4))

try:
    peak1 = peaks1[0]
    idx = fn.get_ingress_idx(wf1_window) + min_idx
    ax.axhline(wf1[idx], color = 'green', alpha = 0.3, linestyle = '--')
    ingress_time1 = t[idx]
    ax.axvline(t[idx], color = 'green', alpha = 0.3, linestyle = '--')
    plt.scatter(t[idx], wf1[idx], s=30, color = 'green', alpha=0.9, label = 'Ingress')
    #ax.axvline(t[peak1], color='skyblue', label = 'Peak 1')
    ax.plot(t, wf1, label='Channel 1')

except:
    ax.plot(t, wf1, label = 'Channel 1')

try:
    peak2 = peaks2[0]
    idx = fn.get_ingress_idx(wf2_window) + min_idx
    ingress_time2 = t[idx]
    ax.axhline(wf2[idx], color = 'green', alpha = 0.3, linestyle = '--')
    ax.axvline(t[idx], color = 'green', alpha = 0.3, linestyle = '--')
    plt.scatter(t[idx], wf2[idx], s=30, color = 'lawngreen', alpha=0.9, label = 'Ingress 2')
    #ax.axvline(t[peak2], color='orange', label = 'Peak 2')
    ax.plot(t, wf2, label='Channel 2')

except:
    ax.plot(t, wf2, label = 'Channel 2')

dt = np.round(ingress_time2 - ingress_time1,2)

ax.set_title(f'{dir_path}; Segment {segment}, dt: {dt}ns')
ax.set_xlabel('Time [ns]')
ax.set_ylabel('Volts')
#ax.set_xlim(0,100)
fig.legend()

# Format for pdf view
fig.tight_layout()

# Save to pdf object
pdf.savefig()
plt.close()

# ==================
# Get ingress index
# ==================
wf = myevent.data[2]
ingress_idx = fn.get_ingress_idx(wf)

"""
fig, ax = plt.subplots(figsize = (6,4))
ax.plot(times[0], wf)
ax.axvline(times[0][ingress_idx], label = 'Ingress', color = 'green', alpha = 0.5)
ax.axhline(wf[ingress_idx], color = 'green', alpha = 0.5)
ax.set_xlim(-80,80)
fig.legend()
fig.tight_layout()
pdf.savefig()
plt.close()
"""

# End entire script in closing pdf object so it can refresh
pdf.close()
