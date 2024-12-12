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
    print("From system error ==> ", e)


# Define important paths
repo_path = cwd.split('/src')[0]
lcd_path  = os.path.join(repo_path, 'lcd')
out_path  = os.path.join(repo_path, 'out')
plt_path  = os.path.join(repo_path, 'plt')

# Define path to live pdf
pdf_path = os.path.join(out_path, 'find_peaks.pdf')

# Initialise pdf
pdf      = PdfPages(pdf_path)

# Define path to specific run
dir_path = 'Calib/Position'
run_path = os.path.join(lcd_path, dir_path)

# Define scope config
scope_config = [('dt-run8',4)] #,('scope-2-run4',4)]

# Choose segment
segment = sys.argv[1]

# Initialise event object
myevent = Event(run_path, segment, scope_config)

# Process event data and store in variables
myevent.get_data()
mydata = myevent.data
times  = myevent.times

# Zero baselines:
for idx, row in enumerate(mydata):
    bl = fn.find_baseline(row)[0]
    mydata[idx] = mydata[idx] - bl

# Define threshold
thresh = 120 #mV

# Define ROI
ROI = (640,880)

# Define sigma to smooth
sigma = 2

wf1 = mydata[2]
wf2 = mydata[3]

# Find first relevant peak
peak1_idx, egress_idx1 = fn.find_peak(wf1, threshold=thresh, ROI=ROI)
peak2_idx, egress_idx2 = fn.find_peak(wf2, threshold=thresh, ROI=ROI)

# Plot plate 2
fig, ax = plt.subplots(figsize=(5,2.5))

ax.plot(times[0], wf1)
if peak1_idx != None:
    ax.axvline(times[0][peak1_idx], color = 'blue', linestyle = '--', alpha = 0.75, linewidth = 1)
    ax.scatter(times[0][egress_idx1], wf1[egress_idx1], s=18, color='blue')

ax.plot(times[0], wf2)
if peak2_idx != None:
    ax.axvline(times[0][peak2_idx], color = 'orange', linestyle = '--', alpha = 0.75, linewidth = 1)
    ax.scatter(times[0][egress_idx2], wf2[egress_idx2], s=18, color='orange')

#ax.set_xlim(0,110)
#ax.set_ylim(-50,200)
ax.axvspan(times[0][ROI[0]], times[0][ROI[1]], color = 'lawngreen', alpha = 0.25)

if peak1_idx and peak2_idx != None:
    dt = np.round(times[0][peak2_idx] - times[0][peak1_idx],1)
    fig.suptitle(rf'$\Delta t = ${dt}')
else:
    fig.suptitle(r'No $\Delta t$ Available')

pdf.savefig()
plt.close()

# =======================
# END OF SCRIPT PROTOCOL
# =======================
pdf.close()
