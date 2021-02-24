import logging
import re
import time
from typing import Iterable, Tuple, List
from urllib.parse import parse_qs
from urllib.parse import urlparse

from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException, StaleElementReferenceException, \
    TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class Whatsapp():
    '''A WhatsApp scraper without a proper docstring'''

    def __init__(self, geckopath=None):
        opts = dict(executable_path=geckopath) if geckopath else {}
        try:
            self.browser = webdriver.Firefox(**opts)
        except WebDriverException:
            logging.error("Geckodriver not found. Either copy the geckodriver to your path or specify its location")
            raise
        self.browser.get("https://web.whatsapp.com/")

    def get_qr(self) -> str:
        # If there is a "click to refresh QR code" message, click it
        clickme = self.browser.find_elements_by_css_selector("[aria-label='Scan me!']")
        if clickme:
            try:
                clickme[0].click()
            except ElementClickInterceptedException:
                pass

        c = WebDriverWait(self.browser, 5).until(
            presence_of_element_located((By.CSS_SELECTOR, "canvas"))
        )
        return c.screenshot_as_base64

    def is_qr_scanned(self):
        try:
            self.browser.find_element_by_xpath('//h1')
            return True
        except NoSuchElementException:
            return False

    def wait_to_be_ready(self):
        while True:
            if self.is_qr_scanned():
                time.sleep(1)
                return
            else:
                logging.info("Seems that WhatsApp is not ready yet, wait for a second...")
                time.sleep(1)

    def get_visible_chats(self) -> Iterable[WebElement]:
        """Yield a name item pair for the chats currently on the screen in the left pane"""
        a = self.browser.find_elements_by_xpath("//div[@id='pane-side']//span[@title and @dir='auto']")
        for item in a:
            try:
                _ = item.text  # trigger StaleElement if it is stale, can probably be done more elegantly?
                yield item
            except StaleElementReferenceException:
                logging.info(f"Skipping stale reference {item}")
                continue  # not sure why this happens, but it does

    def get_all_chats(self) -> Iterable[Tuple[str, WebElement]]:
        """Yield name:item pairs for all chats (scrolling down when needed), ordered from top"""
        seen_names = set()
        while True:
            new_chats = sorted(self.get_visible_chats(), key=lambda chat: chat.location['y'])
            last_chat = None
            for chat in new_chats:
                name = chat.text
                if name in seen_names:
                    continue
                seen_names.add(name)
                last_chat = chat
                yield name, chat
            if last_chat is None:
                # No chats added after the last scroll, reached the end
                break
            print("----- scroll ------ ")
            self.browser.execute_script("arguments[0].scrollIntoView();", last_chat.item)
            time.sleep(1)  # Allow scroll to execute

    def open_links_pane(self):
        """Open the links (in the media, links, docs) pane for the currently open chat"""
        # Find the avatar button to get media link
        try:
            x = self.browser.find_element_by_xpath("//div[@id = 'main']/header/div/div/img")
        except NoSuchElementException:
            x = self.browser.find_element_by_xpath("//div[@id = 'main']/header//*[@dir = 'auto']")
        x.click()
        time.sleep(2)
        # Find the right link for getting the links
        media_link = None
        for linktext in [
            "Medien, Links und Dokumente",
            "Media, links en documenten",
            "Media, Links and Docs"]:
            try:
                xpath = f"//span[@class = '_1fPA0 _27rts' and text() = '{linktext}']"
                media_link = self.browser.find_element_by_xpath(xpath)
            except NoSuchElementException:
                continue
        if media_link is None:
            raise Exception("Cannot find 'media, links and docs' link")
        media_link.click()
        xpath = "//*[text() = 'Links']"
        WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        # Click on the 'links' tab
        linktext2 = self.browser.find_element_by_xpath(xpath)
        linktext2.click()
        time.sleep(5)

    def get_all_links(self) -> Iterable[WebElement]:
        """Yield all links (<a> elements) in the list of links, scrolling down if needed"""
        seen = set()
        while True:
            last_link = None
            for link in self.browser.find_elements_by_xpath(
                "//*[@data-list-scroll-container = 'true']"
                "//*[contains(@class,'message-in') or contains(@class,'message-out')]"):
                if link in seen:
                    continue
                seen.add(link)
                last_link = link
                yield link
            if last_link is None:
                break
            self.browser.execute_script("arguments[0].scrollIntoView();", last_link)

    def scrape_link(self, link: WebElement) -> dict:
        """
        Scrape a single link from the links pane, returning a dict with uri, direction, sender, and date
        """
        result = dict(uri = link.find_element_by_xpath(".//a").get_attribute("href"))
        dir_class = link.get_attribute("class")
        if "message-in" in dir_class:
            result['direction'] = "received"
        elif "message-out" in dir_class:
            result['direction'] = "sent"
        else:
            raise ValueError(f"Unknown dir_class: {dir_class}")
        try:
            #Get the date from the links pane
            x = link.find_element_by_xpath(".//div[contains(@class,'copyable-text')]")
            preplaintext = x.get_attribute("data-pre-plain-text")
            m = re.match(r"\[(.*?)\] (.*):", preplaintext)
            if not m:
                raise ValueError(f"Cannot parse preplaintext: {preplaintext}")
            result['date'] = m.group(1)
            result['sender'] = m.group(2)
        except NoSuchElementException:
            #Alternative: click on link to scroll to chat and get the date from the chat
            try:
                x = link.find_element_by_xpath(".//div[span[@data-icon='tail-in']]")
                x.click()
                xpath = "//div[contains(@class, 'focusable-list-item')]//a[@href = '"+result['uri']+"']"
                WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))
                cm = self.browser.find_element_by_xpath(xpath)
                preplaintext = cm.find_element_by_xpath(
                    "ancestor::div[@data-pre-plain-text]").get_attribute("data-pre-plain-text")
                m = re.match(r"\[(.*?)\] (.*):", preplaintext)
                if not m:
                    raise ValueError(f"Cannot parse preplaintext: {preplaintext}")
                result['date'] = m.group(1)
                result['sender'] = m.group(2)
            except (NoSuchElementException, TimeoutException):
                #At the moment still fails if several links were sent in the same message
                logging.warning(f"Cannot get metadata for {result['uri']}")
        return result

    def get_links_per_chat(self, item: WebElement) -> Iterable[dict]:
        """
        Get all links in a chat (contact).
        :param item should be the WebElement representing the contact's name
        """
        chatname = item.text
        item.click()  # Open this chat
        self.open_links_pane()
        for link in self.get_all_links():
            result = self.scrape_link(link)
            result['chatname'] = chatname
            yield result

    def scrape_links(self) -> Iterable[List[dict]]:
        '''
        Yields the *links* per chat that are shared in the Whatsapp scraper instance
        For each chat, yield list of dicts with keys direction, link, name, date
        '''
        self.wait_to_be_ready()
        for name, chat in self.get_all_chats():
            yield list(self.get_links_per_chat(chat))


    def quit_browser(self):
        self.browser.quit()

    def blur(self):
        self.browser.execute_script("document.getElementsByTagName('body')[0].style.filter = 'blur(30px)';")


def anonymize_url(link, origin):
    base = urlparse(link)
    stripped_link = base.scheme + '://' + base.netloc + base.path
    queries = parse_qs(base.query)
    # Get search queries from search engines (Google, Bing, Yahoo, DuckDuckGo, Ecosia), Youtube and large Dutch media providers
    queries_keep = {k: v for k, v in queries.items() if k in ['v', 'q', 'p', 's', 'query', 'keyword', 'term']}
    return ({"link": stripped_link, "query": queries_keep})