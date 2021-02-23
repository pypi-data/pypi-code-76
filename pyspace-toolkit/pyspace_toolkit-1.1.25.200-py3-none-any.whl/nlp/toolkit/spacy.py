import spacy
import re
import copy

## language
from spacy.lang.en import English
from spacy.lang.tr import Turkish as SpacyTurkish

## tokenization
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher
from spacy.pipeline import EntityRuler

from spacy.tokens import Token, Span
from spacy.tokenizer import Tokenizer

from spacy.pipeline import merge_entities

## ## predefined variables
from spacy.lang.tokenizer_exceptions import TOKEN_MATCH, URL_MATCH
from spacy.lang.punctuation import TOKENIZER_PREFIXES, TOKENIZER_SUFFIXES
from spacy.lang.punctuation import TOKENIZER_INFIXES
from spacy.lang.tokenizer_exceptions import BASE_EXCEPTIONS
from spacy.lang.tr.tokenizer_exceptions import TOKENIZER_EXCEPTIONS
## ## functions for predefined variables
from spacy.util import update_exc, add_lookups

#######################################


#######################################

# EXAMPLES

## tokenization

#### matcher

def __example_matcher():
    nlp = spacy.load("en_core_web_sm")
    matcher = Matcher(nlp.vocab)
    # matcher = Matcher(nlp.vocab, validate=True) # catch invalid patterns
    

    # ORTH, TEXT,
    # LOWER, LENGTH, 
    # IS_ALPHA, IS_ASCII, IS_DIGIT, IS_LOWER, IS_UPPER, IS_TITLE, IS_PUNCT, IS_SPACE, IS_STOP, 
    # LIKE_NUM, LIKE_URL, LIKE_EMAIL,
    # POS, TAG, DEP, LEMMA, SHAPE
    # ENT_TYPE

    # IN, NOT_IN, ==, >=, <=, >, <
    # REGEX

    # OP # !, ?, +, *


    # pattern = [{"LOWER": "hello"}, {"IS_PUNCT": True}, {"LOWER": "world"}]

    # pattern = [{"LEMMA": {"IN": ["like", "love"]}}, {"POS": "NOUN"}]
    # pattern = [{"LENGTH": {">=": 10}}]

    ### When using the REGEX operator, keep in mind that it operates on single tokens.
    # pattern = [{"TEXT": {"REGEX": "^\d$"}}, {"TEXT": {"REGEX": "^\+$"}}, {"TEXT": {"REGEX": "^\d$"}}]
    # pattern = [{"TEXT": {"REGEX": "^[Uu](\.?|nited)$"}}, {"TEXT": {"REGEX": "^[Ss](\.?|tates)$"}},{"LOWER": "president"}]
    # pattern = [{"TAG": {"REGEX": "^V"}}]
    # pattern = [{"_": {"country": {"REGEX": "^[Uu](nited|\.?) ?[Ss](tates|\.?)$"}}}]

    # pattern = [{"LOWER": "hello"}, {"IS_PUNCT": True, "OP": "?"}]
    # pattern = [{'POS': 'ADJ', 'OP': '?'}, {'LEMMA': 'match', 'POS': 'NOUN'}, {'LEMMA': 'be'}]

    # Using wildcard token patterns 
    # pattern = [{"ORTH": "User"}, {"ORTH": "name"}, {"ORTH": ":"}, {}]

    # phone number
    # pattern = [{"ORTH": "("}, {"SHAPE": "ddd"}, {"ORTH": ")"}, {"SHAPE": "dddd"}, {"ORTH": "-", "OP": "?"}, {"SHAPE": "dddd"}]


    # [{"IS_DIGIT": True}, {"ORTH": '+'}, {"IS_DIGIT": True}]
    # [{"TEXT": {"REGEX": "^\d$"}}, {"TEXT": {"REGEX": "^\+$"}}, {"TEXT": {"REGEX": "^\d$"}}]
    # [{"TEXT": {"REGEX": "\d\+\d"}}]

    def base():
        # Add match ID "HelloWorld" with no callback and one pattern
        pattern = [{"LOWER": "hello"}, {"IS_PUNCT": True}, {"LOWER": "world"}]
        matcher.add("HelloWorld", None, pattern)

        doc = nlp("Hello, world! Hello world!")
        matches = matcher(doc)
        for match_id, start, end in matches:
            string_id = nlp.vocab.strings[match_id]  # Get string representation
            span = doc[start:end]  # The matched span
            print(match_id, string_id, start, end, span.text)

    def regex_pattern():
        # Add match ID "HelloWorld" with no callback and one pattern
        pattern = [{"TEXT": {"REGEX": "^\d$"}}, {"TEXT": {"REGEX": "^\+$"}}, {"TEXT": {"REGEX": "^\d$"}}]
        matcher.add("roomcount", None, pattern)

        doc = nlp("Kadikoyde 1+1 ev bulabilirmiyim?")
        matches = matcher(doc)
        for match_id, start, end in matches:
            string_id = nlp.vocab.strings[match_id]  # Get string representation
            span = doc[start:end]  # The matched span
            print(match_id, string_id, start, end, span.text)

    def merge():
        # Add match ID "HelloWorld" with no callback and one pattern
        pattern = [{"LOWER": "hello"}, {"IS_PUNCT": True}, {"LOWER": "world"}]
        matcher.add("HelloWorld", None, pattern)

        doc = nlp("Hello, world! Hello world!")
        matches = matcher(doc)
    
        with doc.retokenize() as retokenizer:
            for match_id, start, end in matches:
                retokenizer.merge(doc[start:end], ) 

    def action():
        def add_event_ent(matcher, doc, i, matches):
            # Get the current match and create tuple of entity label, start and end.
            # Append entity to the doc's entity. (Don't overwrite doc.ents!)
            match_id, start, end = matches[i]
            entity = Span(doc, start, end, label="EVENT")
            doc.ents += (entity,)
            print(entity.text)

        pattern = [{"ORTH": "Google"}, {"ORTH": "I"}, {"ORTH": "/"}, {"ORTH": "O"}]
        matcher.add("GoogleIO", add_event_ent, pattern)
        doc = nlp("This is a text about Google I/O")
        matches = matcher(doc)

    def emoji_hashtag():

        ## v1

        nlp = English()  # We only want the tokenizer, so no need to load a model
        matcher = Matcher(nlp.vocab)

        pos_emoji = ["😀", "😃", "😂", "🤣", "😊", "😍"]  # Positive emoji
        neg_emoji = ["😞", "😠", "😩", "😢", "😭", "😒"]  # Negative emoji

        # Add patterns to match one or more emoji tokens
        pos_patterns = [[{"ORTH": emoji}] for emoji in pos_emoji]
        neg_patterns = [[{"ORTH": emoji}] for emoji in neg_emoji]

        # Function to label the sentiment
        def label_sentiment(matcher, doc, i, matches):
            match_id, start, end = matches[i]
            if doc.vocab.strings[match_id] == "HAPPY":  # Don't forget to get string!
                doc.sentiment += 0.1  # Add 0.1 for positive sentiment
            elif doc.vocab.strings[match_id] == "SAD":
                doc.sentiment -= 0.1  # Subtract 0.1 for negative sentiment

        matcher.add("HAPPY", label_sentiment, *pos_patterns)  # Add positive pattern
        matcher.add("SAD", label_sentiment, *neg_patterns)  # Add negative pattern

        # Add pattern for valid hashtag, i.e. '#' plus any ASCII token
        matcher.add("HASHTAG", None, [{"ORTH": "#"}, {"IS_ASCII": True}])

        doc = nlp("Hello world 😀 #MondayMotivation")
        matches = matcher(doc)
        for match_id, start, end in matches:
            string_id = doc.vocab.strings[match_id]  # Look up string ID
            span = doc[start:end]
            print(string_id, span.text)

        # HAPPY 😀
        # HASHTAG #MondayMotivation

        ## v2 - merge hashtag and set attribute

        nlp = spacy.load("en_core_web_sm")
        matcher = Matcher(nlp.vocab)

        # Add pattern for valid hashtag, i.e. '#' plus any ASCII token
        matcher.add("HASHTAG", None, [{"ORTH": "#"}, {"IS_ASCII": True}])

        # Register token extension
        Token.set_extension("is_hashtag", default=False)

        doc = nlp("Hello world 😀 #MondayMotivation")
        matches = matcher(doc)
        hashtags = []
        for match_id, start, end in matches:
            if doc.vocab.strings[match_id] == "HASHTAG":
                hashtags.append(doc[start:end])
        with doc.retokenize() as retokenizer:
            for span in hashtags:
                retokenizer.merge(span)
                for token in span:
                    token._.is_hashtag = True

        for token in doc:
            print(token.text, token._.is_hashtag)

    ################################################
    ################################################

    def full_text_regex():
        nlp = spacy.load("en_core_web_sm")
        doc = nlp("The United States of America (USA) are commonly known as the United States (U.S. or US) or America.")

        expression = r"[Uu](nited|\.?) ?[Ss](tates|\.?)"
        for match in re.finditer(expression, doc.text):
            start, end = match.span()
            span = doc.char_span(start, end)
            # This is a Span object or None if match doesn't map to valid token sequence
            if span is not None:
                print("Found match:", span.text)

    def full_text_regex_extended_span(): # if regex match does not match token boundaries, extend the regex match 
        nlp = spacy.load("en_core_web_sm")
        doc = nlp("The United States of America (USA) are commonly known as the United States (U.S. or US) or America.")

        chars_to_tokens = {}
        for token in doc:
            for i in range(token.idx, token.idx + len(token.text)):
                chars_to_tokens[i] = token.i

        expression = r"[Uu](nited|\.?) ?[Ss](tates|\.?)"
        for match in re.finditer(expression, doc.text):
            start, end = match.span()

            span = doc.char_span(start, end)
            if span is not None:
                print("Found match:", span.text)
            else:
                start_token = chars_to_tokens.get(start)    
                end_token = chars_to_tokens.get(end)    
                if start_token is not None and end_token is not None:
                    span = doc[start_token:end_token + 1]        
                    print("Found closest match:", span.text)

    ################################################
    ################################################

    ### PHRASE MATCHER

    ################################################
    ################################################

    def base_phrase():
        nlp = spacy.load('en_core_web_sm')
        matcher = PhraseMatcher(nlp.vocab)
        terms = ["Barack Obama", "Angela Merkel", "Washington, D.C."]
        # Only run nlp.make_doc to speed things up
        # patterns = [nlp(term) for term in LOTS_OF_TERMS] # SLOW
        # patterns = [nlp.make_doc(text) for text in terms] # FASTER
        patterns = list(nlp.tokenizer.pipe(LOTS_OF_TERMS)) # FASTEST
        matcher.add("TerminologyList", None, *patterns)

        doc = nlp("German Chancellor Angela Merkel and US President Barack Obama "
                "converse in the Oval Office inside the White House in Washington, D.C.")
        matches = matcher(doc)
        for match_id, start, end in matches:
            span = doc[start:end]
            print(span.text)

    def phrase_shape():
        nlp = English()
        matcher = PhraseMatcher(nlp.vocab, attr="SHAPE")
        matcher.add("IP", None, nlp("127.0.0.1"), nlp("127.127.0.0"))
        
        doc = nlp("Often the router will have an IP address such as 192.168.1.1 or 192.168.2.1.")
        for match_id, start, end in matcher(doc):
            print("Matched based on token shape:", doc[start:end])

    def phrase_lower():
        nlp = English()
        matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
        patterns = [nlp.make_doc(name) for name in ["Angela Merkel", "Barack Obama"]]
        matcher.add("Names", None, *patterns)

        doc = nlp("angela merkel and us president barack Obama")
        for match_id, start, end in matcher(doc):
            print("Matched based on lowercase token text:", doc[start:end])

    ################################################
    ################################################

    ### ENTITY RULER

    ################################################
    ################################################

    def base_entity_ruler():
        nlp = English()
        ruler = EntityRuler(nlp)
        patterns = [{"label": "ORG", "pattern": "Apple"},
                    {"label": "GPE", "pattern": [{"LOWER": "san"}, {"LOWER": "francisco"}]}]
        ruler.add_patterns(patterns)
        nlp.add_pipe(ruler)

        doc = nlp("Apple is opening its first big office in San Francisco.")
        print([(ent.text, ent.label_) for ent in doc.ents])

    def additional_v1():
        nlp = spacy.load("en_core_web_sm")

        def extract_person_orgs(doc):
            person_entities = [ent for ent in doc.ents if ent.label_ == "PERSON"]
            for ent in person_entities:
                head = ent.root.head
                if head.lemma_ == "work":
                    preps = [token for token in head.children if token.dep_ == "prep"]
                    for prep in preps:
                        orgs = [token for token in prep.children if token.ent_type_ == "ORG"]
                        print({'person': ent, 'orgs': orgs, 'past': head.tag_ == "VBD"})
            return doc

        # To make the entities easier to work with, we'll merge them into single tokens
        nlp.add_pipe(merge_entities)
        nlp.add_pipe(extract_person_orgs)
    
    def matcher_pipeline():
        class BadHTMLMerger(object):
            def __init__(self, nlp):
                # Register a new token extension to flag bad HTML
                Token.set_extension("bad_html", default=False)
                self.matcher = Matcher(nlp.vocab)
                self.matcher.add(
                    "BAD_HTML",
                    None,
                    [{"ORTH": "<"}, {"LOWER": "br"}, {"ORTH": ">"}],
                    [{"ORTH": "<"}, {"LOWER": "br/"}, {"ORTH": ">"}],
                )
                
            def __call__(self, doc):
                # This method is invoked when the component is called on a Doc
                matches = self.matcher(doc)
                spans = []  # Collect the matched spans here
                for match_id, start, end in matches:
                    spans.append(doc[start:end])
                with doc.retokenize() as retokenizer:
                    for span in spans:
                        retokenizer.merge(span)
                        for token in span:
                            token._.bad_html = True  # Mark token as bad HTML
                return doc
                
        nlp = spacy.load("en_core_web_sm")
        html_merger = BadHTMLMerger(nlp)
        nlp.add_pipe(html_merger, last=True)  # Add component to the pipeline
        doc = nlp("Hello<br>world! <br/> This is a test.")


