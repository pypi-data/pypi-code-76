class Associable(object):
    def __init__(self, associated_with = None):
        self.__associated_with = associated_with

    def associated_with(self):
        return self.__associated_with

    def is_associated(self):
        return self.associated_with() != None

    def associate(self, associate_with):
        if not self.is_associated():
            self.__associated_with = associate_with
