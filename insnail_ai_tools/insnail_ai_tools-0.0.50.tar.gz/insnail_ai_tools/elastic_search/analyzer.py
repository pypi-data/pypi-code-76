from elasticsearch_dsl.analysis import analyzer

word_analyzer = analyzer(
    "word_analyzer", tokenizer="standard", filter=["lowercase", "stop", "snowball"]
)
