'''
import tkinter 
from tkinter.messagebox import showinfo 
import windnd

def dragged_files(files):
    msg ='\n'.join((item.decode('gbk')for item in files))
    showinfo('您拖放的文件',msg)

tk = tkinter.Tk()
windnd.hook_dropfiles(tk,func=dragged_files)
tk.mainloop()
'''
from types import FunctionType

func_code = 'def dragged_files_{}(self, files): self.set_text(self.current_text_id, files[0].decode("gbk"))'.format("text1")
print(func_code)
foo_code = compile('def foo(x): x=x+"abc";return "bar"+x', "<string>", "exec")
foo_func = FunctionType(foo_code.co_consts[0], globals(), "foo")

print(foo_func("123"))


class CLanguage:
    a = 1
    b = 2
    def __init__ (self):
        self.name = "C语言中文网"
        self.add = "http://c.biancheng.net"
#通过类名调用__dict__
print(CLanguage.__dict__)

#通过类实例对象调用 __dict__
clangs = CLanguage()
print(clangs.__dict__)

func_code = 'def dragged_files_{}(self, files): self.set_text({}, files[0].decode("gbk"))'.format("56", "1234")
print(func_code)