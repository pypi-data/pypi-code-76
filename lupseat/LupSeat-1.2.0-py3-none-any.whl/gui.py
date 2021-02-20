import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk, messagebox
from tkinter.filedialog import askopenfilename, askdirectory
from time import time
import random
import os

default_bg = "#D0D0D0"
basic_margin = 25

def set_student_fname():
    global student_file
    global stdt_row
    student_file = askopenfilename()
    tk.Label(text=os.path.basename(student_file), font=tkFont.Font(size=15), bg=default_bg).grid(row=stdt_row, column=1, sticky="W", padx=basic_margin)

def set_room_fname():
    global room_file
    global room_row
    room_file = askopenfilename()
    tk.Label(text=os.path.basename(room_file), font=tkFont.Font(size=15), bg=default_bg).grid(row=room_row, column=1, sticky="W", padx=basic_margin)

def set_output_dir():
    global output_dir
    global output_row
    output_dir = askdirectory()
    if not os.path.isdir(output_dir):
        tk.Label(text="Error, directory not selected", font=tkFont.Font(size=15), bg=default_bg).grid(row=output_row, column=1, sticky="W", padx=basic_margin)
        output_dir = "./"
    else:
        tk.Label(text=os.path.basename(output_dir), font=tkFont.Font(size=15), bg=default_bg).grid(row=output_row, column=1, sticky="W", padx=basic_margin)

def close_gui():
    global window
    window.destroy()

def regenerate_seed():
    global seed
    random.seed(seed.get())
    seed.set(random.randint(0, 2**63-1))

# Used to track row number
# (Manually updating each row number got tedious)
class Counter:
    count = -1
    def inc(self):
        self.count += 1
        return self.count

    def same(self):
        return self.count


