# -*- coding=utf-8 -*-

import sys, os.path, codecs, re, math
import collections
import threading
from functools import wraps

import mixsegment

try:
    import whoosh
    from analyzer import ChineseAnalyzer, Tokenize
except ImportError:
    # install whoosh to using ChineseAnalyzer
    pass

SEG_LOCK = threading.RLock()
SEG_INIT = False
segment_wrapper = None

# copy some codes from http://github.com/jannson/yaha
def get_sentence_dict():
    cutlist = "\s.[。，,！……!《》<>\"':：？\?、\|\\/“”‘’；]{}（）{}【】()｛｝（）：？！。，;、~——+％%`:“”＂'‘\n\r"
    if not isinstance(cutlist, unicode):
        cutlist = cutlist.decode('utf-8')
    cutlist_dict = []
    for c in list(cutlist):
        cutlist_dict.append(c)
    return frozenset(cutlist_dict)

class SegmentWrapper(object):
    def __init__(self):
        curpath = os.path.normpath( os.path.join( os.getcwd(), os.path.dirname(__file__) )  )
        mixsegment.mix_segment_init(os.path.join(curpath,"dict","jieba.dict.utf8"), os.path.join(curpath,"dict","hmm_model.utf8"))
        self.stage1_regex = re.compile('(\d+)|([a-zA-Z]+)', re.I|re.U)
        self.sentence_dict = get_sentence_dict()

    def cut_to_sentence(self, line):
        if not isinstance(line, unicode):
            #try:
            line = line.decode('utf-8')
            #except UnicodeDecodeError:
            #    line = line.decode('gbk','ignore')

        for s,need_cut in self.do_stage1(line):
            if need_cut:
                if s != '':
                    str = ''
                    for c in s:
                        if c in self.sentence_dict:
                            if str != '':
                                yield (str, True)
                            str = ''
                            yield (c, False)
                        else:
                            str += c
                    if str != '':
                        yield (str, True)
            else:
                yield (s, False)

    #Support for regex 
    def do_stage1(self, sentence):
        start = 0
        for m in self.stage1_regex.finditer(sentence):
            yield (sentence[start:m.start(0)], True)
            yield (sentence[m.start(0):m.end(0)], False)
            start = m.end(0)
        yield (sentence[start:], True)
    
    def cut(self, sentence):
        for s, need_cut in self.cut_to_sentence(sentence):
            if s == '':
                continue
            elif need_cut:
                segs = mixsegment.StringVector()
                mixsegment.mix_segment_cut(s.encode('utf-8'), segs)
                for s in segs:
                    yield s.decode('utf-8')
            else:
                yield s
    
    # Auto delete it in c++
    #def __del__(self):
    #    mixsegment.mix_segment_dispose()

def require_inited(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        global SEG_INIT
        global segment_wrapper
        if SEG_INIT:
            return fn(*args, **kwargs)
        else:
            with SEG_LOCK:
                if SEG_INIT:
                    return fn(*args, **kwargs)
                SEG_INIT = True
                segment_wrapper = SegmentWrapper()
                return fn(*args, **kwargs)
    return wrapped

@require_inited
def cut(str):
    for s in segment_wrapper.cut(str):
        yield s

cut_list = frozenset(u".。！!?；？！。;")
def cut_sentence(txt):
    if not isinstance(txt, unicode):
        txt = txt.decode('utf-8')
    str = ''
    for c in txt:
        if c in cut_list:
            if str != '':
                yield str
            str = ''
        else:
            str += c
    if str != '':
        yield str
