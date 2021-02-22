class Request:
    def __init__(self, req):
        req = req.split('\r\n')
        self.text = req[0]
        self.path = self.text.split()[1]
        for i in range(1, len(req)-1):
            try:
                obj = req[i].split(': ')
                self.__dict__[obj[0].lower().replace('-', '_')] = obj[1]
            except: pass
