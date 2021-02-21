num_dict = {
  "null": 0,
  "eins": 1,
  "zwei": 2,
  "zwo":  2,
  "drei": 3,
  "vier": 4,
  "fünf": 5,
  "sechs": 6,
  "sieben": 7,
  "acht": 8,
  "neun": 9,
  "zehn": 10,
  "elf": 11,
  "zwölf": 12,
  "sechzehn": 16,
  "siebzehn": 17,
  "zwanzig": 20,
  "dreißig": 30,
  "dreissig": 30, # More common in Switzerland
  "vierzig": 40,
  "fünfzig": 50,
  "sechzig": 60,
  "siebzig": 70,
  "achtzig": 80,
  "neunzig": 90,
  "hundert": 100,
  "einhundert": 100,
  "tausend": 1000,
  "eintausend": 1000
}


def trans_with_multiplicand(string, index, multiplicand):
    multiplier = 1

    if string[0:index] == "ein":
        pass
    elif len(string[0:index]) > 1:
        multiplier = word_to_number(string[0:index])
    
    if len(string[index+7:]) == 0:
        rest = 0
    else:
        rest = word_to_number(string[index+7:])

    return (multiplier * multiplicand + rest) if (rest is not None) else None


def sum_numbers(tokens):
    return sum([1 if t=="ein" else num_dict.get(t, 0) for t in tokens])


def word_to_number(word):
    """ Returns the digit as a string given a written out number in German. """

    word = word.lower().strip()
    
    if word in num_dict:
        return num_dict[word]
    
    for d, m in [["tausend", 1000], ["hundert", 100]]:
        if d in word:
            return trans_with_multiplicand(word, word.index(d), m)
    
    if word.endswith("zehn"):
        return 10 + num_dict[word[:-4]]
    
    tokens = word.split("und")

    if len(tokens) <= 1:
        return None

    sum_res = sum_numbers(tokens)
    return sum_res if (sum_res > 0) else None
