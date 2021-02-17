#!/usr/bin/env python
import wx
import wx.adv
from wx.lib.stattext import GenStaticText
import webbrowser

USER_API_KEY_URL = "https://trello.com/app-key"
OAUTH_URL = "URL"


def generate_oauth_session(api_key, api_secret):
    OAUTH_URL = api_key + ":" + api_secret


class Link(GenStaticText):
    def __init__(self, *args, **kw):
        super(Link, self).__init__(*args, **kw)

        self.font1 = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, True)
        self.font2 = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False)

        self.SetFont(self.font2)
        self.SetForegroundColour("#1B95E0")

        self.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouseEvent)
        self.Bind(wx.EVT_MOTION, self.OnMouseEvent)

    def SetUrl(self, url):

        self.url = url

    def OnMouseEvent(self, e):

        if e.Moving():

            self.SetCursor(wx.Cursor(wx.CURSOR_HAND))
            self.SetFont(self.font1)

        elif e.LeftUp():

            webbrowser.open(self.url)

        else:
            self.SetCursor(wx.NullCursor)
            self.SetFont(self.font2)

        e.Skip()


class TitledPage(wx.adv.WizardPageSimple):
    def __init__(self, parent, title):
        wx.adv.WizardPageSimple.__init__(self, parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        titleText = wx.StaticText(self, -1, title)
        # titleText.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.sizer.Add(titleText, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND | wx.ALL, 5)


class Page_One(wx.adv.WizardPageSimple):
    def __init__(self, parent, title):
        wx.adv.WizardPageSimple.__init__(self, parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        titleText = wx.StaticText(self, -1, title)
        # titleText.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        parapragh_text = wx.StaticText(
            self,
            -1,
            "Recuerde que antes de iniciar el proceso de obtención de credenciales\n"
            + "ud debe tener una cuenta en Trello y en el Aula Virtual, y deben estar\n"
            + "iniciadas las sesiones en el navegador predeterminado",
        )
        self.sizer.Add(titleText, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(parapragh_text)


class Page_Two(wx.adv.WizardPageSimple):
    def __init__(self, parent, title):
        wx.adv.WizardPageSimple.__init__(self, parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.first_line_subsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.second_line_subsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.third_line_subsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.sizer)
        titleText = wx.StaticText(self, -1, title)
        parapragh_text = wx.StaticText(
            self, -1, 'De clic en el siguiente enlace y luego copie la "Key" o "Tecla":'
        )
        link = Link(self, label="Enlace")
        link.SetUrl(USER_API_KEY_URL)
        api_key_text = wx.StaticText(
            self, -1, 'Por favor, introduzca el valor de "Tecla" o "Key":'
        )
        api_key_textctrl = wx.TextCtrl(self, -1)
        api_secret_text = wx.StaticText(
            self, -1, 'Por favor, introduzca el valor de "Secret":'
        )
        api_secret_textctrl = wx.TextCtrl(self, -1)
        # titleText.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.sizer.Add(titleText, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND | wx.ALL, 5)
        self.first_line_subsizer.Add(parapragh_text)
        self.first_line_subsizer.Add(link)
        self.second_line_subsizer.Add(api_key_text)
        self.second_line_subsizer.Add(api_key_textctrl)
        self.third_line_subsizer.Add(api_secret_text)
        self.third_line_subsizer.Add(api_secret_textctrl)
        self.sizer.Add(self.first_line_subsizer)
        self.sizer.Add(self.second_line_subsizer)
        self.sizer.Add(self.third_line_subsizer)


class Page_Three(wx.adv.WizardPageSimple):
    def __init__(self, parent, title):
        wx.adv.WizardPageSimple.__init__(self, parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        titleText = wx.StaticText(self, -1, title)
        # titleText.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.sizer.Add(titleText, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND | wx.ALL, 5)


class Page_Four(wx.adv.WizardPageSimple):
    def __init__(self, parent, title):
        wx.adv.WizardPageSimple.__init__(self, parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        titleText = wx.StaticText(self, -1, title)
        # titleText.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.sizer.Add(titleText, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND | wx.ALL, 5)


class PoliCalWizard:
    def __init__(self):
        wizard = wx.adv.Wizard(None, -1, "PoliCal")
        page1 = Page_One(wizard, "Bienvenido a PoliCal!")
        page2 = Page_Two(wizard, "Paso 1")
        page3 = Page_Three(wizard, "Paso 2")
        page4 = Page_Four(wizard, "Paso 3")
        # page1.sizer.Add(wx.StaticText(page1, -1, "Testing the wizard"))
        page4.sizer.Add(wx.StaticText(page4, -1, "This is the last page."))
        wx.adv.WizardPageSimple.Chain(page1, page2)
        wx.adv.WizardPageSimple.Chain(page2, page3)
        wx.adv.WizardPageSimple.Chain(page3, page4)
        wizard.FitToPage(page1)

        if wizard.RunWizard(page1):
            print("Success")


if __name__ == "__main__":
    app = wx.App()
    polical_wizard = PoliCalWizard()
