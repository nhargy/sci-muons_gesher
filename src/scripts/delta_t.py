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
pdf_path = os.path.join(out_path, 'delta_t.pdf')

# Initialise pdf
pdf      = PdfPages(pdf_path)

# Define path to specific run
dir_path = 'Calib/Position'
run_path = os.path.join(lcd_path, dir_path)

thresh=120
ROI=(640,880)
sigma=2

"""
method options: 'peak', 'fwhm', 'tenperc'
"""

def get_dt(scope_config, method = 'peak'):

    seg = 1
    dt_arr = []

    while True:
        try:
            myevent = Event(run_path, seg, scope_config)
        
            # Process event data and store in variables
            myevent.get_data()
            mydata = myevent.data
            times  = myevent.times

            # Zero baselines:
            for idx, row in enumerate(mydata):
                bl = fn.find_baseline(row)[0]
                mydata[idx] = mydata[idx] - bl
    
            wf1 = mydata[2]
            wf2 = mydata[3]

            # Find first relevant peak
            peak1_idx, egress_idx1 = fn.find_peak(wf1, threshold=thresh, ROI=ROI)
            peak2_idx, egress_idx2 = fn.find_peak(wf2, threshold=thresh, ROI=ROI)

            if peak1_idx and peak2_idx != None:
                if method == 'peak':
                    dt = np.round(times[0][peak1_idx] - times[0][peak2_idx], 1)
                    dt_arr.append(dt)
                elif method == 'fwhm':
                    dt = times[0][egress_idx1] - times[0][egress_idx2]
                    dt_arr.append(dt)

            seg += 1
        except:
            break

    return dt_arr

method = 'fwhm'
"""
dt1 = get_dt([('dt-run1',4)], method = method)
dt2 = get_dt([('dt-run2',4)], method = method)
dt3 = get_dt([('dt-run3',4)], method = method)
L   = dt1+dt2+dt3
"""
dt4 = get_dt([('dt-run4',4)])
dt5 = get_dt([('dt-run5',4)])
CL  = dt4+dt5
"""

dt7 = get_dt([('dt-run7',4)], method = method)
dt8 = get_dt([('dt-run8',4)], method = method)
dt9 = get_dt([('dt-run9',4)], method = method)
C   = dt7+dt8+dt9


dt10 = get_dt([('dt-run10',4)], method = method)
dt11 = get_dt([('dt-run11',4)], method = method)
dt12 = get_dt([('dt-run12',4)], method = method)
CR   = dt10+dt11+dt12

dt13 = get_dt([('dt-run1',4)], method = method)
dt14 = get_dt([('dt-run2',4)], method = method)
dt15 = get_dt([('dt-run3',4)], method = method)
R    = dt13+dt14+dt15

fig, ax = plt.subplots(figsize=(5,2.5))

alpha=0.6
bins=np.arange(-21,21,2)
ax.hist(L, bins=bins, label='L', alpha=alpha)
ax.hist(CL, bins=bins, label='CL', alpha=alpha)
ax.hist(C, bins=bins, label='C', alpha=alpha)
ax.hist(CR, bins=bins, label='CR', alpha=alpha)
ax.hist(R, bins=bins, label='R', alpha=alpha)

ax.legend()
pdf.savefig()
plt.close()
"""

def gaussian(x, A, m, s):
    return A * np.exp(-(((x-m)**2)/(s**2)))

def linear(x, m, c):
    return m*x + c

fig, ax = plt.subplots(figsize=(5,2.5))

bins = np.arange(-21,21,2)
hist = np.histogram(CL, bins=bins)
mid_points = hist[1][:-1] + np.diff(hist[1])/2

x,y = mid_points, hist[0]
popt, pcov = scipy.optimize.curve_fit(gaussian, x, y, p0 = [100, -5, 3])
print(popt)

x_vals = np.linspace(-21,21,1000)
ax.scatter(x, y)
ax.plot(x_vals, gaussian(x_vals, *popt))
ax.set_title(rf'$\Delta t = ${np.round(popt[1],2)} $\pm$ {np.round(popt[2],2)}ns')
pdf.savefig()
plt.close()

pos = [24, 48, 72, 96, 120]
dts = [-7.17, -2.74, 0.15, 3.43, 6.99]
sigs = [2.35, 4.9, 2.51, 2.86, 2.78]

fig, ax = plt.subplots(figsize=(5,2.5))

popt, pcov = scipy.optimize.curve_fit(linear, pos, dts, p0 = [1, -10], sigma=sigs)
plt.errorbar(pos,dts, yerr=sigs, fmt='o', capsize=5)

x_vals = np.linspace(0,144, 100)
plt.plot(x_vals, linear(x_vals, *popt), color = 'skyblue')

pdf.savefig()
plt.close()

pdf.close()
