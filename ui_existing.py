import os
import time
import tkinter as tk
import backend as bend          # DataBase & Structure


class Existing():
    ROOT_DIR = bend.CookieDatabase.ROOT_DIR
    #ROOT_DIR = "/Users/Maxi/Desktop/atom/python/bachelor"

    # CHANGE those 2 according to your system:
    FILE_DIR = ROOT_DIR + "/tracking/data/firefox_data/"
    REPORT_DIR = ROOT_DIR + "/tracking/data/reports/"
    SQL_DIR = "~/firefox_data"
    CSV_DIR = "~/reports"

    H_FONT = ("Verdana", 24, 'bold')
    FONT = ("Verdana", 24)
    TT_FONT = ("Verdana", 16)
    BACKGROUND_COLOR = "azure3"
    CONTROLLER = None

    def __init__(self):
        pass

    # Opens up a window for showing existing files in the SQL_DIR
    def openExisting(self, controller):
        self.CONTROLLER = controller
        window = self.createNewWindow(0, -50, "Existing Files", 300, 400)
        window.configure(background=self.BACKGROUND_COLOR)
        self.info_message = "in folder %s:" % self.SQL_DIR

        self.frame = tk.Frame(window)
        # Frames (6 - 3 nested in Frame1 & 1 per other frame)

        # TOP:
        self.label_file = tk.Label(self.frame, text="Available Files", font=self.FONT)
        self.label_path = tk.Label(self.frame, text=self.info_message, font=self.TT_FONT)
        self.scrollbar = tk.Scrollbar(self.frame)
        self.entry_file = tk.Text(self.frame, yscrollcommand=self.scrollbar.set)

        self.frame.configure(background=self.BACKGROUND_COLOR)
        self.label_file.configure(background=self.BACKGROUND_COLOR)
        self.label_path.configure(background=self.BACKGROUND_COLOR)
        self.scrollbar.configure(activebackground=self.BACKGROUND_COLOR, command=self.entry_file.yview)
        self.entry_file.configure(highlightbackground=self.BACKGROUND_COLOR, height=30, width=40, state=tk.NORMAL)

        self.frame.pack()
        self.label_file.pack()
        self.label_path.pack()
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.entry_file.pack()

        self.loadFiles()


    # Opens up a window for showing existing files in the SQL_DIR
    def openExistingReports(self, controller, color):
        self.CONTROLLER = controller
        self.BACKGROUND_COLOR = color
        window2 = self.createNewWindow(0, -50, "Existing Reports", 300, 400)
        window2.configure(background=self.BACKGROUND_COLOR)
        self.info_message2 = "in folder %s:" % self.CSV_DIR

        self.frame2 = tk.Frame(window2)
        # Frames (6 - 3 nested in Frame1 & 1 per other frame)

        # TOP:
        self.label_file2 = tk.Label(self.frame2, text="Available Reports", font=self.FONT)
        self.label_path2 = tk.Label(self.frame2, text=self.info_message2, font=self.TT_FONT)
        self.scrollbar2 = tk.Scrollbar(self.frame2)
        self.entry_file2 = tk.Text(self.frame2, yscrollcommand=self.scrollbar2.set)

        self.frame2.configure(background=self.BACKGROUND_COLOR)
        self.label_file2.configure(background=self.BACKGROUND_COLOR)
        self.label_path2.configure(background=self.BACKGROUND_COLOR)
        self.scrollbar2.configure(activebackground=self.BACKGROUND_COLOR, command=self.entry_file2.yview)
        self.entry_file2.configure(highlightbackground=self.BACKGROUND_COLOR, height=30, width=40, state=tk.NORMAL)

        self.frame2.pack()
        self.label_file2.pack()
        self.label_path2.pack()
        self.scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
        self.entry_file2.pack()

        self.loadReports()


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


    # Load files and display them!
    def loadFiles(self):
        self.list = os.listdir(self.FILE_DIR)
        self.count = 0
        self.files = []
        self.folders = []
        self.result_string = ""

        # GET all folders in the BASE_DIR:
        for element in self.list:
            if os.path.isdir(self.FILE_DIR + element):
                self.folders.append(element)
            elif os.path.isfile(self.FILE_DIR + element):
                self.files.append(element)

        # SHOW Files from PARENT folder:
        self.result_string += "[*] PARENT-FOLDER:\n"
        for file in sorted(self.files):
            self.result_string += " * %s\n" % file
        self.result_string += "\n"

        # WALK all folders in all DIRS (sorted):
        for folder in sorted(self.folders):
            self.list = os.listdir(self.FILE_DIR + folder)
            self.result_string += "[*] SUB-FOLDER '~/%s':\n" % folder

            for elem in sorted(self.list):
                self.result_string += " * %s\n" % elem

            self.result_string += "\n"

        self.entry_file.insert(tk.INSERT, self.result_string)



    # Load files and display them!
    def loadReports(self):
        self.list = os.listdir(self.REPORT_DIR)
        self.count = 0
        self.files = []
        self.folders = []
        self.result_string = ""

        # GET all folders in the BASE_DIR:
        for element in self.list:
            if os.path.isdir(self.REPORT_DIR + element):
                self.folders.append(element)
            elif os.path.isfile(self.REPORT_DIR + element):
                self.files.append(element)

        # SHOW Files from PARENT folder:
        self.result_string += "[*] PARENT-FOLDER:\n"
        for file in sorted(self.files):
            self.result_string += " * %s\n" % file
        self.result_string += "\n"

        # WALK all folders in all DIRS (sorted):
        for folder in sorted(self.folders):
            self.list = os.listdir(self.REPORT_DIR + folder)
            self.result_string += "[*] SUB-FOLDER '~/%s':\n" % folder

            for elem in sorted(self.list):
                self.result_string += " * %s\n" % elem

            self.result_string += "\n"

        self.entry_file2.insert(tk.INSERT, self.result_string)
