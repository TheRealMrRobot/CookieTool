import os
import tkinter as tk
import backend as bend          # DataBase & Structure
import ui_menu as menu
import ui_group as group
import ui_report as report
import ui_menu_data as data
import visualization as viz
import ui_existing as existing

################################################################################
# S A V E
################################################################################


# self.CONTROLLER.update()            # CONTROLLER is the key to THREADING!
class Visual():
    H_FONT = ("Verdana", 24, 'bold')
    FONT = ("Verdana", 24)
    TT_FONT = ("Verdana", 16)
    BACKGROUND_COLOR = "palegreen"

    ROOT_DIR = bend.CookieDatabase.ROOT_DIR
    #ROOT_DIR = "/Users/Maxi/Desktop/atom/python/bachelor"

    PATH = ROOT_DIR + "/tracking/"
    PATH_CSV = ROOT_DIR + "/tracking/data/transformed_csv/"
    PATH_DATA = ROOT_DIR + "/tracking/data/firefox_data/"
    PATH_APP = ROOT_DIR + "/tracking/cookies/"
    REPORT_PATH = ROOT_DIR + "/tracking/data/reports/"
    CONTROLLER = None


    def __init__(self):
        pass


    # Opens up a window for saving data (and selecting which)
    def startVisualization(self, controller):
        window = self.createNewWindow(0, -50, "Vizual. Data", 650, 450)
        window.configure(background=self.BACKGROUND_COLOR)
        self.CONTROLLER = controller

        # Frames (6 - 3 nested in Frame1 & 1 per other frame)
        save_frame_top = tk.Frame(window)
        save_frame_left_top = tk.Frame(save_frame_top)
        save_frame_right_top = tk.Frame(save_frame_top)
        save_frame_bot = tk.Frame(window)


        # TOP:
        self.label_name = tk.Label(save_frame_left_top, text="Report Name:", font=self.FONT)
        self.label_info = tk.Label(save_frame_left_top, text="(Enter name after '..count_' without .csv)", font=self.TT_FONT)
        self.entry_name = tk.Entry(save_frame_left_top, text="", font=self.FONT)
        self.button_name = tk.Button(save_frame_left_top, text="Use Report", font=self.FONT, width=10, command=lambda: self.searchDatabase())
        self.button_existing = tk.Button(save_frame_left_top, text="Show Files", font=self.FONT, width=10, command=lambda: self.showExistingReports(controller))

        # Self:
        self.button_host = tk.Button(save_frame_bot, text="Host", font=self.FONT, width=10, command=lambda: self.showHost())
        self.button_suffix = tk.Button(save_frame_bot, text="Suffix", font=self.FONT, width=10, command=lambda: self.showSuffix())
        self.button_cook1st = tk.Button(save_frame_bot, text="Cook1st", font=self.FONT, width=10, command=lambda: self.showFirst())
        self.button_cook3rd = tk.Button(save_frame_bot, text="Cook3rd", font=self.FONT, width=10, command=lambda: self.showThird())
        self.button_tracker = tk.Button(save_frame_bot, text="Tracker", font=self.FONT, width=10, command=lambda: self.showTracker())
        self.button_total = tk.Button(save_frame_bot, text="Total", font=self.FONT, width=10, command=lambda: self.showTotal())
        self.button_unique = tk.Button(save_frame_bot, text="Unique", font=self.FONT, width=10, command=lambda: self.showUnique())


        save_frame_top.configure(background=self.BACKGROUND_COLOR)
        save_frame_left_top.configure(background=self.BACKGROUND_COLOR)
        save_frame_right_top.configure(background=self.BACKGROUND_COLOR)
        save_frame_bot.configure(background=self.BACKGROUND_COLOR)


        self.label_name.configure(background=self.BACKGROUND_COLOR)
        self.label_info.configure(background=self.BACKGROUND_COLOR)
        self.entry_name.configure(highlightbackground=self.BACKGROUND_COLOR)
        self.button_name.configure(highlightbackground=self.BACKGROUND_COLOR)
        self.button_existing.configure(highlightbackground=self.BACKGROUND_COLOR)

        self.button_host.configure(highlightbackground=self.BACKGROUND_COLOR)
        self.button_suffix.configure(highlightbackground=self.BACKGROUND_COLOR)
        self.button_cook1st.configure(highlightbackground=self.BACKGROUND_COLOR)
        self.button_cook3rd.configure(highlightbackground=self.BACKGROUND_COLOR)
        self.button_tracker.configure(highlightbackground=self.BACKGROUND_COLOR)
        self.button_total.configure(highlightbackground=self.BACKGROUND_COLOR)
        self.button_unique.configure(highlightbackground=self.BACKGROUND_COLOR)


        save_frame_top.pack(side=tk.TOP)
        save_frame_left_top.pack(side=tk.LEFT, pady=10)
        save_frame_right_top.pack(side=tk.RIGHT, pady=10)
        save_frame_bot.pack(side=tk.BOTTOM, pady=5)


        self.label_name.pack()
        self.label_info.pack()
        self.entry_name.pack()
        self.button_name.pack()
        self.button_existing.pack()

        self.button_host.pack()
        self.button_suffix.pack()
        self.button_cook1st.pack()
        self.button_cook3rd.pack()
        self.button_tracker.pack()
        self.button_total.pack()
        self.button_unique.pack()

        self.entry_name.bind("<Return>", self.searchDatabase)


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
        self.search_term = self.entry_name.get()
        self.database = bend.CookieDatabase()
        print("[>] Searching for file '..._count_%s.csv'..." % self.search_term)
        self.host_existing = self.database.checkExistance("report", "host/host_count_" + self.search_term)
        self.suffix_existing = self.database.checkExistance("report", "suffix/suffix_count_" + self.search_term)
        self.cook1st_existing = self.database.checkExistance("report", "cook1st/cook1st_count_" + self.search_term)
        self.cook3rd_existing = self.database.checkExistance("report", "cook3rd/cook3rd_count_" + self.search_term)
        self.tracker_existing = self.database.checkExistance("report", "tracker/tracker_count_" + self.search_term)
        self.unique_existing = self.database.checkExistance("report", "unique/unique_info_" + self.search_term)

        # if self.host_existing and self.suffix_existing and self.cook1st_existing and self.cook3rd_existing and self.tracker_existing and self.unique_existing:
        if self.host_existing:
            self.label_name.configure(text="[*] File exists!", fg='green')
            self.CONTROLLER.update()            # CONTROLLER is the key to THREADING!
            print("[*] File exists!\n")
            self.CONTROLLER.after(1500, self.label_name.configure(text="Report Name:", fg='black'))
        else:
            self.label_name.configure(text="[X] File not found!", fg='red')
            self.CONTROLLER.update()
            print("[X] ERROR! File not found!\n")
            self.CONTROLLER.after(1500, self.label_name.configure(text="Report Name:", fg='black'))


    def showExistingReports(self, controller):
        files = existing.Existing()
        files.openExistingReports(controller, self.BACKGROUND_COLOR)

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


    def showHost(self):
        self.name = self.entry_name.get()
        if self.name != "":
            viz.makeVerticalPieChart(self.REPORT_PATH, "host", self.name, "Hosts")


    def showSuffix(self):
        self.name = self.entry_name.get()
        if self.name != "":
            viz.makeVerticalPieChart(self.REPORT_PATH, "suffix", self.name, "Suffixes")


    def showFirst(self):
        self.name = self.entry_name.get()
        if self.name != "":
            viz.makeVerticalPieChart(self.REPORT_PATH, "cook1st", self.name, "1st Party")


    def showThird(self):
        self.name = self.entry_name.get()
        if self.name != "":
            viz.makeVerticalPieChart(self.REPORT_PATH, "cook3rd", self.name, "3rd Party")


    def showTracker(self):
        self.name = self.entry_name.get()
        if self.name != "":
            viz.makeVerticalPieChart(self.REPORT_PATH, "tracker", self.name, "Tracker")


    def showTotal(self):
        self.name = self.entry_name.get()
        if self.name != "":
            viz.makeTotalBarChart(self.REPORT_PATH, "total", self.name, "TOTAL INFO")


    def showUnique(self):
        self.name = self.entry_name.get()
        if self.name != "":
            viz.makeUniqueBarChart(self.REPORT_PATH, "unique", self.name, "UNIQUE INFO")
