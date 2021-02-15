from .util import *

class Lines:
    def __init__(self, lines):
        self.__lines = []
        self.__line = 0
        self.__new_lines = []
        self.__i = 0

        if lines[0] != "#line 0":
            for i, line in enumerate(lines):
                self.__lines.append("#line %s\n" % i)
                self.__lines.append(line)
        else:
            self.__lines = lines

    def add_line(self, new_line):
        self.__new_lines.append("#line %s\n" % self.__line)
        self.__new_lines.append(new_line)

    def turnover(self):
        self.__lines = self.__new_lines
        self.__line = 0
        self.__new_lines = []

    def annotated(self):
        return self.__lines

    def __iter__(self):
        return self

    def next(self):
        return self.__next__()

    def __next__(self):

        i = self.__i
        while i < len(self.__lines):
            line = str(self.__lines[i])
            i += 1

            if line.startswith("#line"):
                tokens = line.split()
                if len(tokens) == 3:
                    _, line_no, file = tokens
                elif len(tokens) == 2:
                    _, line_no = tokens
                else:
                    debug("Ignoring line: %s\n", line)
                    line_no = self.__line

                line_no = int(line_no)
                self.__line = line_no

                continue
            
            self.__i = i
            return line

        self.turnover()
        raise StopIteration


def main():
    lines = Lines([1,2,3,4,5])
    for i, line in enumerate(lines):
        print line
        lines.add_line("foobar %i" % i)
        lines.add_line("foobar %i" % i)

    print lines.annotated()

if __name__ == "__main__":
    main()
