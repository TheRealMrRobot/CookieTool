import numpy as np
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
def makeBarChart(path, type, name, title):
    text = np.loadtxt("%s%s/%s_info_%s.csv" % (path, type, type, name), dtype='str', delimiter=',')
    b = np.loadtxt("%s%s/%s_info_%s.csv" % (path, type, type, name), delimiter=',', skiprows=1)
    barlist = plt.bar(text[0], b)
    barlist[0].set_color('k')
    barlist[1].set_color('b')
    barlist[2].set_color('g')
    barlist[3].set_color('y')
    barlist[4].set_color('r')
    plt.title(title)
    plt.xlabel("Type")
    plt.ylabel("Amount")
    plt.show()

# makeBarChart(REPORT_PATH, "unique", "vm_standard04", "UNIQUE INFO")
#makePieChart()
