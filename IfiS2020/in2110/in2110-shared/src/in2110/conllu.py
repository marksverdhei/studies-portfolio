from collections import OrderedDict
from spacy.tokens import Doc

class ConlluToken(OrderedDict):
    KEYS = (("id", int),
            ("form", str),
            ("lemma", str),
            ("upos", str),
            ("xpos", str),
            ("feats", str),
            ("head", int),
            ("deprel", str),
            ("deps", str),
            ("misc", str))

    def __init__(self, *values):
        super().__init__(
            ((k, fn(v))
             for (k, fn), v in zip(self.KEYS, values)))

class ConlluSentence(list):
    def to_spacy(self, model, keep_labels=True):
        words, spaces = zip(*((t['form'], t['misc'] != "SpaceAfter=No")
                               for t in self))

        doc = Doc(model.vocab, words, spaces)

        if keep_labels:
            for t1, t2 in zip(self, doc):
                t2.tag_ = t1['upos']
                t2.lemma_ = t1['lemma']
                if t1['head'] > 0:
                    t2.head = doc[t1['head'] - 1]
                else:
                    t2.head = t2
                t2.dep_ = t1['deprel']

            doc.is_tagged = True
            doc.is_parsed = True

        return doc

class ConlluDoc(list):
    @classmethod
    def from_file(cls, filename):
        with open(filename, encoding="utf-8") as fd:
            sentences = cls()
            sentence = ConlluSentence()

            for line in (line.strip() for line in fd):
                if line.startswith("#"):
                    continue
                if not line:
                    sentences.append(sentence)
                    sentence = ConlluSentence()
                else:
                    sentence.append(ConlluToken(*line.split("\t")))

        return sentences

    def to_spacy(self, model, keep_labels=True):
        return [sent.to_spacy(model, keep_labels) for sent in self]
