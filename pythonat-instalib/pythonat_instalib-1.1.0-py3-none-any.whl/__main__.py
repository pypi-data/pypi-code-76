from pyinstatool import *
import sys


def main():
    if len(sys.argv) ==0:
        username = input("username : ")
        password = input("password : ")
        search_query = input("searching for : ")
        scrolls_number = int(input("scroll downs : "))

        bot = Bot("chrome",username,password)
        bot.find(search_query)
        posts, images = bot.get_posts(scrolls_number)
        bot.download_pics_from_page(images,f"./{search_query}","Roady")


if __name__ == '__main__':
    main()
    
