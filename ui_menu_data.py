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
class Data(tk.Frame):

    H_FONT = ("Verdana", 24, 'bold')
    FONT = ("Verdana", 24)
    TT_FONT = ("Verdana", 16)
    BACKGROUND_COLOR = "palegreen"

    # parent is "Structure"
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # INITIALIZATION:
        #self.DATA_WIN = controller
        self.data_text = tk.Label(self, text="Data Menu", height=3, font=self.H_FONT)
        self.save_text = tk.Label(self, text="Transform Data:", font=self.TT_FONT)
        self.save_button = tk.Button(self, text="Transform", height=1, width=10, font=self.FONT, command=lambda: self.openSaveOptions(controller))
        self.report_text = tk.Label(self, text="Create Data Report:", font=self.TT_FONT)
        self.report_button = tk.Button(self, text="Report", height=1, width=10, font=self.FONT, command=lambda: self.openReporting(controller))
        self.visual_text = tk.Label(self, text="Visualize Reports:", font=self.TT_FONT)
        self.visual_button = tk.Button(self, text="Visualize", height=1, width=10, font=self.FONT, command=lambda: self.openVizard(controller))

        self.back_button = tk.Button(self, text="< Back", font=self.FONT, width=10, command=lambda: controller.show_frame(menu.Menu))

        # PACKING:
        self.data_text.pack()
        self.save_text.pack()
        self.save_button.pack()
        self.report_text.pack()
        self.report_button.pack()
        self.visual_text.pack()
        self.visual_button.pack()

        self.back_button.pack(pady=30)

        self.setDesign()


    # Changes the color of all elements in current window
    def setDesign(self):
        self.color = self.BACKGROUND_COLOR

        self.configure(background=self.color)
        self.data_text.configure(background=self.color)
        self.report_text.configure(background=self.color)
        self.report_button.configure(highlightbackground=self.color)
        self.visual_text.configure(background=self.color)
        self.visual_button.configure(highlightbackground=self.color)
        self.save_text.configure(background=self.color)
        self.save_button.configure(highlightbackground=self.color)
        self.back_button.configure(highlightbackground=self.color)

        print("[DESIGN] DATA DESIGN COLOR: %s" % self.color)


    # Opens up a new window for creating reports (link to ui_report.py)
    def openReporting(self, controller):
        report_instance = report.Report()
        report_instance.startReporting(controller)


    # Opens up a new window for saving data (link to ui_save.py)
    def openSaveOptions(self, controller):
        save_instance = save.Save()
        save_instance.startSaveOptions(controller)


    # Open a new Window for VISUALIZING data!
    def openVizard(self, controller):
        visual_instance = visual.Visual()
        visual_instance.startVisualization(controller)