def __legacy_spacy_regex_tokenizer(nlp, matchers=[], phrasematchers=[], token_patterns =[], replace_patterns=[], model_config='stanza'): 
    
    def custom_tokenizer(nlp, token_patterns):

        token_pattern_combined = fr'''({'|'.join(token_patterns)})'''
        token_match = re.compile(token_pattern_combined).search
        url_match = URL_MATCH
        prefixes = tuple(TOKENIZER_PREFIXES)
        suffixes = tuple(TOKENIZER_SUFFIXES)
        infixes = tuple(TOKENIZER_INFIXES)

        tokenizer_exceptions = update_exc(BASE_EXCEPTIONS, TOKENIZER_EXCEPTIONS)

        rules = tokenizer_exceptions
        token_match = token_match
        url_match = url_match
        prefix_search = (spacy.util.compile_prefix_regex(prefixes).search if prefixes else None)
        suffix_search = (spacy.util.compile_suffix_regex(suffixes).search if suffixes else None)
        infix_finditer = (spacy.util.compile_infix_regex(infixes).finditer if infixes else None)
        vocab = nlp.vocab
        return Tokenizer(
            vocab,
            rules=rules,
            prefix_search=prefix_search,
            suffix_search=suffix_search,
            infix_finditer=infix_finditer,
            token_match=token_match,
            url_match=url_match,
        )

    def wrapped_tokenizer(self, text, replace_regexes=[]):
        for p, r in replace_regexes:
            text = re.sub(p, r, text, flags=re.I)
        ############################################

        doc = self.base_tokenizer(text)
        # spacy_nlp.base_tokenizer.explain(text)
        # self.base_tokenizer.explain(text)

        ############################################

        def matcher_merge(matcher):
            matches = matcher(doc)
            matches = [m for m in matches if m != []] # add_entity callback # remove match if an entity already exists

            with doc.retokenize() as retokenizer:
                for match_id, start, end in matches:
                    string_id = self.vocab.strings[match_id]  
                    span = doc[start:end]  # The matched span
                    # print(match_id, string_id, start, end, span.text)
                    # print(string_id, start, end, span.text)
                    retokenizer.merge(span, ) 

        matcher_merge(self.custom_phrasematcher) if hasattr(self, 'custom_phrasematcher') else None
        matcher_merge(self.custom_matcher) if hasattr(self, 'custom_matcher') else None
        matcher_merge(self.custom_default_matcher) if hasattr(self, 'custom_default_matcher') else None

        ############################################

        return doc

    def add_matchers(nlp, matchers):
        if matchers == []:
            return nlp
        
        matcher = Matcher(nlp.vocab)
        for m in matchers:
            # matcher.add(*m) # single pattern # name, callback, pattern
            # matcher.add(m[0], m[1], *m[2]) # multiple patterns # name, callback, pattern1, pattern2
            # matcher.add(*(m[:-1] + [*m[-1]])) # multiple patterns # name, callback, pattern1, pattern2
            matcher.add(m[0], m[2], *m[1])

        nlp.custom_matcher = matcher
        return nlp

    def add_phrase_matchers(nlp, phrasematchers):
        if phrasematchers == []:
            return nlp
        
        matcher = PhraseMatcher(nlp.vocab,)

        # patterns = [nlp.make_doc(text) for text in terms]
        # patterns = [nlp.make_doc(text) for text in pm[1]]
        for pm in phrasematchers:
            patterns = list(nlp.tokenizer.pipe(pm[1])) # FASTEST
            matcher.add(pm[0], pm[2], *patterns)

        nlp.custom_phrasematcher = matcher
        return nlp

    def add_default_matchers(nlp, defaultmatchers):
        matchers = defaultmatchers
        
        if matchers == []:
            return nlp
        
        matcher = Matcher(nlp.vocab)
        for m in matchers:
            matcher.add(m[0], m[2], *m[1])

        nlp.custom_default_matcher = matcher
        return nlp

    def add_entity(matcher, doc, i, matches):

        match_id, start, end = matches[i]
        string_id = matcher.vocab.strings[match_id]        
        entity = Span(doc, start, end, label=string_id)

        #################################################################
        # check existing entity
        #################################################################
        __doc_ents = {}
        __doc_ents.update(  { (s.start, s.end) : s for s in doc.ents} )
        # __doc_ents.update(  { s.label_ : s  for s in doc.ents} )
        __doc_ents.update(  { position : s for s in doc.ents for position in list(range(s.start, s.end))} )
        
        __intersection = list(set(range(start,end)).intersection(set(__doc_ents.keys())))
        if __intersection != []:
            print('Overlapping entity', __doc_ents[__intersection[0]], __doc_ents[__intersection[0]].label_, entity, entity.label_)
            matches[i] = [] # remove match if an entity already exists
            return
        #################################################################

        doc.ents += (entity,)

    matchers = [(i[0], i[1], add_entity) for i in matchers]
    phrasematchers = [(i[0], i[1], add_entity) for i in phrasematchers]
    defaultmatchers = [
        ('<num>', [[{"LIKE_NUM": True}, ],]),
        ('<url>', [[{"LIKE_URL": True}, ],]),
        ('<email>', [[{"LIKE_EMAIL": True}, ],]),]
    defaultmatchers = [(i[0], i[1], add_entity) for i in defaultmatchers]
    
    nlp = add_matchers(nlp, matchers)
    nlp = add_phrase_matchers(nlp, phrasematchers)
    nlp = add_default_matchers(nlp, defaultmatchers)
    
    ## QUESTION : DOES MATCHERS EXECUTED IN APPLIED 'ADD' ORDER


    #if model_config == 'stanza':
    #    import stanza
    #    stanza_model_tokenized = stanza.Pipeline('tr', **{'tokenize_pretokenized':True})
    #    nlp.model_config = ('stanza', stanza_model_tokenized)
    #if hasattr(self, 'model_config'):
    #    mname, model = self.model_config
    #    if mname == 'stanza':

    nlp.base_tokenizer = custom_tokenizer(nlp, token_patterns)

    temp = lambda self, x: wrapped_tokenizer(self, x, replace_regexes=replace_patterns)
    nlp.tokenizer = temp.__get__(nlp)

    return nlp

    def __notes__parameters_and_regexes():
        # regex boundary notes
        # # [^\b]matching text[$\b]

        # # matcher # # match merge and label
        # matchers = [
        #     ('<roomcount>', [[{"TEXT": {"REGEX": r"\b(\d\+\d|10\+1)\b"}}]]), # match one token '4+1'
        #     ('<amount-of-money>', [
        #         [{"TEXT": {"REGEX": r"\b\d+\b"}}, {"TEXT": {"REGEX": r"^[\$]$"}}], # match two tokens '100', '$'
        #         [{"TEXT": {"REGEX": r"\b\d+[\$]$"}},], # match two tokens '100$'
        #     ]), 
        #     ('<USA>'      , [[{"TEXT": {"REGEX": "^[Uu](\.?|nited)$"}}, {"TEXT": {"REGEX": "^[Ss](\.?|tates)$"}}]]), # match two tokens 'United', 'States'
        #             ]

        # # phrasematcher # # match merge and label
        # phrasematchers = [('specialroom', ['a3+1'])]

        # # token match # # merge / split token match
        # token_patterns = [
        #     r'\b\d\+\d\b', # match '1+1'
        #     r'\b10\+1\b', # exact match '10+1'
        #     r'\d+[\$]', # match '1000$'
        #                 ]

        # # normalze text # # replace with regex  
        # replace_patterns = [
        #     (r'\b(\d)\s*(\+)\s*([\d])\b', r'\1\2\3'), # replace '2 + 1' to '2+1'
        #     (r'\b(\d+[\$])(\S+?)(\s)', r'\1 \2\3'), # replace '100$. ' to '100$ . '
        #                     ]
        pass
    def __example():
        ############################################
        # regex boundary notes
        # # [^\b]matching text[$\b]
        ############################################

        ############################################
        ############################################
        ############################################

        # matcher # # match merge and label
        matchers = [
            ('<roomcount>', [[{"TEXT": {"REGEX": r"\b(\d\+\d|10\+1)\b"}}]]), # match one token '4+1'
            ('<amount-of-money>', [
                [{"TEXT": {"REGEX": r"\b\d+\b"}}, {"TEXT": {"REGEX": r"^[\$]$"}}], # match two tokens '100', '$'
                [{"TEXT": {"REGEX": r"\b\d+[\$]$"}},], # match two tokens '100$'
            ]), 
            ('<USA>'      , [[{"TEXT": {"REGEX": "^[Uu](\.?|nited)$"}}, {"TEXT": {"REGEX": "^[Ss](\.?|tates)$"}}]]), # match two tokens 'United', 'States'
                    ]
        # matchers = []

        ############################################
        ############################################
        ############################################

        # phrasematcher # # match merge and label
        # phrasematchers = [('specialroom', ['a3+1'])]
        phrasematchers = []

        ############################################
        ############################################
        ############################################

        # token match # # merge / split token match
        token_patterns = [
            r'\b\d\+\d\b', # match '1+1'
            r'\b10\+1\b', # exact match '10+1'
            r'\d+[\$]', # match '1000$'
                        ]
        # token_patterns = []

        ############################################
        ############################################
        ############################################

        # normalze text # # replace with regex  
        replace_patterns = [
            (r'\b(\d)\s*(\+)\s*([\d])\b', r'\1\2\3'), # replace '2 + 1' to '2+1'
            (r'\b(\d+[\$])(\S+?)(\s)', r'\1 \2\3'), # replace '100$. ' to '100$ . '
                            ]
        # replace_patterns = []

        ############################################
        ############################################
        ############################################

        spacy_nlp = SpacyTurkish()
        spacy_tokenizer(spacy_nlp, matchers, phrasematchers, token_patterns, replace_patterns)
        return spacy_nlp

