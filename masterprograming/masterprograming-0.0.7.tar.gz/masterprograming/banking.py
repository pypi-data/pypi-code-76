from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox

# functions
def action():
	Information = {
	'Account':37098100000016,
	'Name':'Danish Ali',
	'Amount':10000,
	'Mobile':8534867764,
	'Others':'Students'
	}

	def clear():
		ac.delete(0,END)
		name.delete(0,END)
		amount.delete(0,END)
		mobile.delete(0,END)
		others.delete(0,END)

	if ac.get()=="":
			messagebox.showerror("Error" , "Enter Account Number" , parent = des)
	else:
		for i in Information.items():
			if int(ac.get()) == Information['Account'] and len(ac.get()) == 14:
				messagebox.showinfo("Success" , "Successfully Find Account Number" , parent = des)
				data_name = Information['Name']
				data_amount = Information['Amount']
				data_mobile = Information['Mobile']
				data_others = Information['Others']


				name = Label(des , text = "Name :" , font = 'sans-serif 14 bold',bg="#CD5C5C")
				name.place(x=200, y=160,anchor='e')

				amount = Label(des , text = "Amount :" , font = 'sans-serif 14 bold',bg="#CD5C5C")
				amount.place(x=200 , y=220,anchor='e')

				mobile = Label(des , text = "Mobile No :" , font = 'sans-serif 14 bold',bg="#CD5C5C")
				mobile.place(x=200 , y=280,anchor='e')

				funds = Label(des , text = "Source Of Funds :" , font = 'sans-serif 14 bold',bg="#CD5C5C")
				funds.place(x=200 , y=330,anchor='e')

				others = Label(des , text = "Others :" , font = 'sans-serif 14 bold',bg="#CD5C5C")
				others.place(x=200 , y=470,anchor='e')

				name = Entry(des, bd=5,width=40,font = 'sans-serif 14 bold', textvariable = name)
				name.place(x=220 , y= 144)
				name.insert(0,data_name)

				amount = Entry(des, bd=5,width=40,font = 'sans-serif 14 bold', textvariable = amount)
				amount.place(x=220 , y= 205)
				amount.insert(0,data_amount)

				mobile = Entry(des, bd=5,width=40,font = 'sans-serif 14 bold', textvariable = mobile)
				mobile.place(x=220 , y= 262)
				mobile.insert(0,data_mobile)



				Radio_button_sal = Radiobutton(des,text='Salary', value="salary",font = 'sans-serif 10 bold',variable = var)
				Radio_button_sal .place(x= 220 , y= 320)
				var.set('salary')

				Radio_button_vah = Radiobutton(des,text='Vahical Sale', value="vahical",font = 'sans-serif 10 bold',variable = var)
				Radio_button_vah .place(x= 220 , y= 350)

				Radio_button_pro = Radiobutton(des,text='Property Sale', value="property",font = 'sans-serif 10 bold',variable = var)
				Radio_button_pro .place(x= 220 , y= 380)

				Radio_button_others = Radiobutton(des,text='Others', value="others",font = 'sans-serif 10 bold',variable = var)
				Radio_button_others .place(x= 220 , y= 410)

				others = Entry(des, bd=5,width=40,font = 'sans-serif 14 bold', textvariable = others)
				others.place(x=220 , y= 455)
				others.insert(0,data_others)

				clear = Button(des, text = "Clear" ,font='Verdana 13 bold', command = clear)
				clear.place(x=760, y=85)
				break				
			else:
				messagebox.showerror("Error" , "Enter Correct Account Number" , parent = des)
				break
					


def scan():
	des = Tk()
	des.title("Demo Details")	
	des.maxsize(width=600 ,  height=300)
	des.minsize(width=600 ,  height=300)
	# des.iconbitmap('icon.jpg')
	des.config(bg='green')	
	ac_no = Label(des , text = "Demo Account No : 37098100000016" , font = 'sans-serif 20 bold',bg="#CD5C5C")
	ac_no.place(x=550 , y=140,anchor='e')


def disable_event():
    pass	

def cancel():
	messagebox.showinfo("Cancel" , "All Services Cancel" , parent = des)

# functions end

des = Tk()
des.title("Banking Software")	
des.maxsize(width=1200 ,  height=600)
des.minsize(width=1200 ,  height=600)
# des.iconbitmap('icon.jpg')
des.config(bg='yellow')	

# des.protocol("WM_DELETE_WINDOW", disable_event)


f=Frame(des,height=580,width=1180,bg='#CD5C5C')
f.place(x=10,y=10)


ac = StringVar()
name = StringVar()
amount = IntVar(des, value='0')
var= StringVar()
mobile = StringVar()
others = StringVar()

 # Label Name Start 
ac_no = Label(des , text = "Account No :" , font = 'sans-serif 14 bold',bg="#CD5C5C")
ac_no.place(x=200 , y=100,anchor='e')	



 # Label Name End

 # Entry Box Start
ac = Entry(des, bd=5,width=40,font = 'sans-serif 14 bold',textvariable = ac)
ac.focus()
ac.place(x=220 , y= 85)


# Entry Box End


# frame

a=Frame(des,height=1,width=240,bg="white")
a.place(x=880,y=120)

b=Frame(des,height=330,width=1,bg="white")
b.place(x=880,y=120)

c=Frame(des,height=1,width=240,bg="white")
c.place(x=880,y=450)

d=Frame(des,height=330,width=1,bg="white")
d.place(x=1120,y=120)




# Button Start

enter = Button(des, text = "Enter" ,font='Verdana 13 bold', command = action)
enter.place(x=680, y=85)




scan = Button(des, text = "Demo Details" ,font='Verdana 13 bold', width=12, height=6,  command = scan)
scan.place(x=930, y=130)

cancel = Button(des, text = "Cancel" ,font='Verdana 13 bold', width=12, height=6,  command = cancel)
cancel.place(x=930, y=295)

des.mainloop()