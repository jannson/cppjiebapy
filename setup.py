import os,sys
#sys.argv.extend(['--compiler','g++'])
#os.envirom["CXX"] = 'g++-xx'

from distutils.core import setup, Extension
from distutils import ccompiler

sources = ['cppjiebapy/mixsegment.i','cppjiebapy/mixsegment.cpp']

#print ccompiler.show_compilers()

module_jieba = Extension('_mixsegment',
                sources,
                language='c++',
                swig_opts=['-c++'],
                #undef_macros = ['g','O2'],
                define_macros = [('NO_FILTER',None)],
                extra_compile_args=['--std=c++0x','-O3'],
                #extra_link_args=['-std=c++0x -O3'],
                include_dirs=['/usr/include/CppJieba'],
                #libraries=['cppjieba'],
                #library_dirs=['/usr/lib/CppJieba']
                )

setup(name='cppjiebapy',
        version='0.1.0',
        description='segment interrept with c++',
        author='yuzheng',
        author_email='gandancing@gmail.com',
        packages=['cppjiebapy'],
        package_data={'cppjiebapy':['*.py','*.i','*.cpp','*.cxx','dict/*']},
        ext_modules=[module_jieba],
        )
