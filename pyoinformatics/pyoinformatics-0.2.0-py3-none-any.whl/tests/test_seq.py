from pyoinformatics.seq import Seq, consensus


def test_init():
    assert type(Seq("TATA")) == Seq


def test_repr():
    seq1 = Seq("TATA")
    seq2 = Seq("TATA", id="seq2")
    assert repr(seq1) == "Seq(TATA)"
    assert repr(seq2) == "Seq(TATA, id='seq2')"


def test_str():
    seq = Seq("TATA")
    assert str(seq) == "TATA"


def test_len():
    seq = Seq("TATA")
    assert len(seq) == 4


def test_invert():
    seq = Seq("GGAATT")
    assert (~seq).sequence == "AATTCC"


def test_add():
    seq1 = Seq("GGAATT")
    seq2 = Seq("TATA")
    assert (seq1 + seq2).sequence == "GGAATTTATA"


def test_sub():
    seq1 = Seq("TTTT")
    seq2 = Seq("TATA")
    assert (seq1 - seq2) == 2


def test_contains():
    assert Seq("AT") in Seq("ATG")
    assert "AT" in Seq("ATG")
    assert (Seq("ATC") in Seq("ATG")) == False


def test_gc():
    seq = Seq("GCAT")
    assert seq.gc == 50


def test_counts():
    seq = Seq("GGAATT")
    assert seq.counts == {"G": 2, "A": 2, "T": 2}


def test_consensus():
    seq1 = Seq("GGAATT")
    seq2 = Seq("GTAATT")
    seq3 = Seq("TTTTTT")
    assert consensus(seq1, seq2, seq3) == "GTAATT"


def test_fasta():
    seq = Seq(
        id="Example fasta",
        sequence="GGAATTGGAATTGGAATTGGAATTGGAATTGGAATTGGAATTGGAATTGGAATTGGAATTGGAATTGGAATTGGAATTGGAATTGGAATTGGAATTGGAATTGGAATTGGAATTGGAATTGGAATTGGAATTGGAATTGGAATTGGAATTGGAATT",
    )
    fasta = (
        ">Example fasta\n"
        "GGAATTGGAATTGGAATTGGAATTGGAATTGGAATTGGAATTGGAATTGG\n"
        "AATTGGAATTGGAATTGGAATTGGAATTGGAATTGGAATTGGAATTGGAA\n"
        "TTGGAATTGGAATTGGAATTGGAATTGGAATTGGAATTGGAATTGGAATT\n"
        "GGAATT\n"
    )
    assert seq.to_fasta(50) == fasta


def test_count():
    seq1 = Seq("GGGAATT")
    assert seq1.count("G") == 3
    assert seq1.count("GG") == 1
    assert seq1.count("GG", 1) == 3


def test_substitute():
    seq1 = Seq("GGAATT")
    assert seq1.substitute("T", "U") == "GGAAUU"
    assert seq1.substitute("T", "U", 1) == "GGAAUT"


def test_find():
    seq1 = Seq("ACGGGATGATG")
    assert seq1.find("A") == [0, 5, 8]
    assert seq1.find("A", count=1) == [0]
    assert seq1.find("GATG", overlapping=False) == [4]
    assert seq1.find("GATG", overlapping=True) == [4, 7]
    assert len(seq1.find("A[CT]G")) == 3
