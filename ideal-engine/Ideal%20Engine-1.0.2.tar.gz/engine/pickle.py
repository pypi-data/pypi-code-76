import sys
import argparse
from time import sleep
import json
import pickle
from os import path


def getData():
    with open('title.txt', 'rb') as readTitle:
        titleList = pickle.load(readTitle)
        readTitle.close()

    with open('bio.txt', 'rb') as readBio:
        bioList = pickle.load(readBio)
        readBio.close()

    print(titleList)

    return titleList, bioList

def display():
    if(path.exists("title.txt")):

        title, bio = getData()
        print("Retrieving Data ...")
        sleep(1)
        print(title)

        for _ in range(len(title)):
            print(str(_) + ". Title: " + title[_])
            print(str(_) + ". Details: " + bio[_])

    else:
        print("File does not exist. create new entry.")

def newEntry():
    if(path.exists("title.txt")):
        title, bio = getData()
    else:
        title = []
        bio = []
    name = input("Enter project name: ")
    detail = input("Enter project description: ")
    msg = sys.stdin.readlines()
    desc = '\t'.join(msg)

    print("Writing to files ... ")
    sleep(1)
    title.append(name)
    bio.append(desc)

    with open("title.txt", "ab+") as header:
        pickle.dump(title, header)
        header.close()

    with open("bio.txt", "ab+") as footer:
        pickle.dump(bio, footer)
        footer.close()


parser = argparse.ArgumentParser(description="Commands to add/display projects.")
#parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

#parser_display = subparsers.add_parser('display', help='Display entries')
#parser_display.set_defaults(func=display)

#parser_new = subparsers.add_parser('new', help='Add new entries')
#parser_new.set_defaults(func=newEntry)

parser.add_argument("-v", "--version", help="show program version", action="store_true")
parser.add_argument("-n", "--new", help='Add new entries', action="store_true")
parser.add_argument("-d", "--display", help='Display entries', action="store_true")



if len(sys.argv) <= 1:
    sys.argv.append('--help')

options = parser.parse_args()
# Run the appropriate function (in this case display or new)
#options.func()

if options.version:
    print("This is myprogram version 0.1")
elif options.new:
    newEntry()
elif options.display:
    display()

