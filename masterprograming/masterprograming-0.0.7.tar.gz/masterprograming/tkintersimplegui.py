import tkinter as tk
from tkinter import ttk
root=tk.Tk()
root.title("Testing GUI")
root.geometry('300x200')
root.configure(background='red')

welcome=ttk.Label(root, text='Welcome TO Our College From',width=-18,background='blue',)
welcome.grid(sticky=tk.N)

name_label=ttk.Label(root, text='Enter Your Name', background='#00ff00')
name_label.focus()
name_label.grid(row=1, column=0, sticky=tk.W)


email_label=ttk.Label(root, text='Enter Your Email', background='#00ffff')
email_label.grid(row=2, column=0, sticky=tk.W)

age_label=ttk.Label(root, text='Enter Your Age', background='#fffff0')
age_label.grid(row=3, column=0, sticky=tk.W)

clas_label=ttk.Label(root, text='Enter Your Class', background='#00fff0')
clas_label.grid(row=4, column=0, sticky=tk.W)

gender_label=ttk.Label(root, text='Select Gender', background='#fff0ff')
gender_label.grid(row=5, column=0, sticky=tk.W)


#Entry Box

name_var=tk.StringVar()
name_box=ttk.Entry(root, width=18 , textvariable=name_var )
name_box.grid(row=1, column=1)

email_var=tk.StringVar()
email_box=ttk.Entry(root, width=18 , textvariable=email_var )
email_box.grid(row=2, column=1)


age_var=tk.StringVar()
age_box=ttk.Entry(root, width=18 , textvariable=age_var )
age_box.grid(row=3, column=1)


clas_var=tk.IntVar()
clas_box=ttk.Entry(root, width=18 , textvariable=clas_var )
clas_box.grid(row=4, column=1)

gender_var=tk.StringVar()
gender_box=ttk.Combobox(root, width=15,textvariable=gender_var, state='readonly')
gender_box['values']=('Male','Female','Other')
gender_box.current(0)
gender_box.grid(row=5,column=1)

radio_var=tk.StringVar()
radio_bu=ttk.Radiobutton(root,text='Student', value='Student', variable=radio_var)
radio_bu.grid(row=6,column=0)


radio_bu1=ttk.Radiobutton(root,text='Teacher', value='Teacher' , variable=radio_var)
radio_bu1.grid(row=6,column=1)

check_box=tk.IntVar()
check_s=ttk.Checkbutton(root,text='Subscribe Our Channel', variable=check_box)
check_s.grid(row=7,column=0)

def action():
    username=name_var.get()
    userage=age_var.get()
    useremail=email_var.get()
    userclas=clas_var.get()
    usergander=gender_var.get()
    usertype=radio_var.get()
    if check_box.get() == 0:
        subscribe='NO'
    else:
        subscribe='YES'

    print(f'Your Name is {username}')
    print(f'Your Age is {userage}')
    print(f'Your Email is {useremail}')
    print(f'Your Class is {userclas}')
    print(f'Your Gender Is {usergander}')
    print(f'Subscribe {subscribe}')
    print(f'User Type {usertype}')
    with open('file.txt', 'a') as f:
        f.write(f'Name {username} \n Age {userage} \n Email {useremail} \n Class {userclas} \n Gender {usergander} \n Channel {subscribe}\n User type {usertype}\n')
button=ttk.Button(root, text='Sumbit',width=18, command=action)
button.grid(row=8, column=0)
root.mainloop()