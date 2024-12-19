import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import scipy
import json
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


# ==================
# Reconstruct Event
# ==================

# Define path to pdf
pdf_path      = os.path.join(out_path, 'recon.pdf')

# Initialise pdf
pdf           = PdfPages(pdf_path)

# Define path to specific run
dir_path      = 'VS1/Run5'
vs1_run4_path = os.path.join(lcd_path, dir_path)

# Define scope_config
scope_config  = [('scope-1-run5', 4) ,('scope-2-run5', 4)]

# Choose segment, or define it as system input
#segment       = 100
segment       = sys.argv[1]

# Define event object
event       = Event(vs1_run4_path, segment, scope_config)

# Process event data and store in variable
event.get_data()
event.zero_baselines()
data = event.data     # waveform matrix of all channels
times  = event.times    # the x-axis time values, one array for each scope


ROI       = (-55,35)
threshold = 140
fraction  = 0.25


event.calc_risetime_mtx(ROI, threshold, fraction)
event.calc_pos_arr(os.path.join(out_path, 't-x-conv.json'))
rtm = event.risetime_matrix
dta = event.dt_arr
xa  = event.x_arr
dtm = event.dt_meta


colors = ['blue', 'red', 'magenta', 'green']
alpha  = 0.2

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, figsize = (8,6), sharex=True)

ax1.set_xlim(-75,75)

# Plate 1
t = times[0]

wf = data[0]
ax1.set_facecolor(colors[0]); ax1.patch.set_alpha(alpha)
ax1.plot(t, wf)
try:
    peak_idx = dtm[0][0][0]
    rt       = np.round(dtm[0][0][1],2)
    t_idx    = np.argmin(np.abs(t-rt))
    ax1.scatter(t[peak_idx], wf[peak_idx], marker = '*', color='blue', zorder=2)
    #ax1.scatter(t[t_idx], wf[t_idx], color = 'darkblue', zorder=2, label=rt)
    ax1.axvline(rt, color='blue', label=rt)
except:
    pass

wf = data[1]
ax1.plot(t, wf)
try:
    peak_idx = dtm[0][1][0]
    rt       = np.round(dtm[0][1][1],2)
    ax1.scatter(t[peak_idx], wf[peak_idx], marker = '*', color='brown', zorder=2)
    #ax1.scatter(t[t_idx], wf[t_idx], color = 'darkorange', zorder=2, label=rt)
    ax1.axvline(rt, color='brown', label=rt)
except:
    pass

ax1.legend()

# Plate 2
t = times[0]

wf = data[2]
ax2.set_facecolor(colors[1]); ax2.patch.set_alpha(alpha)
ax2.plot(t, wf)
try:
    peak_idx = dtm[1][0][0]
    rt       = np.round(dtm[1][0][1],2)
    t_idx    = np.argmin(np.abs(t-rt))
    ax2.scatter(t[peak_idx], wf[peak_idx], marker = '*', color='blue', zorder=2)
    #ax2.scatter(t[t_idx], wf[t_idx], color = 'darkblue', zorder=2, label=rt)
    ax2.axvline(rt, color='blue', label=rt)
except:
    pass

wf = data[3]
ax2.plot(t, wf)
try:
    peak_idx = dtm[1][1][0]
    rt       = np.round(dtm[1][1][1],2)
    ax2.scatter(t[peak_idx], wf[peak_idx], marker = '*', color='brown', zorder=2)
    #ax2.scatter(t[t_idx], wf[t_idx], color = 'darkorange', zorder=2, label=rt)
    ax2.axvline(rt, color='brown', label=rt)
except:
    pass

ax2.legend()

# Plate 3
t = times[1]

wf = data[4]
ax3.set_facecolor(colors[2]); ax3.patch.set_alpha(alpha)
ax3.plot(t, wf)
try:
    peak_idx = dtm[2][0][0]
    rt       = np.round(dtm[2][0][1],2)
    t_idx    = np.argmin(np.abs(t-rt))
    ax3.scatter(t[peak_idx], wf[peak_idx], marker = '*', color='blue', zorder=2)
    #ax3.scatter(t[t_idx], wf[t_idx], color = 'darkblue', zorder=2, label=rt)
    ax3.axvline(rt, color='blue', label=rt)
