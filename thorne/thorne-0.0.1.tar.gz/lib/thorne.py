# imports
import random
import math
import sys

# gen


def gen(charnr, times=1):
    # char list
    chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
             'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '_', '+', '=', ')', '(', '*', '&', '^', '%', '$', '#', '@', '!', '§', '±', '}', '[', ']', '}', '\\', '/', '?', '|', '\'', '\"', ':', ';', '.', '>', '<', ',', '`', '~']
    charnr = int(charnr) + 1

    # new list of chars
    l = ""

    # get nr of times
    for b in range(0, times):
        z = charnr

        # get charnr numbers
        for i in range(1, charnr):
            n = random.randrange(0, len(chars))
            l += chars[n]
            z -= 1

            # newline if last char
            if (i + 1 == charnr):
                if (b + 1 == times):
                    l += ""
                else:
                    l += "\n"
    return l


# full_gen
def full_gen(charnr, times=1):
    # chars
    chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '_', '+', '=', ')',
             '(', '*', '&', '^', '%', '$', '#', '@', '!', '§', '±', '}', '[', ']', '}', '\\', '/', '?', '|', '\'', '\"', ':', ';', '.', '>', '<', ',', '`', '~', '¡', '™', '£', '¢', '∞', '¶', '•', 'ª', 'º', '–', '≠', '‘', 'æ', '«', '…', 'π', 'ø', 'ˆ', '¨', '¥', '†', '®', '´', '∑', 'œ', '“', '…', '¬', '˚', '∆', '˙', '©', 'ƒ', 'ß', '∂', 'å', '÷', '≥', '≤', 'µ', '˜', '∫', '√', 'ç', '≈', '`']
    charnr = int(charnr) + 1

    # new list of chars
    l = ""

    # for 0 in times
    for b in range(0, times):
        z = charnr

        # get charnr numbers
        for i in range(1, charnr):
            n = random.randrange(0, len(chars))
            l += chars[n]
            z -= 1

            # newline if last char
            if (i + 1 == charnr):
                if (b + 1 == times):
                    l += ""
                else:
                    l += "\n"
    return l

# tofile


def tofile(charnr, filename, add_comment, times=1):
    # chars
    chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '_', '+', '=', ')',
             '(', '*', '&', '^', '%', '$', '#', '@', '!', '§', '±', '}', '[', ']', '}', '\\', '/', '?', '|', '\'', '\"', ':', ';', '.', '>', '<', ',', '`', '~', '¡', '™', '£', '¢', '∞', '¶', '•', 'ª', 'º', '–', '≠', '‘', 'æ', '«', '…', 'π', 'ø', 'ˆ', '¨', '¥', '†', '®', '´', '∑', 'œ', '“', '…', '¬', '˚', '∆', '˙', '©', 'ƒ', 'ß', '∂', 'å', '÷', '≥', '≤', 'µ', '˜', '∫', '√', 'ç', '≈', '`']
    charnr = int(charnr) + 1

    # new list of chars
    l = ""

    # get nr of times
    for i in range(0, times):
        z = charnr
        # get charnr numbers
        for i in range(1, charnr):
            n = random.randrange(0, len(chars))
            l += chars[n]
            z -= 1

    # write to file
    with open(filename, 'a') as f:
        # if addcomment is true
        if add_comment == True:
            # if python source
            if '.py' in filename:
                cmd = "\n# "
                cmd += l
                f.write(cmd)
            else:
                cmd = "\n// "
                cmd += l
                f.write(l)
        else:
            f.write(l)

# inf gen


def infgen(charnr):
    # char list
    chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
             'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '_', '+', '=', ')', '(', '*', '&', '^', '%', '$', '#', '@', '!', '§', '±', '}', '[', ']', '}', '\\', '/', '?', '|', '\'', '\"', ':', ';', '.', '>', '<', ',', '`', '~']
    charnr = int(charnr) + 1
    times = int(sys.maxsize)

    # new list of chars
    l = ""

    # get nr of times
    for b in range(0, times):
        z = charnr

        # get charnr numbers
        for i in range(1, charnr):
            n = random.randrange(0, len(chars))
            l += chars[n]
            z -= 1

            # newline if last char
            if (i + 1 == charnr):
                if (b + 1 == times):
                    l += ""
                else:
                    l += "\n"
        print(l)

# inf full gen


def inffull_gen(charnr):
    # char list
    chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '_', '+', '=', ')',
             '(', '*', '&', '^', '%', '$', '#', '@', '!', '§', '±', '}', '[', ']', '}', '\\', '/', '?', '|', '\'', '\"', ':', ';', '.', '>', '<', ',', '`', '~', '¡', '™', '£', '¢', '∞', '¶', '•', 'ª', 'º', '–', '≠', '‘', 'æ', '«', '…', 'π', 'ø', 'ˆ', '¨', '¥', '†', '®', '´', '∑', 'œ', '“', '…', '¬', '˚', '∆', '˙', '©', 'ƒ', 'ß', '∂', 'å', '÷', '≥', '≤', 'µ', '˜', '∫', '√', 'ç', '≈', '`']
    charnr = int(charnr) + 1
    times = int(sys.maxsize)

    # new list of chars
    l = ""

    # get nr of times
    for b in range(0, times):
        z = charnr

        # get charnr numbers
        for i in range(1, charnr):
            n = random.randrange(0, len(chars))
            l += chars[n]
            z -= 1

            # newline if last char
            if (i + 1 == charnr):
                if (b + 1 == times):
                    l += ""
                else:
                    l += "\n"
        print(l)

# inf tofile


def inf_tofile(charnr, filename, add_comment):
    # chars
    chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '_', '+', '=', ')',
             '(', '*', '&', '^', '%', '$', '#', '@', '!', '§', '±', '}', '[', ']', '}', '\\', '/', '?', '|', '\'', '\"', ':', ';', '.', '>', '<', ',', '`', '~', '¡', '™', '£', '¢', '∞', '¶', '•', 'ª', 'º', '–', '≠', '‘', 'æ', '«', '…', 'π', 'ø', 'ˆ', '¨', '¥', '†', '®', '´', '∑', 'œ', '“', '…', '¬', '˚', '∆', '˙', '©', 'ƒ', 'ß', '∂', 'å', '÷', '≥', '≤', 'µ', '˜', '∫', '√', 'ç', '≈', '`']
    charnr = int(charnr) + 1
    times = int(sys.maxsize)

    # new list of chars
    l = ""

    # get nr of times
    for i in range(0, times):
        z = charnr
        # get charnr numbers
        for i in range(1, charnr):
            n = random.randrange(0, len(chars))
            l += chars[n]
            z -= 1

    # write to file
    with open(filename, 'a') as f:
        # if addcomment is true
        if add_comment == True:
            # if python source
            if '.py' in filename:
                cmd = "\n# "
                cmd += l
                f.write(cmd)
            else:
                cmd = "\n// "
                cmd += l
                f.write(l)
        else:
            f.write(l)
