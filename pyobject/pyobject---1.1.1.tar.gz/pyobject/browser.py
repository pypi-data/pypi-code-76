"以图形方式浏览Python对象的模块。"
import sys,os
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
from inspect import isfunction,ismethod,isgeneratorfunction,isgenerator,iscode
try: from . import objectname,_shortrepr
# (ImportError,SystemError): 修复Python 3.4的bug
except (ImportError,SystemError):from __init__ import objectname,_shortrepr

_IMAGE_PATH=(os.path.split(__file__)[0]+"\images")

class ScrolledTreeview(ttk.Treeview):
    "可滚动的Treeview控件,继承自ttk.Treeview。"
    def __init__(self,master,**options):
        self.frame=tk.Frame(master)
        ttk.Treeview.__init__(self,self.frame,**options)
        
        self.hscroll=ttk.Scrollbar(self.frame,orient=tk.HORIZONTAL,
                                   command=self.xview)
        self.vscroll=ttk.Scrollbar(self.frame,command=self.yview)
        self["yscrollcommand"]=self.vscroll.set
        self.vscroll.pack(side=tk.RIGHT,fill=tk.Y)
        ttk.Treeview.pack(self,side=tk.BOTTOM,expand=True,fill=tk.BOTH)     
    def pack(self,**options):
        self.frame.pack(**options)
    def grid(self,**options):
        self.frame.grid(**options)
    def place(self,**options):
        self.frame.place(**options)

class ObjectBrowser():
    title="Python对象浏览器"
    obj_image=None
    def __init__(self,master,obj,verbose=False,name='obj'):
        self.master=master
        self.verbose=verbose
        self.name=name

        self.master.title(self.title)
        try:
            self.master.iconbitmap(_IMAGE_PATH+r"\python.ico")
        except tk.TclError:pass
        self.create_widgets()
        self.load_image()
        self.browse(obj)
    def create_widgets(self):
        "创建控件"
        tk.Label(self.master,text=" 路径: "+self.name,
                 anchor="w").pack(fill=tk.X)
        self.tvw=ScrolledTreeview(self.master,column='.')
        self.tvw.pack(expand=True,fill=tk.BOTH)
        self.tvw.heading("#0",text="属性")
        self.tvw.heading("#1",text="值")
        self.tvw.bind("<Double-Button-1>",self.on_doubleclick)
        self.tvw.tag_configure("error",foreground="red")

        self.functions=self.tvw.insert('',index=0,text="函数、方法")
        self.attributes=self.tvw.insert('',index=1,text="属性")
        self.classes=self.tvw.insert('',index=2,text="类")
    def load_image(self):
        "加载images文件夹下的图片。"
        self.obj_image=tk.PhotoImage(master=self.master,
                                     file=_IMAGE_PATH+r"\python.gif")
        self.num_image=tk.PhotoImage(master=self.master,
                                     file=_IMAGE_PATH+r"\number.gif")
        self.str_image=tk.PhotoImage(master=self.master,
                                     file=_IMAGE_PATH+r"\string.gif")
        self.list_image=tk.PhotoImage(master=self.master,
                                     file=_IMAGE_PATH+r"\list.gif")
        self.empty_list_image=tk.PhotoImage(master=self.master,
                                     file=_IMAGE_PATH+r"\empty_list.gif")
        self.tuple_image=tk.PhotoImage(master=self.master,
                                     file=_IMAGE_PATH+r"\tuple.gif")
        self.empty_tuple_image=tk.PhotoImage(master=self.master,
                                     file=_IMAGE_PATH+r"\empty_tuple.gif")
        self.dict_image=tk.PhotoImage(master=self.master,
                                     file=_IMAGE_PATH+r"\dict.gif")
        self.empty_dict_image=tk.PhotoImage(master=self.master,
                                     file=_IMAGE_PATH+r"\empty_dict.gif")
        self.func_image=tk.PhotoImage(master=self.master,
                                     file=_IMAGE_PATH+r"\function.gif")
        self.code_image=tk.PhotoImage(master=self.master,
                                     file=_IMAGE_PATH+r"\codeobject.gif")
    def _get_image(self,obj):
        if isinstance(obj,int) or isinstance(obj,float):
            return self.num_image
        elif isinstance(obj,str):
            return self.str_image
        elif isinstance(obj,list):
            return self.list_image if len(obj) else self.empty_list_image
        elif isinstance(obj,tuple):
            return self.tuple_image if len(obj) else self.empty_tuple_image
        elif isinstance(obj,dict):
            return self.dict_image if len(obj) else self.empty_dict_image
        elif isinstance(obj,tuple):
            return self.tuple_image if len(obj) else self.empty_tuple_image
        elif isfunction(obj) or ismethod(obj):
            return self.func_image
        elif iscode(obj):
            return self.code_image
        else:return self.obj_image
    def _get_type(self,obj):
        if isfunction(obj) or ismethod(obj):
            return self.functions
        elif isinstance(obj,type):
            return self.classes
        else:return self.attributes
    def browse(self,obj):
        "浏览一个对象(obj)。"
        self.obj=obj
        self.master.title("{} - {}".format(self.title,objectname(obj)))
        self.attrs=dir(obj)

        for i in range(len(self.attrs)):
            attr=self.attrs[i]
            if self.verbose or not attr.startswith("_"):
                try:
                    object=getattr(obj,attr)
                    value=_shortrepr(object)
                    image=self._get_image(object)
                    tag_name=''
                except Exception as err:
                    value='<{}!>'.format(type(err).__name__)
                    tag_name="error";image=self.obj_image
                else:
                    self.tvw.insert(self._get_type(object), index=i,
                                text=attr, image=image,
                                values=(value,), tag=tag_name)
        if isinstance(obj,dict):
            pass
    def on_doubleclick(self,event):
        #当Treeview被双击时,进一步浏览该属性下的对象。

        #selection为一个元组,以('Hxxx',)的形式表示
        for selection in self.tvw.selection():
            attr=self.tvw.item(selection)["text"]
            obj=getattr(self.obj,attr)
            name=self.name+"."+attr
            browse(obj,self.verbose,name)

def browse(object,verbose=False,name="obj"):
    """以图形方式浏览一个Python对象。
verbose:与describe相同,是否打印出对象的特殊方法(如__init__)"""
    root=tk.Tk()
    ObjectBrowser(root,object,verbose,name)
    root.mainloop()

def test():
    browse(ObjectBrowser,verbose=True)

if __name__=="__main__":test()