## extension

def __example_extension():

    def __example_1():
        def my_component(doc):
            print("The doc is {} characters long and has {} tokens.".format(len(doc.text), len(doc)))
            return doc
        # The component can then be added at any position of the pipeline using the nlp.add_pipe() method. The arguments before, after, first, and last let you specify component names to insert the new component before or after, or tell spaCy to insert it first (i.e. directly after tokenization) or last in the pipeline.
        nlp = spacy.load("en_core_web_sm")
        nlp.add_pipe(my_component, name="print_length", last=True)
        doc = nlp(u"This is a sentence.")

    def __example_2():
        Doc.set_extension("hello_attr", default=True)
        Doc.set_extension("hello_property", getter=get_value, setter=set_value)
        Doc.set_extension("hello_method", method=lambda doc, name: "Hi {}!".format(name))

        doc._.hello_attr            # True
        doc._.hello_property        # return value of get_value
        doc._.hello_method("Ines")  # 'Hi Ines!'
    
    def __example_3():
        import requests
        from spacy.tokens import Token, Span
        from spacy.matcher import PhraseMatcher

        class Countries(object):
            name = 'countries'  # component name shown in pipeline

            def __init__(self, nlp, label="GPE"):
                pass
            def __call__(self, doc):
                matches = self.matcher(doc)
                return doc  # don't forget to return the Doc!

        nlp = spacy.load("en_core_web_sm")
        component = Countries(nlp)
        nlp.add_pipe(component, before="tagger")
        doc = nlp(u"Some text about Colombia and the Czech Republic")

        print([(ent.text, ent.label_) for ent in doc.ents])
        # [('Colombia', 'GPE'), ('Czech Republic', 'GPE')]

        print([(token.text, token._.country_capital) for token in doc if token._.is_country])
        # [('Colombia', 'Bogotá'), ('Czech Republic', 'Prague')]

        has_country = lambda tokens: any([token._.is_country for token in tokens])
        Doc.set_extension("has_country", getter=has_country)
        Span.set_extension("has_country", getter=has_country)

    def __example_4():
        import spacy
        from spacymoji import Emoji
        nlp = spacy.load('en')
        emoji = Emoji(nlp)
        nlp.add_pipe(emoji, first=True)

        doc  = nlp(u"This is a test 😻 👍🏿")
        assert doc._.has_emoji
        assert len(doc._.emoji) == 2
        assert doc[2:5]._.has_emoji
        assert doc[4]._.is_emoji
        assert doc[5]._.emoji_desc == u'thumbs up dark skin tone'
        assert doc._.emoji[1] == (u'👍🏿', 5, u'thumbs up dark skin tone')

    def __example_5():
        # descriptive and specific name 
        # + name = "myapp_lemmatizer"
        # - name = "lemmatizer"

        # When writing to Doc, Token or Span objects, use getter functions wherever possible, and avoid setting values explicitly. 
        # Always add your custom attributes to the global Doc, Token or Span objects, not a particular instance of them. 
        # + is_fruit = lambda token: token.text in ("apple", "orange")
        # + Token.set_extension("is_fruit", getter=is_fruit)
        # - token._.set_extension("is_fruit", default=False)
        # - if token.text in ('"apple", "orange"):
        # -     token._.set("is_fruit", True)
        # + from spacy.tokens import Doc
        # + def __init__(attr="my_attr"):
        # +     Doc.set_extension(attr, getter=self.get_doc_attr)
        # - def __call__(doc):
        # -     doc.set_extension("my_attr", getter=self.get_doc_attr)

        pass

    def __example_6():
        import your_custom_entity_recognizer
        from spacy.gold import offsets_from_biluo_tags

        def custom_ner_wrapper(doc):
            words = [token.text for token in doc]
            custom_entities = your_custom_entity_recognizer(words)
            doc.ents = spans_from_biluo_tags(doc, custom_entities)
            return doc

        pass

    def __example_7():
        pass
    def __example_8():
        pass

