# -*- coding=utf-8 -*-

import re, os, codecs
from whoosh.analysis import RegexAnalyzer,LowercaseFilter,StopFilter,StemFilter
from whoosh.analysis import Tokenizer,Token 
from whoosh.lang.porter import stem

import cppjiebapy

STOP_WORDS = None
def __init_stop_words():
    global STOP_WORDS
    stop_words = []
    curpath = os.path.normpath( os.path.join( os.getcwd(), os.path.dirname(__file__) )  )
    with codecs.open(os.path.join(curpath, 'dict', 'stopword.dic'), "r", "utf-8") as file:
        for line in file:
            tokens = line.split(" ")
            term = tokens[0].strip()
            if len(term)>0:
                stop_words.append(term)
    STOP_WORDS = frozenset(stop_words)
__init_stop_words()

accepted_chars = re.compile(ur"[\u4E00-\u9FA5]+")
ignore_numbers = re.compile(ur"[\d\s]+", re.U|re.I|re.M)

def tokenize_1(text):
    start = 0
    for term in cppjiebapy.cut(text):
        width = len(term)
        yield (term, start, start+width)
        start += width

class ChineseTokenizer(Tokenizer):
    def __call__(self,text,**kargs):
        words = tokenize_1(text)
        token  = Token()
        for (w,start_pos,stop_pos) in words:
            if not accepted_chars.match(w):
                if len(w) <= 1:
                    continue
            token.original = token.text = w
            token.pos = start_pos
            token.startchar = start_pos
            token.endchar = stop_pos
            yield token


def ChineseAnalyzer(stoplist=STOP_WORDS,minsize=1,stemfn=stem,cachesize=50000):
    return ChineseTokenizer()|LowercaseFilter()\
            |StemFilter(stemfn=stemfn, ignore=None,cachesize=cachesize)\
            |StopFilter(stoplist=stoplist,minsize=minsize)

