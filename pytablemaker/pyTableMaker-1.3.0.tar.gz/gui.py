import tkinter as tk
import table as ptm
#* b_:      win.bind()
#* but_:    tk.Button
#* lsb_:    tk.ListBox
#* text:    tk.Text
#* msgbox:  tk.messagebox or tk.simpledialog


class Implementation:
    iTable: ptm.CustomTable  # has to be an instance doesn't have to be directly that cls but an extended cls/subcls/inherit
    def b_addCol(self, k=None):
        name = tk.simpledialog.askstring("New Column", "Type in the name for the new column")
        iTable.new_column(name)


mainwin = tk.Tk()
mainwin.title("Table Maker")
mainwin.geometry("800x600")


text_box = tk.Text(mainwin, font=tk.font.Font(family="Sans Mono", size=20))
but_addCol = tk.Button(mainwin, text="+")
but_delCol = tk.Button(mainwin, text="-")
but_addRow = tk.Button(mainwin, text="+")
but_delRow = tk.Button(mainwin, text="-")
lsb_rows = tk.Listbox(mainwin, width=200)




mainwin.mainloop()
