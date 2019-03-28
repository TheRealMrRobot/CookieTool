import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import backend as bend
# matplotlib.use("TkAgg")

ROOT_DIR = bend.CookieDatabase.ROOT_DIR
#ROOT_DIR = "/Users/Maxi/Desktop/atom/python/bachelor"
REPORT_PATH = ROOT_DIR + "/tracking/data/reports/"
plt.rcParams.update({'font.size': 18})


def makePercentage(pct, allvals):
    absolute = int(round(pct/100.*np.sum(allvals)))
    # absolute2 = round(pct/100.*np.sum(allvals))
    # print("ALLVALS: " + str(allvals))
    # print("SUM ALLVALS: " + str(np.sum(allvals)))
    # print("ABSOULUTE: " + str(absolute2))
    return "{:.1f}%\n({:d})".format(pct, absolute)


def makeVerticalPieChart(path, type, name, title):
    text = np.loadtxt("%s%s/%s_count_%s.csv" % (path, type, type, name), dtype='str', delimiter=',', usecols=0, skiprows=1)
    b = np.loadtxt("%s%s/%s_count_%s.csv" % (path, type, type, name), dtype='str', delimiter=',', usecols=1, skiprows=1)
    #print(text)

    if len(b.shape) == 0:
        print("\n\n[!] Only 1 Cookie!\n\n")
        text = [text]
        x = np.arange(1)
        b = [1]
        data = [1.0]
        plt.pie(b, labels=text, startangle=90, autopct=None)        # Option without AMOUNT
    else:
        x = np.arange(len(b))
        data = [float(num) for num in b]
        plt.pie(b, labels=text, startangle=90, autopct=lambda pct: makePercentage(pct, data))
    #print(data)

    #plt.pie(b, labels=text, startangle=90, autopct="%1.1f%%\n(%s)" % b)        # Option without AMOUNT
    plt.title(title)
    plt.show()
    # EVTL: plt.save()

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


def makeTotalBarChart(path, type, name, title):
    text = np.loadtxt("%s%s/%s_info_%s.csv" % (path, type, type, name), dtype='str', delimiter=',')
    amount = np.loadtxt("%s%s/%s_info_%s.csv" % (path, type, type, name), delimiter=',', skiprows=1)
    barlist = plt.bar(text[0], amount)
    barlist[0].set_color('b')
    barlist[1].set_color('g')
    barlist[2].set_color('y')
    barlist[3].set_color('r')
    plt.title(title)
    plt.xlabel("Type")
    plt.ylabel("Total")

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
        label = "{:.0f}".format(y_value)

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

def makeUniqueBarChart(path, type, name, title):
    text = np.loadtxt("%s%s/%s_info_%s.csv" % (path, type, type, name), dtype='str', delimiter=',')
    amount = np.loadtxt("%s%s/%s_info_%s.csv" % (path, type, type, name), delimiter=',', skiprows=1)
    barlist = plt.bar(text[0], amount)
    barlist[0].set_color('b')
    barlist[1].set_color('g')
    barlist[2].set_color('y')
    barlist[3].set_color('r')
    barlist[4].set_color('orange')
    plt.title(title)
    plt.xlabel("Type")
    plt.ylabel("Unique")

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
        label = "{:.0f}".format(y_value)

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
