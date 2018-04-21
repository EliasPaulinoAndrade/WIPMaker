from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image
import os

from WIPFileObserver import WIPFileObserver

class Application(Tk):
    def __init__(self):
        super().__init__()
        self.file_observer = None
        self.play_image = PhotoImage(file = "images/playimage.png") 
        self.pause_image = PhotoImage(file = "images/pauseimage.png") 
        self.icon = PhotoImage(file = "images/icon.png") 
        self.setupLayout()
    def setupLayout(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.width = 300
        self.height = screen_height

        self.minsize(width = self.width, height = 570)
        self.maxsize(width = 600, height = screen_height)

        self.geometry("%dx%d+%d+%d" % (self.width, self.height, screen_width - self.width, 0))
        self.protocol("WM_DELETE_WINDOW", self.windowClosing)
        self.tk.call('wm', 'iconphoto', self._w, self.icon)
        self.title("WIPMaker") 

        self['bg'] = "#3a99d9"
        title_label = Label(self, text = "WIPMaker", bg = "#3a99d9", fg = "#ecf0f1", font= "MSSansSerif 15")
        title_label.pack(fill = X, pady = 50)

        self.mid_pane = Frame(self, bg = "#ecf0f1", width = self.width)
        self.mid_pane.pack(fill = X, padx = 10, pady = 10)
      
        self.play_button = Button(self.mid_pane, width = 110, height = 110, highlightthickness = 0, bd = 0, bg = "#ecf0f1")       
        self.play_button.config(image = self.play_image)
        self.play_button.pack(padx = 20, pady = 20)
        self.play_button['state'] = 'disabled'

        self.pick_file_label = Label(self.mid_pane, 
            text = "Click here to select the target file", 
            bg = "#ecf0f1",
            fg = "#3a99d9", 
            font= "MSSansSerif 12")
        self.pick_file_label.pack(padx = 20, pady = (10, 50))
        self.pick_file_label.bind("<Button-1>", self.pickImage)

        self.scale_time_seconds = Scale(self.mid_pane, 
            label = "SECONDS",
            from_ = 3, 
            to = 60, 
            orient = HORIZONTAL, 
            bg = "#ecf0f1", 
            fg = "#3a99d9", 
            bd = 0, 
            highlightthickness = 0, 
            troughcolor = "#3a99d9")
        self.scale_time_seconds.pack(fill = X, padx = 20, pady = 20)
        self.scale_time_seconds.set(15)

        self.scale_time_minutes = Scale(self.mid_pane, 
            label = "MINUTES",
            from_ = 0, 
            to = 60, 
            orient = HORIZONTAL, 
            bg = "#ecf0f1", 
            fg = "#3a99d9", 
            bd = 0, 
            highlightthickness = 0, 
            troughcolor = "#3a99d9")
        self.scale_time_minutes.pack(fill = X, padx = 20, pady = 20)
        self.scale_time_minutes.set(0)


    def pickImage(self, event):
        file_name = askopenfilename(initialdir = os.path.abspath(__file__), title="Select the target file")
        if type(file_name) == tuple or file_name == "":
            return
        self.pick_file_label['text'] = file_name.split("/")[-1] + " selected"
        self.play_button['state'] = 'normal'
        self.play_button.bind("<Button-1>", self.playObserver)

        self.file_observer = WIPFileObserver(file_name)
    def playObserver(self, event):
        if self.file_observer.running:
            self.scale_time_minutes['state'] = self.scale_time_seconds['state'] = 'normal'
            self.file_observer.stop()
            self.file_observer = WIPFileObserver(self.file_observer.file_name)
            self.play_button['image'] = self.play_image
            self.pick_file_label['state'] = 'normal'
            self.pick_file_label.bind("<Button-1>", self.pickImage)
        else:
            self.scale_time_minutes['state'] = self.scale_time_seconds['state'] = 'disabled'
            self.file_observer.offset_time = self.scale_time_minutes.get()*60 + self.scale_time_seconds.get()
            self.file_observer.start()
            self.play_button['image'] = self.pause_image
            self.pick_file_label['state'] = 'disabled'
            self.pick_file_label.unbind("<Button-1>")
    def windowClosing(self):
        if self.file_observer == None:
            self.destroy()
            return  
        elif self.file_observer.running:
            self.file_observer.stop()
            self.play_button['image'] = self.play_image
        self.destroy()
Application().mainloop()