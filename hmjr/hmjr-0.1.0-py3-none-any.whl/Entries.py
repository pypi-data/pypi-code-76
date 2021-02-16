import numpy as np
import datetime
from functools import cmp_to_key

def splitIntoWords(str, badChars):
    return np.array(str.translate(str.maketrans( '', '', badChars)).split(" "))

BAD_CHARS = "\""
BAD_WORDS = "of and to for Book Page in by on from with See"

def convertDate(date):
    return (datetime.datetime(1900 + date["year"], date["month"], date["day"]) - datetime.datetime(1934, 2, 27)).days

class By:
    def date():
        return cmp_to_key(lambda a, b: -1 if a["year"] < b["year"] else -1 if a["year"] > b["year"] else 1 if a["month"] < b["month"] else -1 if a["month"] > b["month"] else 1 if a["day"] < b["day"] else -1)
    def index():
        return cmp_to_key(lambda a, b: 1 if b["book"] is None else -1 if a["book"] is None else 1 if a["book"] < b["book"] else -1 if a["book"] > b["book"] else 1 if min(a["page"].split(',')) < min(b["page"].split(',')) else -1)

class Entries:
    def __init__(self, entries):
        self.entries = np.array(entries)

    def sorted(self, key):
        """Sort the current entries with the given key function."""
        try:
            self.entries = np.array(sorted(self.entries, key=key))
            return self
        except:
            print("No results found. Try running a query first.")

    def headers(self):
        """Return a numpy array of the result header strings."""
        try:
            return np.array([i["header"] for i in self.entries])
        except:
            print("No results found. Try running a query first.")

    def content(self):
        """Return a numpy array of the result content strings."""
        try:
            return np.array([i["content"] for i in self.entries])
        except:
            print("No results found. Try running a query first.")

    def dates(self):
        """Return a numpy array of the result date dictionaries."""
        try:
            return np.array([d for i in self.entries for d in i["dates"]])
        except:
            print("No results found. Try running a query first.")

    def dateRange(self, dates=[]):
        """Return a tuple containing the minimum and maximum date in the entries."""
        if len(dates) < 1:
            dates = self.dates()
        return (min(dates, key=By.date()), max(dates, key=By.date()))

    def bookRange(self, indexes=[]):
        """Return a tuple containing the minimum and maximum book in the entries."""
        if len(indexes) < 1:
            indexes = self.indexes()
        return (min(indexes, key=By.index()), max(indexes, key=By.index()))

    def indexes(self):
        """Return a numpy array of the result index dictionaries."""
        try:
            tmp = [d for i in self.entries for d in i["indexes"] if d["page"] is not None]
            return np.array([{**index, "page": page} for index in tmp for page in index["page"].split(',')])
        except:
            print("No results found. Try running a query first.")

    def headerWords(self, badChars=BAD_CHARS):
        """Return a numpy array of all the words in all headers. Repetitions are allowed."""
        try:
            return splitIntoWords(' '.join(self.headers()), badChars)
        except:
            print("No results found. Try running a query first.")

    def headerCounts(self):
        """Count the appearances of each unique header."""
        unique, counts = np.unique(self.headers(), return_counts=True)
        return dict(zip(unique, counts))

    def contentWords(self, badChars=BAD_CHARS):
        """Return a numpy array of all the words in all headers. Repetitions are allowed."""
        try:
            return splitIntoWords(' '.join(self.content()), badChars)
        except:
            print("No results found. Try running a query first.")

    def words(self, badChars=BAD_CHARS):
        """Return a numpy array of all the words in each entry. Equivalent to headerWords + contentWords."""
        try:
            return np.concatenate((self.headerWords(badChars),self.contentWords(badChars)))
        except:
            print("No results found. Try running a query first.")

    def associate(self, words, badWords=BAD_WORDS):
        """Count the appearances of each unique word in indexes that contain the given words. """
        indexes = self.indexes()
        if indexes.any():
            containedStrs = [s["content"] for s in indexes for word in words if s["content"] is not None if word in s["content"]]
            words = [word for s in containedStrs for word in s.split(" ") ]
            return {word:words.count(word) for word in words if word not in badWords}

    def deltaTime(self, words, daysSince=False):
        """Count the appearances of a string over time in the entries."""
        dates = self.dates()
        if dates.any():
            containedDates = [date for date in dates for word in words if date["content"] is not None if word in date["content"]]
            if not daysSince:
                cnt = [date["stringified"].strip('.') for date in containedDates]
                return {date: cnt.count(date) for date in cnt}
            else:
                cnt = [convertDate(date) for date in containedDates]
                return {date: cnt.count(date) for date in cnt}

    def deltaBooks(self, words):
        """Count the appearances of a string over a volumes in the entries."""
        if self.entries.any():
            containedEntries = [entry for entry in self.entries for word in words if entry["content"] is not None if word in entry["content"] or entry["header"] is not None or word in entry["header"]]
            cnt = [entry['book'] for entry in containedEntries]
            return {entry: cnt.count(entry) for entry in cnt}


