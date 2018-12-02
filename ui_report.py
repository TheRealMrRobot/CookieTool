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

    def __init__(self):
        pass


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


    # Does the REAL report creation!
    def createReport(self, input, output):
        # Just for the moment (could be read from seperate file one day)
        visited_hosts = ["google", "youtube", "amazon", "facebook", "ebay", "web", "instagram", "spiegel", "t-online", "bild",]
        known_trackers = ['doubleclick',
                          'twimg',
                          'usa',
                          'imrworldwide',
                          'scoredcardresearch',
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
                          'bluekai',]

        backend = bend.CookieDatabase()
        self.data = backend.loadCSV("transformed", input)
        print(self.data)
        self.hosts = self.data['HOST']

        self.sliced_hosts = self.sliceHosts(self.hosts)
        self.sliced_suffixes = self.sliceSuffixes(self.hosts)

        # print("Amount of all Hosts: " + str(self.countEntries(self.hosts))) -> would be wrong : "HOST" is NO Host!
        print("Amount of all Hosts: " + str(self.countEntries(self.sliced_hosts)))

        # HERE COMES the stuff from website -> COUNT occurrencies!
        self.unique_hosts = self.getUniqueEntries(self.sliced_hosts)
        print(self.unique_hosts)
        print("\n########### O C C U R R E N C I E S ###########")
        print("Amount unique Hosts: " + str(self.countEntries(self.unique_hosts)))

        # HOST SAVING AND HANDLING:
        self.host_dict = Counter(self.sliced_hosts)    # Counts the number of occurrencies within the LIST (from unique websites)
        self.sorted_host_dict = {}
        # SORT the list here! -> Better for VIZUALIZATION!
        for value in sorted(self.host_dict.items(), key=lambda x: x[1]):
            self.sorted_host_dict[value[0]] = self.host_dict[value[0]]
        self.host_df = pd.DataFrame.from_dict(self.sorted_host_dict, orient='index').reset_index()
        self.host_df.to_csv(backend.REPORT_SAVE + 'host_count_%s.csv' % output, header=["HOST", "AMOUNT"], sep=',', index=False, mode='w+')
        print("[+] WROTE new hostname CSV to host_count_%s.csv" % output)
        print(self.host_df)
        # print(self.host_dict)
        # for entry in self.unique_hosts:
        #     print("%s: %i" % (entry, self.host_dict[entry]))

        # SUFFIX SAVING AND HANDLING:
        self.unique_suffixes = self.getUniqueEntries(self.sliced_suffixes)
        print(self.unique_suffixes)
        print("\n########### O C C U R R E N C I E S ###########")
        print("Amount unique Suffixes: " + str(self.countEntries(self.unique_suffixes)))
        self.suffix_dict = Counter(self.sliced_suffixes)
        self.sorted_suffix_dict = {}

        for value in sorted(self.suffix_dict.items(), key=lambda x: x[1]):
            self.sorted_suffix_dict[value[0]] = self.suffix_dict[value[0]]
        self.suffix_df = pd.DataFrame.from_dict(self.sorted_suffix_dict, orient='index').reset_index()
        self.suffix_df.to_csv(backend.REPORT_SAVE + 'suffix_count_%s.csv' % output, header=["SUFFIX", "AMOUNT"], sep=',', index=False, mode='w+')
        print("[+] WROTE new hostname CSV to suffix_count_%s.csv" % output)
        print(self.suffix_df)
        # print(self.suffix_dict)
        # for entry in self.unique_suffixes:
        #     print("%s: %i" % (entry, self.suffix_dict[entry]))




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


    # RETURNS only UNIQUE elements of a list (STRINGS)
    def getUniqueEntries(self, entry_list):
        self.unique_hosts = []

        for host in entry_list:
            if host not in self.unique_hosts:
                self.unique_hosts.append(host)

        return self.unique_hosts
