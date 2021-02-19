from syntok.tokenizer import Tokenizer

def tokenize_by_space(text):
    tokens = text.split(" ")
    tokens = [t for t in tokens if len(t) > 0]
    return tokens

class GazetteerTermExtractor:
    def __init__(self, term_list):
        self.tokenizer = Tokenizer()
        self.terms_by_lengths = {}
        for term in term_list:
            term = tuple(tokenize_by_space(term))
            length = len(term)
            if length not in self.terms_by_lengths:
                self.terms_by_lengths[length] = set()
            self.terms_by_lengths[length].add(term)
        self.window_sizes = sorted(list(self.terms_by_lengths.keys()))

    def extract_terms(self, text: str):
        sentence = list(self.tokenizer.tokenize(text))
        tokens = [t.value for t in sentence]

        found_terms = self._find_terms(tokens)
        unique_dnts = self._resolve_overlappings(found_terms, len(tokens))

        result = []
        for start, end in unique_dnts:
            start_char = sentence[start].offset
            end_char = sentence[end - 1].offset + len(tokens[end - 1])
            result.append((start_char, end_char))
        return result

    def _find_terms(self, tokens):
        found_terms = []
        n_tokens = len(tokens)
        for window_size in self.window_sizes:
            dnt_list = self.terms_by_lengths[window_size]
            for i in range(n_tokens - window_size + 1):
                window = tuple(tokens[i:i+window_size])
                if window in dnt_list:
                    found_terms.append((i, i+window_size))
        return found_terms

    @staticmethod
    def _resolve_overlappings(found_terms, n_tokens):
        unique_terms = []
        tok_id = 0
        while tok_id < n_tokens:
            overlapping_dnts = [(s, e) for s, e in found_terms if s <= tok_id < e]
            if len(overlapping_dnts) == 0:
                tok_id += 1
                continue

            end = max(e for s, e in overlapping_dnts)
            overlapping_dnts.extend((s, e) for s, e in found_terms if tok_id < s < end)
            start = tok_id
            end = max(e for s, e in overlapping_dnts)
            unique_terms.append((start, end))
            tok_id = end

        unique_terms = sorted(list(set(unique_terms)), key=lambda d: d[0])
        return unique_terms


def test():
    extractor = GazetteerTermExtractor([
        "Azure", "Microsoft", "AI for LOC", "Power BI", "Xbox", "Xbox 360", "Xbox One X", "Xbox Series X", "AppSource"
    ])

    for text in [
        "I don't know how to use Azure",
        "Microsoft is my favourite OS",
        "I am working on new project called AI  for LOC",
        "Power BI directional graph",
        "Xbox 360 is better than Xbox One, but worse than Xbox Series X!",
        "I love App Source"
    ]:
        print(text)
        for s, e in extractor.extract_terms(text):
            print(text[s:e])
        print()


if __name__ == "__main__":
    test()