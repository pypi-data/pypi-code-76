import sys
import argparse
from time import sleep
import json
from os import path, chdir, getcwd

curr_dir = getcwd()
data_path= 'data'
store = path.join(curr_dir, data_path)

def version():
    print("Version 1.0.1")

def getData():
    global store
    chdir(store)
    with open('data.txt', 'r') as readFile:
        data = json.load(readFile)

    return data

def display():
    global store
    chdir(store)
    if(path.exists("data.txt")):

        dataDict = getData()
        print("got data, printing:   ")
        sleep(1)

        # Print the names of the columns.
        print ("{:<10} {:<10}".format('NAME', 'DESCRIPTION'))

        # print each data item. 
        for key, value in dataDict.items():
            name, desc = key, value
            desc = desc.replace("\n", "\n\t   ")
            print ("{:<10} {:<10}".format(name, desc))


    else:
        print("File does not exist. create new entry.")

def newEntry():

    global store
    name = input("Enter project name: ")
    detail = input("Enter project description: ")
    msg = sys.stdin.readlines()
    desc = ''.join(msg)
    print("Writing to files ... ")
    sleep(0.5)

    chdir(store)
    if(path.exists("data.txt")):
        dataDict = getData()
    else:
        dataDict = {}

    dataDict[name] = desc

    with open("data.txt", "w") as header:
        json.dump(dataDict, header)


#parser = argparse.ArgumentParser(description="Commands to add/display projects.")
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

parser_display = subparsers.add_parser('display', help='Display entries')
parser_display.set_defaults(func=display)

parser_new = subparsers.add_parser('new', help='Add new entries')
parser_new.set_defaults(func=newEntry)

parser_new = subparsers.add_parser('version', help='Display version')
parser_new.set_defaults(func=version)

#parser.add_argument("-v", "--version", help="show program version", action="store_true")
#parser.add_argument('-n', '--new', help='Add new entries', action="store_true")
#parser.add_argument('-d', '--display', help='Display entries', action="store_true")



if len(sys.argv) <= 1:
    sys.argv.append('--help')

options = parser.parse_args()
# Run the appropriate function (in this case display or new)
options.func()

#if options.version:
#    print("This is myprogram version 0.1")
#elif options.new:
#    newEntry()
#elif options.display:
#    display()
