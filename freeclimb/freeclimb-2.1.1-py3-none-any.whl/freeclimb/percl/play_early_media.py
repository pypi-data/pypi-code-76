class PlayEarlyMedia(dict):
    
    __cmd = 'PlayEarlyMedia'
    
    def __init__(self, file):
        super().__init__()
        self.__setitem__(PlayEarlyMedia.__cmd, {})
        self.file(file)

    def file(self, file):
        self.__getitem__(PlayEarlyMedia.__cmd)['file'] = file
        return self