########################################

try:
    import stanza
    from stanza import Document as stanzaDocument
    import_stanza = True
except:
    import_stanza = False

from spacy.symbols import POS, TAG, DEP, LEMMA, HEAD
from spacy.tokens import Doc, Span, Token

import numpy
import re
import warnings
## language model

class SpacyStanzaPipeline():

    name = 'stanza_pipeline'

    """Because we're only running the Stanza pipeline once and don't split
    it up into spaCy pipeline components, we'll set all the attributes within
    a custom tokenizer. The tokenizer is currently expected to
    implement serialization methods so we're mocking them up here. When loading
    the serialized nlp object back in, you can pass `snlp` to spacy.load:
    >>> nlp.to_disk('/path/to/model')
    >>> nlp = spacy.load('/path/to/model', snlp=snlp)
    """

    to_disk = lambda self, *args, **kwargs: None
    from_disk = lambda self, *args, **kwargs: None
    to_bytes = lambda self, *args, **kwargs: None
    from_bytes = lambda self, *args, **kwargs: None
    _ws_pattern = re.compile(r"\s+")

    def __init__(self, nlp):
        """Initialize the tokenizer.
        snlp (stanza.Pipeline): The initialized Stanza pipeline.
        vocab (spacy.vocab.Vocab): The vocabulary to use.
        RETURNS (Tokenizer): The custom tokenizer.
        """
        
        stanza.download('tr')

        self.snlp = stanza.Pipeline('tr', **{'tokenize_pretokenized':True})
        self.vocab = nlp.vocab

        try:
            Token.set_extension('feats', default='')
            Token.set_extension('feats_', default='')
        except:
            print("feats/feats_ extension already exists.")

    def __call__(self, doc):
        """Convert a Stanza Doc to a spaCy Doc.
        text (unicode): The text to process.
        RETURNS (spacy.tokens.Doc): The spaCy Doc object.
        """
        snlp_doc = self.snlp([[t.text for t in doc]]) if doc else stanzaDocument("")
        text = snlp_doc.text
        tokens, heads = self.get_tokens_with_heads(snlp_doc)
        if not len(tokens):
            return doc # Doc(self.vocab)
        words = []
        spaces = []
        pos = []
        tags = []
        deps = []
        lemmas = []
        feats = []
        offset = 0
        is_aligned = self.check_aligned(text, tokens)
        for i, token in enumerate(tokens):
            span = text[offset:]
            if not len(span):
                break
            while len(span) and span[0].isspace():
                # If we encounter leading whitespace, skip one character ahead
                offset += 1
                span = text[offset:]
            words.append(token.text)
            # Make sure all strings are in the vocabulary
            pos.append(self.vocab.strings.add(token.upos or ""))
            tags.append(self.vocab.strings.add(token.xpos or ""))
            deps.append(self.vocab.strings.add(token.deprel or ""))
            lemmas.append(self.vocab.strings.add(token.lemma or ""))
            feats.append(self.vocab.strings.add(token.feats or ""))
            offset += len(token.text)
            span = text[offset:]
            if i == len(tokens) - 1:
                spaces.append(False)
            elif not is_aligned:
                spaces.append(True)
            else:
                next_token = tokens[i + 1]
                spaces.append(not span.startswith(next_token.text))
        attrs = [POS, TAG, DEP, HEAD]
        array = numpy.array(list(zip(pos, tags, deps, heads)), dtype="uint64")
        # doc = Doc(self.vocab, words=words, spaces=spaces).from_array(attrs, array)
        doc = doc.from_array(attrs, array)

        for token, feats_i in zip(doc, feats):
            token._.feats = feats_i
            token._.feats_ = self.vocab.strings[feats_i]
            
        ents = []
        for ent in snlp_doc.entities:
            ent_span = doc.char_span(ent.start_char, ent.end_char, ent.type)
            ents.append(ent_span)
        if not all(ents):
            warnings.warn(
                f"Can't set named entities because the character offsets don't "
                f"map to valid tokens produced by the Stanza tokenizer:\n"
                f"Words: {words}\n"
                f"Entities: {[(e.text, e.type, e.start_char, e.end_char) for e in snlp_doc.entities]}",
                stacklevel=4,
            )
        else:
            doc.ents = ents
        # Overwrite lemmas separately to prevent them from being overwritten by spaCy
        lemma_array = numpy.array([[lemma] for lemma in lemmas], dtype="uint64")
        doc.from_array([LEMMA], lemma_array)
        if any(pos) and any(tags):
            doc.is_tagged = True
        if any(deps):
            doc.is_parsed = True
        return doc

    def pipe(self, texts):
        """Tokenize a stream of texts.
        texts: A sequence of unicode texts.
        YIELDS (Doc): A sequence of Doc objects, in order.
        """
        for text in texts:
            yield self(text)

    def get_tokens_with_heads(self, snlp_doc):
        """Flatten the tokens in the Stanza Doc and extract the token indices
        of the sentence start tokens to set is_sent_start.
        snlp_doc (stanza.Document): The processed Stanza doc.
        RETURNS (list): The tokens (words).
        """
        tokens = []
        heads = []
        offset = 0
        for sentence in snlp_doc.sentences:
            for token in sentence.tokens:
                for word in token.words:
                    # Here, we're calculating the absolute token index in the doc,
                    # then the *relative* index of the head, -1 for zero-indexed
                    # and if the governor is 0 (root), we leave it at 0
                    if word.head:
                        head = word.head + offset - len(tokens) - 1
                    else:
                        head = 0
                    heads.append(head)
                    tokens.append(word)
            offset += sum(len(token.words) for token in sentence.tokens)
        return tokens, heads

    def check_aligned(self, text, tokens):
        token_texts = "".join(t.text for t in tokens)
        return re.sub(self._ws_pattern, "", text) == token_texts


