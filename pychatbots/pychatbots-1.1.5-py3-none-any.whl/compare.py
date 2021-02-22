import difflib
class compare():
    def compare(str1,str2):
        return difflib.SequenceMatcher(None, str1, str2).quick_ratio()
if __name__=='__main__':
    compare = compare()

