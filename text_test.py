import pytest

from text import *

from random import choice
from math import isclose

def  test_unigram_text_model():
    flatland = DataFile("aima-data/EN-text/flatland.txt").read()
    wordseq = words(flatland)
    P = UnigramTextModel(wordseq)

    s, p = viterbi_segment('itiseasytoreadwordswithoutspaces', P)

    assert s == ['it', 'is', 'easy', 'to', 'read', 'words', 'without', 'spaces']

def test_shift_encoding():
    code = shift_encode("This is a secret message.", 17)

    assert code == 'Kyzj zj r jvtivk dvjjrxv.'

def test_shift_decoding():
    code = shift_encode("This is a secret message.", 17)

    ring = ShiftDecoder(flatland)
    msg = ring.decode('Kyzj zj r jvtivk dvjjrxv.')

    assert msg == 'This is a secret message.'

def test_rot13_decoding():
    msg = ring.decode(rot13('Hello, world!'))

    assert msg == 'Hello, world!'

def test_counting_probability_distribution():
    D = CountingProbDist()

    for i in range(10000):
        D.add(random.choice('123456'))

    ps = [D[n] for n in '123456']

    assert 1/7 <= min(ps) <= max(ps) <= 1/5

def test_ngram_models():
    flatland = DataFile("aima-data/EN-text/flatland.txt").read()
    wordseq = words(flatland)
    P1 = UnigramTextModel(wordseq)
    P2 = NgramTextModel(2, wordseq)
    P3 = NgramTextModel(3, wordseq)

    ## The most frequent entries in each model
    assert P1.top(10) == [(2081, 'the'), (1479, 'of'), (1021, 'and'), (1008, 'to'), (850, 'a'), 
                            (722, 'i'), (640, 'in'), (478, 'that'), (399, 'is'), (348, 'you')]

    assert P2.top(10) == [(368, ('of', 'the')), (152, ('to', 'the')), (152, ('in', 'the')), (86, ('of', 'a')), 
                            (80, ('it', 'is'   )), (71, ('by', 'the' )), (68, ('for', 'the'  )),
                            (68, ('and', 'the' )), (62, ('on', 'the' )), (60, ('to', 'be'))]

    assert P3.top(10) == [(30, ('a', 'straight', 'line')), (19, ('of', 'three', 'dimensions')), 
                            (16, ('the', 'sense', 'of'         )), (13, ('by', 'the', 'sense'   )),
                            (13, ('as', 'well', 'as'           )), (12, ('of', 'the', 'circles' )),
                            (12, ('of', 'sight', 'recognition' )), (11, ('the', 'number', 'of'  )),
                            (11, ('that', 'i', 'had'           )), (11, ('so', 'as', 'to'))]


    assert isclose(P1['the'], 0.0611)

    assert isclose(P2['of', 'the'], 0.0108)

    assert isclose(P3['', '', 'but'], 0.0)
    assert isclose(P3['', '', 'but'], 0.0)
    assert isclose(P3['so', 'as', 'to'], 0.000323)

    assert not P2.cond_prob['went',].dictionary

    assert P3.cond_prob['in','order'].dictionary == {'to': 6}

def test_ir_system():
    from collections import namedtuple
    Results = namedtuple('IRResults', ['score', 'url'])

    uc = UnixConsultant()

    def verify_query(query, expected):
        assert len(expected) == len(query)

        for expected, (score, d) in zip(expected, query):
            doc = uc.documents[d]

            assert expected.score == score * 100
            assert expected.url == doc.url

    q1 = uc.query("how do I remove a file")
    assert verify_query(q1, [
        Results(76.83, "../aima-data/MAN/rm.txt"),
        Results(67.83, "../aima-data/MAN/tar.txt"),
        Results(67.79, "../aima-data/MAN/cp.txt"),
        Results(66.58, "../aima-data/MAN/zip.txt"),
        Results(64.58, "../aima-data/MAN/gzip.txt"),
        Results(63.74, "../aima-data/MAN/pine.txt"),
        Results(62.95, "../aima-data/MAN/shred.txt"),
        Results(57.46, "../aima-data/MAN/pico.txt"),
        Results(43.38, "../aima-data/MAN/login.txt"),
        Results(41.93, "../aima-data/MAN/ln.txt"),
    ])

    q2 = uc.query("how do I delete a file")
    assert verify_query(q2, [
        Results(75.47, "../aima-data/MAN/diff.txt"),
        Results(69.12, "../aima-data/MAN/pine.txt"),
        Results(63.56, "../aima-data/MAN/tar.txt"),
        Results(60.63, "../aima-data/MAN/zip.txt"),
        Results(57.46, "../aima-data/MAN/pico.txt"),
        Results(51.28, "../aima-data/MAN/shred.txt"),
        Results(26.72, "../aima-data/MAN/tr.txt"),
    ])

    q3 = uc.query("email")
    assert verify_query(q3, [
        Results(18.39, "../aima-data/MAN/pine.txt"),
        Results(12.01, "../aima-data/MAN/info.txt"),
        Results(9.89, "../aima-data/MAN/pico.txt"),
        Results(8.73, "../aima-data/MAN/grep.txt"),
        Results(8.07, "../aima-data/MAN/zip.txt"),
    ])

    q4 = uc.query("word countrs for files")
    assert verify_query(q4, [
        Results(112.38, "../aima-data/MAN/grep.txt"),
        Results(101.84, "../aima-data/MAN/wc.txt"),
        Results(82.46, "../aima-data/MAN/find.txt"),
        Results(74.64, "../aima-data/MAN/du.txt"),
    ])

    q5 = uc.query("learn: date")
    assert verify_query(q5, [])

    q6 = uc.query("2003")
    assert verify_query(q6, [
        Results(14.58, "../aima-data/MAN/pine.txt"),
        Results(11.62, "../aima-data/MAN/jar.txt"),
    ])

if __name__ == '__main__':
    pytest.main()
