import os
import time
import tkinter as tk
import backend as bend          # DataBase & Structure
import ui_menu as Menu
import ui_menu_data as Data
import pandas as pd

# JUST a SAVE of ui_report.py -> 4 csvs could be added in window (with auto fill) !


class Compare():

    H_FONT = ("Verdana", 24, 'bold')
    FONT = ("Verdana", 24)
    TT_FONT = ("Verdana", 16)
    BACKGROUND_COLOR = "palegreen"

    def __init__(self):
        pass


    def startReporting(self):
        window = self.createNewWindow(0, -50, "Reports", 800, 440)
        window.configure(background=self.BACKGROUND_COLOR)

        report_frame_first = tk.Frame(window)
        report_frame_top = tk.Frame(window)
        report_frame_mid = tk.Frame(window)
        report_frame_bot = tk.Frame(window)
        report_frame_left_top = tk.Frame(report_frame_top)
        report_frame_right_top = tk.Frame(report_frame_top)
        report_frame_left = tk.Frame(report_frame_mid)
        report_frame_right = tk.Frame(report_frame_mid)
        report_frame_bottom = tk.Frame(report_frame_bot)

        # TOP:
        self.label_fast = tk.Label(report_frame_first, text="Standard:", font=self.TT_FONT)
        self.entry_fast = tk.Entry(report_frame_first, text="", font=self.TT_FONT)
        self.button_fast = tk.Button(report_frame_first, text="Search", font=self.FONT, width=10, command=lambda: self.autoFillEntries())
        # FIRST ENTRIES:
        self.label_stand = tk.Label(report_frame_left_top, text="Standard:", font=self.TT_FONT)
        self.entry_stand = tk.Entry(report_frame_left_top, text="", font=self.TT_FONT)
        self.label_priv = tk.Label(report_frame_right_top, text="Privacy Badger:", font=self.TT_FONT)
        self.entry_priv = tk.Entry(report_frame_right_top, text="", font=self.TT_FONT)
        # SECOND ROW:
        self.label_http = tk.Label(report_frame_left, text="HTTPs Everywhere:", font=self.TT_FONT)
        self.entry_http = tk.Entry(report_frame_left, text="", font=self.TT_FONT)
        self.label_matrix = tk.Label(report_frame_right, text="uMatrix:", font=self.TT_FONT)
        self.entry_matrix = tk.Entry(report_frame_right, text="", font=self.TT_FONT)
        # REPORT:
        self.label_name = tk.Label(report_frame_bottom, text="Report Name:", font=self.TT_FONT)
        self.entry_name = tk.Entry(report_frame_bottom, text="", font=self.TT_FONT)
        self.button_gen = tk.Button(report_frame_bottom, text="Save", font=self.FONT, width=10, command=lambda: self.createReport())


        report_frame_first.configure(background=self.BACKGROUND_COLOR)
        report_frame_top.configure(background=self.BACKGROUND_COLOR)
        report_frame_mid.configure(background=self.BACKGROUND_COLOR)
        report_frame_bot.configure(background=self.BACKGROUND_COLOR)

        report_frame_left_top.configure(background=self.BACKGROUND_COLOR)
        report_frame_right_top.configure(background=self.BACKGROUND_COLOR)
        report_frame_left.configure(background=self.BACKGROUND_COLOR)
        report_frame_right.configure(background=self.BACKGROUND_COLOR)
        report_frame_bottom.configure(background=self.BACKGROUND_COLOR)


        self.label_fast.configure(background=self.BACKGROUND_COLOR)
        self.entry_fast.configure(highlightbackground=self.BACKGROUND_COLOR)
        self.button_fast.configure(highlightbackground=self.BACKGROUND_COLOR)
        self.label_stand.configure(background=self.BACKGROUND_COLOR)
        self.entry_stand.configure(highlightbackground=self.BACKGROUND_COLOR)
        self.label_priv.configure(background=self.BACKGROUND_COLOR)
        self.entry_priv.configure(highlightbackground=self.BACKGROUND_COLOR)
        self.label_http.configure(background=self.BACKGROUND_COLOR)
        self.entry_http.configure(highlightbackground=self.BACKGROUND_COLOR)
        self.label_matrix.configure(background=self.BACKGROUND_COLOR)
        self.entry_matrix.configure(highlightbackground=self.BACKGROUND_COLOR)
        self.label_name.configure(background=self.BACKGROUND_COLOR)
        self.entry_name.configure(highlightbackground=self.BACKGROUND_COLOR)
        self.button_gen.configure(highlightbackground=self.BACKGROUND_COLOR)


        report_frame_first.pack()
        report_frame_top.pack(side=tk.TOP)
        report_frame_left_top.pack(side=tk.LEFT, pady=10)
        report_frame_right_top.pack(side=tk.RIGHT, pady=10)
        report_frame_mid.pack()
        report_frame_left.pack(side=tk.LEFT)
        report_frame_right.pack(side=tk.RIGHT)
        report_frame_bot.pack(side=tk.BOTTOM)
        report_frame_bottom.pack(side=tk.BOTTOM, pady=5)


        self.label_fast.pack()
        self.entry_fast.pack()
        self.button_fast.pack()
        self.label_stand.pack()
        self.entry_stand.pack()
        self.label_priv.pack()
        self.entry_priv.pack()
        self.label_http.pack()
        self.entry_http.pack()
        self.label_matrix.pack()
        self.entry_matrix.pack()
        self.label_name.pack()
        self.entry_name.pack()
        self.button_gen.pack()

        self.entry_fast.bind("<Return>", self.autoFillEntries)
        self.entry_name.bind("<Return>", self.createReport)



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


    # Should check if all CSVs are existing:
    def checkCSVFiles(self):
        # Check each file ->

        # Returns TRUE or FALSE
        pass


    # Handles automatic filling of entries (according to fast-entry):
    def autoFillEntries(self, event=None):
        self.entry = self.entry_fast.get()


        # if empty:
        if self.entry_stand.get() == None:
            # fill each of the 4:
            self.entry_stand.insert(tk.INSERT, "%s_standard.csv" % self.entry)
            self.entry_priv.insert(tk.INSERT, "%s_privacy.csv" % self.entry)
            self.entry_http.insert(tk.INSERT, "%s_https.csv" % self.entry)
            self.entry_matrix.insert(tk.INSERT, "%s_umatrix.csv" % self.entry)
            self.entry_name.insert(tk.INSERT, "%s_report.csv" % self.entry)

        # if full:
        else:
            # delete each of the 4:
            self.entry_stand.delete(0, tk.END)
            self.entry_priv.delete(0, tk.END)
            self.entry_http.delete(0, tk.END)
            self.entry_matrix.delete(0, tk.END)
            self.entry_name.delete(0, tk.END)
            # fill each of the 4:
            self.entry_stand.insert(tk.INSERT, "%s_standard.csv" % self.entry)
            self.entry_priv.insert(tk.INSERT, "%s_privacy.csv" % self.entry)
            self.entry_http.insert(tk.INSERT, "%s_https.csv" % self.entry)
            self.entry_matrix.insert(tk.INSERT, "%s_umatrix.csv" % self.entry)
            self.entry_name.insert(tk.INSERT, "%s_report.csv" % self.entry)


    # Should create a report for certain sites.. (DOES NOTHING at the moment)
    def createReport(self, event=None):
        print("[>] Trying to save report-data...")
        self.data_existing = False
        self.data_existing = self.checkCSVFiles()
        pass
