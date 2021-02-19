from asn1crypto.core import Sequence, VisibleString, Integer, SequenceOf, Choice, UTF8String, Null

class Textseqid(Sequence):
    _fields = [
        ('name', VisibleString, {"optional": True}),
        ('accession', VisibleString, {"optional": True}),
        ('release', VisibleString, {"optional": True}),
        ('version', Integer, {"optional": True})
    ]

class ObjectId(Choice):
    _alternatives = [
        ('id', Integer),
        ('str', VisibleString)
    ]
    
class GiimportId(Sequence):
    _fields = [
        ('id', Integer),
        ('db', VisibleString, {"optional": True}),
        ('release', VisibleString, {"optional": True})
    ]

class Dbtag(Sequence):
    _fields = [
        ('db', VisibleString),
        ('tag', ObjectId)
    ]

class SeqId(Choice):
    _alternatives = [
        ('local', ObjectId),
        ('gibbsq', Integer),
        ('gibbmt', Integer),
        ('giim', GiimportId),
        ('genbank', Textseqid),
        ('embl', Textseqid),
        ('pir', Textseqid),
        ('swissprot', Textseqid),
        ('patent', Integer),
        ('other', Textseqid), # for historical reasons, 'other' = 'refseq'
        ('general', Dbtag),
        ('gi', Integer),
        ('ddbj', Textseqid),
        ('prf', Textseqid),
        ('pdb', Integer),
        ('tpg', Textseqid),
        ('tpe', Textseqid),
        ('tpd', Textseqid),
        ('gpipe', Textseqid),
        ('named-annot-track', Textseqid)
    ]

class SeqIds(SequenceOf):
    _child_spec = SeqId

class other(SequenceOf):
    _child_spec = Integer

class Defline(Sequence):
    _fields = [
        ('title', VisibleString, {"optional": True}),
        ('seqid', SeqIds),
        ('taxid', Integer, {"optional": True}),
#        ('other1', other, {"optional": True}),
#        ('other2', other, {"optional": True}),
#        ('other3', other, {"optional": True})
    ]

