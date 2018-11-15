import os
import tkinter as tk
import backend as bend          # DataBase & Structure
import ui_menu as Menu
import ui_info as Info



class Group():

    PATH = "/Users/Maxi/Desktop/atom/python/bachelor/tracking/data/reports/"
    DATA_LOADED = False
    DATABASE_LOADED = False
    H_FONT = ("Verdana", 24, 'bold')
    FONT = ("Verdana", 24)
    TT_FONT = ("Verdana", 16)
    BACKGROUND_COLOR = "deepskyblue"
    CONTROLLER = ""
    DATA_WIN = ""

    # GUI Stuff that needs to be global
    idty_box = None
    name_box = None
    host_box = None
    var_idty = None
    var_name = None
    var_host = None


    def __init__(self):
        pass


    # Handles new window
    def openCookieGrouping(self):
        self.var_idty = tk.IntVar()
        self.var_name = tk.IntVar()
        self.var_host = tk.IntVar()
        # root = tk.Tk()
        group_win = self.createNewWindow(-450, "Cookie Group", 1200, 800)
        # CREATING:
        group_frame_top = tk.Frame(group_win)
        group_frame_mid = tk.Frame(group_win)
        group_frame_sub = tk.Frame(group_win)
        group_frame_bot = tk.Frame(group_win)
        group_frame_last = tk.Frame(group_win)
        # PACKING:
        group_frame_top.pack()
        group_frame_mid.pack()
        group_frame_sub.pack()
        group_frame_bot.pack()
        group_frame_last.pack()

        # VARs for the RADIOBUTTONs:
        self.var_idty.set(1)
        self.var_name.set(0)
        self.var_host.set(0)

        # TOP widgets:
        self.search_label = tk.Label(group_frame_top, text="Search:", font=self.TT_FONT)
        self.search_field = tk.Entry(group_frame_top, text="", font=self.TT_FONT)
        self.idty_box = tk.Radiobutton(group_frame_mid, text="ID", font=self.TT_FONT, indicatoron=1, value=self.var_idty, width=6, command=lambda: self.checkRadioState("id"))
        self.name_box = tk.Radiobutton(group_frame_mid, text="NAME", font=self.TT_FONT, indicatoron=1, value=self.var_name, width=7, command=lambda: self.checkRadioState("name"))
        self.host_box = tk.Radiobutton(group_frame_mid, text="HOST", font=self.TT_FONT, indicatoron=1, value=self.var_host, width=7, command=lambda: self.checkRadioState("host"))
        self.go_button = tk.Button(group_frame_sub, text="Search", font=self.FONT, width=10, command=lambda: self.searchForEntries())
        # MID widgets:
        self.counter_label = tk.Label(group_frame_sub, text="", font=self.TT_FONT)
        self.text_space = tk.Text(group_frame_bot)
        # LAST widgets:
        self.csv_label = tk.Label(group_frame_last, text="CSV-Name:", font=self.TT_FONT)
        self.csv_field = tk.Entry(group_frame_last, text="", font=self.TT_FONT)
        self.csv_button = tk.Button(group_frame_last, text="Save Results", font=self.FONT, width=10, command=lambda: self.generateReport())

        # Layout FRAMES:
        group_win.configure(background=self.BACKGROUND_COLOR)
        group_frame_top.configure(background=self.BACKGROUND_COLOR)
        group_frame_mid.configure(background=self.BACKGROUND_COLOR)
        group_frame_sub.configure(background=self.BACKGROUND_COLOR)
        group_frame_bot.configure(background=self.BACKGROUND_COLOR)
        group_frame_last.configure(background=self.BACKGROUND_COLOR)

        # TOP widgets:
        self.search_label.configure(background=self.BACKGROUND_COLOR)
        self.search_field.configure(highlightbackground=self.BACKGROUND_COLOR)
        self.idty_box.configure(background=self.BACKGROUND_COLOR)
        self.name_box.configure(background=self.BACKGROUND_COLOR)
        self.host_box.configure(background=self.BACKGROUND_COLOR)
        self.go_button.configure(highlightbackground=self.BACKGROUND_COLOR)
        # MID widgets:
        self.counter_label.configure(background=self.BACKGROUND_COLOR)
        self.text_space.configure(highlightbackground=self.BACKGROUND_COLOR, height=35, width=170, state=tk.NORMAL)
        # BOT widgets:
        self.csv_label.configure(background=self.BACKGROUND_COLOR)
        self.csv_field.configure(highlightbackground=self.BACKGROUND_COLOR)
        self.csv_button.configure(highlightbackground=self.BACKGROUND_COLOR)

        # TOP widgets:
        self.search_label.pack()
        self.search_field.pack()
        self.idty_box.pack(side="left")
        self.host_box.pack(side="right")
        self.name_box.pack(side="right")
        self.go_button.pack(pady=5)
        # MID widgets:
        self.counter_label.pack()
        self.text_space.pack(expand=False)
        self.csv_label.pack()
        self.csv_field.pack()
        self.csv_button.pack(pady=5)

        self.search_field.bind("<Return>", self.searchForEntries)


    # Generic WINDOW-CREATOR
    def createNewWindow(self, x_movement, title, width, height):
        root = tk.Tk()
        root.title("Cookie Data - " + title)
        w = width # width for the Tk root
        h = height # height for the Tk root

        # get screen width and height
        ws = root.winfo_screenwidth() # width of the screen
        hs = root.winfo_screenheight() # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (w/2) + x_movement
        y = (hs/2) - (h/2)

        # set the dimensions of the screen
        # and where it is placed
        root.geometry('%dx%d+%d+%d' % (w, h, x, y))

        return root


    # Checks the given state and selects or deselects the choice.
    def checkRadioState(self, state):
        if state == "id":
            print("\n[<] SELECTED - ID")
            self.var_idty.set(1)
            self.var_name.set(0)
            self.var_host.set(0)
        elif state == "name":
            print("\n[<] SELECTED - NAME")
            self.var_idty.set(0)
            self.var_name.set(1)
            self.var_host.set(0)
        elif state == "host":
            print("\n[<] SELECTED - HOST")
            self.var_idty.set(0)
            self.var_name.set(0)
            self.var_host.set(1)


    # Checks selected RadioButton and TextEntry -> gives it to loadFilteredData (EVENT because of ENTER KEY Support!) ("""FOR GROUPING ONLY!""")
    def searchForEntries(self, event=None):

        if self.csv_field.get() != None:
            self.csv_field.delete(0, tk.END)                                    # Delete the text in CSV - Name FIELD

        self.search_text = self.search_field.get()                              # Get the entered TEXT from SEARCH FIELD
        self.csv_field.insert(tk.INSERT, self.search_text)                      # Auto-Fill TEXT to CSV - Name FIELD

        if (self.search_text == "") == False:
            print("[<] '%s' has been entered!" % self.search_text)
            self.text_space.delete('1.0', tk.END)
            self.id_state = self.var_idty.get()
            self.name_state = self.var_name.get()
            self.host_state = self.var_host.get()

            # Should load the data
            self.loadFilteredData(self.id_state, self.name_state, self.host_state, self.search_text)
        else:
            self.counter_label.configure(text="[X] ENTER Something first!")
            print("[X] ERROR!! ENTER Something!")


    # Loads selected data -> Handles data retrieving (-> Sends specific request to backend.)
    def loadFilteredData(self, id_state, name_state, host_state, searchtext):
        database = bend.CookieDatabase()
        result_string = ""
        amount = 0
        amount_string = ""

        if id_state == 1:
            result_string = database.getSelectedEntries(1, searchtext)
            amount = database.getResultCount()
        elif name_state == 1:
            result_string = database.getSelectedEntries(2, searchtext)
            amount = database.getResultCount()
        elif host_state == 1:
            result_string = database.getSelectedEntries(3, searchtext)
            amount = database.getResultCount()

        self.amount_string = "Found [" + str(amount) + "] Entries."
        self.text_space.insert(tk.INSERT, result_string)
        self.counter_label.configure(text=self.amount_string)
        print("[>] " + self.amount_string + "\n")


    # Loads selected data -> Handles data retrieving (-> Sends specific request to backend.)
    def loadReportData(self, id_state, name_state, host_state, searchtext):
        database = bend.CookieDatabase()
        result_string = ""
        amount = 0
        amount_string = ""

        if id_state == 1:
            result_string = database.getSelectedEntries(1, searchtext)
            amount = database.getResultCount()
        elif name_state == 1:
            result_string = database.getSelectedEntries(2, searchtext)
            amount = database.getResultCount()
        elif host_state == 1:
            result_string = database.getSelectedEntries(3, searchtext)
            amount = database.getResultCount()



        self.info = "SHOWING RESULTS FOR SEARCH-TERM: '%s'\n" % searchtext
        self.amount_string = "\nFound [" + str(amount) + "] Entries.\n\n"
        self.result = self.info + self.amount_string + result_string

        print("[>] " + self.amount_string + "\n")
        return self.result


    def generateReport(self):
        self.search_term = self.search_field.get()

        if (self.search_term == "") == False:
            self.id_state = self.var_idty.get()
            self.name_state = self.var_name.get()
            self.host_state = self.var_host.get()

            # Should load the data
            self.data = self.loadReportData(self.id_state, self.name_state, self.host_state, self.search_text)
        else:
            self.counter_label.configure(text="[X] ENTER Something first!")
            print("[X] ERROR!! ENTER Something!")


        print("\n[+] Creating REPORT for the search term: %s..." % self.search_term)

        #if os.path.isfile(self.PATH + "report.txt"):
            #print("[X] ERROR! File Already exists!")
        #else:
        print("[>] Report written to: ~/%s.txt\n" % self.search_term)
        file = open(self.PATH + "%s.txt" % self.search_term, "w+")
        file.write(self.data)
