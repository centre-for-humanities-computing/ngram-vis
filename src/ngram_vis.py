#!/usr/bin/python3
"""
Time series plot with quadratic fit for Google Ngram data

"""
import os
import json
import re
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

mpl.rcParams.update(
    {'text.usetex': False, 'font.family': 'serif', 'font.serif': 'cmr10',
     'font.weight': 'bold', 'mathtext.fontset': 'cm',
     'axes.unicode_minus': False}
    )


def smooth(l, N=5):
    """
    smooting with a moving average over N steps
    """
    sum = 0
    res = list(0 for x in l)
    for i in range(0, N):
        sum = sum + l[i]
        res[i] = sum / (i + 1)
    for i in range(N, len(l)):
        sum = sum - l[i - N] + l[i]
        res[i] = sum / N
    return res


def ngram2plot(dat, begin=0):
    varnames = list(dat.keys())
    varnames.sort

    end = begin + len(dat[varnames[0]])
    yr = range(begin, end)
    for varname in varnames:
        y = smooth(dat[varname], 5)
        p = np.poly1d(np.polyfit(yr, y, 2))
        xp = np.linspace(begin, end, len(yr))
        fig, ax = plt.subplots()
        fig.set_size_inches(12, 6)
        fig.subplots_adjust(wspace=.35, hspace=.35)
        ax.plot(yr, y, '-o', color="tab:gray", linewidth=2, label=varname)
        ax.plot(xp, p(xp), '-', color="k", linewidth=3)  # , zorder = 0)
        ax.tick_params(axis='both', which='both', labelsize=15)
        ax.set_xlabel("Time", size=20)
        ax.set_ylabel(u"Frequency(%)", size=20)
        varname = re.sub(r"_", r" ", varname.lower())
        varname = varname[0].upper() + varname[1:]
        title_string = r"{}".format(varname)
        ax.set_title(title_string, size=25)
        [i.set_linewidth(1.5) for i in ax.spines.values()]
        plt.savefig(os.path.join(
            "..", "fig", re.sub(r" ", r"_", varname.lower()) + ".png"
            ), dpi=300
            )
        plt.close()


def main():
    datapath = os.path.join("..", "dat")
    fname = os.path.join(datapath, "ngrams.json")
    with open(fname, "r") as f:
        data = json.load(f)
    ngram2plot(data, begin=1950)


if __name__ == '__main__':
    main()
