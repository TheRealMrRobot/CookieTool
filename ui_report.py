import os
import time
import tkinter as tk
import backend as bend          # DataBase & Structure
import ui_menu as Menu
import ui_menu_data as Data
import pandas as pd
from collections import Counter


class Report():

    H_FONT = ("Verdana", 24, 'bold')
    FONT = ("Verdana", 24)
    TT_FONT = ("Verdana", 16)
    BACKGROUND_COLOR = "palegreen"
    CONTROLLER = None

    visited_hosts = ["google",
                     "youtube",
                     "amazon",
                     "facebook",
                     "ebay",
                     "web",
                     "instagram",
                     "spiegel",
                     "t-online",
                     "bild"]

    # List of 20 known tracker from: "Measuring Personal Privacy Breaches Using Third-Party Trackers" - Shuford, Erica et al.
    known_tracker = ['doubleclick',
                     'twimg',
                     'usa',
                     'imrworldwide',
                     'scorecardresearch',
                     'facebook',
                     'atwola',
                     'advertising',
                     'adtechus',
                     'adnxs',
                     'quantserve',
                     'adsrvr',
                     'openx',
                     'videohub',
                     'stickyadstv',
                     'googleadservice',
                     'googleusercontent',
                     'ebaystatic',
                     'ebayrtm',
                     'bluekai']

    def __init__(self):
        pass


    # OPENS a new WINDOW!
    def startReporting(self, controller):
        window = self.createNewWindow(0, -50, "Reports", 800, 440)
        window.configure(background=self.BACKGROUND_COLOR)
        self.CONTROLLER = controller

        report_frame_top = tk.Frame(window)
        report_frame_mid = tk.Frame(window)
        report_frame_bot = tk.Frame(window)

        # TOP:
        self.label_fast = tk.Label(report_frame_top, text="Enter CSV name:", font=self.TT_FONT)
        self.entry_fast = tk.Entry(report_frame_top, text="", font=self.TT_FONT)
        self.button_fast = tk.Button(report_frame_top, text="Search", font=self.FONT, width=10, command=lambda: self.checkCSVFile())
        # MESSAGE LABEL:
        self.label_message = tk.Label(report_frame_mid, text="", font=self.TT_FONT)
        # REPORT:
        self.label_name = tk.Label(report_frame_bot, text="Save Report as:", font=self.TT_FONT)
        self.entry_name = tk.Entry(report_frame_bot, text="", font=self.TT_FONT)
        self.button_gen = tk.Button(report_frame_bot, text="Save", font=self.FONT, width=10, command=lambda: self.startReportCreation())


        report_frame_top.configure(background=self.BACKGROUND_COLOR)
        report_frame_mid.configure(background=self.BACKGROUND_COLOR)
        report_frame_bot.configure(background=self.BACKGROUND_COLOR)

        self.label_fast.configure(background=self.BACKGROUND_COLOR)
        self.entry_fast.configure(highlightbackground=self.BACKGROUND_COLOR)
        self.button_fast.configure(highlightbackground=self.BACKGROUND_COLOR)
        self.label_message.configure(background=self.BACKGROUND_COLOR)
        self.label_name.configure(background=self.BACKGROUND_COLOR)
        self.entry_name.configure(highlightbackground=self.BACKGROUND_COLOR)
        self.button_gen.configure(highlightbackground=self.BACKGROUND_COLOR)


        report_frame_top.pack(side=tk.TOP)
        report_frame_mid.pack()
        report_frame_bot.pack(side=tk.BOTTOM, pady=5)


        self.label_fast.pack()
        self.entry_fast.pack()
        self.button_fast.pack()
        self.label_message.pack()
        self.label_name.pack()
        self.entry_name.pack()
        self.button_gen.pack()

        self.entry_fast.bind("<Return>", self.checkCSVFile)
        self.entry_name.bind("<Return>", self.startReportCreation)


    # Generic WINDOW-CREATOR
    def createNewWindow(self, x_movement, y_movement, title, width, height):
        root = tk.Tk()
        root.title("Cookie Data - " + title)
        w = width # width for the Tk root
        h = height # height for the Tk root

        # get screen width and height
        ws = root.winfo_screenwidth() # width of the screen
        hs = root.winfo_screenheight() # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (w/2) + x_movement
        y = (hs/2) - (h/2) + y_movement

        # set the dimensions of the screen
        # and where it is placed
        root.geometry('%dx%d+%d+%d' % (w, h, x, y))

        return root


    # Should check if a CSV is existing:
    def checkCSVFile(self, event=None):
        # Check each file ->
        self.database = bend.CookieDatabase()
        self.input_name = self.entry_fast.get()


        if (self.input_name == "") == False:
            self.existing = self.database.checkExistance('transformed', self.input_name)

            if self.existing == False:
                self.label_message.configure(text="[X] ERROR! File does not exist!", fg='red')
                self.CONTROLLER.update()            # CONTROLLER is the key to THREADING!
                print("[X] ERROR! File does not exist!\n")
                self.CONTROLLER.after(1500, self.label_message.configure(text="", fg='black'))
            elif self.existing == True:
                self.label_message.configure(text="[*] CSV exists!", fg='green')
                self.CONTROLLER.update()
                print("[*] CSV exists!\n")
                self.CONTROLLER.after(1500, self.label_message.configure(text="", fg='black'))
        else:
            self.label_message.configure(text="[X] Enter CSV name first!", fg='red')
            self.CONTROLLER.update()            # CONTROLLER is the key to "THREADING"!
            print("[X] Enter CSV name first!\n")
            self.CONTROLLER.after(1500, self.label_message.configure(text="", fg='black'))


    # Should create a report for certain sites.. (DOES NOTHING at the moment)
    def startReportCreation(self, event=None):
        self.database = bend.CookieDatabase()
        self.input_name = self.entry_fast.get()
        self.output_name = self.entry_name.get()

        self.fields_valid = self.checkIfFieldsAreValid(self.input_name, self.output_name)

        if self.fields_valid:
            self.label_message.configure(text="[*] Saving report...", fg='green')
            self.CONTROLLER.update()            # CONTROLLER is the key to THREADING!
            print("[*] Saving report...\n")
            ## HERE GOES the SAVING / TRANSFORMING ? -> new method!
            self.createReport(self.input_name, self.output_name)
            self.CONTROLLER.after(200, self.label_message.configure(text="[*] Saving SUCCESSFULL!", fg='green'))
            self.CONTROLLER.update()            # CONTROLLER is the key to THREADING!
            self.CONTROLLER.after(1500, self.label_message.configure(text="", fg='black'))


    # Checks, if both fields of the REPORT-WINDOW are valid. -> If not, warnings are displayed.
    def checkIfFieldsAreValid(self, input, output):
        database = bend.CookieDatabase()

        # IF input is NOT None (-> if the user entered something):
        if (input == "") == False:
            self.existing = database.checkExistance('transformed', input)       # Is the requested CSV-DataBase (transformed from SQlite) available ?
            self.save_taken = database.checkExistance('report', output)         # Is the wished csv-name (for the report) already TAKEN (by another file) ?

            # IF SQlite DB exists and the csv-name is available (free / not taken)
            if self.existing and self.save_taken == False:
                return True
            elif self.save_taken == True:
                self.label_message.configure(text="[X] CSV already existing!", fg='red')
                self.CONTROLLER.update()
                print("[X] ERROR! CSV already existing!!\n")
                self.CONTROLLER.after(1500, self.label_message.configure(text="", fg='black'))
            elif self.existing == False:
                self.label_message.configure(text="[X] PATH not found!", fg='red')
                self.CONTROLLER.update()
                print("[X] ERROR! PATH not found!\n")
                self.CONTROLLER.after(1500, self.label_message.configure(text="", fg='black'))
        # ELSE if the user has not entered anything:
        else:
            self.label_message.configure(text="[X] Enter CSV name first!", fg='red')
            self.CONTROLLER.update()            # CONTROLLER is the key to THREADING!
            print("[X] Enter CSV name first!\n")
            self.CONTROLLER.after(1500, self.label_message.configure(text="", fg='black'))

        return False


    # Does the REAL report creation! (-> MULTIPLE FILES!)
    def createReport(self, input, output):
        backend = bend.CookieDatabase()
        self.data = backend.loadCSV("transformed", input)
        print(self.data)
        self.hosts = self.data['HOST']

        # HOST SAVING AND HANDLING:
        self.sliced_hosts = self.sliceHosts(self.hosts)         # Slice Hosts
        self.host_dict = Counter(self.sliced_hosts)             # Counts the number of occurrencies within the LIST (from unique websites)
        self.saveDict(self.host_dict, "host", output)           # Save the dist (SORTED!)
        print("\n[1] Amount of all Hosts: " + str(self.countEntries(self.sliced_hosts)))

        # GET suffix dict out of sliced_suffixes and SAVE data:
        self.sliced_suffixes = self.sliceSuffixes(self.hosts)   # Slice Suffixes
        self.suffix_dict = Counter(self.sliced_suffixes)        # Counts the number of occurrencies within the LIST (from unique websites)
        self.saveDict(self.suffix_dict, "suffix", output)       # Save the dict (SORTED!)
        print("\n[2] Amount of all Suffixes: " + str(self.countEntries(self.sliced_suffixes)))

        # GET matching "entries" from database ():
        self.cook1st = self.findMatching(self.sliced_hosts, self.visited_hosts)
        self.cook1st_dict = Counter(self.cook1st)
        print("COOK1st: ######### T E S T ##########")
        print(self.cook1st)
        self.saveDict(self.cook1st_dict, "cook1st", output)       # Save the dict (SORTED!)
        print("\n[3] Amount of all 1st Party Cookies: " + str(self.countEntries(self.cook1st)))

        # GET matching "entries" from database ():
        self.cook3rd = self.findNotMatching(self.sliced_hosts, self.visited_hosts)
        self.cook3rd_dict = Counter(self.cook3rd)
        self.saveDict(self.cook3rd_dict, "cook3rd", output)       # Save the dict (SORTED!)
        print("\n[4] Amount of all 3rd Party Cookies: " + str(self.countEntries(self.cook3rd)))

        # GET matching "entries" from database ():
        self.tracker = self.findMatching(self.sliced_hosts, self.known_tracker)
        self.tracker_dict = Counter(self.tracker)
        self.saveDict(self.tracker_dict, "tracker", output)       # Save the dict (SORTED!)
        print("\n[5] Amount of all Tracking Cookies: " + str(self.countEntries(self.tracker)))

        ####### CSV CREATION: ###############################################################################
        print("\n\n #########  [6.] FILE-Creation:  #########\n")
        # AMOUNT of all cookies (should be in Graph too!)
        self.amount_cookies = str(self.countEntries(self.sliced_hosts))



        # COUNT unique HOSTS (occurrencies)
        self.unique_hosts = self.getUniqueEntries(self.sliced_hosts)
        print("\n########### O C C U R R E N C I E S ###########")
        self.count_hosts = str(self.countEntries(self.unique_hosts))
        print("[6] Amount unique Hosts: " + self.count_hosts)
        print(self.unique_hosts)

        # COUNT unique HOSTS (occurrencies)
        self.unique_suffixes = self.getUniqueEntries(self.sliced_suffixes)
        print("\n########### O C C U R R E N C I E S ###########")
        self.count_suffixes = str(self.countEntries(self.unique_suffixes))
        print("[7] Amount unique Suffixes: " + self.count_suffixes)
        print(self.unique_suffixes)

        # COUNT unique 1st COOKIES (occurrencies)
        self.unique_cook1st = self.getUniqueEntries(self.cook1st)
        print("\n########### O C C U R R E N C I E S ###########")
        self.count_cook1st = str(self.countEntries(self.unique_cook1st))
        print("[8] Amount unique 1st Party Cookies: " + self.count_cook1st)
        print(self.unique_cook1st)

        # COUNT unique 3rd COOKIES (occurrencies)
        self.unique_cook3rd = self.getUniqueEntries(self.cook3rd)
        print("\n########### O C C U R R E N C I E S ###########")
        self.count_cook3rd = str(self.countEntries(self.unique_cook3rd))
        print("[9] Amount unique 3rd Party Cookies: " + self.count_cook3rd)
        print(self.unique_cook3rd)

        # COUNT unique TRACKER (occurrencies)
        self.unique_tracker = self.getUniqueEntries(self.tracker)
        print("\n########### O C C U R R E N C I E S ###########")
        self.count_tracker = str(self.countEntries(self.unique_tracker))
        print("[10] Amount unique Tracking Cookies: " + self.count_tracker)
        print(self.unique_tracker)

        self.saveUniqueInfoAsCSV(self.count_hosts, self.count_cook1st, self.count_cook3rd, self.count_tracker, self.count_suffixes, output)


        self.total_cookies = str(self.countEntries(self.sliced_hosts))
        print("\n### N E W ###\nTOTAL COOKIES: %s" % self.total_cookies)
        self.total_1st = str(self.countEntries(self.cook1st))
        print("\nTOTAL 1ST PARTY: %s" % self.total_1st)
        self.total_3rd = str(self.countEntries(self.cook3rd))
        print("\nTOTAL 3RD PARTY: %s" % self.total_3rd)
        self.total_tracker = str(self.countEntries(self.tracker))
        print("\nTOTAL TRACKER: %s" % self.total_tracker)

        self.saveInfoAsCSV(self.total_cookies, self.total_1st, self.total_3rd, self.total_tracker, output)

    # Slices URLS and returns only the HOST-PART:
    def sliceHosts(self, host_list):
        self.sliced_hosts = []

        for host in host_list:
            self.sliced_list = str(host).split(".")
            if len(self.sliced_list) == 2:
                self.sliced_host = self.sliced_list[0]
                self.sliced_hosts.append(self.sliced_host)
            elif len(self.sliced_list) == 3:
                self.sliced_host = self.sliced_list[1]
                self.sliced_hosts.append(self.sliced_host)
            elif len(self.sliced_list) == 4:
                self.sliced_host = self.sliced_list[2]
                self.sliced_hosts.append(self.sliced_host)
            elif len(self.sliced_list) == 5:
                self.sliced_host = self.sliced_list[3]
                self.sliced_hosts.append(self.sliced_host)

        return self.sliced_hosts


    # Slices URLS and returns only the SUFFIX-PART:
    def sliceSuffixes(self, suffix_list):
        self.sliced_suffixes = []

        for host in suffix_list:
            # print("\n+Complete: " + str(host))
            self.sliced_list = str(host).split(".")
            if len(self.sliced_list) == 2:
                self.sliced_suffix = self.sliced_list[1]
                self.sliced_suffixes.append(self.sliced_suffix)
            elif len(self.sliced_list) == 3:
                self.sliced_suffix = self.sliced_list[2]
                self.sliced_suffixes.append(self.sliced_suffix)
            elif len(self.sliced_list) == 4:
                self.sliced_suffix = self.sliced_list[3]
                self.sliced_suffixes.append(self.sliced_suffix)
            elif len(self.sliced_list) == 5:
                self.sliced_suffix = self.sliced_list[4]
                self.sliced_suffixes.append(self.sliced_suffix)

        return self.sliced_suffixes


    # Counts the number of elements in a list   ( COULD ALSO USE len(entry_list))
    def countEntries(self, entry_list):
        amount = 0

        for entry in entry_list:
            amount += 1

        return amount


    # Saves a dictionary (ordered by AMOUNT -> most is at bottom)
    def saveDict(self, dict, type, name):
        backend = bend.CookieDatabase()
        sorted_dict = {}

        if len(dict) > 1:
            # SORT the list here! -> Better for VIZUALIZATION!   (SORTING FOR >AMOUNT<)
            for value in sorted(dict.items(), key=lambda x: x[1]):
                if dict[value[0]] != "":
                    sorted_dict[value[0]] = dict[value[0]]
                else:
                    sorted_dict[value[0]] = "0"
        elif len(dict) == 1:
            for value in sorted(dict.items(), key=lambda x: x[1]):
                    sorted_dict[value[0]] = dict[value[0]]
        else:
            sorted_dict = None

        try:
            self.df = pd.DataFrame(columns=["HOST", "AMOUNT"]).from_dict(sorted_dict, orient='index').reset_index()
            self.df.to_csv(backend.REPORT_SAVE + '%s/%s_count_%s.csv' % (type, type, name), header=["HOST", "AMOUNT"], sep=',', index=False, mode='w+')
            print("[+] WROTE new %sname CSV to %s_count_%s.csv\n" % (type, type, name))
            print(self.df)
        except Exception:
            print("%s of %sdict could not be saved! -> No Cookies found in here!" % (type, name))
        #return self.df             # Only if needed -> not sure


    # RETURNS only hosts that have been visited! (ALSO multiple times! -> Neccessary for counter!)
    def findMatching(self, hosts, visited):
        self.matching = []

        for host in hosts:
            if host in visited:
                self.matching.append(host)

        return self.matching


    # RETURNS only hosts that were not directly visited (3rd Party (+ Tracker!))
    def findNotMatching(self, hosts, visited):
        self.unmatching = []

        for host in hosts:
            if host not in visited:
                self.unmatching.append(host)

        return self.unmatching


    # RETURNS only UNIQUE elements of a list (STRINGS)
    def getUniqueEntries(self, entry_list):
        self.unique_hosts = []

        for host in entry_list:
            if host not in self.unique_hosts:
                self.unique_hosts.append(host)

        return self.unique_hosts


    # GENERATES empty cols for saveDict() -> neccessary only for 1st, 3rd and Tracker -> NO tracker, no number! ( how to handle? )
    def generateSpecialInfo(self, dict):
        pass


    # SAVES the unique (count) INFO into a CSV-File!
    def saveInfoAsCSV(self, amount, cook1st, cook3rd, tracker, name):
        backend = bend.CookieDatabase()
        info_list = [amount, cook1st, cook3rd, tracker]
        info_columns = ["TOTAL", "COOKIES 1st", "COOKIES 3rd", "TRACKER"]
        self.unique_info = pd.DataFrame(columns=info_columns, index=None)
        self.unique_info.loc[0] = info_list
        self.unique_info.to_csv(backend.REPORT_SAVE + "total/total_info_%s.csv" % name, header=info_columns, sep=',', index=False, mode='w+')
        print("\n[+] WROTE new UNIQUE-INFO_CSV to total_info_%s.csv\n" % (name))
        print(self.unique_info)


    # SAVES the unique (count) INFO into a CSV-File!
    def saveUniqueInfoAsCSV(self, host, cook1st, cook3rd, tracker, suffix, name):
        backend = bend.CookieDatabase()
        info_list = [host, cook1st, cook3rd, tracker, suffix]
        info_columns = ["HOSTS", "COOKIES 1st", "COOKIES 3rd", "TRACKER", "SUFFIXES"]
        self.unique_info = pd.DataFrame(columns=info_columns, index=None)
        self.unique_info.loc[0] = info_list
        self.unique_info.to_csv(backend.REPORT_SAVE + "unique/unique_info_%s.csv" % name, header=info_columns, sep=',', index=False, mode='w+')
        print("\n[+] WROTE new UNIQUE-INFO_CSV to unique_info_%s.csv\n" % (name))
        print(self.unique_info)
