import numpy as np
import matplotlib.pyplot as plt

# text = np.loadtxt("/Users/Maxi/Desktop/atom/python/bachelor/tracking/data/reports/host_count_test.csv", dtype='str', delimiter=',', usecols=0, skiprows=1)
# b = np.loadtxt("/Users/Maxi/Desktop/atom/python/bachelor/tracking/data/reports/host_count_test.csv", delimiter=',', unpack=False, skiprows=1, usecols=1)
# x = np.arange(len(b))
# fig, ax = plt.subplots()
# ax.bar(x, b)
# ax.set_xticklabels(text, minor=False)
# plt.show()
#
#
# text = np.loadtxt("/Users/Maxi/Desktop/atom/python/bachelor/tracking/data/reports/suffix_count_test.csv", dtype='str', delimiter=',', usecols=0, skiprows=1)
# b = np.loadtxt("/Users/Maxi/Desktop/atom/python/bachelor/tracking/data/reports/suffix_count_test.csv", delimiter=',', unpack=False, skiprows=1, usecols=1)
# x = np.arange(len(b))
# fig, ax = plt.subplots()
# ax.barh(x, b)
# ax.set_yticklabels(text)
# plt.show()

text = np.loadtxt("/Users/Maxi/Desktop/atom/python/bachelor/tracking/data/reports/host_count_test.csv", dtype='str', delimiter=',', usecols=0, skiprows=1)
b = np.loadtxt("/Users/Maxi/Desktop/atom/python/bachelor/tracking/data/reports/host_count_test.csv", delimiter=',', unpack=False, skiprows=1, usecols=1)
x = np.arange(len(b))
# fig, ax = plt.subplots()
plt.pie(b, labels=text, startangle=90, autopct="%1.1f%%")
plt.title("Hosts")
plt.show()


text = np.loadtxt("/Users/Maxi/Desktop/atom/python/bachelor/tracking/data/reports/suffix_count_test.csv", dtype='str', delimiter=',', usecols=0, skiprows=1)
b = np.loadtxt("/Users/Maxi/Desktop/atom/python/bachelor/tracking/data/reports/suffix_count_test.csv", delimiter=',', unpack=False, skiprows=1, usecols=1)
x = np.arange(len(b))
# fig, ax = plt.subplots()
plt.pie(b, labels=text, startangle=90, autopct="%1.1f%%")
plt.title("Suffixes")
plt.show()
