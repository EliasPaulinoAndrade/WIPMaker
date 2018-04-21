import time, os, hashlib, datetime
from FileWrapper import FileWrapper
from threading import Event, Thread

class WIPFileObserver(Thread):
    def __init__(self, file_name):
        super().__init__()
        self.file_name = file_name
        self.wip_directory = file_name + ".wip"
        self.running = False
        if not os.path.isfile(file_name):
            return None
        if not os.path.isdir(self.wip_directory):
            os.makedirs(file_name + ".wip")
        
        self.target_file = FileWrapper.openFile(file_name)
        self.time_event = Event()
    def variationFound(self, file):
        md5 = self.generateMD5ByFile(file)
        current_date = datetime.datetime.now().strftime("%S%M%H%d%m%y") 
        new_file_path = self.wip_directory + "/wip_" + current_date + "_" + md5 + "_" + self.file_name.split("/")[-1]
        print(new_file_path)
        file.copyToPath(new_file_path)
    def generateMD5ByFile(self, file):
        md5 = hashlib.md5()
        file_string = file.toByteString()
        md5.update(file_string)
        
        return md5.hexdigest()
    def stop(self):
        self.running = False
        self.time_event.set()
    def run(self):
        self.observerLoop()
    def observerLoop(self):
        current_file = None
        variation = None
        self.running = True
        while self.running:
            current_file = FileWrapper.openFile(self.file_name)
            variation = not self.target_file == current_file
            if variation: 
                self.variationFound(current_file)
                self.target_file = current_file
            self.time_event.wait(2)