except:
    pass

wf = data[5]
ax3.plot(t, wf)
try:
    peak_idx = dtm[2][1][0]
    rt       = np.round(dtm[2][1][1],2)
    ax3.scatter(t[peak_idx], wf[peak_idx], marker = '*', color='brown', zorder=2)
    #ax3.scatter(t[t_idx], wf[t_idx], color = 'darkorange', zorder=2, label=rt)
    ax3.axvline(rt, color='brown', label=rt)
except:
    pass

ax3.legend()

# Plate 4
t = times[1]

wf = data[6]
ax4.set_facecolor(colors[3]); ax4.patch.set_alpha(alpha)
ax4.plot(t, wf)
try:
    peak_idx = dtm[3][0][0]
    rt       = np.round(dtm[3][0][1],2)
    t_idx    = np.argmin(np.abs(t-rt))
    ax4.scatter(t[peak_idx], wf[peak_idx], marker = '*', color='blue', zorder=2)
    #ax4.scatter(t[t_idx], wf[t_idx], color = 'darkblue', zorder=2, label=rt)
    ax4.axvline(rt, color='blue', label=rt)
except:
    pass

wf = data[7]
ax4.plot(t, wf)
try:
    peak_idx = dtm[3][1][0]
    rt       = np.round(dtm[3][1][1],2)
    ax4.scatter(t[peak_idx], wf[peak_idx], marker = '*', color='brown', zorder=2)
    #ax4.scatter(t[t_idx], wf[t_idx], color = 'darkorange', zorder=2, label=rt)
    ax4.axvline(rt, color='brown', label=rt)
except:
    pass

ax4.legend()

fig.supxlabel("Time [ns]")
fig.supylabel("Voltage [mV]")

fig.tight_layout()

pdf.savefig()
plt.close()

L = 43 #cm
s = 25 #cm

plate_pos = np.array([L*4, L*3, L*2, L*1])
xerr     = np.full(len(xa), s)
xerr = None

mask = ~np.isnan(xa)
print(mask)

x_masked = xa[mask]
print(xa, plate_pos)
y_masked = plate_pos[mask]

def linear(x, m, c):
    return m*x + c

try:
    popt, pcov = scipy.optimize.curve_fit(linear, y_masked, x_masked, sigma=xerr, p0=[-1, 100])
except:
    popt, pcov = scipy.optimize.curve_fit(linear, y_masked, x_masked, sigma=xerr, p0=[1, -100])

fig, ax = plt.subplots(figsize = (7,6))


s = 0
f = 144
w = 1
colors = ['blue', 'red', 'magenta', 'green']
xticks = [0,24,48,72,96,120,144]
yticks = [L*0, L*1, L*2, L*3, L*4]

for idx, plate in enumerate(plate_pos):
    ax.hlines(plate, xmin=-2, xmax=146, linewidth = 8, colors='black', zorder=1)
    ax.hlines(plate, xmin=0, xmax=144, linewidth = 4, colors=colors[idx], label = f'Plate {idx+1}', zorder=2)


for idx, x in enumerate(xa):
    try:
        ax.scatter(x, plate_pos[idx], color = 'darkorange', marker='x', s=200, linewidth = 8, zorder=3)
        ax.scatter(x, plate_pos[idx], color = 'yellow', marker='x', s=150, linewidth = 5, zorder=4)
    except:
        pass

height_vals = np.linspace(220, -80)
ax.plot(linear(height_vals, *popt),height_vals,linestyle='dashed',color ='black',linewidth = 3, zorder=2)

ax.set_xlim(-20,165)
ax.set_ylim(0,220)

ax.set_xticks(ticks=xticks)
ax.set_yticks(ticks=yticks)

ax.set_xlabel("Position Along Plate [cm]")
ax.set_ylabel("Height [cm]")

ax.grid('on', linestyle = '--')

ax.legend()
fig.tight_layout()

pdf.savefig()
plt.close()

pdf.close()



