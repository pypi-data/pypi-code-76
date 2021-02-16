# Print iterations progress
import time
flag=0
def printProgressBar (iteration, total, boundary_percent, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    # print(percent)
    if iteration == total or boundary_percent<float(percent):
        global flag
        flag=1
        print()
        pass
    else:
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
        
        

def main():
    global flag 
    items = list(range(0, 100))
    l = len(items)

    printProgressBar(0, l,70.0, prefix = 'Python:    ', suffix = ' ', length = 50)
    for i, item in enumerate(items):
        time.sleep(0.03)
        if not flag:
            printProgressBar(i + 1,l,70.0,prefix = 'Python:    ', suffix = ' ', length = 50)
        else:
            print()
            break
        
    flag=0
    printProgressBar(0, l,80.0, prefix = 'React JS:  ', suffix = ' ', length = 50)
    for i, item in enumerate(items):
        time.sleep(0.03)
        if not flag:
            printProgressBar(i + 1,l,80.0,prefix = 'React JS:  ', suffix = ' ', length = 50)
        else:
            print()
            break
        
    flag=0
    printProgressBar(0, l,35.0, prefix = 'C++:       ', suffix = ' ', length = 50)
    for i, item in enumerate(items):
        time.sleep(0.03)
        if not flag:
            printProgressBar(i + 1,l,35.0,prefix = 'C++:       ', suffix = ' ', length = 50)
        else:
            print()
            break
        
    flag=0
    printProgressBar(0, l,50.0, prefix = 'Docker:    ', suffix = ' ', length = 50)
    for i, item in enumerate(items):
        time.sleep(0.03)
        if not flag:
            printProgressBar(i + 1,l,50.0,prefix = 'Docker:    ', suffix = ' ', length = 50)
        else:
            print()
            break
        
    flag=0
    printProgressBar(0, l,60.0, prefix = 'Javascript:', suffix = ' ', length = 6)
    for i, item in enumerate(items):
        time.sleep(0.03)
        if not flag:
            printProgressBar(i + 1,l,60.0,prefix = 'Javascript:', suffix = ' ', length = 50)
        else:
            print()
            break
        
    flag=0
    printProgressBar(0, l,50.0, prefix = 'Node JS:   ', suffix = ' ', length = 50)
    for i, item in enumerate(items):
        time.sleep(0.03)
        if not flag:
            printProgressBar(i + 1,l,50.0,prefix = 'Node JS:   ', suffix = ' ', length = 50)
        else:
            print()
            break

    flag=0
    printProgressBar(0, l,50.0, prefix = 'Flutter:   ', suffix = ' ', length = 50)
    for i, item in enumerate(items):
        time.sleep(0.03)
        if not flag:
            printProgressBar(i + 1,l,50.0,prefix = 'Flutter:   ', suffix = ' ', length = 50)
        else:
            print()
            break
