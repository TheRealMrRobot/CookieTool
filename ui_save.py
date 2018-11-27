import os
import tkinter as tk
import backend as bend          # DataBase & Structure
import ui_menu as menu
import ui_group as group
import ui_report as report
import ui_info as info
import ui_data as data


class Save():

    H_FONT = ("Verdana", 24, 'bold')
    FONT = ("Verdana", 24)
    TT_FONT = ("Verdana", 16)
    BACKGROUND_COLOR = "palegreen"

    def __init__(self):
        pass


    # Opens up a window for saving data (and selecting which)
    def startSaveOptions(self):
        window = self.createNewWindow(0, -50, "Save Data", 800, 440)
        window.configure(background=self.BACKGROUND_COLOR)

        # Frames (6 - 3 nested in Frame1 & 1 per other frame)
        save_frame_top = tk.Frame(window)
        save_frame_left_top = tk.Frame(save_frame_top)
        save_frame_mid_top = tk.Frame(save_frame_top)
        save_frame_right_top = tk.Frame(save_frame_top)
        save_frame_mid = tk.Frame(window)
        save_frame_bot = tk.Frame(window)



        # TOP:
        self.label_fast = tk.Label(save_frame_first, text="Standard:", font=self.TT_FONT)
        self.entry_fast = tk.Entry(save_frame_first, text="", font=self.TT_FONT)
        self.button_fast = tk.Button(save_frame_first, text="Search", font=self.FONT, width=10, command=lambda: self.autoFillEntries())
        # FIRST ENTRIES:
        self.label_stand = tk.Label(save_frame_left_top, text="Standard:", font=self.TT_FONT)
        self.entry_stand = tk.Entry(save_frame_left_top, text="", font=self.TT_FONT)
        self.label_priv = tk.Label(save_frame_right_top, text="Privacy Badger:", font=self.TT_FONT)
        self.entry_priv = tk.Entry(save_frame_right_top, text="", font=self.TT_FONT)
        # SECOND ROW:
        self.label_http = tk.Label(save_frame_left, text="HTTPs Everywhere:", font=self.TT_FONT)
        self.entry_http = tk.Entry(save_frame_left, text="", font=self.TT_FONT)
        self.label_matrix = tk.Label(save_frame_right, text="uMatrix:", font=self.TT_FONT)
        self.entry_matrix = tk.Entry(save_frame_right, text="", font=self.TT_FONT)
        # save:
        self.label_name = tk.Label(save_frame_bottom, text="save Name:", font=self.TT_FONT)
        self.entry_name = tk.Entry(save_frame_bottom, text="", font=self.TT_FONT)
        self.button_gen = tk.Button(save_frame_bottom, text="Save", font=self.FONT, width=10, command=lambda: self.createsave())


        save_frame_first.configure(background=self.BACKGROUND_COLOR)
        save_frame_top.configure(background=self.BACKGROUND_COLOR)
        save_frame_mid.configure(background=self.BACKGROUND_COLOR)
        save_frame_bot.configure(background=self.BACKGROUND_COLOR)

        save_frame_left_top.configure(background=self.BACKGROUND_COLOR)
        save_frame_right_top.configure(background=self.BACKGROUND_COLOR)
        save_frame_left.configure(background=self.BACKGROUND_COLOR)
        save_frame_right.configure(background=self.BACKGROUND_COLOR)
        save_frame_bottom.configure(background=self.BACKGROUND_COLOR)


        self.label_fast.configure(background=self.BACKGROUND_COLOR)
        self.entry_fast.configure(highlightbackground=self.BACKGROUND_COLOR)
        self.button_fast.configure(highlightbackground=self.BACKGROUND_COLOR)
        self.label_stand.configure(background=self.BACKGROUND_COLOR)
        self.entry_stand.configure(highlightbackground=self.BACKGROUND_COLOR)
        self.label_priv.configure(background=self.BACKGROUND_COLOR)
        self.entry_priv.configure(highlightbackground=self.BACKGROUND_COLOR)
        self.label_http.configure(background=self.BACKGROUND_COLOR)
        self.entry_http.configure(highlightbackground=self.BACKGROUND_COLOR)
        self.label_matrix.configure(background=self.BACKGROUND_COLOR)
        self.entry_matrix.configure(highlightbackground=self.BACKGROUND_COLOR)
        self.label_name.configure(background=self.BACKGROUND_COLOR)
        self.entry_name.configure(highlightbackground=self.BACKGROUND_COLOR)
        self.button_gen.configure(highlightbackground=self.BACKGROUND_COLOR)


        save_frame_first.pack()
        save_frame_top.pack(side=tk.TOP)
        save_frame_left_top.pack(side=tk.LEFT, pady=10)
        save_frame_right_top.pack(side=tk.RIGHT, pady=10)
        save_frame_mid.pack()
        save_frame_left.pack(side=tk.LEFT)
        save_frame_right.pack(side=tk.RIGHT)
        save_frame_bot.pack(side=tk.BOTTOM)
        save_frame_bottom.pack(side=tk.BOTTOM, pady=5)


        self.label_fast.pack()
        self.entry_fast.pack()
        self.button_fast.pack()
        self.label_stand.pack()
        self.entry_stand.pack()
        self.label_priv.pack()
        self.entry_priv.pack()
        self.label_http.pack()
        self.entry_http.pack()
        self.label_matrix.pack()
        self.entry_matrix.pack()
        self.label_name.pack()
        self.entry_name.pack()
        self.button_gen.pack()

        self.entry_fast.bind("<Return>", self.autoFillEntries)
        self.entry_name.bind("<Return>", self.createReport)



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
