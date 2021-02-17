import wx
import sys
from wx.lib.stattext import GenStaticText
from requests_oauthlib import OAuth1Session
from requests_oauthlib.oauth1_session import TokenRequestDenied
import webbrowser

USER_API_KEY_URL = "https://trello.com/app-key"
REQUEST_TOKEN_URL = "https://trello.com/1/OAuthGetRequestToken"
AUTHORIZE_URL = "https://trello.com/1/OAuthAuthorizeToken"
ACCESS_TOKEN_URL = "https://trello.com/1/OAuthGetAccessToken"
CALENDAR_MOODLE_EPN_URL = (
    "https://educacionvirtual.epn.edu.ec/calendar/view.php?view=upcoming&course=1"
)


def generate_oauth_session(api_key, api_secret):
    # The following code is cannibalized from trello.util.create_oauth_token from the py-trello project.
    # Rewriting because it does not support opening the auth URLs using webbrowser.open and since we're using
    # click, a lot of the input methods used in that script are simplistic compared to what's available to us.
    # Thank you to the original authors!
    """Step 1: Get a request token. This is a temporary token that is used for
    having the user authorize an access token and to sign the request to obtain
    said access token."""
    session = OAuth1Session(client_key=api_key, client_secret=api_secret)
    try:
        response = session.fetch_request_token(REQUEST_TOKEN_URL)
    except TokenRequestDenied:
        print("Invalid API key/secret provided: {0} / {1}".format(api_key, api_secret))
        return ""
    resource_owner_key, resource_owner_secret = (
        response.get("oauth_token"),
        response.get("oauth_token_secret"),
    )
    """Step 2: Redirect to the provider. Since this is a CLI script we do not
    redirect. In a web application you would redirect the user to the URL
    below."""
    user_confirmation_url = "{AUTHORIZE_URL}?oauth_token={oauth_token}&scope={scope}&expiration={expiration}&name={name}".format(
        AUTHORIZE_URL=AUTHORIZE_URL,
        oauth_token=resource_owner_key,
        expiration="never",
        scope="read,write",
        name="PoliCal",
    )
    return user_confirmation_url, response


def obtain_access_token(oauth_verifier, api_key, api_secret, response):
    resource_owner_key, resource_owner_secret = (
        response.get("oauth_token"),
        response.get("oauth_token_secret"),
    )
    session = OAuth1Session(
        client_key=api_key,
        client_secret=api_secret,
        resource_owner_key=resource_owner_key,
        resource_owner_secret=resource_owner_secret,
        verifier=oauth_verifier,
    )
    access_token = session.fetch_access_token(ACCESS_TOKEN_URL)
    return access_token


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


