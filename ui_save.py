import os
import tkinter as tk
import backend as bend          # DataBase & Structure
import ui_menu as menu
import ui_group as group
import ui_report as report
import ui_menu_info as info
import ui_menu_data as data

################################################################################
# S A V E
################################################################################


# self.CONTROLLER.update()            # CONTROLLER is the key to "THREADING"!
class Save():

    H_FONT = ("Verdana", 24, 'bold')
    FONT = ("Verdana", 24)
    TT_FONT = ("Verdana", 16)
    BACKGROUND_COLOR = "palegreen"

    ROOT_DIR = bend.CookieDatabase.ROOT_DIR
    #ROOT_DIR = "/Users/Maxi/Desktop/atom/python/bachelor"

    PATH = ROOT_DIR + "/tracking/"
    PATH_CSV = ROOT_DIR + "/tracking/data/transformed_csv/"
    PATH_DATA = ROOT_DIR + "/tracking/data/firefox_data/"
    SHORT_PATH = "firefox_data"
    PATH_APP = ROOT_DIR + "/tracking/cookies/"
    CONTROLLER = None


    def __init__(self):
        pass


    # Opens up a window for saving data (and selecting which)
    def startSaveOptions(self, controller):
        window = self.createNewWindow(0, -50, "Save Data", 650, 300)
        window.configure(background=self.BACKGROUND_COLOR)
        self.CONTROLLER = controller

        # Frames (6 - 3 nested in Frame1 & 1 per other frame)
        save_frame_top = tk.Frame(window)
        save_frame_top_top = tk.Frame(save_frame_top)
        save_frame_left_top = tk.Frame(save_frame_top)
        save_frame_mid_top = tk.Frame(save_frame_top)
        save_frame_right_top = tk.Frame(save_frame_top)
        save_frame_mid = tk.Frame(window)
        save_frame_bot = tk.Frame(window)


        # TOP:
        self.info_label = tk.Label(save_frame_top_top, text="Transform SQLite DB from '~/%s'" % self.SHORT_PATH, font=self.FONT)
        self.label_sqlite = tk.Label(save_frame_left_top, text="File:", font=self.FONT)
        self.entry_sqlite = tk.Entry(save_frame_mid_top, text="", font=self.FONT)
        self.button_sqlite = tk.Button(save_frame_right_top, text="Search", font=self.FONT, width=10, command=lambda: self.searchDatabase())
        self.label_status = tk.Label(save_frame_mid, text="", font=self.FONT)

        # save:
        self.label_csv = tk.Label(save_frame_bot, text="CSV Name:", font=self.TT_FONT)
        self.entry_csv = tk.Entry(save_frame_bot, text="", font=self.TT_FONT)
        self.button_csv = tk.Button(save_frame_bot, text="Save .csv", font=self.FONT, width=10, command=lambda: self.saveData())

        save_frame_top_top.configure(background=self.BACKGROUND_COLOR)
        save_frame_top.configure(background=self.BACKGROUND_COLOR)
        save_frame_left_top.configure(background=self.BACKGROUND_COLOR)
        save_frame_mid_top.configure(background=self.BACKGROUND_COLOR)
        save_frame_right_top.configure(background=self.BACKGROUND_COLOR)
        save_frame_mid.configure(background=self.BACKGROUND_COLOR)
        save_frame_bot.configure(background=self.BACKGROUND_COLOR)

        self.info_label.configure(background=self.BACKGROUND_COLOR)
        self.label_sqlite.configure(background=self.BACKGROUND_COLOR)
        self.entry_sqlite.configure(highlightbackground=self.BACKGROUND_COLOR)
        self.button_sqlite.configure(highlightbackground=self.BACKGROUND_COLOR)
        self.label_status.configure(background=self.BACKGROUND_COLOR)
        self.label_csv.configure(background=self.BACKGROUND_COLOR)
        self.entry_csv.configure(highlightbackground=self.BACKGROUND_COLOR)
        self.button_csv.configure(highlightbackground=self.BACKGROUND_COLOR)


        save_frame_top.pack(side=tk.TOP)
        save_frame_top_top.pack(side=tk.TOP)
        save_frame_left_top.pack(side=tk.LEFT, pady=10)
        save_frame_mid_top.pack(side=tk.LEFT, pady=10)
        save_frame_right_top.pack(side=tk.RIGHT, pady=10)
        save_frame_mid.pack()
        save_frame_bot.pack(side=tk.BOTTOM, pady=5)

        self.info_label.pack()
        self.label_sqlite.pack()
        self.entry_sqlite.pack()
        self.button_sqlite.pack()
        self.label_status.pack()
        self.label_csv.pack()
        self.entry_csv.pack()
        self.button_csv.pack()

        self.entry_sqlite.bind("<Return>", self.searchDatabase)
        self.entry_csv.bind("<Return>", self.saveData)


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


    # Should look for the requested database -> in local path(es)?
    def searchDatabase(self, event=None):
        self.search_term = self.entry_sqlite.get()
        self.database = bend.CookieDatabase()
        print("[>] Searching for file '%s.sqlite'..." % self.search_term)
        self.existing = self.database.checkExistance("sqlite", self.search_term)

        if self.existing:
            self.label_status.configure(text="[*] File exists!", fg='green')
            self.CONTROLLER.update()            # CONTROLLER is the key to THREADING!
            print("[*] File exists!\n")
            self.CONTROLLER.after(1500, self.label_status.configure(text="", fg='black'))
        else:
            self.label_status.configure(text="[X] File not found!", fg='red')
            self.CONTROLLER.update()
            print("[X] ERROR! File not found!\n")
            self.CONTROLLER.after(1500, self.label_status.configure(text="", fg='black'))


    # SAVES & TRANSFORMS data into CSV -> with extra content!
    def saveData(self, event=None):
        self.database = bend.CookieDatabase()
        self.search_term = self.entry_sqlite.get()
        self.csv_name = self.entry_csv.get()

        if (self.csv_name == "") == False:
            self.existing = self.database.checkExistance("sqlite", self.search_term)
            self.csv_existing = self.database.checkExistance("transformed", self.csv_name)

            if self.existing and self.csv_existing == False:
                self.label_status.configure(text="[*] Saving file...", fg='green')
                self.CONTROLLER.update()            # CONTROLLER is the key to THREADING!
                print("[*] Saving file...\n")
                self.processData(self.search_term, self.csv_name)
                self.CONTROLLER.after(200, self.label_status.configure(text="[*] Saving SUCCESSFULL!", fg='green'))
                self.CONTROLLER.update()            # CONTROLLER is the key to THREADING!
                self.CONTROLLER.after(1500, self.label_status.configure(text="", fg='black'))
            elif self.csv_existing == True:
                self.label_status.configure(text="[X] CSV already existing!", fg='red')
                self.CONTROLLER.update()
                print("[X] ERROR! CSV already existing!!\n")
                self.CONTROLLER.after(1500, self.label_status.configure(text="", fg='black'))
            else:
                self.label_status.configure(text="[X] File not found!", fg='red')
                self.CONTROLLER.update()
                print("[X] ERROR! File not found!\n")
                self.CONTROLLER.after(1500, self.label_status.configure(text="", fg='black'))
        else:
            self.label_status.configure(text="[X] Enter CSV name first!", fg='red')
            self.CONTROLLER.update()            # CONTROLLER is the key to THREADING!
            self.CONTROLLER.after(1500, self.label_status.configure(text="", fg='black'))


    # Processes and Saves DATA!
    def processData(self, search_term, csv_name):
        self.database = bend.CookieDatabase()
        self.data = self.database.transformToDataFrame(search_term)
        try:
            #self.data.to_csv(self.PATH_CSV + "%s.csv" % csv_name, sep=',', index=False, mode='w+')
            self.data.to_csv(self.database.TRANSFORM_PATH + "%s.csv" % csv_name, sep=';', index=False, mode='w+')
            print("[*] Saving SUCCESSFULL!")
        except Exception:
            print("ERROR while saving file!")
        #print(self.data)
