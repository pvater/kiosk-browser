#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

import sys
import argparse
import re

# so ctrl-c terminates the app
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

import logging
# logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

from PyQt5.QtWidgets import QApplication, QPushButton, QToolBar, QMainWindow, QAction
from PyQt5.QtCore import QCoreApplication, Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage

# sys.settrace(trace)

class DataAccess:
    def readUrlWhitelist(self, whitelistFile):
        logging.debug("DataAccess.readUrlWhitelist()")
        whitelist=[]
        with open(whitelistFile, 'r') as f:
            whitelist = f.read().splitlines()
        logging.debug(whitelist)
        return whitelist

    def readBlockedHtml(self, blockedFile):
        logging.debug("DataAccess.readBlockedHtml()")
        # FIXME actually return the contents
        with open(blockedFile, 'r') as myBlockedHtml:
            return myBlockedHtml.read()
        return "<html><body>Site blocked!</body></html>"

class Context:
    def __init__(self):
        logging.debug("Context.init()")

class Controller:
    def __init__(self, args):
        logging.debug("Controller.init()")
        self.args = args
        self.dataAccess = DataAccess()
        self.context = self.createContext(args)

    def startBrowser(self):
        self.mainwindow = MyMainWindow(self.context)

    def createContext(self, args):
        logging.debug("Controller.createContext()")
        context = Context()
        context.useragent = args.useragent
        # context.starturl = QUrl(args.starturl)
        qStartUrl = QUrl(args.starturl)
        if not qStartUrl.scheme():
            qStartUrl.setScheme('http')
        context.starturl = qStartUrl
        context.whitelist = self.dataAccess.readUrlWhitelist(args.whitelist)
        # startUrlRegex = '(www\.)*' + re.escape(context.starturl.authority() + context.starturl.path()) + '/*'
        startUrlRegex = regexForUrl(context.starturl)
        context.whitelist.append(startUrlRegex)
        # logging.debug("startUrlRegex = " + startUrlRegex)
        context.blocked = self.dataAccess.readBlockedHtml(args.blocked)
        return context

def regexForUrl(qUrl):
    return '(www\.)?' + re.escape(qUrl.authority() + qUrl.path()) + '/?'

class MyMainWindow(QMainWindow):
    def __init__(self, context):
        logging.debug("MyMainWindow.init()")
        # logging.debug("URL!!!(mainwindowinit) " + context.starturl.toString())
        super().__init__()
        self.initUI(context)

    def initUI(self, context):
        logging.debug("MyMainWindow.initUI()")
        self.setWindowTitle('Kiosk-Browser')
        self.showMaximized()
        # self.showFullScreen()
        # self.setFixedSize(800, 600)

        logging.debug("start url: " + context.starturl.toString())

        self.browser = BrowserWidget(context)
        # self.browser.settings().setUserStyleSheetUrl(QUrl("file:///net/exa/bin/nohighlight.css"))
        self.browser.load(QUrl(context.starturl))

        self.addToolbar()
        self.setCentralWidget(self.browser)
        self.show()

    def addToolbar(self):
        self.toolBar = QToolBar("Navigation")
        # self.toolBar.setToolButtonStyle(3)
        self.toolBar.addAction(self.browser.pageAction(QWebEnginePage.Back))
        self.toolBar.addAction(self.browser.pageAction(QWebEnginePage.Forward))
        self.toolBar.addAction(self.browser.pageAction(QWebEnginePage.Reload))
        self.toolBar.addAction(self.browser.pageAction(QWebEnginePage.Stop))

        self.addToolBar(Qt.TopToolBarArea, self.toolBar)
        self.toolBar.setFloatable(False)
        self.toolBar.setMovable(False)

class BrowserWidget(QWebEngineView):
    def __init__(self, context):
        logging.debug("BrowserWidget.init()")
        super().__init__()
        self.context = context
        self.setPage(self.WebPageUserAgent(context.useragent))
        self.urlChanged.connect(self.onUrlChanged)
        # self.loadFinished.connect(self._result_available)
    # def _result_available(self, ok):
    #     self.show
    def onUrlChanged(self, qurl):
        logging.debug("BrowserWidget.onUrlChanged()")
        logging.debug(qurl)
        logging.debug(qurl.toString())
        logging.debug(self.context.whitelist)
        if not (qurl.isEmpty() or urlValid(qurl, self.context.whitelist)):
            logging.info("blocked...")
            # TODO there seems to be a problem when qurl is an image, it then just crashes with a segfault
            # self.load(QUrl(context.blocked))
            self.setHtml(self.context.blocked)
            # self.setUrl(QUrl('https://wikipedia.org'))
    class WebPageUserAgent(QWebEnginePage):
        def __init__(self, userAgent):
            self.userAgent = userAgent
            super().__init__()
        def userAgentForUrl(self, url):
            return self.userAgent

def urlValid(url, urls):
    urlString = url.authority() + url.path()
    logging.debug("urlString = " + urlString)
    for regex in urls:
        logging.debug("regex = " + regex)
        if re.fullmatch(regex, urlString):
            return True
    logging.debug("url invalid")
    return False

def parseArgs():
    parser = argparse.ArgumentParser(prog="kioskbrowser", description="Optional app description", epilog="bottom text")

    parser.add_argument("starturl", help="Initial URL.")
    parser.add_argument("-w", "--whitelist", nargs=1, required=False, default="url-whitelist",help="Filename of a list of URLs to be whitelisted (allows regex).")
    parser.add_argument("-u", "--useragent", nargs=1, required=False, default="", help="Custom user agent")
    parser.add_argument("-b", "--blocked", nargs=1, required=False, default="blocked.html", help="HTML file to display instead of blacklisted url's")

    args = parser.parse_args()
    logging.debug("\n\tstarturl = " + args.starturl + "\n\twhitelist = " + str(args.whitelist) + "\n\tuseragent = " + str(args.useragent) + "\n\tblocked = " + str(args.blocked))
    return args

if __name__ == "__main__":
    args = parseArgs()

    app = QApplication(sys.argv)
    app.setApplicationName("Kiosk-Browser")

    controller = Controller(args)
    controller.startBrowser()

    sys.exit(app.exec_())
