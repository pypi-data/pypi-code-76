from neomodel import (
    FloatProperty,
    IntegerProperty,
    Relationship,
    RelationshipTo,
    StringProperty,
    StructuredNode,
    StructuredRel,
    UniqueIdProperty,
    DateTimeProperty,
    BooleanProperty,
)


class Topic(StructuredNode):
    text = StringProperty(required=True)
    process_datetime = DateTimeProperty(default_now=True)


class Sentiment(StructuredNode):
    sentiment = IntegerProperty(required=True)
    process_datetime = DateTimeProperty(default_now=True)

    
class Emoji(StructuredNode):
    label = StringProperty(required=True)
    pax_label = StringProperty(required=True)
    group = StringProperty(required=True)
    plutchik_category = StringProperty()
    process_datetime = DateTimeProperty(default_now=True)


class EmojiRel(StructuredRel):
    intensity = IntegerProperty(required=False)
    probability = FloatProperty(required=False)


class User(StructuredNode):
    uid = StringProperty(required=True)
    process_datetime = DateTimeProperty(default_now=True)
    anonymous = BooleanProperty()
    

class Comment(StructuredNode):
    uid = StringProperty(required=True)
    text = StringProperty(required=True)
    client_id = StringProperty(required=True)
    forum_id = StringProperty(required=True)
    conversation_id = StringProperty()
    create_datetime = DateTimeProperty(default_now=False)
    process_datetime = DateTimeProperty(default_now=True)
    avg_sentiment = Relationship(Sentiment, 'HAS_AVG_SENTIMENT')
    emoji = Relationship(Emoji, 'HAS_EMOJI', model=EmojiRel)
    topic = Relationship(Topic, 'HAS_TOPIC')
    user = Relationship(User, 'POSTED_BY')

class Sentence(StructuredNode):
    uid = UniqueIdProperty()
    text = StringProperty(required=True)
    client_id = StringProperty(required=True)
    forum_id = StringProperty(required=True)
    conversation_id = StringProperty()
    process_datetime = DateTimeProperty(default_now=True)
    comment = Relationship(Comment, 'DECOMPOSES')
    sentiment = Relationship(Sentiment, 'HAS_SENTIMENT')
    emoji = Relationship(Emoji, 'HAS_EMOJI', model=EmojiRel)
    topic = Relationship(Topic, 'HAS_TOPIC')


class Chunk(StructuredNode):
    uid = UniqueIdProperty()
    text = StringProperty(required=True)
    client_id = StringProperty(required=True)
    forum_id = StringProperty(required=True)
    conversation_id = StringProperty()
    process_datetime = DateTimeProperty(default_now=True)
    comment = Relationship(Comment, 'DECOMPOSES')
    sentiment = Relationship(Sentiment, 'HAS_SENTIMENT')
    emoji = Relationship(Emoji, 'HAS_EMOJI', model=EmojiRel)
    topic = Relationship(Topic, 'HAS_TOPIC')


class Question(StructuredNode):
    uid = UniqueIdProperty()
    text = StringProperty(required=True)
    client_id = StringProperty(required=True)
    forum_id = StringProperty(required=True)
    conversation_id = StringProperty()
    process_datetime = DateTimeProperty(default_now=True)


class ClusterHead(StructuredNode):
    uid = UniqueIdProperty()
    text = StringProperty(required=True)
    similarity_score = FloatProperty(required=True)
    element_count = IntegerProperty()
    client_id = StringProperty(required=True)
    forum_id = StringProperty(required=True)
    conversation_id = StringProperty()
    process_datetime = DateTimeProperty(default_now=True)
    question = Relationship(Question, 'ANSWERS')


class ClusterElement(StructuredNode):
    uid = UniqueIdProperty()
    text = StringProperty(required=True)
    client_id = StringProperty(required=True)
    forum_id = StringProperty(required=True)
    conversation_id = StringProperty()
    process_datetime = DateTimeProperty(default_now=True)
    sentences = Relationship(Sentence, 'DERIVES_FROM')
    chunks = Relationship(Chunk, 'DERIVES_FROM')
    cluster_head = Relationship(ClusterHead, 'DECOMPOSES')
    