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
            print("copy already exists, using existing copy\n")
            return "copyOf{}".format(fileName)
        else:
            print("new file was created!\n")
            return shutil.copyfile(fileName, "copyOf{}".format(fileName))

    # find the index of the parameter they want to change
    def findChangeIndex(fileName, ogFileName, changeParam):

        with open(fileName, 'r') as cf:
            lines = cf.readlines()

        for row in lines:
            if row.find(changeParam[0]) != -1:
                return (str(lines.index(row)))
            else:
                continue

        return ('Parameter {} not found in {}'.format(changeParam[0], ogFileName))

    # change the value of the parameter
    def makeChange(fileName, index, change):
        with open(fileName, 'r') as file:

            fileData = file.readlines()

            fileData[int(index) + 1] = change

        with open(fileName, 'w') as file:
            file.writelines(fileData)
