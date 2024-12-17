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

# Define path to pdf
pdf_path      = os.path.join(out_path, 'rate.pdf')

# Initialise pdf
pdf           = PdfPages(pdf_path)

info_paths = [
            ('TLV0/Run0/scp-bot-0_info.txt', 1000),
            ('TLV1/Run7/scope-1-run7_info.txt', 1000),
            ('TLV1/Run8/scope-1-run8_info.txt', 1000),
            ('TLV1/Run9/scope-1-run9_info.txt', 1000),
            ('TLV1/Run10/scope-1-run10_info.txt', 1000),
            ('TLV1/Run11/scope-1-run11_info.txt', 1000),
            ('TLV1/Run12/scope-1-run12_info.txt', 1000),
            ('TLV1/Run13/scope-1-run13_info.txt', 1000),
            ('TLV1/Run14/scope-1-run14_info.txt', 1000),
            ('TLV1/Run15/scope-1-run15_info.txt', 1000),
            ('TLV1/Run16/scope-1-run16_info.txt', 1000),
            ('VS0/Run0/scope-1-run0_info.txt', 631),
            ('VS0/Run1/scope-1-run1_info.txt', 1000),
            ('VS1/Run3/scope-1-run3_info.txt', 725),
            ('VS1/Run4/scope-1-run4_info.txt', 743),
            ('VS1/Run5/scope-1-run5_info.txt', 690),
            ('VS1/Run6/scope-1-run6_info.txt', 918)
        ]


def dec_exp(x, A, t):
    return A * np.exp(-x/t)

fig, ((ax1,ax2), (ax3,ax4)) = plt.subplots(nrows=2,ncols=2, figsize=(8,6))

bins_tlv = np.arange(0, 0.2, 0.008)
bins_vs  = np.arange(0, 1000, 40)

# TLV0 char_time
file_path      = info_paths[0][0]
info_path      = os.path.join(lcd_path, file_path)
segs           = info_paths[0][1]
timestamps     = fn.get_timestamps(info_path, segs)
diff = np.diff(timestamps)


n, bin_edges, patches = ax1.hist(diff, bins=bins_tlv, edgecolor='black', density=True)
x_mid = bin_edges[:-1] + np.diff(bin_edges)/2

popt, pcov = scipy.optimize.curve_fit(dec_exp, x_mid, n, p0=[10, 0.025])
ax1.scatter(x_mid, n, color='black')
ax1.plot(x_mid, dec_exp(x_mid, *popt), color = 'black', label = rf'$\tau = $ {np.round(popt[1],4)} sec')

ax1.legend()

# TLV1 char_time
TLV1_diffs = []
for i in range(1, 11):
    file_path      = info_paths[i][0]
    info_path      = os.path.join(lcd_path, file_path)
    segs           = info_paths[i][1]
    timestamps     = fn.get_timestamps(info_path, segs)
    diff = np.diff(timestamps)
    TLV1_diffs.append(diff)

TLV1_diffs = np.array(TLV1_diffs).flatten()

n, bin_edges, patches = ax2.hist(TLV1_diffs, bins=bins_tlv, edgecolor='black', density=True)
x_mid = bin_edges[:-1] + np.diff(bin_edges)/2

popt, pcov = scipy.optimize.curve_fit(dec_exp, x_mid, n, p0=[10, 0.025])
ax2.scatter(x_mid, n, color='black')
ax2.plot(x_mid, dec_exp(x_mid, *popt), color = 'black', label = rf'$\tau = $ {np.round(popt[1],4)} sec')

ax2.legend()

# VS0 char_time
VS0_diffs = []
for i in range(11, 13):
    file_path      = info_paths[i][0]
    info_path      = os.path.join(lcd_path, file_path)
    segs           = info_paths[i][1]
    timestamps     = fn.get_timestamps(info_path, segs)
    diff = np.diff(timestamps)
    VS0_diffs.append(diff)

diffs = []
for arr in VS0_diffs:
    for elm in arr:
        diffs.append(elm)

n, bin_edges,patches = ax3.hist(diffs, bins=bins_vs, edgecolor='black', density=True)
x_mid = bin_edges[:-1] + np.diff(bin_edges)/2

popt, pcov = scipy.optimize.curve_fit(dec_exp, x_mid, n, p0=[0.001, 100])
ax3.scatter(x_mid, n, color='black')
ax3.plot(x_mid, dec_exp(x_mid, *popt), color='black', label = rf'$\tau = $ {np.round(popt[1],1)} sec')

ax3.legend()

# VS1 char_time
VS1_diffs = []
for i in range(13, 17):
    file_path      = info_paths[i][0]
    info_path      = os.path.join(lcd_path, file_path)
    segs           = info_paths[i][1]
    timestamps     = fn.get_timestamps(info_path, segs)
    diff = np.diff(timestamps)
    VS0_diffs.append(diff)

diffs = []
for arr in VS0_diffs:
    for elm in arr:
        diffs.append(elm)


n, bin_edges,patches = ax4.hist(diffs, bins=bins_vs, edgecolor='black', density=True)
x_mid = bin_edges[:-1] + np.diff(bin_edges)/2

popt, pcov = scipy.optimize.curve_fit(dec_exp, x_mid, n, p0=[0.001, 100])
ax4.scatter(x_mid, n, color='black')
ax4.plot(x_mid, dec_exp(x_mid, *popt), color='black', label = rf'$\tau = $ {np.round(popt[1],1)} sec')

ax4.legend()


ax1.set_title('TLV0')
ax2.set_title('TLV1')
ax3.set_title('VS0')
ax4.set_title('VS1')

fig.supxlabel("Time Between Events [seconds]")

fig.tight_layout()

pdf.savefig()
plt.close()


pdf.close()

