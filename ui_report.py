import os
import time
import tkinter as tk
import backend as bend          # DataBase & Structure
import ui_menu as Menu
import ui_menu_data as Data
import pandas as pd


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
        backend = bend.CookieDatabase()
        self.data = backend.loadCSV("transformed", input)
        print(self.data)
        self.hosts = self.data['HOST']
        self.sliced_hosts = []
        self.sliced_suffixes = []

        for host in self.hosts:
            print("\n+Complete: " + str(host))
            self.sliced_list = str(host).split(".")
            if len(self.sliced_list) == 2:

                self.sliced_host = self.sliced_list[0]
                print("-Site: " + self.sliced_host)
                self.sliced_suffix = self.sliced_list[1]
                self.sliced_suffixes.append(self.sliced_suffix)
                print("-Suffix: " + str(self.sliced_suffix))
                self.sliced_hosts.append(self.sliced_host)
            elif len(self.sliced_list) == 3:
                self.sliced_host = self.sliced_list[1]
                print("-Site: " + self.sliced_host)
                self.sliced_suffix = self.sliced_list[2]
                self.sliced_suffixes.append(self.sliced_suffix)
                print("-Suffix: " + str(self.sliced_suffix))
                self.sliced_hosts.append(self.sliced_host)
            elif len(self.sliced_list) == 4:
                self.sliced_host = self.sliced_list[2]
                print("-Site: " + self.sliced_host)
                self.sliced_suffix = self.sliced_list[3]
                self.sliced_suffixes.append(self.sliced_suffix)
                print("-Suffix: " + str(self.sliced_suffix))
                self.sliced_hosts.append(self.sliced_host)

        print(self.sliced_hosts)
        print(self.sliced_suffixes)
            #if
        #self.host_data = pd.DataFrame()
