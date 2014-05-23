
# version: 3.001

from selenium import selenium
import TscUnitTestLib as unittest


class gsmarena_nokia(unittest.TestCase):

    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*firefox", "http://www.gsmarena.com/")
        self.selenium.start()

    def test_gsmarena_nokia(self):
        sel = self.selenium
        sel.open("/")
        sel.click("link=Phone Finder")
        sel.wait_for_page_to_load("30000")
        sel.select("name=idMaker", "label=Nokia")
        sel.click("name=chkHSDPA2100")
        sel.select("name=TalkTime", "label=More than 10 hours")
        sel.click("css=input.st-button")
        sel.wait_for_page_to_load("30000")

    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)


print('Starting test...')

test = gsmarena_nokia()
print test, '\n'
_RESULT = test.main()

print('Test finished.')
