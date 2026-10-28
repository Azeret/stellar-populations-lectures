"""Plot style matching the lecture slides (dark navy background, blue accent)."""
import matplotlib as mpl
import matplotlib.pyplot as plt

BG = "#1b1a2e"       # slide background
FG = "#f4f4f6"       # text / axes
BLUE = "#1e8fd5"     # main accent (the dogs)
ORANGE = "#f5a623"
PINK = "#ef5d8f"
GREEN = "#5cc8a1"
GREY = "#8a8aa3"
PALETTE = [BLUE, ORANGE, PINK, GREEN, "#b58cf0", GREY]


def use_slide_style(dark=True, scale=1.0):
    """Call once at the top of a script/notebook. dark=False gives a light version."""
    bg, fg = (BG, FG) if dark else ("white", "#1b1a2e")
    mpl.rcParams.update({
        "figure.facecolor": bg, "axes.facecolor": bg, "savefig.facecolor": bg,
        "text.color": fg, "axes.labelcolor": fg, "axes.edgecolor": fg,
        "xtick.color": fg, "ytick.color": fg, "grid.color": GREY, "grid.alpha": 0.25,
        "axes.prop_cycle": mpl.cycler(color=PALETTE),
        "font.size": 18 * scale, "axes.titlesize": 22 * scale, "axes.labelsize": 20 * scale,
        "legend.fontsize": 16 * scale, "legend.frameon": False,
        "axes.spines.top": False, "axes.spines.right": False,
        "lines.linewidth": 2.5, "figure.dpi": 100,
    })
    return bg, fg
