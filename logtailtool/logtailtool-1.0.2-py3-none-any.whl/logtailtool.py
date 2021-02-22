import os
import re
import sys
import time
import argparse


class LogTailTool:
    def __init__(self, filename, interval=1, read_from_begin=False, pattern=None):
        self.filename = filename
        self.interval = interval
        self.read_from_begin = read_from_begin
        self.pattern = pattern

        self.openfile()

    def __iter__(self):
        return self

    # Python 3
    def __next__(self):
        return self.next()

    # Python 2
    def next(self):
        return self.read()

    def openfile(self):
        self.fh = open(self.filename, encoding='UTF8')
        self.curino = os.fstat(self.fh.fileno()).st_ino
        if not self.read_from_begin:
            self.fh.seek(0, os.SEEK_END)

    def is_file_rotated(self):
        return os.stat(self.filename).st_ino != self.curino

    def read(self):
        while True:
            curposition = self.fh.tell()
            line = self.fh.readline()
            if line:
                if self.pattern:
                    if re.search(self.pattern, line):
                        return line.strip()
                else:
                    return line.strip()
            else:
                self.fh.seek(curposition)
                if self.is_file_rotated():
                    self.fh.close()
                    self.openfile()
                time.sleep(self.interval)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LogTailTool")
    parser.add_argument(
        "-f", "--file",
        type=str,
        dest="filename",
        required=True,
        help="Log file path (required)"
    )
    parser.add_argument(
        "-p", "--pattern",
        type=str,
        dest="pattern",
        default=None,
        help="Pattern to extract (default: None)"
    )
    parser.add_argument(
        "-b", "--read-from-begin",
        dest="read_from_begin",
        action="store_true",
        help="Read from the begin of the file (default: false)"
    )
    parser.add_argument(
        "-i", "--interval",
        type=int,
        default=1,
        help="Interval time (default: 1)"
    )
    args = parser.parse_args()

    lines = LogTailTool(
        args.filename,
        args.interval,
        args.read_from_begin,
        args.pattern
    )

    for line in lines:
        print(line)
