class Redirect(dict):

    __cmd = 'Redirect'

    def __init__(self, action_url):
        super().__init__()
        self.__setitem__(Redirect.__cmd, {})
        self.action_url(action_url)

    def action_url(self, action_url):
        self.__getitem__(Redirect.__cmd)['actionUrl'] = action_url
        return self
