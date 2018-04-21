from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image
import os

from WIPFileObserver import WIPFileObserver

class Application(Tk):
    def __init__(self):
        super().__init__()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.width = 300
        self.height = screen_height
        self.geometry("%dx%d+%d+%d" % (self.width, self.height, screen_width - self.width, 0))
        self.wip_bserver = None
        self.play_image = PhotoImage(file = "images/playImage.png") 
        self.pause_image = PhotoImage(file = "images/pauseImage.png") 
        self.file_is_set = False
        self.setupLayout()
    def setupLayout(self):
        self['bg'] = "#3a99d9"
        title_label = Label(self, text = "WIPMaker", bg = "#3a99d9", fg = "#ecf0f1", font= "MSSansSerif 15")
        title_label.pack(fill = X, pady = 30)

        mid_pane = Frame(self, bg = "#ecf0f1")
        mid_pane.pack(fill = X)

        self.play_button = Button(mid_pane, width = 50, height = 50, highlightthickness = 0, bd = 0, bg = "#ecf0f1")       
        self.play_button.config(image = self.play_image)
        self.play_button.pack(padx = 20, pady = 20)
        self.play_button['state'] = 'disabled'

        self.pick_file_label = Label(mid_pane, text = "Click here to select the target file", bg = "#ecf0f1",fg = "#3a99d9", font= "MSSansSerif 12")
        self.pick_file_label.pack(padx = 20, pady = 10)
        self.pick_file_label.bind("<Button-1>", self.pickImage)

    def pickImage(self, event):
        file_name = askopenfilename(initialdir = os.path.abspath(__file__), title="Select the target file")
        if type(file_name) == tuple or file_name == "":
            return
        self.pick_file_label['text'] = file_name.split("/")[-1] + " selected"
        self.file_observer = WIPFileObserver(file_name)
        self.play_button['state'] = 'normal'
        self.play_button.bind("<Button-1>", self.playObserver)
        print(file_name)
    def playObserver(self, event):
        if self.file_observer.running:
            self.file_observer.stop()
            self.play_button['image'] = self.play_image
            self.pick_file_label['state'] = 'normal'
            self.pick_file_label.bind("<Button-1>", self.pickImage)
        else:
            self.file_observer.start()
            self.play_button['image'] = self.pause_image
            self.pick_file_label['state'] = 'disabled'
            self.pick_file_label.unbind("<Button-1>")
Application().mainloop()