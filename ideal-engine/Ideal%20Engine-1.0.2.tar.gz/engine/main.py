import sys
from time import sleep
import json
from os import path, chdir, getcwd

curr_dir = getcwd()
data_path= 'data'
store = path.join(curr_dir, data_path)


def getData():
    global store
    chdir(store)
    with open('data.txt', 'r') as readFile:
        data = json.load(readFile)

    return data

def display():
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

    name = input("Enter project name: ")
    detail = input("Enter project description: ")
    msg = sys.stdin.readlines()
    desc = ''.join(msg)
    print("Writing to files ... ")
    sleep(0.5)

    if(path.exists("data.txt")):
        dataDict = getData()
    else:
        dataDict = {}

    dataDict[name] = desc

    with open("data.txt", "w") as header:
        json.dump(dataDict, header)
