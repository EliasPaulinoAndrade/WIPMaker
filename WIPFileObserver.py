import time, os, hashlib, datetime
from FileWrapper import FileWrapper
from threading import Event, Thread

class WIPFileObserver(Thread):
    #create the wip folder if the file exist, the time_event helps the loop to stop during the wait()
    def __init__(self, file_name, offset_time = 2):
        super().__init__()
        self.file_name = file_name
        self.wip_directory = file_name + ".wip"
        self.running = False
        self.offset_time = offset_time
        if not os.path.isfile(file_name):
            return None
        if not os.path.isdir(self.wip_directory):
            os.makedirs(file_name + ".wip")
        
        self.target_file = FileWrapper.openFile(file_name)
        self.time_event = Event()

    #it's called if the file have changed since the last seen, the new file is copied to the wip folder
    def variationFound(self, file):
        md5 = self.generateMD5ByFile(file)
        current_date = datetime.datetime.now().strftime("%S%M%H%d%m%y") 
        new_file_path = self.wip_directory + "/wip_" + current_date + "_" + md5 + "_" + self.file_name.split("/")[-1]
        print(new_file_path)
        file.copyToPath(new_file_path)

    #generate the md5 by the file lines as string
    def generateMD5ByFile(self, file):
        md5 = hashlib.md5()
        file_string = file.toByteString()
        md5.update(file_string)
        return md5.hexdigest()

    #stop the wait setting the event, and running is false, the observer is dead
    def stop(self):
        self.running = False
        self.time_event.set()
    def run(self):
        self.observerLoop()
        
    #it check the file variance from time to time, the off set time is a wait on the thread. 
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
            self.time_event.wait(self.offset_time)