def start_gui(args):
    global window
    global student_file, room_file, output_dir
    global stdt_row, room_row, output_row
    global seed

    window = tk.Tk()
    window.title("LupSeat")
    window.configure(background=default_bg)

    output_dir = "./"
    student_file = args.student
    room_file = args.seats
    csv_chart_name = tk.StringVar(value=args.out)
    graphic_chart_name = tk.StringVar(value=args.g_chart)
    graphic_chart_size = tk.StringVar(value=args.g_chart_size)
    graphic_room_name = tk.StringVar(value=args.g_room)
    graphic_room_size = tk.StringVar(value=args.g_room_size)
    format_string = tk.StringVar(value=args.fmt)
    seed = tk.StringVar(value=args.seed)
    sort_by = tk.StringVar(value=args.sort_by)
    algorithm = tk.StringVar(value=args.algorithm)

    c = Counter()

    tk.Label(text="LupSeat", font=tkFont.Font(size=30), bg=default_bg).grid(row=c.inc(), column=0, columnspan=3, padx=30, pady=30)

    # INPUT
    tk.Label(text="Input Settings", font=tkFont.Font(size=20), bg=default_bg).grid(row=c.inc(), column=0, padx=basic_margin, pady=5, sticky="W")
    tk.ttk.Separator(window, orient="horizontal").grid(row=c.inc(), column=0, columnspan=3, sticky='we')

    tk.ttk.Button(text="Set student file", command=set_student_fname).grid(row=c.inc(), column=0, padx=basic_margin, pady=5, sticky="W")
    stdt_row = c.same()
    tk.ttk.Button(text="Set room layout file", command=set_room_fname).grid(row=c.inc(), column=0, padx=basic_margin, pady=5, sticky="W")
    room_row = c.same()

    window.grid_rowconfigure(c.inc(), minsize=25)

    # OUTPUT
    tk.Label(text="Output Settings", font=tkFont.Font(size=20), bg=default_bg).grid(row=c.inc(), column=0, padx=basic_margin, pady=5, sticky="W")
    tk.ttk.Separator(window, orient="horizontal").grid(row=c.inc(), column=0, padx=basic_margin, columnspan=3, sticky='we')

    tk.ttk.Button(text="Set output directory", command=set_output_dir).grid(row=c.inc(), column=0, padx=basic_margin, pady=5, sticky="W")
    output_row = c.same()

    tk.Label(text="CSV chart name", font=tkFont.Font(size=15), bg=default_bg).grid(row=c.inc(), column=0, padx=basic_margin, pady=5, sticky="W")
    tk.Entry(textvariable=csv_chart_name).grid(row=c.same(), column=1)

    tk.Label(text="Graphic chart name/size", font=tkFont.Font(size=15), bg=default_bg).grid(row=c.inc(), column=0, padx=basic_margin, pady=5, sticky="W")
    tk.Entry(textvariable=graphic_chart_name).grid(row=c.same(), column=1, padx=basic_margin)
    tk.Entry(textvariable=graphic_chart_size).grid(row=c.same(), column=2, padx=basic_margin)

    tk.Label(text="Graphic room name/size", font=tkFont.Font(size=15), bg=default_bg).grid(row=c.inc(), column=0, padx=basic_margin, pady=5, sticky="W")
    tk.Entry(textvariable=graphic_room_name).grid(row=c.same(), column=1, padx=basic_margin)
    tk.Entry(textvariable=graphic_room_size).grid(row=c.same(), column=2, padx=basic_margin)

    tk.Label(text="Image size can be specified with standard paper size formats (e.g. A2). Add keyword \"flip\" to switch horizontal and vertical orientation", 
            font=tkFont.Font(size=10), bg=default_bg).grid(row=c.inc(), column=0, padx=basic_margin, pady=5, columnspan=3, sticky="W")

    window.grid_rowconfigure(c.inc(), minsize=25)

    # ADVANCED SETTINGS
    tk.Label(text="Advanced Settings", font=tkFont.Font(size=20), bg=default_bg).grid(row=c.inc(), column=0, padx=basic_margin, pady=5, sticky="W")
    tk.ttk.Separator(window, orient="horizontal").grid(row=c.inc(), column=0, columnspan=3, sticky='we')

    tk.Label(text="Format String", font=tkFont.Font(size=15), bg=default_bg).grid(row=c.inc(), column=0, padx=basic_margin, pady=5, sticky="W")
    tk.Entry(textvariable=format_string).grid(row=c.same(), column=1, padx=basic_margin)
    tk.Label(text="Variables: sid, fname, lname. Can be sliced with form {fname|0,5} for the first 6 letters", 
            font=tkFont.Font(size=10), bg=default_bg).grid(row=c.inc(), column=0, padx=basic_margin, pady=5, columnspan=3, sticky="W")

    tk.Label(text="Sort Output By", font=tkFont.Font(size=15), bg=default_bg).grid(row=c.inc(), column=0, padx=basic_margin, pady=5, sticky="W")
    tk.OptionMenu(window, sort_by, "fname", "lname", "sid", "seat").grid(row=c.same(), column=1, padx=basic_margin + 25, sticky="W")

    tk.Label(text="Seed", font=tkFont.Font(size=15), bg=default_bg).grid(row=c.inc(), column=0, padx=basic_margin, pady=5, sticky="W")
    tk.Entry(textvariable=seed).grid(row=c.same(), column=1, padx=basic_margin)
    tk.ttk.Button(text="Generate new seed", command=regenerate_seed).grid(row=c.same(), column=2, padx=basic_margin, sticky="W")

    tk.Label(window, text="Choose the algorithm", font=tkFont.Font(size=15), bg=default_bg).grid(row=c.inc(), column=0, padx=basic_margin, pady=5, sticky="W")
    tk.OptionMenu(window, algorithm, "consecdivide", "chunkincrease", "randomassign").grid(row=c.same(), column=1, padx=basic_margin + 25, sticky="W")

#    tk.Radiobutton(window, text="ConsecDivide", variable=algorithm, value="consecdivide", bg=default_bg).grid(row=c.inc(), column=0, padx=20, sticky="W")
#    tk.Radiobutton(window, text="ChunkIncrease", variable=algorithm, value="chunkincrease", bg=default_bg).grid(row=c.inc(), column=0, padx=20, sticky="W")
#    tk.Radiobutton(window, text="RandomAssign", variable=algorithm, value="randomassign", bg=default_bg).grid(row=c.inc(), column=0, padx=20, sticky="W")

    window.grid_rowconfigure(c.inc(), minsize=25)

    # RUN PROGRAM
    s = tk.ttk.Style()
    s.configure('Run.TButton', font=('Helvetica', 18))
    tk.ttk.Button(text="Run Lupseat", command=close_gui, style="Run.TButton").grid(row=c.inc(), column=0, pady=30, columnspan=3)
    window.mainloop()

    # GET VARS
    [args.out, args.g_chart, args.g_chart_size, args.g_room, args.g_room_size, args.fmt, args.seed, args.algorithm, args.sort_by]= list(map(lambda x: x.get(), 
        [csv_chart_name, graphic_chart_name, graphic_chart_size, graphic_room_name, graphic_room_size, format_string, seed, algorithm, sort_by]))

    args.student = student_file
    args.seats = room_file
    args.out = os.path.join(output_dir, args.out)
    args.g_chart = os.path.join(output_dir, args.g_chart)
    args.g_room = os.path.join(output_dir, args.g_room)

    return args

def done_gui():
    window = tk.Tk()
    window.withdraw()
    tk.messagebox.showinfo(title="Lupseat", message="Lupseat Completed!")

