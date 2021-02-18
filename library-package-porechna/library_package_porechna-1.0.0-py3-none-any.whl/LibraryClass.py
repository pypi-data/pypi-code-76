
from BookClass import Book

class Library:
    
    def __init__(self):
        self.reader_list = []
        self.book_list = []

        print("Library added")
    
    def add_book(self, title:str, author:str, year:int):
        if not any(item.title == title and item.author == author and item.year == year for item in self.book_list):
            book = Book(title, author, year)
            self.book_list.append(book)
            
            return book
        else:
            print("Book already exists")

    def add_reader(self, reader):
        self.reader_list.append(reader)

        print("Reader {} added to library".format(reader.reader_id))
        
    
    def delete_book(self, book_id):
        for i, item in enumerate(self.book_list):
            if item.book_id == book_id:
                del self.book_list[i]
                break

        print("Book {} deleted".format(book_id))

    def give_book(self, book_id, reader_id):
        book_inst = [item for item in self.book_list if item.book_id == book_id]
        if book_inst[0].owned:
            print("Book already given")
        
        else:
            setattr(book_inst[0], "owned", True)
            reader_inst = [item for item in self.reader_list if item.reader_id == reader_id]
            getattr(reader_inst[0], "books_owned").append(book_id)
            print("Book {} given to reader {}".format(book_id, reader_id))

    def return_book(self, book_id, reader_id):
        book_inst = [item for item in self.book_list if item.book_id == book_id]
        if book_inst[0].owned:
            setattr(book_inst[0], "owned", False)
            reader_inst = [item for item in self.reader_list if item.reader_id == reader_id]
            getattr(reader_inst[0], "books_owned").remove(book_id)
            print("Book {} returned from {}".format(book_id, reader_id))
        else:
            print("Book already returned")

    def list_all_books(self):
        for item in self.book_list:
            print(item.title, item.author, item.year, item.book_id, sep =' ')
    
    def list_available_books(self):
        for item in self.book_list:
            if not item.owned:
                print(item.title, item.author, item.year, item.book_id, sep =' ')

    def list_not_available_books(self):
        for item in self.book_list:
            if item.owned:
                print(item.title, item.author, item.year, item.book_id, sep =' ')
    
    def sort_books(self, option:str):
        if option == "author":
            self.book_list.sort(key = lambda b: b.author)
        elif option == "title":
            self.book_list.sort(key = lambda b: b.title)
        elif option == "year":
            self.book_list.sort(key = lambda b: b.year)
        else:
            print("Can only sort by author, title or year")
    
