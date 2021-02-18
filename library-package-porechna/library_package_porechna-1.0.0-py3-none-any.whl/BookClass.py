from uuid import uuid4
class Book:

    def __init__(self, title, author, year, owned = False):
        self.book_id = str(uuid4())
        self.title = title
        self.author = author
        self.year = year
        self.owned = owned

        print("Book {} created".format(self.book_id))