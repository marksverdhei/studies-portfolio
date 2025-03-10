import random
import json

from zipfile import ZipFile
from io import TextIOWrapper
from collections import namedtuple

Document = namedtuple('Document', ['text', 'metadata'])

class Norec(object):
    def __init__(self, filename, metadata):
        self.zf = ZipFile(filename)

        with open(metadata, encoding="utf-8") as fd:
            self.metadata = json.load(fd)


    def open(self, member, mode="r", encoding=None):
        return TextIOWrapper(self.zf.open(member, mode),
                             encoding=encoding)

    def document_list(self):
        return self.zf.namelist()

    def get_document(self, filename):
        with self.open(filename, encoding="utf-8") as fd:
            return fd.read()

    def get_metadata(self, filename):
        ident = '{0:0>6}'.format(filename.split(".")[0])

        return self.metadata[ident]

    def random_document(self):
        return random.choice(self.document_list())

    def iter_documents(self, subset=None):
        for name in self.document_list():
            doc = Document(self.get_document(name), self.get_metadata(name))
            if not subset or doc.metadata['split'] == subset:
                yield doc

    def train_set(self):
        return self.iter_documents("train")

    def dev_set(self):
        return self.iter_documents("dev")

    def test_set(self):
        return self.iter_documents("test")
