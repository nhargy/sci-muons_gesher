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
pdf_path = os.path.join(out_path, 't-x-calib.pdf')

# Initialise pdf
pdf      = PdfPages(pdf_path)

# Define path to specific run
dir_path = 'Calib/Position'
run_path = os.path.join(lcd_path, dir_path)

def gaussian(x, A, m, s):
    return A * np.exp(-(((x-m)**2)/(s**2)))


def get_dt_arr(scope_config, fraction):

    seg    = 1
    dt_arr = []

    while True:

        try:
            # Instantiate event
            myevent = Event(run_path, seg, scope_config)

            # Process event data and store
            myevent.get_data()
            myevent.zero_baselines()
            data = myevent.data
            
            t   = myevent.times[0]
            wf1 = data[2]
            wf2 = data[3]

            # ROI boundaries
            a = np.argmin(np.abs(t - 0))
            b = np.argmin(np.abs(t - 100))
            ROI = (a,b)

            # Get first peaks of waveforms
            threshold = 140
            p1, _ = fn.get_first_peak(wf1, threshold=threshold, ROI=ROI)
            p2, _ = fn.get_first_peak(wf2, threshold=threshold, ROI=ROI)


            if p1 and p2 != None:
                # Get risetimes
                fraction = fraction
                risetime1 = fn.get_risetime(t, wf1, p1, fraction=fraction)
                risetime2 = fn.get_risetime(t, wf2, p2, fraction=fraction)

                dt = risetime1 - risetime2
                dt_arr.append(dt)

            seg+=1

        except Exception:
            break

    return dt_arr


def get_dist(s, f, bins, p0, fraction=0.25):

    A = []
    for i in range(s, f+1):
        try:
            dt = get_dt_arr([(f'dt-run{i}', 4)], fraction=0.25)
            A.append(dt)
        except:
            A.append([])

    A = A[0] + A[1] + A[2]

    hist = np.histogram(A, bins=bins)
    mid_points = hist[1][:-1] + np.diff(hist[1])/2
    x,y = mid_points, hist[0]

    popt, pcov = scipy.optimize.curve_fit(gaussian, x, y, p0=p0)

    return popt

fig, ax = plt.subplots(figsize=(6,3))
bins = np.arange(-22.5, 22.5, 1)
x_vals = np.linspace(-15,15,200)

m_arr = []
s_arr = []

popt = get_dist(1, 3, bins, [50, -7, 2])
ax.plot(x_vals, gaussian(x_vals, *popt), label='L')
m_arr.append(popt[1]); s_arr.append(popt[2])

popt = get_dist(4, 6, bins, [50, -3, 2])
ax.plot(x_vals, gaussian(x_vals, *popt), label='CL')
m_arr.append(popt[1]); s_arr.append(popt[2])


popt = get_dist(7, 9, bins, [50, 0, 2])
ax.plot(x_vals, gaussian(x_vals, *popt), label='C')
m_arr.append(popt[1]); s_arr.append(popt[2])


popt = get_dist(10, 12, bins, [50, 3, 2])
ax.plot(x_vals, gaussian(x_vals, *popt), label = 'CR')
m_arr.append(popt[1]); s_arr.append(popt[2])


popt = get_dist(13, 15, bins, [50, 7, 2])
ax.plot(x_vals, gaussian(x_vals, *popt), label = 'R')
m_arr.append(popt[1]); s_arr.append(popt[2])

ax.legend()
ax.set_xlabel(r'$\Delta t$ [ns]')
ax.grid('on', linestyle='--', alpha=0.5)
fig.tight_layout()

pdf.savefig()
plt.close()

# =====
# Fit 
# =====

def linear(x, m, c):
    return m*x + c

pos = [24, 48, 72, 96, 120]
popt, pcov = scipy.optimize.curve_fit(linear, pos, m_arr, p0=[1, 70], sigma=s_arr)

fig, ax = plt.subplots(figsize=(6,3))
x_vals = np.linspace(0,144,100)
ax.plot(x_vals, linear(x_vals, *popt), color = 'black', label = 'Linear Fit')

labels = ['L', 'CL', 'C', 'CR', 'R']

for i in range(0,5):
    ax.errorbar(pos[i], m_arr[i], yerr=s_arr[i],fmt='o', capsize=5, capthick=3, label = labels[i])

ax.set_xlabel('Position [cm]')
ax.set_ylabel(r'$\Delta t$ [ns]')

ax.grid('on', linestyle = '--', alpha=0.5)
ax.legend()

fig.tight_layout()

pdf.savefig()
plt.close()


# =======================
# SAVE LINEAR FIT TO JSON
# =======================
json_path = os.path.join(out_path, 't-x-conv.json')
with open(json_path, 'w') as json:
    json.write('{\n')
    json.write(f'\"popt\": [{popt[0]}, {popt[1]}], \n')
    json.write(f'\"pcov\": [[{pcov[0][0]}, {pcov[0][1]}], [{pcov[1][0]}, {pcov[1][1]}]] \n')
    json.write('}')



pdf.close()

