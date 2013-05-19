# coding: utf-8
import sys
import csv
import json


class UnicodeDictReader(csv.DictReader):
    """値をデコードするDictReader
    """

    def __init__(self, f, fieldnames=None, restkey=None, restval=None,
                 dialect="excel", encoding="cp932", *args, **kwds):
        csv.DictReader.__init__(
            self, f, fieldnames, restkey, restval, dialect, *args, **kwds)
        self.encoding = encoding

    def decode(self, value):
        return value and value.decode(self.encoding) or value

    def next(self):
        d = csv.DictReader.next(self)
        for key in d:
            d[key] = self.decode(d[key])
        return d


def main():
    filename = sys.argv[1]
    if len(sys.argv) > 2:
        encoding = sys.argv[2]
    else:
        encoding = 'cp932'
    with open(filename) as fin:
        reader = UnicodeDictReader(fin, encoding=encoding)
        output = json.dumps(list(reader), indent=2)
    print(output)


if __name__ == '__main__':
    main()
