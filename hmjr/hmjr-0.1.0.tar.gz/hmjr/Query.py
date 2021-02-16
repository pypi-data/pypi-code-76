from hmjr import Entries
from python_graphql_client import GraphqlClient

def validateBook(book):
    strBook = str(book)
    while len(strBook) < 3:
        strBook = "0" + strBook
    return strBook

class Query:
    def __init__(self):
       self.client = GraphqlClient(endpoint="https://hmjrapi-prod.herokuapp.com/")
       self.dates = []
       self.keywords = []
       self.books = []

    def query(self, query, variables, name="entries"):
        """Make a raw GQL query to the hmjrapi backend."""
        try:
            data = self.client.execute(query=query,variables=variables)["data"][name]
            return Entries(data)
        except Exception as e:
            print("Query resulted in error: " + e)

    def run(self, max=50):
        """Run the built query."""
        query = """
            query ($max: Float!, $keywords: [String!]!, $dates: [DateInput!]!, $books: [String!]!) {
                entries(max: $max, keywords: $keywords, dates: $dates, books:$books) {
                    book
                    header
                    content
                    dates {
                        day
                        month
                        year
                        stringified
                        content
                    }
                    indexes {
                        book
                        page
                        content
                    }
                }
            }
        """
        variables = {"max": max, "keywords": self.keywords, "dates": self.dates, "books": [validateBook(book) for book in self.books]}
        return self.query(query, variables)

    def withDates(self, dates):
        """Query entries with at least one date greater than the minimum given and less than the maximum given."""
        self.dates = dates
        return self

    def withKeywords(self, keywords):
        """Query entries which contain at least one word in the keywords given in their content or header."""
        self.keywords = keywords
        return self

    def withBook(self, books):
        """Query entries from the books given."""
        self.books = books
        return self

    def withBookBetween(self, minBook, maxBook):
        """Query entries between two books, including the lower bound."""
        return self.withBook([x for x in range(minBook, maxBook, 1)])

    def withDateBetween(self, dateA, dateB):
        """Query entries with at least one date between the given dates."""
        return self.withDates([dateA, dateB])

