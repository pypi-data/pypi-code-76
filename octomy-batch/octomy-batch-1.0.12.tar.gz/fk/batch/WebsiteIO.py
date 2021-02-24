from BrowserRobot import BrowserRobot
from Printful import Printful
from Shopify import Shopify
from ClassicScraper import ClassicScraper
from Cache import Cache
from Svg import Svg
from IntelligenceTool import IntelligenceTool
from Profiler import Profiler
from N1Handler import N1Handler
from N2Handler import N2Handler
from Database import Database
from ScraperFactory import ScraperFactory
from ScreenshotHandler import ScreenshotHandler
from SPopScrapeHandler import SPopScrapeHandler
import logging

logger = logging.getLogger(__name__)

import utils
import credentials

import os
import sys
import time
import re


class WebsiteIO:
    def __init__(self, credentials):
        self.credentials = credentials

        # Make sure we have a database to work with
        self.db = Database(self.credentials)
        if not self.db:
            logger.error("No db")
            return

    def _handle_scrape_csv(self, link, website, ok, user_data):
        logger.info("CSV CALLBACK: ")
        logger.info(f"  ok={ok} ")
        logger.info(f"  link={link} ")
        # logger.info(f"  website={website} ")
        logger.info(f"  user_data={user_data} ")

    def _handle_scrape_db(self, link, website, ok, user_data):
        # logger.info("DB CALLBACK: ")
        # logger.info(f"  ok={ok} ")
        # logger.info(f"  link={link} ")
        # logger.info(f"  website={website} ")
        # logger.info(f"  user_data={user_data} ")
        logger.info(f"insert page_source={len(website['page_source'])} bytes, page_dom={len(website['page_dom'])} bytes into db for  {link}")
        self.db.insert_website(website)

    def scrape_csv(self, type="classic", input_fn="wio.csv", output_fn=None):
        with Profiler(f"scraping '{input_fn}' with {type}") as p:
            sf = ScraperFactory(credentials)
            scraper = sf.get_scraper(type)
            cb = self._handle_scrape_db
            self.output_file = None
            if scraper:
                if output_fn is not None:
                    self.output_file = open(self.output_fn, "w")
                    if self.output_file:
                        cb = self._handle_scrape_csv
                elif not self.db:
                    logger.error("No db")
                    return
                # Load input_links from .csv file line by line and for each step invoke the browser robot
                with open(input_fn, "r") as input_links_file:
                    input_link = input_links_file.readline()
                    while input_link:
                        input_link = input_link.strip()
                        if input_link != "":
                            input_link = utils.decorate_url(input_link)
                            # logger.info(f"{type} SCRAPING {input_link}")
                            user_data = {"test": input_link}
                            scraper.scrape_url(input_link, cb, user_data)
                        input_link = input_links_file.readline()
                # Wait for scraper to complete it's work before we continue
                scraper.finish()
                if self.output_file:
                    close(self.output_file)

    def scrape_db(self, type="classic", output_fn=None):
        with Profiler(f"scraping 'database' with {type}") as p:
            if not self.db:
                logger.error("No db")
                return
            limit = 10
            total = self.db.get_recsys_count()
            offset = 0

            match = "shopify"
            not_match = "myshopify"
            sf = ScraperFactory(credentials)
            scraper = sf.get_scraper(type)
            cb = self._handle_scrape_db
            self.output_file = None
            if scraper:
                if output_fn is not None:
                    self.output_file = open(self.output_fn, "w")
                    if self.output_file:
                        cb = self._handle_scrape_csv
                # Load input_links from  db line by line and for each step invoke the browser robot
                while offset < total:

                    links = self.db.get_beeketing_account_recsys(offset, limit, match, not_match)
                    for input_link in links:
                        input_link = input_link.strip()
                        if input_link != "":
                            input_link = utils.decorate_url(input_link)
                            logger.info(f"{type} SCRAPING {input_link}")
                            user_data = {"test": input_link}
                            scraper.scrape_url(input_link, cb, user_data)
                    offset += limit
                # Wait for scraper to complete it's work before we continue
                scraper.finish()
                if self.output_file:
                    close(self.output_file)


# Main entrypoint of script
if __name__ == "__main__":
    # Change current working dir to that of this script's location
    cwd = os.path.dirname(os.path.realpath(__file__))
    os.chdir(cwd)
    print("Set working dir to " + cwd)

    # Load credentials
    credentials = credentials.load_credentials()
    if not credentials:
        sys.exit(1)

    print("#############################################################################")

    wio = WebsiteIO(credentials)

    wio.scrape_csv("robot", "wio.csv", None)
    # wio.scrape_db('robot', None)
