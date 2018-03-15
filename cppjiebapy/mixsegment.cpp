/*
 * =====================================================================================
 *
 *       Filename:  mixsegment.cpp
 *
 *    Description:
 *
 *        Version:  1.0
 *        Created:  2013年11月07日 16时17分14秒
 *       Revision:  none
 *       Compiler:  gcc
 *
 *   Organization:
 *
 * g++ -c -fPIC  mixsegment.cpp -L/usr/lib/cppJieba/ -lcppjieba -o mixsegment.o
 * g++ -shared -Wl,-soname,libmixsegment.so -o libmixsegment.so mixsegment.o
 *
 * swig -python -c++  mixsegment.i
 * g++ -c -fPIC  mixsegment.cpp mixsegment_wrap.cxx  -I/usr/local/bin/python/include/python2.7/
 * g++ -shared mixsegment.o mixsegment_wrap.o -L/usr/lib/cppjieba/ -lcppjieba  -o _mixsegment.so
 * =====================================================================================
 */
#include <iostream>
#include <fstream>
#include <cstdlib>
#include <cstdio>
#include <assert.h>
#include "limonp/ArgvContext.hpp"
#include "MPSegment.hpp"
#include "HMMSegment.hpp"
#include "MixSegment.hpp"
#include "mixsegment.h"

using namespace cppjieba;

class MixSegmentWrap
{
public:
	MixSegmentWrap():mix_seg(NULL)
	{}
    bool init(const char* const _mpSegDict, const char* const _hmmSegDict)
	{
		/* Already init */
		if(NULL != this->mix_seg)
		{
			return false;
		}
		this->mix_seg = new MixSegment(_mpSegDict, _hmmSegDict);
        return true;
	}
	~MixSegmentWrap()
	{
		if(NULL != mix_seg)
		{
			delete mix_seg;
		}
	}
public:
	MixSegment* mix_seg;/* TODO do it better */
};

MixSegmentWrap GMIXSEG;

int mix_segment_init(char* jieba_dic, char* hmm_model);

bool mix_segment_cut(const std::string& str, StringVector& res);

void mix_segment_dispose();

int mix_segment_init(char* jieba_dic, char* hmm_model)
{
	MixSegmentWrap &wrap = GMIXSEG;

	if(!wrap.init(jieba_dic, hmm_model))
	{
		cout<<"seg init failed."<<endl;
		return EXIT_FAILURE;
	}

	return EXIT_SUCCESS;
}

bool mix_segment_cut(const std::string& str, vector<string>& res)
{
	MixSegment *pseg = GMIXSEG.mix_seg;
	assert(pseg != NULL);
	pseg->Cut(str, res);
    return true;
}

void mix_segment_dispose()
{
	//Auto dispose
	//MixSegment &seg = GMIXSEG;
	//seg.dispose();
}
