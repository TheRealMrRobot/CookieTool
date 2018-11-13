import os
import tkinter as tk
import backend as bend          # DataBase & Structure
import ui_menu as Menu

################################################################################
# I N F O
################################################################################


### TEST EDIT ####


# INFO Page
class Info(tk.Frame):

    PATH = "/Users/Maxi/Desktop/atom/python/bachelor/tracking/cookies/reports/"
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


    # parent will be "Structure"
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.var_idty = tk.IntVar()
        self.var_name = tk.IntVar()
        self.var_host = tk.IntVar()

        self.DATA_WIN = controller
        self.menu_label = tk.Label(self, text="Info Menu", font=self.H_FONT, height=3)
        self.load_label = tk.Label(self, text="Complete Database:", font=self.TT_FONT)
        self.load_button = tk.Button(self, text="Database", font=self.FONT, width=10, command=lambda: self.loadDatabase())
        self.group_label = tk.Label(self, text="Group Information:", font=self.TT_FONT)
        self.group_button = tk.Button(self, text="Group", font=self.FONT, width=10, command=lambda: self.openCookieGrouping())
        self.show_label = tk.Label(self, text="Specific Cookie Information:", font=self.TT_FONT)
        self.show_button = tk.Button(self, text="Info", font=self.FONT, width=10, command=lambda: self.showInfo())
        self.back_button = tk.Button(self, text="< Back", font=self.FONT, width=10, command=lambda: controller.show_frame(Menu.Menu))

        self.setDesign()

        self.menu_label.pack()
        self.load_label.pack()
        self.load_button.pack()
        self.group_label.pack()
        self.group_button.pack()
        self.show_label.pack()
        self.show_button.pack()
        self.back_button.pack(pady=30)


    # Changes the color of all elements in current window
    def setDesign(self):
        self.color = self.BACKGROUND_COLOR

        self.configure(background=self.color)
        self.menu_label.configure(background=self.color)
        self.show_label.configure(background=self.color)
        self.show_button.configure(highlightbackground=self.color)
        self.load_label.configure(background=self.color)
        self.load_button.configure(highlightbackground=self.color)
        self.back_button.configure(highlightbackground=self.color)
        self.group_label.configure(background=self.color)
        self.group_button.configure(highlightbackground=self.color)

        print("[DESIGN] INFO DESIGN COLOR: %s" % self.color)


    # Opens up a new window where an ID can be entered in (in order to see all info about a cookie)
    def showInfo(self):
        # root = tk.Tk()
        info_win = self.createNewWindow(850, "Info", 282, 360)
        info_frame_top = tk.Frame(info_win)
        info_frame_mid = tk.Frame(info_win)
        info_frame_sub = tk.Frame(info_win)
        info_frame_bot = tk.Frame(info_win)
        info_frame_last = tk.Frame(info_win)
        info_frame_top.pack()
        info_frame_mid.pack()
        info_frame_sub.pack()
        info_frame_bot.pack()
        info_frame_last.pack()


        self.info_label = tk.Label(info_frame_top, text="Search:", font=self.TT_FONT)
        self.search_entry = tk.Entry(info_frame_top, text="", font=self.TT_FONT)
        self.search_button = tk.Button(info_frame_sub, text="Search", font=self.FONT, width=10, command=lambda: self.searchEntry())
        self.result_space = tk.Text(info_frame_bot)
        self.general_info = tk.Button(info_frame_bot, text="General Info", font=self.FONT, width=10, command=lambda: self.generalInfo())


        info_win.configure(background=self.BACKGROUND_COLOR)
        info_frame_top.configure(background=self.BACKGROUND_COLOR)
        info_frame_mid.configure(background=self.BACKGROUND_COLOR)
        info_frame_sub.configure(background=self.BACKGROUND_COLOR)
        info_frame_bot.configure(background=self.BACKGROUND_COLOR)
        info_frame_last.configure(background=self.BACKGROUND_COLOR)

        self.info_label.configure(background=self.BACKGROUND_COLOR)
        self.search_entry.configure(highlightbackground=self.BACKGROUND_COLOR)
        self.search_button.configure(highlightbackground=self.BACKGROUND_COLOR)
        self.result_space.configure(highlightbackground=self.BACKGROUND_COLOR, height=14, width=60, state=tk.NORMAL)
        self.general_info.configure(highlightbackground=self.BACKGROUND_COLOR)

        self.info_label.pack()
        self.search_entry.pack()
        self.search_button.pack(pady=5)
        self.result_space.pack(expand=False)
        self.general_info.pack()

        self.search_entry.bind('<Return>', self.searchEntry)


    # Checks selected RadioButton and TextEntry -> gives it to loadData
    def searchEntry(self, event=None):
        self.search_string = self.search_entry.get()
        print("Searching ID: %s..." % str(self.search_string))

        if (self.search_string == "") == False:
            #print("[<] TEXT has been entered!")
            self.result_space.delete('1.0', tk.END)

            # Should load the data
            self.loadData(self.search_string)
        else:
            print("[X] ERROR!! ENTER Something!")


    # Opens a new window and shows general INFO about Cookies
    def generalInfo(self):
        self.database = bend.CookieDatabase()

        # Checks if windows are still open
        if self.DATA_LOADED == False:
            info_win = self.createNewWindow(725, "Info", 420, 320)
            self.textField = tk.Text(info_win)
            self.textField.configure(highlightbackground=self.color)
            self.textField.pack()
            self.DATA_LOADED = True
            #self.database.saveImportantDatabase()
            #self.database.saveCompleteDatabase()
            self.textField.insert(tk.INSERT, self.database.getInfo())
        else:
            info_win = self.createNewWindow(725, "Info", 420, 320)
            self.textField = tk.Text(info_win)
            self.textField.configure(highlightbackground=self.color)
            self.textField.pack()
            #self.DATA_LOADED = False
            self.textField.insert(tk.INSERT, self.database.getInfo())


    # Loads selected data -> Handles data retrieving (-> Sends specific request to backend.) (""" ONLY FOR SPECIFIC INFO!! """)
    def loadData(self, searchtext):
        database = bend.CookieDatabase()
        result_string = ""

        result_string = database.getSelectedEntryInfo(1, searchtext)
        self.result_space.insert(tk.INSERT, result_string)


    # Handles new window
    def openCookieGrouping(self):
        # root = tk.Tk()
        group_win = self.createNewWindow(-450, "Cookle Group", 1200, 800)
        group_frame_top = tk.Frame(group_win)
        group_frame_mid = tk.Frame(group_win)
        group_frame_sub = tk.Frame(group_win)
        group_frame_bot = tk.Frame(group_win)
        group_frame_last = tk.Frame(group_win)
        group_frame_top.pack()
        group_frame_mid.pack()
        group_frame_sub.pack()
        group_frame_bot.pack()
        group_frame_last.pack()


        self.var_idty.set(1)
        self.var_name.set(0)
        self.var_host.set(0)

        self.search_label = tk.Label(group_frame_top, text="Search:", font=self.TT_FONT)
        self.search_field = tk.Entry(group_frame_top, text="", font=self.TT_FONT)
        self.idty_box = tk.Radiobutton(group_frame_mid, text="ID", font=self.TT_FONT, indicatoron=1, value=self.var_idty, width=6, command=lambda: self.checkRadioState("id"))
        self.name_box = tk.Radiobutton(group_frame_mid, text="NAME", font=self.TT_FONT, indicatoron=1, value=self.var_name, width=7, command=lambda: self.checkRadioState("name"))
        self.host_box = tk.Radiobutton(group_frame_mid, text="HOST", font=self.TT_FONT, indicatoron=1, value=self.var_host, width=7, command=lambda: self.checkRadioState("host"))
        self.go_button = tk.Button(group_frame_sub, text="Search", font=self.FONT, width=10, command=lambda: self.searchForEntries())
        self.report_button = tk.Button(group_frame_last, text="Make Report", font=self.FONT, width=10, command=lambda: self.generateReport())

        self.counter_label = tk.Label(group_frame_sub, text="", font=self.TT_FONT)
        self.text_space = tk.Text(group_frame_bot)


        group_win.configure(background=self.BACKGROUND_COLOR)
        group_frame_top.configure(background=self.BACKGROUND_COLOR)
        group_frame_mid.configure(background=self.BACKGROUND_COLOR)
        group_frame_sub.configure(background=self.BACKGROUND_COLOR)
        group_frame_bot.configure(background=self.BACKGROUND_COLOR)
        group_frame_last.configure(background=self.BACKGROUND_COLOR)

        self.search_label.configure(background=self.BACKGROUND_COLOR)
        self.search_field.configure(highlightbackground=self.BACKGROUND_COLOR)
        self.idty_box.configure(background=self.BACKGROUND_COLOR)
        self.name_box.configure(background=self.BACKGROUND_COLOR)
        self.host_box.configure(background=self.BACKGROUND_COLOR)
        self.go_button.configure(highlightbackground=self.BACKGROUND_COLOR)
        self.counter_label.configure(background=self.BACKGROUND_COLOR)
        self.text_space.configure(highlightbackground=self.BACKGROUND_COLOR, height=35, width=170, state=tk.NORMAL)
        self.report_button.configure(highlightbackground=self.BACKGROUND_COLOR)


        self.search_label.pack()
        self.search_field.pack()
        self.idty_box.pack(side="left")
        self.host_box.pack(side="right")
        self.name_box.pack(side="right")
        self.go_button.pack(pady=5)
        self.counter_label.pack()
        self.text_space.pack(expand=False)
        self.report_button.pack(pady=5)

        self.search_field.bind("<Return>", self.searchForEntries)


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
        self.search_text = self.search_field.get()
        #print("TEST " + self.search_field.get())

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


    # Opens a new window and shows the whole Cookie - Database
    def loadDatabase(self):
        self.database = bend.CookieDatabase()
        # BELOW is just a stupid workaround for opening windows, after they have been withdrawn -> stupid because the window is instantly destroyed
        data_win = tk.Tk()
        data_win.state('withdrawn')

        # Checks if windows are still open
        if self.DATABASE_LOADED == False:
            data_win.destroy()
            data_win = self.createNewWindow(-650, "Database", 1000, 800)
            self.textField = tk.Text(data_win)
            self.textField.configure(highlightbackground=self.color, height=800)
            self.textField.pack(fill=tk.BOTH)
            self.DATABASE_LOADED = True
            self.textField.insert(tk.INSERT, self.database.getDatabase())
        elif 'withdrawn' == data_win.state():
            data_win.destroy()
            self.DATABASE_LOADED = False
            data_win = self.createNewWindow(-650, "Database", 1000, 800)
            self.textField = tk.Text(data_win)
            self.textField.configure(highlightbackground=self.color, height=800)
            self.textField.pack(fill=tk.BOTH)
            self.DATABASE_LOADED = True
            self.textField.insert(tk.INSERT, self.database.getDatabase())
            # self.CONTROLLER.show_frame(data_win)


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



    def generateReport(self):
        self.database = bend.CookieDatabase()
        self.info = self.database.getReport()

        #print(self.info)

        #if os.path.isfile(self.PATH + "report.txt"):
            #print("[X] ERROR! File Already exists!")
        #else:
        print("[>] Report written to: ~/report.txt")
        file = open(self.PATH + "report.txt", "w+")
        file.write(self.info)