########################################

## normalization

class SpacyEndPunctuationNormalizer():

    def __init__(self):
        pass

    def __call__(self, text):
        
        if len(text) != 0 and text[-1] not in "?!.":
            text += " ."

        return text

from pyspace.nlp.preprocessing.normalizer.xnormalizer import xNormalizer
class SpacyWhitespaceNormalizer():

    @staticmethod
    def update_entities(entities, text, ):
        normalizedtext, replace_patterns = xNormalizer.clean_text(text, return_replace_patterns=True)
        
        entities = SpacyRegexReplaceNormalizer.update_entities(entities, text, replace_patterns)
        
        return entities

    def __init__(self, ):
        pass

    def __call__(self, text):
        normalizedtext, replace_patterns = xNormalizer.clean_text(text, return_replace_patterns=True)

        text = SpacyRegexReplaceNormalizer.replace_text(text, replace_patterns)
        assert text == normalizedtext

        return text

class SpacyRegexReplaceNormalizer():

    @staticmethod
    def replace_text(text, replace_patterns):
        for p, r in replace_patterns:
            text = re.sub(p, r, text, flags=re.I)
        return text

    @staticmethod
    def update_entities(entities, text, replace_patterns=[], verbose=0):
        
        entities = sorted(entities, key=lambda x: x['start'], reverse=True)
        
        for p, r in replace_patterns:
            matches = list(re.finditer(p, text, re.I))
            matches = sorted(matches, key= lambda x: x.span()[0], reverse=True)

            for m in matches:
                rep = m.expand(r)
                lendiff = len(rep) - len(m.group())

                if verbose == 1:
                    print()
                    print(text)
                    print(p)
                    print(m)
                    print(rep)
                    print()

                tempentities = []
                for e in entities:
                    e = copy.deepcopy(e)
                    
                    # SACMALIK # (e['end'] > m.span()[0] and e['end'] < m.span()[1]) 
                    # SACMALIK # (e['start'] < m.span()[1] and e['start'] > m.span()[0])
                    
                    if e['start'] >= m.span()[1]:
                        e['start'] += lendiff
                        e['end'] += lendiff
                        tempentities.append(e)
                        
                    elif e['end'] <= m.span()[0]:
                        tempentities.append(e)
                    
                    elif (e['start'] <= m.span()[0] and e['end'] >= m.span()[1]):
                        e['end'] += lendiff
                        e['value'] = text[e['start']:m.span()[0]] + rep + text[m.span()[1]:e['end']]
                        tempentities.append(e)
                    
                    else:
                        ## TODO 
                        # from pyspace.nlp.dataset.alignment import align_fuzzy_multi
                        # fuzzy alignment can be applied.

                        print('Entity conflict with replace pattern in the text.')
                        print('    - entity  - ', e)
                        print('    - pattern - ', p)
                        print('    - match   - ', m)
                        print('    - replace - ', rep)
                        print('    - text    - ', text)
                        print()
                        print('Entity is removed from training.')
                
                entities = tempentities

            text = SpacyRegexReplaceNormalizer.replace_text(text, [(p,r)])

        return entities

    def __init__(self, replace_patterns,):
        self.replace_patterns = replace_patterns

    def __call__(self, text):
        text = SpacyRegexReplaceNormalizer.replace_text(text, self.replace_patterns)
        return text

