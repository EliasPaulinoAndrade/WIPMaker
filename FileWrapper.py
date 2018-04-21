import os, sys
from PIL import Image

class FileWrapper:
    def __init__(self, file):
        self.file = file
        self.file_lines = FileWrapper.fileToList(self.file)
        self.file_str = None
    def __eq__(self, other):
        '''compare two files by comparing the lines
        '''
        if len(self) != len(other):
            return False
        for lineIndex in range(len(self)): 
            if self[lineIndex] != other[lineIndex]:
                return False
        return True
    def __len__(self):
        return len(self.file_lines)
    def __getitem__(self, index):
        return self.file_lines[index]
    
    def copyToPath(self, path):
        new_file = open(path, "wb")
        new_file.write(self.toByteString())
        new_file.close()
    def toByteString(self):
        if self.file_str != None:
            return self.file_str
        f_string = b"".join(self) 
        self.file_str = f_string

        return f_string
    def fileToList(file):
        '''receive a file, iterate over and add it lines in a array, 
        witch is returned
        '''
        file.seek(0)
        fileList = []
        for line in file:
            fileList.append(line)
        return fileList
    def openFile(name):
        return FileWrapper(open(name, "rb"))