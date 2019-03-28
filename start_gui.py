import tkinter as tk
import ui_menu as Menu
import ui_menu_info as Info
import ui_menu_delete as Delete
import ui_menu_data as Data
import ui_menu_setting as Setting
import backend as bend

################################################################################
#   G U I
################################################################################

# Base of the program (OF ALL PROGRAMS (at least should be))
class Structure(tk.Tk):

    # Arguments (variables as many as you want)   &    # Keyword Arguments (lists as many as you want)
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        # geometry(600, 300)

        for i in range(22):
            print("\n")
        print("[+] STARTING GUI...")

        # The container of any Frame
        container = tk.Frame(self)
        # container.geometry(600, 300)

        # Pack the container into the window
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # A dictionary for frames
        self.frames = {}

        # ADD new windows / frames HERE:    <-------  F R A M E S
        for F in (Menu.Menu, Info.Info, Delete.Delete, Data.Data, Setting.Settings):
            # A new Frame that is created as a StartPage object (other class)
            frame = F(container, self)
            # Add the frame to the dictionary
            self.frames[F] = frame
                                              # nsew = North South East West
            frame.grid(row=0, column=0, sticky="nsew")      # Position the frame inside the window

        print("[+] GUI READY!\n\n")

        # Bring up the given frame
        self.show_frame(Menu.Menu)


    # Brings given frame up to the front
    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()     # Brings frame to the front


################################################################################
#   S T A R T I N G     P O I N T
################################################################################

# New instance of Type: Structure()
app = Structure(className="Cookle")
app.title("Cookie Data - Menu")
#app.name("Cookle")

w = 420 # width for the Tk root
h = 430 # height for the Tk root

# get screen width and height
ws = app.winfo_screenwidth() # width of the screen
hs = app.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

# set the dimensions of the screen
# and where it is placed
#app.iconbitmap(r'/Users/Maxi/Desktop/atom/python/bachelor/tracking/cookies/pic/Cookie.ico')
app.geometry('%dx%d+%d+%d' % (w, h, x+560, y-60))

ROOT_DIR = bend.CookieDatabase.ROOT_DIR
#ROOT_DIR = "/Users/Maxi/Desktop/atom/python/bachelor"
# V  THIS right here is defining the logo of the app (MAC OS -> Instead of TKinter Feather!)
img = tk.PhotoImage(file=ROOT_DIR + '/tracking/cookies/pic/Cookie.gif')
app.tk.call('wm', 'iconphoto', app._w, img)

# Run the instance!
try:
    app.mainloop()
except KeyboardInterrupt:
    print("\n[X] SHUTTING DOWN...")
