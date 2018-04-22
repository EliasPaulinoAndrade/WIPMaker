import os, sys, fnmatch, datetime
import imageio

class GIFWrapper:
    #these are the gif to create the gif
    def __init__(self, images):
        self.images = images
    def __str__(self):
        return "GIF[" + ", ".join(self) + "]"
    def __len__(self):
        return len(self.images)
    def __getitem__(self, index):
        return self.images[index]
    def sort(self):
        self.images.sort(key = GIFWrapper.sortKey)

    #use imageio to create a gif
    def makeGIF(self, path):
        self.sort()
        image_files = []
        for image in self:
            image_files.append(imageio.imread(image))
        imageio.mimsave(path, image_files)
        
    #the sort key is the date in the file name
    def sortKey(item):
        str_date = item.split("_")[1]
        date_format = "%S%M%H%d%m%y"
        date = datetime.datetime.strptime(str_date, date_format)
        return date