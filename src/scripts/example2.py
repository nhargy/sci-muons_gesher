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
except Exception as e:
    print("Failed to import module packages. Check whether relative path to /src is correct:")
    print(src_path)
    print(e)

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
dir_path      = 'VS1/Run3'
run_path = os.path.join(lcd_path, dir_path)

# Define scope_config
scope_config  = [('scope-1-run3', 4) ,('scope-2-run3', 4)]
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

bl_mean1, bl_std1, wf1_smooth, mask1 = fn.find_baseline(wf1)
bl_mean2, bl_std2, wf2_smooth, mask2 = fn.find_baseline(wf2)

wf1_smooth = wf1_smooth - bl_mean1
wf2_smooth = wf2_smooth - bl_mean2

wf1_masked = np.ma.array(wf1_smooth, mask=mask1)
wf2_masked = np.ma.array(wf2_smooth, mask=mask2)

# Plot
fig, ax = plt.subplots(figsize=(7,4))

ax.plot(t,wf1_smooth, label=rf'Ch1')  #: {bl_mean1}$\pm${bl_std1}')
ax.plot(t,wf2_smooth, label=rf'Ch2')  #: {bl_mean2}$\pm${bl_std2}')

ax.plot(t,wf1_masked, color='green')
ax.plot(t,wf2_masked, color='lawngreen')
ax.set_title(f'{dir_path}; Segment {segment}')
ax.set_xlabel('Time [ns]')
ax.set_ylabel('Voltage [mV]')
ax.axhline(0, linewidth = 5, color = 'grey', alpha = 0.35)

#ax.set_ylim(-20,20)

fig.legend()

# Format for pdf view
fig.tight_layout()

# Save to pdf object
pdf.savefig()
plt.close()

# ==================
# Get ingress index
# ==================
"""
wf = myevent.data[2]
mask = np.zeros(len(wf))
idxs, dicts = scipy.signal.find_peaks(wf, width=5, distance=8, prominence=0.02)

fig, ax = plt.subplots(figsize=(7,4))
ax.plot(t, wf, color='red', label = 'Masked')

#ax.set_ylim(-0.1,0.2)

for num, idx in enumerate(idxs):
    lb = dicts['left_bases'][num]
    rb = dicts['right_bases'][num]
    width = dicts['widths'][num]

    c = 1.5

    if idx < int(c*width):
        left = t[0]
        left_idx = 0
    else:
        left = int(t[idx - int(c*width)])
        left_idx = idx - int(c*width)
    try:
        right = int(t[idx + int(c*width)])
        right_idx = idx + int(c*width)
    except:
        right = int(t[-1])
        right_idx = -1

    ax.axvline(t[idx], color = 'grey', linestyle = '--')
    ax.axvspan(left, right, alpha = 0.2, color = 'red')

    mask[left_idx:right_idx]=1

mask[int((len(t)/2)-1):]=1

bl_wf = np.ma.array(wf, mask=mask)
bl_mean = np.round(np.nanmean(bl_wf),5)

ax.plot(t, bl_wf, color='green', label='Baseline')

ax.set_title(f'Detected Peaks: {len(idxs)}, Baseline Mean: {bl_mean}V')
fig.legend()
fig.tight_layout()
pdf.savefig()
plt.close()

"""
# End entire script in closing pdf object so it can refresh
pdf.close()
