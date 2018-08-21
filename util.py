# -*- coding: utf-8 -*-H

import re


class WordIn(object):

    __kusa = re.compile("[wW草]")
    __8 = re.compile("[8]")

    @classmethod
    def siba(cls, text):
        return cls.__isin(cls.__kusa, text)

    @classmethod
    def patipati(cls, text):
        return cls.__isin(cls.__8, text)

    @staticmethod
    def __isin(ptn, text):
        return re.search(ptn, text) is not None


if __name__ == '__main__':
    s = "あいうえお"
