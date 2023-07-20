import unittest

import kioskbrowser

from PyQt5.QtCore import QUrl
import re

# import sys
# import logging
# logging.basicConfig(stream=sys.stderr, level=logging.INFO)

class TestUrlWhitelist(unittest.TestCase):
    # whitelistForUrl = {
    #         "google.com" : ["^.*google\\.com$"],
    #         "www.google.com" : ["^.*google\\.com$"],
    #         "http://google.com" : ["^.*google\\.com$"],
    #         "http://www.google.com" : ["^.*google\\.com$"],
    #         }
    def test_urlValid(self):
        qUrl = QUrl("google.com")
        whitelist = ["^\.*google\.com$"]
        urlValid = kioskbrowser.urlValid(qUrl, whitelist)

        self.assertTrue(urlValid)

    def test_regexForUrl(self):
        qUrl = QUrl("google.com")
        regex = kioskbrowser.regexForUrl(qUrl)

        self.assertTrue(re.fullmatch(regex, qUrl.toString()))

if __name__ == '__main__':
    unittest.main()
