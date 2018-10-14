import tkinter as tk
import backend as bend          # DataBase & Structure
import ui_menu as Menu

################################################################################
# I N F O
################################################################################


### TEST EDIT ####


# INFO Page
class Info(tk.Frame):

    DATA_LOADED = False
    DATABASE_LOADED = False
    H_FONT = ("Verdana", 24, 'bold')
    FONT = ("Verdana", 24)
    TT_FONT = ("Verdana", 16)
    BACKGROUND_COLOR = "deepskyblue"
    CONTROLLER = ""
    DATA_WIN = ""

    # parent will be "Structure"
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.DATA_WIN = controller
        self.menu_label = tk.Label(self, text="Info Menu", font=self.H_FONT, height=3)
        self.show_label = tk.Label(self, text="General Cookie Information:", font=self.TT_FONT)
        self.show_button = tk.Button(self, text="Info", font=self.FONT, width=10, command=lambda: self.showInfo())
        self.load_label = tk.Label(self, text="Complete Database:", font=self.TT_FONT)
        self.load_button = tk.Button(self, text="Database", font=self.FONT, width=10, command=lambda: self.loadDatabase())
        self.back_button = tk.Button(self, text="< Back", font=self.FONT, width=10, command=lambda: controller.show_frame(Menu.Menu))

        self.setDesign()

        self.menu_label.pack()
        self.show_label.pack()
        self.show_button.pack()
        self.load_label.pack()
        self.load_button.pack()
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

        print("[DESIGN] INFO DESIGN COLOR: %s" % self.color)


    # Opens a new window and shows general INFO about Cookies
    def showInfo(self):
        self.database = bend.CookieDatabase()

        # Checks if windows are still open
        if self.DATA_LOADED == False:
            info_win = self.createNewWindow(725, "Info", 420, 320)
            self.textField = tk.Text(info_win)
            self.textField.configure(highlightbackground=self.color)
            self.textField.pack()
            self.DATA_LOADED = True
            self.database.saveImportantDatabase()
            self.database.saveCompleteDatabase()
            self.textField.insert(tk.INSERT, self.database.getInfo())
        else:
            info_win = self.createNewWindow(725, "Info", 420, 320)
            self.textField = tk.Text(info_win)
            self.textField.configure(highlightbackground=self.color)
            self.textField.pack()
            #self.DATA_LOADED = False
            self.textField.insert(tk.INSERT, self.database.getInfo())



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
