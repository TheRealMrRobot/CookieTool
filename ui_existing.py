import os
import time
import tkinter as tk
import backend as bend          # DataBase & Structure


class Existing():

    # CHANGE those 2 according to your system:
    FILE_DIR = "/Users/Maxi/Desktop/atom/python/bachelor/tracking/data/firefox_data/"
    SQL_DIR = "~/firefox_data"

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
        self.folders = []
        self.result_string = ""

        # GET all folders in the BASE_DIR:
        for element in self.list:
            if os.path.isdir(self.FILE_DIR + element):
                self.folders.append(element)

        # WALK all folders in all DIRS (sorted):
        for folder in sorted(self.folders):
            self.list = os.listdir(self.FILE_DIR + folder)
            self.result_string += "[*] FOLDER '~/%s':\n" % folder

            for elem in sorted(self.list):
                self.result_string += " * %s\n" % elem

            self.result_string += "\n"

        self.entry_file.insert(tk.INSERT, self.result_string)
