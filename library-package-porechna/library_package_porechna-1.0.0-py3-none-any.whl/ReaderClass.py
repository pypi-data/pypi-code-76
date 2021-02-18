from uuid import uuid4
class Reader:

    def __init__(self, name, surname):
        self.reader_id = str(uuid4())
        self.name = name
        self.surname = surname
        self.books_owned = []

        print("Reader {} created".format(self.reader_id))

    def owned_books(self):
        print("Owned books:"+str(self.books_owned))