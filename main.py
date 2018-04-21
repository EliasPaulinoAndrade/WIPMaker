import time, os, hashlib, datetime
from FileWrapper import FileWrapper

def variationFound(file, file_name, wip_directory):
    md5 = hashlib.md5()
    file_string = file.toByteString()
    md5.update(file_string)
    current_date = datetime.datetime.now().strftime("%S%M%H%d%m%y") 

    new_file_path =wip_directory + "/wip_" + current_date + "_" + md5.hexdigest() + "_" + file_name
    print(new_file_path)
    file.copyToPath(new_file_path)

name = input("Name: ")
wip_directory = name + ".wip"

if not os.path.isdir(wip_directory) or not os.path.isfile(name):
    os.makedirs(name + ".wip")

target_file = FileWrapper.openFile(name)
current_file = None
variation = False

while True:
    current_file = FileWrapper.openFile(name)
    variation = not target_file == current_file
    if variation: 
        variationFound(current_file, name, wip_directory)
        target_file = current_file
    time.sleep(1)