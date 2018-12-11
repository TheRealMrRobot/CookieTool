import os
import tkinter as tk
import backend as bend          # DataBase & Structure
import ui_menu as menu
import ui_group as group
import ui_report as report
import ui_menu_data as data
import visualization as viz

################################################################################
# S A V E
################################################################################


# self.CONTROLLER.update()            # CONTROLLER is the key to THREADING!
class Visual():

    H_FONT = ("Verdana", 24, 'bold')
    FONT = ("Verdana", 24)
    TT_FONT = ("Verdana", 16)
    BACKGROUND_COLOR = "palegreen"
    PATH = "/users/Maxi/Desktop/atom/python/bachelor/tracking/"
    PATH_CSV = "/users/Maxi/Desktop/atom/python/bachelor/tracking/data/transformed_csv/"
    PATH_DATA = "/users/Maxi/Desktop/atom/python/bachelor/tracking/data/firefox_data/"
    PATH_APP = "/users/Maxi/Desktop/atom/python/bachelor/tracking/cookies/"
    REPORT_PATH = "/Users/Maxi/Desktop/atom/python/bachelor/tracking/data/reports/"
    CONTROLLER = None


    def __init__(self):
        pass


    # Opens up a window for saving data (and selecting which)
    def startVisualization(self, controller):
        window = self.createNewWindow(0, -50, "Vizual. Data", 650, 350)
        window.configure(background=self.BACKGROUND_COLOR)
        self.CONTROLLER = controller

        # Frames (6 - 3 nested in Frame1 & 1 per other frame)
        save_frame_top = tk.Frame(window)
        save_frame_left_top = tk.Frame(save_frame_top)
        save_frame_right_top = tk.Frame(save_frame_top)
        save_frame_bot = tk.Frame(window)


        # TOP:
        self.label_name = tk.Label(save_frame_left_top, text="Name:", font=self.FONT)
        self.entry_name = tk.Entry(save_frame_left_top, text="", font=self.FONT)
        self.button_name = tk.Button(save_frame_left_top, text="OK", font=self.FONT, width=10, command=lambda: self.searchDatabase())
        self.label_chart = tk.Label(save_frame_right_top, text="Chart Name:", font=self.FONT)
        self.entry_chart = tk.Entry(save_frame_right_top, text="", font=self.FONT)
        self.button_chart = tk.Button(save_frame_right_top, text="OK", font=self.FONT, width=10, command=lambda: self.searchDatabase())

        # Self:
        self.button_host = tk.Button(save_frame_bot, text="Host", font=self.FONT, width=10, command=lambda: self.showHost())
        self.button_suffix = tk.Button(save_frame_bot, text="Suffix", font=self.FONT, width=10, command=lambda: self.showSuffix())
        self.button_cook1st = tk.Button(save_frame_bot, text="Cook1st", font=self.FONT, width=10, command=lambda: self.showFirst())
        self.button_cook3rd = tk.Button(save_frame_bot, text="Cook3rd", font=self.FONT, width=10, command=lambda: self.showThird())
        self.button_tracker = tk.Button(save_frame_bot, text="Tracker", font=self.FONT, width=10, command=lambda: self.showTracker())
        self.button_unique = tk.Button(save_frame_bot, text="Unique", font=self.FONT, width=10, command=lambda: self.showUnique())


        save_frame_top.configure(background=self.BACKGROUND_COLOR)
        save_frame_left_top.configure(background=self.BACKGROUND_COLOR)
        save_frame_right_top.configure(background=self.BACKGROUND_COLOR)
        save_frame_bot.configure(background=self.BACKGROUND_COLOR)


        self.label_name.configure(background=self.BACKGROUND_COLOR)
        self.entry_name.configure(highlightbackground=self.BACKGROUND_COLOR)
        self.button_name.configure(highlightbackground=self.BACKGROUND_COLOR)
        self.label_chart.configure(background=self.BACKGROUND_COLOR)
        self.entry_chart.configure(highlightbackground=self.BACKGROUND_COLOR)
        self.button_chart.configure(highlightbackground=self.BACKGROUND_COLOR)

        self.button_host.configure(highlightbackground=self.BACKGROUND_COLOR)
        self.button_suffix.configure(highlightbackground=self.BACKGROUND_COLOR)
        self.button_cook1st.configure(highlightbackground=self.BACKGROUND_COLOR)
        self.button_cook3rd.configure(highlightbackground=self.BACKGROUND_COLOR)
        self.button_tracker.configure(highlightbackground=self.BACKGROUND_COLOR)
        self.button_unique.configure(highlightbackground=self.BACKGROUND_COLOR)


        save_frame_top.pack(side=tk.TOP)
        save_frame_left_top.pack(side=tk.LEFT, pady=10)
        save_frame_right_top.pack(side=tk.RIGHT, pady=10)
        save_frame_bot.pack(side=tk.BOTTOM, pady=5)


        self.label_name.pack()
        self.entry_name.pack()
        self.button_name.pack()
        self.label_chart.pack()
        self.entry_chart.pack()
        self.button_chart.pack()

        self.button_host.pack()
        self.button_suffix.pack()
        self.button_cook1st.pack()
        self.button_cook3rd.pack()
        self.button_tracker.pack()
        self.button_unique.pack()

        self.entry_name.bind("<Return>", self.searchDatabase)
        self.entry_chart.bind("<Return>", self.saveData)


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
        print("[>] Searching for file '%s.csv'..." % self.search_term)
        self.host_existing = self.database.checkExistance("report", "host/host_count_" + self.search_term)
        self.suffix_existing = self.database.checkExistance("report", "suffix/suffix_count_" + self.search_term)
        self.cook1st_existing = self.database.checkExistance("report", "cook1st/cook1st_count_" + self.search_term)
        self.cook3rd_existing = self.database.checkExistance("report", "cook3rd/cook3rd_count_" + self.search_term)
        self.tracker_existing = self.database.checkExistance("report", "tracker/tracker_count_" + self.search_term)
        self.unique_existing = self.database.checkExistance("report", "unique/unique_info_" + self.search_term)

        if self.host_existing and self.suffix_existing and self.cook1st_existing and self.cook3rd_existing and self.tracker_existing and self.unique_existing:
            self.label_name.configure(text="[*] File exists!", fg='green')
            self.CONTROLLER.update()            # CONTROLLER is the key to THREADING!
            print("[*] File exists!\n")
            self.CONTROLLER.after(1500, self.label_name.configure(text="", fg='black'))
        else:
            self.label_name.configure(text="[X] File not found!", fg='red')
            self.CONTROLLER.update()
            print("[X] ERROR! File not found!\n")
            self.CONTROLLER.after(1500, self.label_name.configure(text="", fg='black'))


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
        viz.makeVerticalPieChart(self.REPORT_PATH, "suffix", "vm_standard04", "Suffixes")


    def showFirst(self):
        viz.makeVerticalPieChart(self.REPORT_PATH, "cook1st", "vm_standard04", "1st Party")


    def showThird(self):
        viz.makeVerticalPieChart(self.REPORT_PATH, "cook3rd", "vm_standard04", "3rd Party")


    def showTracker(self):
        viz.makeVerticalPieChart(self.REPORT_PATH, "tracker", "vm_standard04", "Tracker")


    def showUnique(self):
        viz.makeBarChart(self.REPORT_PATH, "unique", "vm_standard04", "UNIQUE INFO")