########################################################################
class WizardPage(wx.Panel):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, parent, title=None):
        """Constructor"""
        wx.Panel.__init__(self, parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        if title:
            title = wx.StaticText(self, -1, title)
            # title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
            sizer.Add(title, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
            sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND | wx.ALL, 5)


########################################################################
class page_one(wx.Panel):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, parent, title=None):
        """Constructor"""
        wx.Panel.__init__(self, parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        if title:
            title = wx.StaticText(self, -1, title)
            # title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
            sizer.Add(title, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
            sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND | wx.ALL, 5)

        parapragh_text = wx.StaticText(
            self,
            -1,
            "Recuerde que antes de iniciar el proceso de obtención de credenciales\n"
            + "ud debe tener una cuenta en Trello y en el Aula Virtual, y deben estar\n"
            + "iniciadas las sesiones en el navegador predeterminado",
        )
        sizer.Add(parapragh_text)


########################################################################
class page_two(wx.Panel):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, parent, title=None):
        """Constructor"""
        wx.Panel.__init__(self, parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        if title:
            title = wx.StaticText(self, -1, title)
            # title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
            sizer.Add(title, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
            sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND | wx.ALL, 5)

        self.first_line_subsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.second_line_subsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.third_line_subsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(sizer)
        parapragh_text = wx.StaticText(
            self, -1, 'De clic en el siguiente enlace y luego copie la "Key" o "Tecla":'
        )
        link = Link(self, label="Enlace")
        link.SetUrl(USER_API_KEY_URL)
        api_key_text = wx.StaticText(
            self, -1, 'Por favor, introduzca el valor de "Tecla" o "Key":'
        )
        self.api_key_textctrl = wx.TextCtrl(self, -1)
        api_secret_text = wx.StaticText(
            self, -1, 'Por favor, introduzca el valor de "Secret":'
        )
        self.api_secret_textctrl = wx.TextCtrl(self, -1)
        # titleText.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.first_line_subsizer.Add(parapragh_text)
        self.first_line_subsizer.Add(link)
        self.second_line_subsizer.Add(api_key_text)
        self.second_line_subsizer.Add(self.api_key_textctrl)
        self.third_line_subsizer.Add(api_secret_text)
        self.third_line_subsizer.Add(self.api_secret_textctrl)
        sizer.Add(self.first_line_subsizer)
        sizer.Add(self.second_line_subsizer)
        sizer.Add(self.third_line_subsizer)


########################################################################
class page_three(wx.Panel):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, parent, title=None):
        """Constructor"""
        wx.Panel.__init__(self, parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        if title:
            title = wx.StaticText(self, -1, title)
            # title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
            sizer.Add(title, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
            sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND | wx.ALL, 5)

        self.first_line_subsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.second_line_subsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(sizer)
        parapragh_text = wx.StaticText(
            self,
            -1,
            "Visite la siguiente URL en su navegador web para autorizar a \nPoliCal acceso a su cuenta:",
        )
        self.link = Link(self, label="Enlace")
        verification_code_text = wx.StaticText(
            self,
            -1,
            "A continuación debe autorizar a PoliCal y luego\ndebe escribir el código de verificación: ",
        )
        self.verification_code_textctrl = wx.TextCtrl(self, -1)
        # titleText.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.first_line_subsizer.Add(parapragh_text)
        self.first_line_subsizer.Add(self.link)
        self.second_line_subsizer.Add(verification_code_text)
        self.second_line_subsizer.Add(self.verification_code_textctrl)
        sizer.Add(self.first_line_subsizer)
        sizer.Add(self.second_line_subsizer)


########################################################################
class page_four(wx.Panel):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, parent, title=None):
        """Constructor"""
        wx.Panel.__init__(self, parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        if title:
            title = wx.StaticText(self, -1, title)
            # title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
            sizer.Add(title, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
            sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND | wx.ALL, 5)

        self.first_line_subsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.second_line_subsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.third_line_subsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(sizer)
        parapragh_text = wx.StaticText(
            self,
            -1,
            'A continuación debe dar clic el enlace hacia el Aula Virtual,se le mostrará la opción\n"Proximos eventos para" donde deberá seleccionar "Todos los cursos"'
            + " luego desplácese\na la parte más inferior de la página y de clic en el Obtener URL del calendario.\n"
            + 'Después, en la opción "Exportar" seleccione todos los eventos y en "para" seleccione los\n60 días recientes y próximos.\n'
            + "Finalmente de clic en el boton Obtener URL del calendario.",
        )
        previus_message = wx.StaticText(
            self,
            -1,
            "Recuerde ingresar e iniciar sesion en ",
        )
        previus_link = Link(self, label="https://educacionvirtual.epn.edu.ec/")
        previus_link.SetUrl("https://educacionvirtual.epn.edu.ec/")
        self.first_line_subsizer.Add(previus_message)
        self.first_line_subsizer.Add(previus_link)
        self.link = Link(self, label="Clic para iniciar proceso de exportación")
        self.link.SetUrl(CALENDAR_MOODLE_EPN_URL)
        self.second_line_subsizer.Add(self.link)
        calendar_url_text = wx.StaticText(
            self,
            -1,
            "Por favor, introduzca el URL generado por el Aula Virtual:",
        )
        self.calendar_url_textctrl = wx.TextCtrl(self, -1, size=(480, 30))
        # titleText.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        sizer.Add(self.first_line_subsizer)
        sizer.Add(parapragh_text)
        sizer.Add(self.second_line_subsizer)
        # sizer.Add(self.link)
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(calendar_url_text)
        sizer.Add(self.calendar_url_textctrl)


########################################################################
class page_five(wx.Panel):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, parent, title=None):
        """Constructor"""
        wx.Panel.__init__(self, parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        if title:
            title = wx.StaticText(self, -1, title)
            # title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
            sizer.Add(title, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
            sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND | wx.ALL, 5)


########################################################################
class WizardPanel(wx.Panel):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        self.pages = []
        self.page_num = 0

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.panelSizer = wx.BoxSizer(wx.VERTICAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)

        # add prev/next buttons
        self.prevBtn = wx.Button(self, label="Previous")
        self.prevBtn.Bind(wx.EVT_BUTTON, self.onPrev)
        btnSizer.Add(self.prevBtn, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        self.nextBtn = wx.Button(self, label="Next")
        self.nextBtn.Bind(wx.EVT_BUTTON, self.onNext)
        btnSizer.Add(self.nextBtn, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        # finish layout
        self.mainSizer.Add(self.panelSizer, 1, wx.EXPAND)
        self.mainSizer.Add(btnSizer, 0, wx.ALIGN_RIGHT)
        self.SetSizer(self.mainSizer)

    # ----------------------------------------------------------------------
    def addPage(self, title=None):
        """"""
        panel = WizardPage(self, title)
        self.panelSizer.Add(panel, 2, wx.EXPAND)
        self.pages.append(panel)
        if len(self.pages) > 1:
            # hide all panels after the first one
            panel.Hide()
            self.Layout()

    # ----------------------------------------------------------------------
    def add_page_one(self, title=None):
        """"""
        panel = page_one(self, title)
        self.panelSizer.Add(panel, 2, wx.EXPAND)
        self.pages.append(panel)
        if len(self.pages) > 1:
            # hide all panels after the first one
            panel.Hide()
            self.Layout()

    # ----------------------------------------------------------------------
    def add_page_two(self, title=None):
        """"""
        panel = page_two(self, title)
        self.panelSizer.Add(panel, 2, wx.EXPAND)
        self.pages.append(panel)
        if len(self.pages) > 1:
            # hide all panels after the first one
            panel.Hide()
            self.Layout()

    # ----------------------------------------------------------------------
    def add_page_three(self, title=None):
        """"""
        panel = page_three(self, title)
        self.panelSizer.Add(panel, 2, wx.EXPAND)
        self.pages.append(panel)
        if len(self.pages) > 1:
            # hide all panels after the first one
            panel.Hide()
            self.Layout()

    # ----------------------------------------------------------------------
    def add_page_four(self, title=None):
        """"""
        panel = page_four(self, title)
        self.panelSizer.Add(panel, 2, wx.EXPAND)
        self.pages.append(panel)
        if len(self.pages) > 1:
            # hide all panels after the first one
            panel.Hide()
            self.Layout()

    # ----------------------------------------------------------------------
    def onNext(self, event):
        """"""
        pageCount = len(self.pages)
        if pageCount - 1 != self.page_num:
            self.pages[self.page_num].Hide()
            self.page_num += 1
            """if self.page_num == 2:
                self.api_key = self.pages[
                    self.page_num - 1
                ].api_key_textctrl.GetLineText(0)
                self.api_secret = self.pages[
                    self.page_num - 1
                ].api_secret_textctrl.GetLineText(0)
                self.url, self.response = generate_oauth_session(
                    self.api_key, self.api_secret
                )
                self.pages[self.page_num].link.SetUrl(self.url)
            if self.page_num == 3:
                code_verification = self.pages[
                    self.page_num - 1
                ].verification_code_textctrl.GetLineText(0)
                self.access_token = obtain_access_token(
                    code_verification, self.api_key, self.api_secret, self.response
                )"""

            # self.pages[self.page_num].sizer.Add()
            self.pages[self.page_num].Show()
            self.panelSizer.Layout()
            print(self.page_num)
        else:
            print("End of pages!")

        if self.page_num == 1:
            print("Pagina 1")

        if self.nextBtn.GetLabel() == "Finish":
            # close the app
            self.GetParent().Close()

        if pageCount == self.page_num + 1:
            # change label
            self.nextBtn.SetLabel("Finish")

    # ----------------------------------------------------------------------
    def onPrev(self, event):
        """"""
        pageCount = len(self.pages)
        if self.page_num - 1 != -1:
            self.pages[self.page_num].Hide()
            self.page_num -= 1
            self.pages[self.page_num].Show()
            self.panelSizer.Layout()
        else:
            print("You're already on the first page!")


########################################################################
class MainFrame(wx.Frame):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="PoliCal", size=(550, 400))

        self.panel = WizardPanel(self)
        self.panel.add_page_one("Page 1")
        # self.panel.add_page_two("Page 2")
        # self.panel.add_page_three("Page 3")
        self.panel.add_page_four("Page 4")

        self.Show()


if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()