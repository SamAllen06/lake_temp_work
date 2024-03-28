from unittest import TestCase, main
from paramChanger import paramChanger
import os


class testParamChanger(TestCase):
    def setup(self):
        self.pc = paramChanger
        self.testFile = "testFile.txt"

# dupeFile - test if a duped file exists already

    def testDupeFileExists(self):
        actual = os.path.exists(paramChanger.dupeFile("testFile.txt"))
        assert actual == True, "got {}, expected {}".format(actual, True)

        # this one is failing and i'm not totally sure why... we may have to look at it together
    def testDupeFileNew(self):
        os.remove("copyOftestFile.txt")
        actual = os.path.exists(paramChanger.dupeFile("testFile.txt"))
        assert actual == False, "got {}, expected {}".format(actual, False)

# findChangeIndex

    def testFindChangeIndex(self):
        actual = paramChanger.findChangeIndex(
            'copyOfTestFile.txt', 'testFile.txt', 'sue')
        assert actual == str(2), "got {}, expected {}".format(actual, 2)

        # this one is also failing... whyyyyy
    def testFindChangeIndex(self):
        actual = paramChanger.findChangeIndex(
            'copyOfTestFile.txt', 'testFile.txt', 'blahblahblah')
        assert "Parameter" in actual, "got {}, expected {}".format(
            actual, True)

    # def tearDown(self):
    #     del self.paramChanger


if __name__ == "__main__":
    main()
