import os
import glob
import re
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
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


def main():
    dat_path = os.path.join("..", "dat")
    fnames = glob.glob(os.path.join(dat_path, "*.txt"))
    fnames.sort()
    scopus2plot(fnames)


def scopus2plot(fnames, cutoff=1950):
    for fname in fnames:
        with open(fname, "r") as fobj:
            content = fobj.read()

        lst = content.split("\n")
        lst = [s for s in lst if s]
        xy = list()
        for i in range(0, len(lst), 2):
            xy.append((int(lst[i]), int(lst[i + 1])))
        xy = xy[::-1]
        x = [t[0] for t in xy]
        y = [t[1] for t in xy]

        idx = 0
        for val in x:
            if val < cutoff:
                idx = x.index(val) + 1
        if idx:
            x = x[idx:]
            y = y[idx:]

        begin = x[0]
        end = x[-1]
        y = smooth(y, 5)
        p = np.poly1d(np.polyfit(x, y, 2))
        xp = np.linspace(begin, end, len(x))
        query = os.path.basename(fname).split(".")[0].split("_")
        query = [s[0].upper()+s[1:] for s in query]
        query = " ".join(query)

        fig, ax = plt.subplots()
        fig.set_size_inches(12, 6)
        fig.subplots_adjust(wspace=.35, hspace=.35)
        ax.plot(x, y, '-o', color="tab:gray", linewidth=2)
        ax.plot(xp, p(xp), '-', color="k", linewidth=3)
        ax.tick_params(axis='both', which='both', labelsize=15)
        ax.set_xlabel("Time", size=20)
        ax.set_ylabel(u"Number of publications", size=20)
        ax.set_title(query, size=25)
        [i.set_linewidth(1.5) for i in ax.spines.values()]
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.savefig(os.path.join(
            "..", "fig", "{}_v2.png".format(re.sub(" ", "_", query.lower()))
            ), dpi=300
            )
        plt.close()


if __name__ == '__main__':
    main()
