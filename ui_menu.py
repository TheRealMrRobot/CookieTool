import tkinter as tk
import ui_menu_info as Info
import ui_menu_delete as Delete
import ui_menu_data as Data
import ui_menu_setting as Setting

################################################################################
# M E N U
################################################################################

# First Page at Startup
class Menu(tk.Frame):

    H_FONT = ("Verdana", 24, 'bold')
    FONT = ("Verdana", 24)
    TT_FONT = ("Verdana", 16)
    BACKGROUND_COLOR = "skyblue"

    # parent is "Structure"
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # INITIALIZATION:
        self.menu_text = tk.Label(self, text="Main Menu", height=3, font=self.H_FONT)
        self.info_text = tk.Label(self, text="Get Cookie Info:", font=self.TT_FONT)
        self.info_button = tk.Button(self, text="General", height=1, width=10, font=self.FONT, command=lambda: controller.show_frame(Info.Info))
        self.data_text = tk.Label(self, text="Get Data Insight:", font=self.TT_FONT)
        self.data_button = tk.Button(self, text="Insights", height=1, width=10, font=self.FONT, command=lambda: controller.show_frame(Data.Data))
        self.delete_text = tk.Label(self, text="Delete Cookies:", font=self.TT_FONT)
        self.delete_button = tk.Button(self, text="Delete", height=1, width=10, font=self.FONT, command=lambda: controller.show_frame(Delete.Delete))
        self.settings_text = tk.Label(self, text="Choose File:", font=self.TT_FONT)
        self.settings_button = tk.Button(self, text="Settings", height=1, width=10, font=self.FONT, command=lambda: controller.show_frame(Setting.Settings))

        # PACKING:
        self.menu_text.pack()
        self.info_text.pack()
        self.info_button.pack()
        self.data_text.pack()
        self.data_button.pack()
        self.delete_text.pack()
        self.delete_button.pack()
        self.settings_text.pack()
        self.settings_button.pack()

        self.setDesign()


    # Changes the color of all elements in current window
    def setDesign(self):
        self.color = self.BACKGROUND_COLOR

        self.configure(background=self.color)
        self.menu_text.configure(background=self.color)
        self.info_text.configure(background=self.color)
        self.info_button.configure(highlightbackground=self.color)
        self.data_text.configure(background=self.color)
        self.data_button.configure(highlightbackground=self.color)
        self.delete_text.configure(background=self.color)
        self.delete_button.configure(highlightbackground=self.color)
        self.settings_text.configure(background=self.color)
        self.settings_button.configure(highlightbackground=self.color)

        print("[DESIGN] MENU DESIGN COLOR: %s" % self.color)