## tokenization

class SpacyTokenizer():

    @staticmethod
    def custom_tokenizer(nlp, token_patterns):

        if token_patterns != []:
            token_pattern_combined = fr'''({'|'.join(token_patterns)})'''
            token_match = re.compile(token_pattern_combined).search
        else:
            token_match = None
        url_match = URL_MATCH
        prefixes = tuple(TOKENIZER_PREFIXES)
        suffixes = tuple(TOKENIZER_SUFFIXES)
        infixes = tuple(TOKENIZER_INFIXES)

        tokenizer_exceptions = update_exc(BASE_EXCEPTIONS, TOKENIZER_EXCEPTIONS)

        rules = tokenizer_exceptions
        token_match = token_match
        url_match = url_match
        prefix_search = (spacy.util.compile_prefix_regex(prefixes).search if prefixes else None)
        suffix_search = (spacy.util.compile_suffix_regex(suffixes).search if suffixes else None)
        infix_finditer = (spacy.util.compile_infix_regex(infixes).finditer if infixes else None)
        vocab = nlp.vocab
        return Tokenizer(
            vocab,
            rules=rules,
            prefix_search=prefix_search,
            suffix_search=suffix_search,
            infix_finditer=infix_finditer,
            token_match=token_match,
            url_match=url_match,
        )

    def __init__(self, nlp, token_patterns=[]):
        self.base_tokenizer = self.custom_tokenizer(nlp, token_patterns)

    def __call__(self, text):
        doc = self.base_tokenizer(text)
        return doc

    def pipe(self, texts, batch_size=1000, n_threads=-1):
        
        for text in texts:
            yield self(text)

