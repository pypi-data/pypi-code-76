from pmakeup.SessionScript import SessionScript


class LinuxSessionScript(SessionScript):

    def __init__(self, model: "PMakeupModel"):
        super().__init__(model)

    def test_linux(self, string: str):
        """
        Test if linux commands is loaded
        :param string: the string to echo'ed
        """
        self.echo(string)