"""

Author : Eng. Nasser AlOstath
         nasser@dotslashhack.io

pythonatinstagramtool, is a simple library/bot developed by The CEO of www.dotslashhack.io for educational perposes as an asset code to an article
written in arabic for www.pythonat.com that talks about writing and uploading a user built python package to pypi.org
so that it can be installed using pip.

this library is opensource that yields to the MIT license.

for more information, please check www.pythonat.com
or
www.dotslashhack.io to contact the author

this library is build mainly on top of selenium and webdriver-manager

the webdriver-manager library is usefull because it will automatically find and download the suitable browser webdriver depending on it's version and OS.


NOTE:

it is always better to keep you instagram credentials in a separate file and import them here

"""


# importing dependencies
from pynput import keyboard
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import IEDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import os, sys
import wget
from time import sleep
from pynput.keyboard import Key, Controller

# from auth import username, password


class Bot():
    """
    The Bot class is the Main and only Class in this educational library,the Bot will be able to

    initialize , login to account, find pictures(posts) using a word or hashtag , downloads the pics appearing 
    
    on the page after specifying the number of scroll downs and the path which the pictures are wanted to be
    
    saved at as well as giving them a simple name
    
    """
    
    # supported browser drivers to be downloaded by webdriver-manager
    supported_browsers =["chrome","firefox","chromium","ie","edge"]

    # statuses
    os_name =os.name # to know OS name
    clear_command ="" #to be used as a clear command in terminal depending on OS
    instagram_login_url ="https://www.instagram.com/accounts/login/" # instagram login url
    

    def __init__(self,browser_name,account_name,password):
        """
        initiating the driver object and downloading the desired browser webdriver to your operating system
        
        + checks os name and clears screen
        + downloads the corresponding webdriver for the selectd desired browser

        + browser_name : is desired browsername
        + account_name : is instagram username for the desired account for loging in
        + account_password : is the password for the account


        """
        # clear screeen according to os shell for windows and *nix OS's
        if "win".lower() in self.os_name:
            self.clear_command ="cls"
            os.system(self.clear_command)
        else:
            self.clear_command ="clear"
            os.system(self.clear_command)

        #initializing our browser
        self.browser_name = browser_name    #choosing which browser
        self.account_name = account_name    #instagram account username
        self.account_password = password    # instagram account password

        # checking if browsername is not in supported browsers
        if self.browser_name.lower() not in self.supported_browsers:
            print(f"""
            
                [-] {self.browser_name} browser is not supported
            
            
            """)
            
        # check browser name to install it's webdriver

        if self.browser_name.lower() == "chrome":
            self.driver = webdriver.Chrome(ChromeDriverManager().install())

        elif self.browser_name.lower() == "chromium":
            self.driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

        elif self.browser_name.lower() == "firefox":
            self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        
        elif self.browser_name.lower() == "ie":
            driver = webdriver.Ie(IEDriverManager().install())
        
        elif self.browser_name.lower() == "edge":
            driver = webdriver.Edge(EdgeChromiumDriverManager().install())
        else:
            print(f"""

            [-] Can't find a supported webdriver ...

            >>>> please choose a supported browser :
            {self.supported_browsers}
            
            
            
            """)
            sys.exit()

        print(f"""

        [+] {self.os_name} ===> is the operating system ....

        [+] {self.browser_name} browser is selected ....

        [+] {self.account_name} ==> instagram username ...

        """)
        self.login()

    def login(self):

        
        """
        + logs in to the desired account <account_name>, using the driver and the login url of instagram

        
        
        """

        self.driver.get(self.instagram_login_url,)
        sleep(3)

        # Accessing the username and password from the html page and clicking on the
        # not now buttons that appear twice after logging in as alerts
        element_username = self.driver.find_element_by_xpath('//input[@name="username"]')
        element_username.clear()    # makes sure that the input field is empty
        element_password = self.driver.find_element_by_xpath('//input[@name="password"]')
        element_password.clear()    # makes sure that the input field is empty

        # sending username to the input at the page
        element_username.send_keys(self.account_name)
        print(f"[+] entering {self.account_name} in username element field ...\n")

        # sending password to the password iput in the page
        element_password.send_keys(self.account_password)
        print(f"[+] entering {self.account_password} in password element field ...\n")

        # submitting the username and password
        element_password.submit()
        print(f"[+] clicked submit button ...\n")
        sleep(3)

        # finding and clicking the 1st Not Now button at the alert apperating on the page
        not_now_button = self.driver.find_element_by_xpath('//button[@type="button"]')
        not_now_button.click()
        print(f"[+] clicked a Not Now button [1]...\n")
        sleep(6)

        # finding and clicking the 2nd Not Now button at the alert apperating on the page
        not_now_2 = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]')
        not_now_2.click()
        print(f"[+] clicked a now button [2]...\n")
        sleep(3)
     
    def find(self,hashtag_string):
        """
        finds the searchbar in the page and inserts the hastag or word
        and presses enter to show the latest posts for that hashtag or word

        + search_bar : is our targetted searchbar
        + keyboard : is an instance of Controller class of pynout module
        
        """

        # finding the searchbar
        search_bar = self.driver.find_element_by_xpath('//input[@placeholder="Search"]')
        print(f"[+] found search bar ...")

        # sending the hashtag/or word to the searchbar
        search_bar.send_keys(hashtag_string)
        print(f"[+] sent word/hashtag to search bar ...")

        search_bar.find_element_by_xpath('/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input')
        sleep(3)
        
        # The Keys.ENTER didnt work here
        search_bar.send_keys(Keys.ENTER)

        # needed to import pynput library to simulate the enter pressing in a keyboard
        keyboard = Controller()     # keyboard.Controller object to control the Keyboard
        keyboard.press(Key.enter)   # pressing enter key
        sleep(0.2)
        keyboard.release(Key.enter) # sometime extra enters are needed
        print(f"[+] pressed ENTER in search bar ...")
      
    def get_posts(self,scrolls_num):
        """
        gets posts shown in the current page (hashtag / featured). gets their image links and post links

        + scrolls_num : number of desired scroll downs to scroll down the page to get more pictures
        
        + posts_link : list of links to posts collected
        + images_links: list of links to images collected

        returns : both mentioned lists
        """ 

        # Scroll down desired times
        for i in range(1,scrolls_num):
            self.driver.execute_script("window.window.scrollTo(0, document.body.scrollHeight);")
            sleep(3)   
       
        # list of posts links, and lists of images links to be filled  and returned by the Method
        posts_links =[]
        images_links =[]

        # finding all posts to get access to images links
        posts = self.driver.find_elements_by_xpath('//div[@class="KL4Bh"]/img')

        # iterate theough the harvested posts to get to the images links
        for post in posts:
            image_link = post.get_attribute("src")
            sleep(.5)
            images_links.append(image_link) # append to the images links list

        
        # getting all the actual posts [container] to access the links to each full post and it's media
        actual_posts = self.driver.find_elements_by_xpath('//div[@class="v1Nh3 kIKUG  _bz0w"]/a')
        for ap in actual_posts:
            post_link = ap.get_attribute("href")
            sleep(.5)
            posts_links.append(post_link) # append to the posts links list

        return posts_links, images_links # returning the wander lists
        

    def download_pics_from_page(self,images_links,path,naming_string):
        """
        downloads actual images using the links collected in images_links, and gives them a name
        using the nameing_string congatinated with a number in a path

        + images_list : list im images links
        + path : path to directory of downloaded images
        + naming_string : a name for naming files concatinating with a number


        
        """
       
        count =0 # counter to generate a number to be concatenated with the filename

        # check if path exists
        if os.path.exists(path):
            # loop through images links 
            for img_link in images_links:
                # give them a proper filename+counter numberand .jpg file extension
                save_file_name = os.path.join(path,naming_string+f"_{count}_"+"jpg")
                # downlad the file with wget(link, full_path_to_file)
                wget.download(img_link,save_file_name)
                # increment counter
                count+=1 
        else:
            print("\n\n\n[-] directory to path does not exist, please create one ...\n\n\n")




####### MAIN TESTING PROGRAM ##########
# bot = Bot("chrome",username,password)
# bot.find("#plymouthroadrunner")
# # # # # bot.find("nasser_b_o")
# posts, images = bot.get_posts(10)

# bot.download_pics_from_page(images,"./plymouthroadrunner","Roady")

