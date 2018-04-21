import os, sys, fnmatch, datetime

name = input("Name: ")
wip_directory = name + ".wip"
wip_names = []
gif_images = []

if not os.path.isdir(wip_directory):
    sys.exit()

for wip_file in os.listdir(name + ".wip"):
    if fnmatch.fnmatch(wip_file, "wip_*"):
        wip_names.append(wip_file)
        

wip_names.sort(key = lambda item : datetime.datetime.strptime(item.split("_")[1], "%S%M%H%d%m%y"))
print('\n')
print('\n'.join(wip_names))

