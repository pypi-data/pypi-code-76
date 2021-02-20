from browser import html, document,ajax
from visualife.utils.text_utils import substitute_template

tooltip_style = {
    'backgroundColor': 'black',
    'color': '#fff',
    'textAlign': 'center',
    'padding': '5px 0px',
    'borderRadius': '6px',
    'visibility': 'hidden',
    'position': 'fixed'
}

def run_async_func(function,url="http://0.0.0.0:8000/"):
    ajax.get(url,oncomplete=function)


def create_tooltip(id_text, tooltip_text, width, height):
    """Creates DIV with tooltip and returns it"""
    tooltip = html.DIV(tooltip_text, id=id_text,
                       style={**tooltip_style, 'height': height, 'width': width})
    return tooltip


class MenuWidget:
    __menu_style = """
        .three_dots:after {
            content: '\\2807';
            font-size: 1.5em;
        }
        .box-shadow-menu {
          position: relative;
          padding-left: 1.25em;
        }
        .box-shadow-menu:before {
          content: "";
          position: absolute;
          left: 0;
          top: 0.25em;
          width: 1em;
          height: 0.15em;
          background: black;
          box-shadow: 
            0 0.25em 0 0 black,
            0 0.5em 0 0 black;
        }

.Menu div ul li {
    width: 30px;
    background-color: white;
}

.Menu ul ul li { width: {%width%}px; }

.Menu span.dropBottom, span.dropRight {
    display: block;
    box-shadow: inset 2px 0px 0px #222;
    position: absolute;
    left: 0px;
    width: 100%;
    height: 100%;
    top: 0px;
}

.Menu span.dropBottom {
    box-shadow: inset 0px 2px 0px #222;
    position: absolute;
    width: 100%;
    bottom: 0px;
}

/* exclude border from the top-most menu level */
div.Menu ul li { font-size: 120%; }
div.Menu ul li a { padding: 0px; }
div.Menu ul li span.dropBottom { box-shadow: inset 0px 0px 0px 0px; } 

.Menu ul {
    margin: 0;
    padding: 0;
    list-style: none;
}

.Menu ul ul {
    opacity: 0;
    position: absolute;
    top: 160%;
    visibility: hidden;
    transition: all .4s ease;
    -webkit-transition: all .4s ease;
}

.Menu ul ul ul { top: 0%; left: 160%; }

.Menu ul ul li:hover > ul {
    top: 0%;
    left: 100%;
    opacity: 1;
    visibility: visible;
}

.Menu ul li:hover > ul {
    opacity: 1; 
    background-color: rgba(255,255,255,0.8);
    top: 100%;
    visibility: visible;
    border: 1px solid gray;
}

.Menu ul li { 
    float: left; 
    position: relative; 
    background-color: rgba(255,255,255,0.8);
    cursor: pointer; 
    padding: 5px 15px;
    list-style: none;
}

.Menu ul ul li { float: none; }

.Menu ul a {
    text-decoration: none;  
    color: #000;
    padding: 10px 15px;
    text-align: center;
    font: 13px Tahoma, Sans-serif;
}

.Menu ul ul li:hover { background-color: rgba(200,200,200,0.8); }

    """

    def __init__(self, element_id, dict_of_menu_items={}, **kwargs):
        """Creates a HTML menu

        :param element_id: ID of a html DIV element that will contain this menu instance
        :param dict_of_menu_items: dictionary that contains the menu
        :param kwargs: see below

        :Keyword Arguments:
            * *style* (``string``) --
              style of "burger" icon: ``"burger`` or ``"dots"``
            * *width* (``int``) --
              width of menu in pixels
        """
        self.__element_id = element_id
        self.__dict_of_menu_items = dict_of_menu_items

        replacements = {"{%width%}": str(kwargs.get("width", 170))}
        document <= html.STYLE(substitute_template(MenuWidget.__menu_style, replacements))

        style = kwargs.get("style", "burger")
        self.__style = "three_dots" if style == "dots" else "box-shadow-menu"

        if self.__dict_of_menu_items:
            self.__create_widget()

        document[element_id].class_name += " Menu"

    def __create_widget(self):
        """ Remove the preious menu (if there is any) before creating a new one"""
        document[self.__element_id].innerHTML = ""

        ul1 = html.UL(id="ul-1-" + self.__element_id)
        li1 = MenuWidget.__create_item("", None, "dropBottom")
        li1.class_name = self.__style
        ul1 <= li1
        li1 <= MenuWidget.__create_list(self.__dict_of_menu_items)
        document[self.__element_id] <= ul1

    @staticmethod
    def __create_item(menu_item, callback, span_class=""):

        li = html.LI(style={"list-style": "none", "margin": "0px"})
        a = html.A(menu_item, id=menu_item, href="#")
        if callable(callback):
            a.bind("click", callback)
        li <= a
        if span_class != "":
            li <= html.SPAN(Class=span_class)

        return li

    @staticmethod
    def __create_list(menu_items):

        ul = html.UL()
        for item, callback_or_submenu in menu_items.items():
            if isinstance(callback_or_submenu, dict):
                li = MenuWidget.__create_item(item, None, "dropRight")
                li <= MenuWidget.__create_list(callback_or_submenu)
                ul <= li
            else:
                if callback_or_submenu == "": callback_or_submenu = None
                ul <= MenuWidget.__create_item(item, callback_or_submenu, "")

        return ul


    def add_menu_option(self,new_option,callback_or_submenu):
        """Adds option to the menu

        :param new_option: name od added option
        :param callback_or_submenu: function object ot a dictionary which has names of options 
        as a keys and callback_functions as values
        """
        if new_option in self.__dict_of_menu_items:
            print("Cannot add opion ",new_option,". Option already exists in Menu")
            exit()
        self.__dict_of_menu_items[new_option]=callback_or_submenu

    def update_menu(self):
        """Recalculates Menu with current dict_of_menu_items. Must be call after 
        add_menu_option() to iclude new options in MenuWidget.
        """
        self.__create_widget()

    def print_menu(self):
        """Prints current menu, print is included in a function so you don't need to call print 
        with this function
        """
        for opt in self.__dict_of_menu_items.keys():
            print(opt," : ")
            rest = self.__dict_of_menu_items[opt]
            if isinstance(rest, dict):
                for a in rest.keys():
                    print("\t",a," : ",rest[a])
            else:
                print(rest)

    def delete_option(self,option_to_delete):
        """Delete option from a Menu with all its suboptions
        """
        if option_to_delete not in self.__dict_of_menu_items:
            print("No option ",option_to_delete," in this menu")
            return False
        else:
            self.__dict_of_menu_items.pop(option_to_delete)


