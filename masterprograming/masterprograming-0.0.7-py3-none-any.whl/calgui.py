from tkinter import *
import tkinter
top = tkinter.Tk()


top.geometry('250x250')
top.maxsize(width=250,height=180)
top.minsize(width=250,height=180)
top.title('Calculator')
top.configure(bg='red')

l= Label(top,text='My Calculator',fg='red').grid(row=0,column=1,sticky=W)
l1=Label(top,text='First Number',).grid(row=1,column=0,sticky=W)
l2=Label(top,text='Second Number',).grid(row=2,column=0,sticky=W)
l3=Label(top,text='Opeartor',).grid(row=3,column=0,sticky=W)
l4=Label(top,text='Answer',).grid(row=4,column=0,sticky=W)

E1= Entry(top,bd=5)
E1.grid(row=1,column=1)
E2= Entry(top,bd=5)
E2.grid(row=2,column=1)
E3= Entry(top,bd=5)
E3.grid(row=3,column=1)
E4= Entry(top,bd=5)
E4.grid(row=4,column=1)



def proces():
    number1=Entry.get(E1)
    number2=Entry.get(E2)
    operator=Entry.get(E3)
    number1=int(number1)
    number2=int(number2)
    if operator =="+":
        answer=number1+number2
    if operator =="-":
        answer=number1-number2
    if operator=="*":
        answer=number1*number2
    if operator=="/":
        answer=number1/number2
    Entry.insert(E4,0,answer)
    print(answer)


B=Button(top, text ="Submit",command = proces,bg='yellow').grid(row=5,column=1,)

top.mainloop()