class SpacyPostTokenizer():

    @staticmethod
    def update_entities(entities, doc):
        entities = SpacyPostTokenizer.sort_and_validate_posttokenization(entities)

        result = []

        for e in entities:
            entity_text = e['entity']
            entity_role_text = e['role'] if 'role' in e else None
            related_tokens = SpacyPostTokenizer.match_entity_in_doc(e, doc)
            first_related_token = related_tokens[0]

            temp = {}
            temp['start'] = first_related_token.idx
            temp['end'] = first_related_token.idx + len(first_related_token.text)
            temp['value'] = first_related_token.text
            temp['entity'] = entity_text
            if entity_role_text:
                temp['role'] = entity_role_text
            result.append(temp)
            
            entity_text = re.sub('^B-', 'I-', entity_text)

            for t in related_tokens[1:]:
                    
                temp = {}
                temp['start'] = t.idx
                temp['end'] = t.idx + len(t.text)
                temp['value'] = t.text
                temp['entity'] = entity_text
                if entity_role_text:
                    temp['role'] = entity_role_text
                result.append(temp)
        
        return result

    @staticmethod
    def match_entity_in_doc(e, doc):
        related_tokens = []
        for t in doc:
            
            if ( e['start'] <= t.idx+len(t.text)-1 ) and related_tokens == []:
                related_tokens.append(t)
                
            elif e['end']-1 >= t.idx and related_tokens != []:
                related_tokens.append(t)
                
            elif related_tokens != []:
                break

        if related_tokens == []:
            print(e, doc)
            assert 1 == 0
            
        return related_tokens
        
    @staticmethod
    def split_edges(e, doc):
        related_tokens = SpacyPostTokenizer.match_entity_in_doc(e, doc)

        ft = related_tokens[0]
        fts = ft.idx
        fte = fts + len(ft.text)

        lt = related_tokens[-1]
        lts = lt.idx
        lte = lts + len(lt.text)

        es = e['start']
        ee = e['end']

        with doc.retokenize() as retokenizer:
            if fts != es:
                me = min(ee,fte)
                retokenizer.split(ft, [doc.text[fts:es], doc.text[es:me]], heads=[(ft,0), (ft,1)], attrs={})
                
            if lte != ee and len(related_tokens) != 1:
                retokenizer.split(lt, [doc.text[lts:ee], doc.text[ee:lte]], heads=[(lt,0), (lt,1)], attrs={})
            
            
        return doc
    
    @staticmethod
    def merge_posttokenization(e, doc):
        related_tokens = SpacyPostTokenizer.match_entity_in_doc(e, doc)

        with doc.retokenize() as retokenizer:
            span = doc[related_tokens[0].i:related_tokens[-1].i+1]
            retokenizer.merge(span, ) 

        return doc

    @staticmethod
    def sort_and_validate_posttokenization(posttokenization):
        posttokenization = sorted(posttokenization, key=lambda x: x['start'])
        assert all([posttokenization[i-1]['end']<=posttokenization[i]['start'] for i in range(1, len(posttokenization))])
        return posttokenization

    def __init__(self, merge_bool=False, verbose=1, ):
        self.verbose = verbose
        self.merge_bool = merge_bool
        pass

    def __call__(self, doc, posttokenization=[], ):
        """
        posttokenization = [
            {'start': 4, 'end': 13, 'value': 'y kredi k', 'entity': 'B-account'}
            {'start': 18, 'end': 24, 'value': 'borcum', 'entity': 'I-account'}
        ]
        """

        posttokenization = SpacyPostTokenizer.sort_and_validate_posttokenization(posttokenization)
        
        unprocessed_tokens = [t.text for t in doc]
        
        for e in posttokenization:
            doc = SpacyPostTokenizer.split_edges(e, doc)
        
        if self.merge_bool:
            for e in posttokenization:
                doc = SpacyPostTokenizer.merge_posttokenization(e, doc)

        processed_tokens = [t.text for t in doc]
        
        if self.verbose == 1 and unprocessed_tokens != processed_tokens:
            print('before : ', unprocessed_tokens)
            print('after  : ', processed_tokens)

        return doc

## merge multiword entities

class SpacyMatcherMerger():
    name = 'matcher_merger'

    @staticmethod
    def add_matchers(nlp, matchers):
        if matchers == []:
            return None
        
        matcher = Matcher(nlp.vocab)
        for m in matchers:
            matcher.add(m[0], m[2], *m[1])

        return matcher

    @staticmethod
    def add_phrase_matchers(nlp, phrasematchers):
        if phrasematchers == []:
            return None
        
        matcher = PhraseMatcher(nlp.vocab,)
        # patterns = [nlp.make_doc(text) for text in terms]
        # patterns = [nlp.make_doc(text) for text in pm[1]]
        for pm in phrasematchers:
            patterns = list(nlp.tokenizer.pipe(pm[1])) # FASTEST
            matcher.add(pm[0], pm[2], *patterns)

        return matcher

    @staticmethod
    def add_entity(matcher, doc, i, matches):

        match_id, start, end = matches[i]
        string_id = matcher.vocab.strings[match_id]        
        entity = Span(doc, start, end, label=string_id)

        #################################################################
        # check existing entity
        #################################################################
        __doc_ents = {}
        __doc_ents.update(  { (s.start, s.end) : s for s in doc.ents} )
        __doc_ents.update(  { position : s for s in doc.ents for position in list(range(s.start, s.end))} )
        
        __intersection = list(set(range(start,end)).intersection(set(__doc_ents.keys())))
        if __intersection != []:
            print('Overlapping entity', __doc_ents[__intersection[0]], __doc_ents[__intersection[0]].label_, entity, entity.label_)
            matches[i] = [] # remove match if an entity already exists
            return
        #################################################################

        doc.ents += (entity,)

    def __init__(self, nlp, matchers=[], phrasematchers=[]):

        matchers = [(i[0], i[1], self.add_entity) for i in matchers]
        phrasematchers = [(i[0], i[1], self.add_entity) for i in phrasematchers]
        defaultmatchers = [
            ('<num>', [[{"LIKE_NUM": True}, ],]),
            ('<url>', [[{"LIKE_URL": True}, ],]),
            ('<email>', [[{"LIKE_EMAIL": True}, ],]),]
        defaultmatchers = [(i[0], i[1], self.add_entity) for i in defaultmatchers]

        self.nlp = nlp
        self.custom_matcher = self.add_matchers(nlp, matchers)
        self.custom_phrasematcher = self.add_phrase_matchers(nlp, phrasematchers)
        self.custom_defaultmatcher = self.add_matchers(nlp, defaultmatchers)

    def __call__(self, doc):
        def matcher_merge(matcher, doc):
            matches = matcher(doc)
            matches = [m for m in matches if m != []] # add_entity callback # remove match if an entity already exists

            with doc.retokenize() as retokenizer:
                for match_id, start, end in matches:
                    string_id = self.nlp.vocab.strings[match_id]  
                    span = doc[start:end]  # The matched span
                    # print(match_id, string_id, start, end, span.text)
                    # print(string_id, start, end, span.text)
                    retokenizer.merge(span, ) 

        if self.custom_phrasematcher:
            matcher_merge(self.custom_phrasematcher, doc)
        if self.custom_matcher:
            matcher_merge(self.custom_matcher, doc)
        if self.custom_defaultmatcher:
            matcher_merge(self.custom_defaultmatcher, doc)

        ############################################

        return doc


## update entities

