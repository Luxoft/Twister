from selenium import selenium
import unittest, time, re

class gmail(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*firefox", "https://accounts.google.com/")
        self.selenium.start()
    
    def test_gmail(self):
        sel = self.selenium
        sel.open("/ServiceLogin?service=mail&passive=true&rm=false&continue=http://mail.google.com/mail/&scc=1&ltmpl=default&ltmplcache=2")
        sel.type("id=Email", "twister.selenium")
        sel.type("id=Passwd", "selenium123")
        sel.click("id=signIn")
        sel.wait_for_page_to_load("30000")
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
