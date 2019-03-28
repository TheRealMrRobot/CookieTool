import os
import tkinter as tk
import backend as bend          # DataBase & Structure
import ui_menu as menu
import ui_group as group
import ui_report as report
import ui_menu_info as info
import ui_save as save
import ui_visual as visual
import ui_existing as existing


################################################################################
# D A T A  -  (SELF CREATED!)
################################################################################

# First Page at Startup
class Settings(tk.Frame):

    H_FONT = ("Verdana", 24, 'bold')
    FONT = ("Verdana", 24)
    TT_FONT = ("Verdana", 16)
    BACKGROUND_COLOR = "azure3"

    ROOT_DIR = bend.CookieDatabase.ROOT_DIR
    #ROOT_DIR = "/Users/Maxi/Desktop/atom/python/bachelor"

    SETTINGS_PATH = ROOT_DIR + "/tracking/data/settings/settings.txt"
    BASE_DIR = ROOT_DIR + "/tracking/data/firefox_data/"
    SQL_DIR = "~/firefox_data"
    CONTROLLER = None

    # parent is "Structure"
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.CONTROLLER = controller
        # INITIALIZATION:
        #self.DATA_WIN = controller
        self.set_text = tk.Label(self, text="SETTINGS", height=3, font=self.H_FONT)
        self.save_text = tk.Label(self, text="Choose File from '%s':" % self.SQL_DIR, font=self.TT_FONT)
        self.save_entry = tk.Entry(self, text="", font=self.TT_FONT)
        self.info_text2 = tk.Label(self, text="", font=self.TT_FONT)
        self.save_button = tk.Button(self, text="Apply", height=1, width=10, font=self.FONT, command=lambda: self.applySettings())
        self.check_text = tk.Label(self, text="Show existing files:", font=self.TT_FONT)
        self.check_button = tk.Button(self, text="Show Files", height=1, width=10, font=self.FONT, command=lambda: self.showExistingFiles(controller))

        self.back_button = tk.Button(self, text="< Back", font=self.FONT, width=10, command=lambda: controller.show_frame(menu.Menu))

        # PACKING:
        self.set_text.pack()
        self.save_text.pack()
        self.save_entry.pack()
        self.info_text2.pack()
        self.save_button.pack(pady=5)
        self.check_text.pack()
        self.check_button.pack()
        self.back_button.pack(pady=30)

        self.setDesign()

        self.save_entry.bind("<Return>", self.applySettings)


    # Changes the color of all elements in current window
    def setDesign(self):
        self.color = self.BACKGROUND_COLOR
        path = open(self.SETTINGS_PATH, 'r')
        lookup = str(path.read())
        path.close()
        self.save_entry.insert(tk.INSERT, lookup)

        self.configure(background=self.color)
        self.set_text.configure(background=self.color)
        self.save_text.configure(background=self.color)
        self.save_entry.configure(width=30, highlightbackground=self.color)
        self.info_text2.configure(background=self.color)
        self.check_text.configure(background=self.color)
        self.check_button.configure(highlightbackground=self.color)
        self.save_button.configure(highlightbackground=self.color)
        self.back_button.configure(highlightbackground=self.color)

        print("[DESIGN] SETTINGS DESIGN COLOR: %s" % self.color)
        print("[D_BASE] DATABASE PATH: ~/%s" % lookup)


    def showExistingFiles(self, controller):
        files = existing.Existing()
        files.openExisting(controller)


    def applySettings(self, event=None):
        backend = bend.CookieDatabase()
        path = self.save_entry.get()

        if os.path.isfile(self.BASE_DIR + path):
            file = open(self.SETTINGS_PATH, 'w+')
            file.write(path)
            file.close()
            backend.reload_path()
            self.info_text2.configure(text="New Filepath: %s" % path, fg='green')
            self.CONTROLLER.update()
            self.CONTROLLER.after(2000, self.info_text2.configure(text="", fg='black'))
        else:
            # EVENTUELL hier noch textfeld im GUI ansprechen!
            self.info_text2.configure(text="ERROR! File not found!", fg='red')
            self.CONTROLLER.update()
            print("[X] ERROR! File not found!")
            self.CONTROLLER.after(2000, self.info_text2.configure(text="", fg='black'))
