import gzip

from io import TextIOWrapper

class NAK(object):
    def __init__(self, filename):
        self.filename = filename

    def open(self, encoding="iso-8859-1"):
        return TextIOWrapper(gzip.open(self.filename),
                             encoding=encoding)

    def sentences(self):
        with self.open() as fd:
            for line in fd:
                yield line.strip()

