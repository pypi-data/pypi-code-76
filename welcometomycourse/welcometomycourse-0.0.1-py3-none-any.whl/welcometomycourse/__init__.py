def welcome():
    yourname = input("Please enter your name: ")

    if(len(yourname)>0):
        message = f'Hi {yourname},'
    else:
        message = 'Hi buddy,'

    print(message + ' Wishing you joy for my Python Journey in percept.ir/@k90mirzaei')
