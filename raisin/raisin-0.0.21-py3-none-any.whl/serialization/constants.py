#!/usr/bin/env python3

"""
C'est ici qu'il y a les constantes partagees.
"""

BUFFER_SIZE = 10*1024*1024 # taille des packets en octet
ALPHABET = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k",
            "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
            "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G",
            "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R",
            "S", "T", "U", "V", "W", "X", "Y", "Z", "0", "1", "2",
            "3", "4", "5", "6", "7", "8", "9", "!", "#", "$", "_",
            "&", "(", ")", "*", "+", "]", "-", ".", "/", ":", ";",
            "<", "=", ">", "?", "@", "["] # alphabet pour encoder joliment des octets en str
N_SYMB = 64 # c'est le nombre de symbols qu'il faut pour encoder N_BYTES efficacement
N_BYTES = 51 # resultat inement choisi tel que 51*log(256)/log(len(ALPHABET)) = 63.9996
ALPHABET2 = ["^", "{", "}", "~", ",", "|"] # on exclut ', " et \ qui n'ont pas le meme repr que str
HEADER = {
    "pickle":       [b"</>pickle</>",                   b"\x00"],
    "json":         [b"</>json</>",                     b"\x01"],
    "small int":    [b"</>small int</>",                b"\x02"],
    "large int":    [b"</>large int</>",                b"\x03"],
    "filename":     [b"</>filename + file_content</>",  b"\x04"],
    "str":          [b"</>str</>",                      b"\x05"],
    "round float":  [b"</>round float</>",              b"\x06"],
    "normal float": [b"</>normal float</>",             b"\x07"],
    "float":        [b"</>float</>",                    b"\x08"],
    "bytes":        [b"</>bytes</>",                    b"\x09"],
    "TextIOWrapper":[b"</>io.TextIOWrapper</>",         b"\x0a"],
    "BufferedReader":[b"</>io.BufferedReader</>",       b"\x0b"],
    "BufferedWriter":[b"</>io.BufferedWriter</>",       b"\x0c"],
    "list":         [b"</>list</>",                     b"\x0d"],
    "tuple":        [b"</>tuple</>",                    b"\x0e"],
    "dict":         [b"</>dict</>",                     b"\x0f"],
    "complex":      [b"</>complex</>",                  b"\x10"],
    "tuple":        [b"</>tuple</>",                    b"\x11"],
    "class":        [b"</>class</>",                    b"\x12"],
    "function":     [b"</>function</>",                 b"\x13"],
    "null":         [b"</>none</>",                     b"\x14"],
    "true":         [b"</>true</>",                     b"\x15"],
    "false":        [b"</>false</>",                    b"\x16"],
    "set":          [b"</>set</>",                      b"\x17"],
    "frozenset":    [b"</>frozenset</>",                b"\x18"],
    "generator":    [b"</>generator</>",                b"\x19"],
    "small dumps":  [b"</>small dumps</>",              b"\x30"], # correspond au caractere b"0"
    "large dumps":  [b"</>large dumps</>",              b"\x31"], # correspond au caractere b"1"
    "aes bloc":     [b"</>aes bloc</>",                 b"\x32"],
    "rsa bloc":     [b"</>rsa bloc</>",                 b"\x33"],
    "aes gen":      [b"</>aes gen</>",                  b"\x34"],
    "rsa gen":      [b"</>rsa gen</>",                  b"\x35"],
    "aes sel":      [b"</>aes sel</>",                  b"\x36"],
    "authenticity": [b"</>authenticity</>",             b"\x37"],
    
} # les entetes pour les donnees serialisee, eviter b"\x3c" = b"<"