class SpacyMatcherEntityUpdater():
    name = 'matcher_entity_updater'

    @staticmethod
    def add_matchers(nlp, matchers):
        if matchers == []:
            return None
        
        matcher = Matcher(nlp.vocab)
        for m in matchers:
            matcher.add(m[0], m[2], *m[1])

        return matcher

    @staticmethod
    def update_entity(matcher, doc, i, matches):

        match_id, start, end = matches[i]
        string_id = matcher.vocab.strings[match_id]
        
        update_indices = list(range(start, end))
        update_entities = string_id.split('___')
        existing_entities = [doc[i].ent_type_ for i in update_indices]
        update_entities = [up if up != 'X' else ex for up, ex in zip(update_entities, existing_entities)]
        update_entities = tuple(Span(doc, idx, idx+1, label=en) for idx, en in zip(update_indices, update_entities) )
        
        if all([not doc[idx]._.is_entity_rule_applied for idx in update_indices]) or doc._.is_entity_rule_override:
            doc.ents = doc.ents[0:start] + update_entities + doc.ents[end:]

            for idx in update_indices:
                doc[idx]._.is_entity_rule_applied = True
        

    def __init__(self, nlp, matchers_list=[], verbose=0, is_entity_rule_override=False):

        matchers_list = [[(i[0], i[1], self.update_entity) for i in matchers] for matchers in matchers_list]
        matchers_list = [self.add_matchers(nlp, matchers) for matchers in matchers_list]

        self.nlp = nlp
        self.matchers_list = matchers_list
        self.verbose = verbose


        Doc.set_extension('is_entity_rule_override', default=is_entity_rule_override, force=True)
        try:
            Token.set_extension('is_entity_rule_applied', default=False)
        except:
            pass

    def __call__(self, doc):

        prev_ents = tuple(Span(s.doc, s.start, s.end, label=s.label_) for s in doc.ents) 

        for matcher in self.matchers_list:
            matcher(doc)

        if self.verbose:
            __updates = [(ds.text, " "*(15-len(ds.text)), ps.label_, " "*(12-len(ps.label_)), ds.label_, ) for ps, ds in zip(prev_ents, doc.ents) if ds.label_ != ps.label_]
            if __updates:
                print(doc.text)
                for u in __updates:
                    print('  - ',*u)
                print()
            # [print(ds.text, " "*(15-len(ds.text)), ps.label_, " "*(12-len(ps.label_)), ds.label_, ) for ps, ds in zip(prev_ents, doc.ents) if ds.label_ != ps.label_]

        return doc

    def help(self,):
        response = ""

        response = """
            # ('B-account___X', [[{"ENT_TYPE": "B-account"}, {"ENT_TYPE": "I-account"} ],]),
            # ('B-accountX', [[{"LOWER": "kredi"}, ],]),
            # ('<emoji>', [[{"_": {"is_emoji": True}}],]),
            # ('temp', [[{"LOWER": {"REGEX": r"^.*?$"}}]]),
            # [('B-account___XY', [[{"ENT_TYPE": "B-account"}, {"ENT_TYPE": "I-account"} ],]),],
            # [('temp', [[{"LOWER": {"REGEX": r"^.*?$"}}]]),]
            #     [('temp', [[{"LOWER": {"REGEX": r"^hesa", "ENT_TYPE":"O"}}]]),] # FALSE
            #     [('temp', [[{"LOWER": {"REGEX": r"^hesa", "ENT_TYPE":{"!=": "O"},}}]]),]  # NOT WORKING
            #     [('temp', [[{"LOWER": {"REGEX": r"^hesa",}, "ENT_TYPE":{"NOT_IN": ["O"]},} ]]),] # WORKS
            #     [('temp', [[{"LOWER": {"REGEX": r"^hesa",}, "ENT_TYPE":{"!=": "O"},} ]]),] # NOT WORKING
            #     [('temp', [[{"LOWER": {"REGEX": r"^hesa",}, "ENT_TYPE": "O", "OP":"!"} ]]),] # NEGATE ALL
            #     [('temp', [[{"LOWER": {"REGEX": r"^hesa",}, "ENT_TYPE":{"REGEX": "O", "OP":"!"}} ]]),] # NOT WORKING
            #     [('temp', [[{"LOWER": {"REGEX": r"^hesa",}, "ENT_TYPE":{"REGEX": "(?!O).+",}} ]]),] # WORKING
            #     [('temp', [[{"LOWER": {"REGEX": r"^hesa",}, "ENT_TYPE":{"REGEX": "(?!O)",}} ]]),] # NOT WORKING

            # matcher order is important
            # first matcher is applied
            # then 'is_entity_rule_applied' extension blocks the others

            # sdoc = matcherupdater(copy.deepcopy(psdocs[0]))
            # # print([(t.text, t.ent_type_) for t in sdoc])
        """

        



## usable class container

from spacymoji import Emoji

class SpacyNLP():

    def __init__(self, config={}):

        defaults = {
            'embedding_model': False,

            'whitespace_normalizer':True,
            'token_patterns':[], 
            'replace_patterns':[],

            'post_tokenization_bool':True, 
            'post_tokenization_merge_bool':False, 
            'emoji_bool':True,
            'stanza_bool':True,

            'matchers':[],
            'phrasematchers':[],
            }
        defaults.update(config)

        if defaults['embedding_model']:
            if defaults['embedding_model'] == 'fasttext_tr':
                try:
                    nlp = spacy.load('fasttext_tr')
                    backupnlp = SpacyTurkish()
                    backupnlp.vocab = nlp.vocab
                except:
                    print('Error, could not load fasttext_tr.')

        else:
            nlp = SpacyTurkish()
            backupnlp = SpacyTurkish()
            backupnlp.vocab = nlp.vocab

        nlp.tokenizer = lambda x: x
        
        nlp.add_pipe(SpacyWhitespaceNormalizer()) if defaults['whitespace_normalizer'] else None
        nlp.add_pipe(SpacyRegexReplaceNormalizer(defaults['replace_patterns'])) if defaults['replace_patterns'] else None
        nlp.add_pipe(SpacyEndPunctuationNormalizer())
        nlp.add_pipe(SpacyTokenizer(nlp, token_patterns=defaults['token_patterns']))
        nlp.add_pipe(SpacyPostTokenizer(merge_bool=defaults['post_tokenization_merge_bool'])) if defaults['post_tokenization_bool'] else None

        [nlp.add_pipe(Emoji(backupnlp)), defaults['matchers'].append(('<emoji>', [[{"_": {"is_emoji": True}}],]))] if defaults['emoji_bool'] else None
        nlp.add_pipe(SpacyStanzaPipeline(backupnlp)) if defaults['stanza_bool'] else None

        nlp.add_pipe(SpacyMatcherMerger(backupnlp, matchers=defaults['matchers'], phrasematchers=defaults['phrasematchers'])) if defaults['matchers'] or defaults['phrasematchers'] else None


        self.defaults = defaults
        self.nlp = nlp
        self.backupnlp = backupnlp

    def __call__(self, text, entities=[]):

        if entities:
            spacy_pipelines = dict(self.nlp.pipeline)
            temptext = text

            if 'SpacyWhitespaceNormalizer' in spacy_pipelines:
                entities = spacy_pipelines['SpacyWhitespaceNormalizer'].update_entities(entities, text, )
                temptext = spacy_pipelines['SpacyWhitespaceNormalizer'](text)
            if 'SpacyRegexReplaceNormalizer' in spacy_pipelines:
                replace_patterns = spacy_pipelines['SpacyRegexReplaceNormalizer'].replace_patterns
                entities = spacy_pipelines['SpacyRegexReplaceNormalizer'].update_entities(entities, temptext, replace_patterns)
            if 'SpacyPostTokenizer' in spacy_pipelines:
                doc = self.nlp(text, component_cfg={"SpacyPostTokenizer": {"posttokenization": entities, }})
                entities = spacy_pipelines['SpacyPostTokenizer'].update_entities(entities, doc)
            else:
                doc = self.nlp(text)

            return doc, entities

        else:
            doc = self.nlp(text)
            return doc        