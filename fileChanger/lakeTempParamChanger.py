import os
from paramChanger import paramChanger
import shutil


def main():
    pc = paramChanger

    # get the name of the file that's to be worked on
    ogFile = input(
        "Please input the name of the file you would like to change (make sure it's in the same folder as this program): ")

    # make a dupe of the file, unless one already exists
    dupedFile = pc.dupeFile(ogFile)

    # get the change that is to be made
    change = pc.getChange(input("Which parameter do you want to change: "), input(
        "Input the value to change to: ") + "\n")

    changeIndex = (pc.findChangeIndex(dupedFile, ogFile, change))

    # make the change in the copied file
    pc.makeChange(dupedFile, changeIndex, str(change[1]))


if __name__ == "__main__":
    main()
