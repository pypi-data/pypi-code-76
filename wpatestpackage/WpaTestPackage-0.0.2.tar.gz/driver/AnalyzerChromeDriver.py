from selenium import webdriver
from client.WebPageAnalyzerClient import WebPageAnalyzerClient
from model.PageDetails import PageDetails
from selenium.webdriver.chrome.options import Options
import os



class AnalyzerChromeDriver:

    def initializeDriver(self, host, port):
        WebPageAnalyzerClient.set_port(self, port)
        WebPageAnalyzerClient.set_host(self, host)
        WebPageAnalyzerClient.initializeWebPageAnalyzer(self)
        chrome_options = Options()
        chrome_options.experimental_options["debuggerAddress"]= host+":9222"
        chrome_options.add_argument("--ignore-certificate-errors")
        global driver
        driver = webdriver.Chrome(executable_path="../chromedriver.exe", options=chrome_options)
        driver.maximize_window()

    def scanPage(self, applicationName, buildID, pageTitle,url):
        driver.get(url)
        # pageDetails={
        #     "applicationName": applicationName,
        #     "buildId": buildID,
        #     "pageTitle": pageTitle,
        #     "typeScan": "Automation"
        # }
        pageDetails=PageDetails(buildID,pageTitle,applicationName)
        WebPageAnalyzerClient.scanPage(self, pageDetails, driver.current_url)

    def closeDriver(self):
        driver.close()
        WebPageAnalyzerClient.stopPageAnalyzer(self)
