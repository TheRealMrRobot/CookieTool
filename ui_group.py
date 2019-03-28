import os
import time
import tkinter as tk
import backend as bend          # DataBase & Structure
import ui_menu as Menu
import ui_menu_info as Info
import pandas as pd



class Group():
    ROOT_DIR = bend.CookieDatabase.ROOT_DIR
    #ROOT_DIR = "/Users/Maxi/Desktop/atom/python/bachelor"
    PATH = ROOT_DIR + "/tracking/data/csv/"
    DATA_LOADED = False
    DATABASE_LOADED = False
    H_FONT = ("Verdana", 24, 'bold')
    FONT = ("Verdana", 24)
    TT_FONT = ("Verdana", 16)
    BACKGROUND_COLOR = "burlywood3"
    CONTROLLER = None
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
    def openCookieGrouping(self, controller):
        self.backend_access = bend.CookieDatabase().SETTINGS_CONTENT
        self.search_label_text = ("Search File - '%s':" % self.backend_access)

        self.var_idty = tk.IntVar()
        self.var_name = tk.IntVar()
        self.var_host = tk.IntVar()
        self.CONTROLLER = controller
        # root = tk.Tk()
        group_win = self.createNewWindow(0, -50, "Cookie Group", 1215, 800)
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
        self.var_idty.set(0)
        self.var_name.set(0)
        self.var_host.set(1)

        # TOP widgets:
        self.search_label = tk.Label(group_frame_top, text=self.search_label_text, font=self.TT_FONT)
        self.search_field = tk.Entry(group_frame_top, text="", font=self.TT_FONT)
        self.idty_box = tk.Radiobutton(group_frame_mid, text="ID", font=self.TT_FONT, indicatoron=1, value=self.var_idty, width=6, command=lambda: self.checkRadioState("id"))
        self.name_box = tk.Radiobutton(group_frame_mid, text="NAME", font=self.TT_FONT, indicatoron=1, value=self.var_name, width=7, command=lambda: self.checkRadioState("name"))
        self.host_box = tk.Radiobutton(group_frame_mid, text="HOST", font=self.TT_FONT, indicatoron=1, value=self.var_host, width=7, command=lambda: self.checkRadioState("host"))
        self.go_button = tk.Button(group_frame_sub, text="Search", font=self.FONT, width=10, command=lambda: self.searchForEntries())
        # MID widgets:
        self.counter_label = tk.Label(group_frame_sub, text="", font=self.TT_FONT)
        self.scrollbar = tk.Scrollbar(group_frame_bot)
        self.text_space = tk.Text(group_frame_bot, yscrollcommand=self.scrollbar.set)

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
        self.scrollbar.configure(activebackground=self.BACKGROUND_COLOR, command=self.text_space.yview)
        # BOT widgets:
        self.csv_label.configure(background=self.BACKGROUND_COLOR)
        self.csv_field.configure(highlightbackground=self.BACKGROUND_COLOR)
        self.csv_button.configure(highlightbackground=self.BACKGROUND_COLOR)

        self.idty_box.deselect()
        self.name_box.deselect()
        self.host_box.select()

        # TOP widgets:
        self.search_label.pack()
        self.search_field.pack()
        self.idty_box.pack(side="left")
        self.host_box.pack(side="right")
        self.name_box.pack(side="right")
        self.go_button.pack(pady=5)
        # MID widgets:
        self.counter_label.pack()
        self.text_space.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.csv_label.pack()
        self.csv_field.pack()
        self.csv_button.pack(pady=5)

        self.search_field.bind("<Return>", self.searchForEntries)
        self.csv_field.bind("<Return>", self.generateReport)


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
        self.csv_label.configure(text="CSV Name:", fg='black')

        # If something has been entered!
        if (self.search_text == "") == False:
            print("\n[<] '%s' has been entered!" % self.search_text)
            self.text_space.delete('1.0', tk.END)
            self.id_state = self.var_idty.get()
            self.name_state = self.var_name.get()
            self.host_state = self.var_host.get()

            # Should load the data
            self.loadFilteredData(self.id_state, self.name_state, self.host_state, self.search_text)
        else:
            self.counter_label.configure(text="[X] ENTER Something first!", fg='red')
            self.CONTROLLER.update()
            print("[X] ERROR!! ENTER Something!\n")
            self.CONTROLLER.after(2000, self.counter_label.configure(text="", fg='black'))



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
        print("[>] " + self.amount_string + "")


    # Loads selected data -> Handles data retrieving (-> Sends specific request to backend.)
    def loadReportData(self, id_state, name_state, host_state, searchtext):
        database = bend.CookieDatabase()
        self.data = pd.DataFrame(columns=['ID', 'VALUE', 'NAME', 'HOST', 'ACCESSED', 'EXPIRY', 'SECURE', 'HTTP'], index=None)

        if id_state == 1:
            self.data = database.makeCSV(1, searchtext)
        elif name_state == 1:
            self.data = database.makeCSV(2, searchtext)
        elif host_state == 1:
            self.data = database.makeCSV(3, searchtext)

        self.info = "FETCHING RESULTS FOR SEARCH-TERM: '%s'\n" % searchtext
        self.amount_string = "Fetched [" + str(database.RESULT_AMOUNT) + "] Entries."
        self.result = self.info + "[>] " + self.amount_string

        print("\n[>] " + self.result)
        return self.data


    def generateReport(self):
        self.csv_label.configure(text="CSV Name:", fg='black')
        self.search_term = self.search_field.get()
        self.csv_name = self.csv_field.get()

        # Only if there was some search_term! -> ELSE it would be wasted time and caclulation power, if a csv was created, before it was checked, if it is necessary or not!
        if (self.search_term == "") == False:
            self.id_state = self.var_idty.get()
            self.name_state = self.var_name.get()
            self.host_state = self.var_host.get()

            print("[+] Creating CSV File...")
            #print(self.data)

            if os.path.isfile(self.PATH + "%s.csv" % self.csv_name):
                print("[X] ERROR! File Already exists!")
                self.warnMessage()

            else:
                # Should load the data
                self.data = self.loadReportData(self.id_state, self.name_state, self.host_state, self.search_text)
                print("[>] Report written to: ~/%s.csv\n" % self.csv_name)
                self.data.to_csv(self.PATH + "%s.csv" % self.csv_name, sep=',', index=False, mode='w+')
                self.csv_label.configure(text="[!] SUCCESS!", fg="green")
                self.CONTROLLER.update()
                self.CONTROLLER.after(2000, self.csv_label.configure(text="CSV Name:", fg='black'))
            #   file = open(self.PATH + "%s.txt" % self.csv_name, "w+")
            #file.write(self.data)

        else:
            self.counter_label.configure(text="[X] ENTER Something first!", fg='red')
            self.CONTROLLER.update()
            self.CONTROLLER.after(2000, self.counter_label.configure(text="", fg='black'))
            print("[X] ERROR!! ENTER Something!")


    def warnMessage(self):
        self.csv_label.configure(text="[X] ERROR! File Already exists!", fg="red")
        self.CONTROLLER.update()
        self.CONTROLLER.after(2000, self.csv_label.configure(text="CSV Name:", fg='black'))
