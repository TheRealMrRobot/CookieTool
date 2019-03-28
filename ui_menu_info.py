import os
import tkinter as tk
import backend as bend          # DataBase & Structure
import ui_menu as menu
import ui_group as group

################################################################################
# I N F O
################################################################################


### TEST EDIT ####


# INFO Page
class Info(tk.Frame):
    ROOT_DIR = bend.CookieDatabase.ROOT_DIR
    #ROOT_DIR = "/Users/Maxi/Desktop/atom/python/bachelor"
    PATH = ROOT_DIR + "/tracking/data/reports/"
    DATA_LOADED = False
    DATABASE_LOADED = False
    H_FONT = ("Verdana", 24, 'bold')
    FONT = ("Verdana", 24)
    TT_FONT = ("Verdana", 16)
    BACKGROUND_COLOR = "burlywood3"
    CONTROLLER = ""
    DATA_WIN = ""


    # parent will be "Structure"
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.DATA_WIN = controller
        self.menu_label = tk.Label(self, text="Info Menu", font=self.H_FONT, height=3)
        self.load_label = tk.Label(self, text="Complete Database:", font=self.TT_FONT)
        self.load_button = tk.Button(self, text="Database", font=self.FONT, width=10, command=lambda: self.loadDatabase())
        self.group_label = tk.Label(self, text="Group Information:", font=self.TT_FONT)
        self.group_button = tk.Button(self, text="Group", font=self.FONT, width=10, command=lambda: self.createCookieGrouping(controller))
        self.show_label = tk.Label(self, text="Specific Cookie Information:", font=self.TT_FONT)
        self.show_button = tk.Button(self, text="Info", font=self.FONT, width=10, command=lambda: self.showInfo())
        self.general_label = tk.Label(self, text="Quantitative Information:", font=self.TT_FONT)
        self.general_info = tk.Button(self, text="Numbers", font=self.FONT, width=10, command=lambda: self.generalInfo())
        self.back_button = tk.Button(self, text="< Back", font=self.FONT, width=10, command=lambda: controller.show_frame(menu.Menu))

        self.setDesign()

        self.menu_label.pack()
        self.load_label.pack()
        self.load_button.pack()
        self.group_label.pack()
        self.group_button.pack()
        self.show_label.pack()
        self.show_button.pack()
        self.general_label.pack()
        self.general_info.pack()
        self.back_button.pack(pady=29)


    # Changes the color of all elements in current window
    def setDesign(self):
        self.color = self.BACKGROUND_COLOR

        self.configure(background=self.color)
        self.menu_label.configure(background=self.color)
        self.show_label.configure(background=self.color)
        self.show_button.configure(highlightbackground=self.color)
        self.load_label.configure(background=self.color)
        self.load_button.configure(highlightbackground=self.color)
        self.general_label.configure(background=self.color)
        self.general_info.configure(highlightbackground=self.color)
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

        self.info_label.pack()
        self.search_entry.pack()
        self.search_button.pack(pady=5)
        self.result_space.pack(expand=False)

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


    # Opens up new Instance of ui_group:
    def createCookieGrouping(self, controller):
        cookie_group = group.Group()
        cookie_group.openCookieGrouping(controller)


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
            self.scrollbar = tk.Scrollbar(data_win)
            self.textField = tk.Text(data_win, yscrollcommand=self.scrollbar.set)
            self.scrollbar.configure(activebackground=self.BACKGROUND_COLOR, command=self.textField.yview)
            self.textField.configure(highlightbackground=self.color, height=800, width=1000, state=tk.NORMAL)
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            self.textField.pack()
            self.DATABASE_LOADED = True
            self.textField.insert(tk.INSERT, self.database.getDatabase())
        elif 'withdrawn' == data_win.state():
            data_win.destroy()
            self.DATABASE_LOADED = False
            data_win = self.createNewWindow(-650, "Database", 1000, 800)
            self.scrollbar = tk.Scrollbar(data_win)
            self.textField = tk.Text(data_win, yscrollcommand=self.scrollbar.set)
            self.scrollbar.configure(activebackground=self.BACKGROUND_COLOR, command=self.textField.yview)
            self.textField.configure(highlightbackground=self.color, height=800, width=1000, state=tk.NORMAL)
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            self.textField.pack()
            self.DATABASE_LOADED = True
            self.textField.insert(tk.INSERT, self.database.getDatabase())


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
