import tkinter as tk
import backend as back_end          # DataBase & Structure
import ui_menu as Menu

################################################################################
# D E L E T E    C O O K I E S
################################################################################

# DELETE Page
class Delete(tk.Frame):

    ROOT = None
    H_FONT = ("Verdana", 24, 'bold')
    FONT = ("Verdana", 24)
    TT_FONT = ("Verdana", 16)
    BACKGROUND_COLOR = "tomato"

    # GUI Stuff that needs to be global
    idty_box = None
    name_box = None
    host_box = None
    var_idty = None
    var_name = None
    var_host = None

    # GUI Initialisation:
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.var_idty = tk.IntVar()
        self.var_name = tk.IntVar()
        self.var_host = tk.IntVar()

        self.menu_label = tk.Label(self, text="Deletion Menu", font=self.H_FONT, height=3)
        self.info_label = tk.Label(self, text="Choose Cookies to delete:", font=self.TT_FONT)
        self.delete_win = tk.Button(self, text="Cookies", font=self.FONT, width=10, command=lambda: self.openCookieDeletion())
        self.del_all_label = tk.Label(self, text="Delete ALL Cookie Data:", font=self.TT_FONT)
        self.delete_all = tk.Button(self, text="ALL", font=self.FONT, width=10, command=lambda: self.deleteEverything())
        self.back_button = tk.Button(self, text="< Back", font=self.FONT, width=10, command=lambda: controller.show_frame(Menu.Menu))

        self.setDesign()

        self.menu_label.pack()
        self.info_label.pack()
        self.delete_win.pack()
        self.del_all_label.pack()
        self.delete_all.pack()
        self.back_button.pack(pady=30)


    # Changes the color of all elements in current window
    def setDesign(self):
        self.color = self.BACKGROUND_COLOR

        self.configure(background=self.color)
        self.menu_label.configure(background=self.color)
        self.info_label.configure(background=self.color)
        self.delete_win.configure(highlightbackground=self.color)
        self.del_all_label.configure(background=self.color)
        self.delete_all.configure(highlightbackground=self.color)
        self.back_button.configure(highlightbackground=self.color)


        print("[DESIGN] DELETE DESIGN COLOR: %s" % self.color)


    # Handles new window
    def openCookieDeletion(self):
        # root = tk.Tk()
        delete_win = self.createWindow(-450, "Delete", 1200, 800)
        delete_frame_top = tk.Frame(delete_win)
        delete_frame_mid = tk.Frame(delete_win)
        delete_frame_sub = tk.Frame(delete_win)
        delete_frame_bot = tk.Frame(delete_win)
        delete_frame_last = tk.Frame(delete_win)
        delete_frame_top.pack()
        delete_frame_mid.pack()
        delete_frame_sub.pack()
        delete_frame_bot.pack()
        delete_frame_last.pack()


        self.var_idty.set(1)
        self.var_name.set(0)
        self.var_host.set(0)

        self.search_label = tk.Label(delete_frame_top, text="Search:", font=self.TT_FONT)
        self.search_field = tk.Entry(delete_frame_top, text="", font=self.TT_FONT)
        self.idty_box = tk.Radiobutton(delete_frame_mid, text="ID", font=self.TT_FONT, indicatoron=1, value=self.var_idty, width=6, command=lambda: self.checkRadioState("id"))
        self.name_box = tk.Radiobutton(delete_frame_mid, text="NAME", font=self.TT_FONT, indicatoron=1, value=self.var_name, width=7, command=lambda: self.checkRadioState("name"))
        self.host_box = tk.Radiobutton(delete_frame_mid, text="HOST", font=self.TT_FONT, indicatoron=1, value=self.var_host, width=7, command=lambda: self.checkRadioState("host"))
        self.go_button = tk.Button(delete_frame_sub, text="Search", font=self.FONT, width=10, command=lambda: self.searchForEntries())

        self.counter_label = tk.Label(delete_frame_sub, text="", font=self.TT_FONT)
        self.text_space = tk.Text(delete_frame_bot)
        self.remove_visible = tk.Button(delete_frame_last, text="Delete ALL", font=self.FONT, width=10, command=lambda: self.deleteVisible())
        self.remove_entry = tk.Button(delete_frame_last, text="Delete Entry", font=self.FONT, width=10, command=lambda: self.deleteEntry())

        delete_win.configure(background=self.BACKGROUND_COLOR)
        delete_frame_top.configure(background=self.BACKGROUND_COLOR)
        delete_frame_mid.configure(background=self.BACKGROUND_COLOR)
        delete_frame_sub.configure(background=self.BACKGROUND_COLOR)
        delete_frame_bot.configure(background=self.BACKGROUND_COLOR)
        delete_frame_last.configure(background=self.BACKGROUND_COLOR)

        self.search_label.configure(background=self.BACKGROUND_COLOR)
        self.search_field.configure(highlightbackground=self.BACKGROUND_COLOR)
        self.idty_box.configure(background=self.BACKGROUND_COLOR)
        self.name_box.configure(background=self.BACKGROUND_COLOR)
        self.host_box.configure(background=self.BACKGROUND_COLOR)
        self.go_button.configure(highlightbackground=self.BACKGROUND_COLOR)
        self.counter_label.configure(background=self.BACKGROUND_COLOR)
        self.text_space.configure(highlightbackground=self.BACKGROUND_COLOR, height=35, width=170, state=tk.NORMAL)
        self.remove_visible.configure(highlightbackground=self.BACKGROUND_COLOR)
        self.remove_entry.configure(highlightbackground=self.BACKGROUND_COLOR)

        self.search_label.pack()
        self.search_field.pack()
        self.idty_box.pack(side="left")
        self.host_box.pack(side="right")
        self.name_box.pack(side="right")
        self.go_button.pack(pady=5)
        self.counter_label.pack()
        self.text_space.pack(expand=False)
        self.remove_visible.pack()
        self.remove_entry.pack()

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


    # Creates new functional Window
    def createWindow(self, x_movement, title, wid, hei):
        root = tk.Tk()
        root.title("Cookie Data - " + title)
        w = wid   # width for the Tk root
        h = hei  # height for the Tk root

        # get screen width and height
        ws = root.winfo_screenwidth()   # width of the screen
        hs = root.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (w/2) + x_movement
        y = (hs/2) - (h/2)

        # set the dimensions of the screen
        # and where it is placed
        root.geometry('%dx%d+%d+%d' % (w, h, x, y))

        return root


    # Checks selected RadioButton and TextEntry -> gives it to loadData (EVENT because of ENTER KEY Support!)
    def searchForEntries(self, event=None):
        self.search_text = self.search_field.get()

        if (self.search_text == "") == False:
            print("[<] '%s' has been entered!" % self.search_text)
            self.text_space.delete('1.0', tk.END)
            self.id_state = self.var_idty.get()
            self.name_state = self.var_name.get()
            self.host_state = self.var_host.get()

            # Should load the data
            self.loadData(self.id_state, self.name_state, self.host_state, self.search_text)
        else:
            self.counter_label.configure(text="[X] ENTER Something first!")
            print("[X] ERROR!! ENTER Something!")



    # Loads selected data -> Handles data retrieving (-> Sends specific request to backend.)
    def loadData(self, id_state, name_state, host_state, searchtext):
        database = back_end.CookieDatabase()
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
        print("\n[>] " + self.amount_string + "\n")



    def deleteEverything(self):
        pass


    def deleteVisible(self):
        pass


    def deleteEntry(self):
        pass
