from unittest import TestCase, main
from paramChanger import paramChanger
import os


class testParamChanger(TestCase):
    def setup(self):
        self.pc = paramChanger
        self.testFile = "testFile.txt"

    # dupeFile - test if a duped file exists already

    def testDupeFileNew(self):
        actual = os.path.exists(paramChanger.dupeFile("testFile.txt"))
        assert actual == True, "got {}, expected {}".format(actual, True)

    def testDupeFileNew(self):
        os.remove("copyOftestFile.txt")
        actual = os.path.exists(paramChanger.dupeFile("testFile.txt"))
        assert actual == False, "got {}, expected {}".format(actual, False)

    # def tearDown(self):
    #     del self.pc


if __name__ == "__main__":
    main()
