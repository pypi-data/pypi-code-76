import tokenizations
from spacy.util import filter_spans

def punct_get_tag_values():
    return [
            "PAD",
            "NONE",
            "PERIOD",
            "COMMA",
            "SEMICOLON",
            "COLON",
            "QUESTION_MARK",
            "HYPHEN",
            "DASH",
        ] 

def casing_get_tag_values():
    return ["PAD", "NONE", "KEEP", "UPPER", "TITLE"]


def casing_label_realizer(label, token):
    # applies casing label transformation to a token
    if label == "UPPER":
        token = token.upper()
    elif label == "TITLE":
        token = token.title()
    return [token]


def punct_label_realizer(label, token):
    # applies punct label transformation to a token
    tokens = [token]
    if label == "PERIOD":
        tokens += ["."]
    elif label == "COMMA":
        tokens += [","]
    elif label == "SEMICOLON":
        tokens += [";"]
    elif label == "COLON":
        tokens += [":"]
    elif label == "QUESTION_MARK":
        tokens += ["?"]
    elif label == "HYPHEN":
        tokens += ["-"]
    elif label == "DASH":
        tokens += ["—"]
    return tokens

token_as_span = lambda t: t.doc[t.i : t.i + 1]

def casing_doc2chunks(doc):
    return [token.lower_ for token in doc]

def casing_doc2text(doc):
    return doc[:].lower_

punct = [".", ",", ";", ":", "?", "-", "—"]

def retokenize_for_punct(doc):
    punct_tokens = [token for token in doc if token.text in punct]
    spans_ending_with_punct = []
    for token in punct_tokens:
        if token.i == 0:
            # a weird case when the sentence starts with punct?
            spans_ending_with_punct.append(doc[0:1])
        else:
            spans_ending_with_punct.append(doc[token.i-1: token.i+1])
    # no duplicates (like conseq punct)
    spans_ending_with_punct = filter_spans(spans_ending_with_punct)

    with doc.retokenize() as retokenizer:
        for span in spans_ending_with_punct:
            retokenizer.merge(span)
    return doc


def punct_doc2chunks(doc):
    return [token.text for token in doc if not token.text in punct]

def punct_doc2text(doc):
    sent = doc.text
    for p in punct:
        sent = sent.replace(p, "")
    return sent

def get_spans(doc, bert_chunks, labels, label_realizer, doc2chunks):

    # if empty inputs, early return nothing
    if not len(doc)*len(bert_chunks)*len(labels):
        return []

    # crop labels if [CLS] and [SEP] included
    if len(labels) == len(bert_chunks) + 2:
        labels = labels[1:-1]

    # here should be equal already
    # if not - early return nothing
    if not len(labels) == len(bert_chunks):
        return []

    # doc2chunks projects the spaCy doc into token chunks
    # ex. for punctuation removing punct
    # ex. for casing lowercasing
    spacy_chunks = doc2chunks(doc)

    # spaCy chunks vs bert chunks alignment
    spacy2bert, bert2spacy = tokenizations.get_alignments(spacy_chunks, bert_chunks)

    # assumption: bert tokens are always finer than bert tokens
    # if this is not true ... oh well, I guess I will return nothing
    if not len(spacy2bert) == len(doc) and all([len(a)==1 for a in bert2spacy]):
        return []

    spans = []

    for spacy_token, idx_group in zip(doc, spacy2bert):
        token_group = [bert_chunks[i] for i in idx_group]
        # remove ##
        token_group = [token.replace("##", "") for token in token_group]
        label_group = [labels[i] for i in idx_group]
        # apply labels
        real_token_group = [label_realizer(label, token) for label, token in zip(label_group, token_group)]
        # flatten
        real_token_group = [item for sublist in real_token_group for item in sublist]
        # join into spacy tokens
        real_token = "".join(real_token_group)
        # compare
        if not spacy_token.text == real_token:
            span = token_as_span(spacy_token)
            span._.suggestions = [real_token]
            spans.append(span)
    return spans

def punct_get_spans(doc, bert_chunks, labels):
    doc = retokenize_for_punct(doc)
    return get_spans(doc, bert_chunks, labels, punct_label_realizer, punct_doc2chunks)

def casing_get_spans(doc, bert_chunks, labels):
    return get_spans(doc, bert_chunks, labels, casing_label_realizer, casing_doc2chunks)


if __name__=="__main__":
    
    import spacy
    from transformers import BertTokenizer
    
    nlp = spacy.load("en_core_web_sm")
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)

    sentence = "COVID times are very difficult so Mary's husband got depression. This is an e-mail."
    doc = nlp(sentence)
    tokens = tokenizer.tokenize(sentence)
    labels = ["NONE", "UPPER", "UPPER", "KEEP","KEEP", "KEEP", "KEEP", "KEEP", "TITLE", "KEEP", "KEEP", "KEEP", "KEEP", "KEEP","KEEP","TITLE","KEEP","KEEP","KEEP","KEEP","KEEP","KEEP","NONE" ]
    print(tokens)

    spans = get_spans(doc, tokens, labels, casing_label_realizer, casing_doc2chunks)
    print(spans)
















