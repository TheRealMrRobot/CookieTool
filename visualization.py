import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# matplotlib.use("TkAgg")

REPORT_PATH = "/Users/Maxi/Desktop/atom/python/bachelor/tracking/data/reports/"

def makeVerticalPieChart(path, type, name, title):
    text = np.loadtxt("%s%s/%s_count_%s.csv" % (path, type, type, name), dtype='str', delimiter=',', usecols=0, skiprows=1)
    b = np.loadtxt("%s%s/%s_count_%s.csv" % (path, type, type, name), dtype='str', delimiter=',', usecols=1, skiprows=1)
    x = np.arange(len(b))
    plt.pie(b, labels=text, startangle=90, autopct="%1.1f%%")
    plt.title(title)
    plt.show()
    # EVTL: plt.save()

# makeVerticalPieChart(REPORT_PATH, "host", "vm_standard04", "Hosts")
# makeVerticalPieChart(REPORT_PATH, "suffix", "vm_standard04", "Suffixes")
# makeVerticalPieChart(REPORT_PATH, "cook1st", "vm_standard04", "1st Party")
# makeVerticalPieChart(REPORT_PATH, "cook3rd", "vm_standard04", "3rd Party")
# makeVerticalPieChart(REPORT_PATH, "tracker", "vm_standard04", "Tracker")

#
def makeBarChart1(path, type, name, title):
    text = np.loadtxt("%s%s/%s_info_%s.csv" % (path, type, type, name), dtype='str', delimiter=',')
    amount = np.loadtxt("%s%s/%s_info_%s.csv" % (path, type, type, name), delimiter=',', skiprows=1)
    barlist = plt.bar(text[0], amount)
    barlist[0].set_color('k')
    barlist[1].set_color('b')
    barlist[2].set_color('g')
    barlist[3].set_color('y')
    barlist[4].set_color('r')
    barlist[5].set_color('orange')
    plt.title(title)
    plt.xlabel("Type")
    plt.ylabel("Amount")
    plt.show()


def makeBarChart(path, type, name, title):
    text = np.loadtxt("%s%s/%s_info_%s.csv" % (path, type, type, name), dtype='str', delimiter=',')
    amount = np.loadtxt("%s%s/%s_info_%s.csv" % (path, type, type, name), delimiter=',', skiprows=1)
    barlist = plt.bar(text[0], amount)
    barlist[0].set_color('k')
    barlist[1].set_color('b')
    barlist[2].set_color('g')
    barlist[3].set_color('y')
    barlist[4].set_color('r')
    barlist[5].set_color('orange')
    plt.title(title)
    plt.xlabel("Type")
    plt.ylabel("Amount")

    # amnt_series = pd.Series(text)
    #ax = plt.plot(kind='bar')
    # ax.set_xlabel('Amount ($)')
    # ax.set_ylabel('Frequency')
    # ax.set_xticklabels(text[0])
    # ax.title(title)

    rects = barlist.patches

    for rect in rects:
        # Get X and Y placement of label from rect.
        y_value = rect.get_height()
        x_value = rect.get_x() + rect.get_width() / 2

        # Number of points between bar and label. Change to your liking.
        space = 5
        # Vertical alignment for positive values
        va = 'bottom'

        # If value of bar is negative: Place label below bar
        if y_value < 0:
            # Invert space to place label below
            space *= -1
            # Vertically align label at top
            va = 'top'

        # Use Y value as label and format number with one decimal place
        label = "{:.1f}".format(y_value)

        # Create annotation
        plt.annotate(
            label,                      # Use `label` as label
            (x_value, y_value),         # Place label at end of the bar
            xytext=(0, space),          # Vertically shift label by `space`
            textcoords="offset points", # Interpret `xytext` as offset in points
            ha='center',                # Horizontally center label
            va=va)                      # Vertically align label differently for
                                        # positive and negative values.
    plt.show()

# makeBarChart(REPORT_PATH, "unique", "vm_standard04", "UNIQUE INFO")
#makePieChart()
