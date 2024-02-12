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

    # find the index of the parameter they want to change
    def findChangeIndex(fileName, ogFileName, change):

        with open(fileName, 'r') as cf:
            lines = cf.readlines()

        for row in lines:
            if row.find(change[0]) != -1:
                return (str(lines.index(row)))
            else:
                continue

        return ('Parameter {} not found in {}'.format(change[0], ogFileName))
