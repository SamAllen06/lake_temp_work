import os
import shutil


class paramChanger():

    def getFileName(fileName):
        return fileName

    def getChange(paramToChange, valueToChange):
        return [paramToChange, valueToChange]

    # make a copy of the file
    def dupeFile(fileName):
        if os.path.exists("copyOf{}".format(fileName)):
            print("copy already exists\n")
            return "copyOf{}".format(fileName)
        else:
            print("new file was created!\n")
            return shutil.copyfile(fileName, "copyOf{}".format(fileName))
