import os, sys, fnmatch
from PIL import Image

'''
it contains some functions to manage files, how read it lines, the file names from folder, 
and copy to other folder
'''
class FileWrapper:
    def __init__(self, file):
        self.file = file
        self.file_lines = FileWrapper.fileToList(self.file)
        self.file_str = None

    #compare two files by comparing the lines
    def __eq__(self, other):
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

    #copy it self to the origin path 
    def copyToPath(self, path):
        new_file = open(path, "wb")
        new_file.write(self.toByteString())
        new_file.close()

    #join the self list as a byte string
    def toByteString(self):
        if self.file_str != None:
            return self.file_str
        f_string = b"".join(self) 
        self.file_str = f_string
        return f_string

    #get a name file list from a folder, testing the pattern
    def readFilesNameFromDirectory(dic_name ,pattern = "*"):
        if not os.path.isdir(dic_name):
            return None
        files_name = []
        for file_ in os.listdir(dic_name):
            if fnmatch.fnmatch(file_, pattern):
                files_name.append(dic_name + "/" + file_)
        return files_name        
        
    #store the file lines in a list
    def fileToList(file):
        '''receive a file, iterate over and add it lines in a array, witch is returned'''
        file.seek(0)
        fileList = []
        for line in file:
            fileList.append(line)
        return fileList

    def openFile(name):
        return FileWrapper(open(name, "rb"))