import os
import tkinter as tk
import backend as bend          # DataBase & Structure
import ui_menu as menu
import ui_group as group
import ui_report as report
import ui_menu_info as info
import ui_save as save
import ui_visual as visual


################################################################################
# D A T A  -  (SELF CREATED!)
################################################################################

# First Page at Startup
class Settings(tk.Frame):

    H_FONT = ("Verdana", 24, 'bold')
    FONT = ("Verdana", 24)
    TT_FONT = ("Verdana", 16)
    BACKGROUND_COLOR = "palegreen"
    SETTINGS_PATH = "/Users/Maxi/Desktop/atom/python/bachelor/tracking/data/settings/settings.txt"

    # parent is "Structure"
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # INITIALIZATION:
        #self.DATA_WIN = controller
        self.set_text = tk.Label(self, text="SETTINGS", height=3, font=self.H_FONT)
        self.save_text = tk.Label(self, text="SQLITE - PATH:", font=self.TT_FONT)
        self.save_entry = tk.Entry(self, text="", font=self.TT_FONT)
        self.save_button = tk.Button(self, text="Apply", height=1, width=10, font=self.FONT, command=lambda: self.applySettings(controller))

        self.back_button = tk.Button(self, text="< Back", font=self.FONT, width=10, command=lambda: controller.show_frame(menu.Menu))

        # PACKING:
        self.set_text.pack()
        self.save_text.pack()
        self.save_entry.pack()
        self.save_button.pack()
        self.back_button.pack(pady=30)

        self.setDesign()

        self.save_entry.bind("<Return>", self.applySettings)


    # Changes the color of all elements in current window
    def setDesign(self):
        self.color = self.BACKGROUND_COLOR
        path = open(self.SETTINGS_PATH, 'r')
        lookup = str(path.read())
        print(lookup)
        path.close()
        self.save_entry.insert(tk.INSERT, lookup)

        self.configure(background=self.color)
        self.set_text.configure(background=self.color)
        self.save_text.configure(background=self.color)
        self.save_entry.configure(width=30, highlightbackground=self.color)
        self.save_button.configure(highlightbackground=self.color)
        self.back_button.configure(highlightbackground=self.color)

        print("[DESIGN] DATA DESIGN COLOR: %s" % self.color)





    def applySettings(self, controller):
        path = self.save_entry.get()
        if len(path) >= 40:
            print("WROTE new Path!")
            file = open(self.SETTINGS_PATH, 'w+')
            file.write(path)
            file.close()
