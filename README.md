cppjiebapy
==========

wrap cppjieba by swig. 若想使用python来调用cppjieba，或者像知道python调用c++的方法，可查阅此代码。

### 使用Python调用CppJieba方法

  * 安装swig

  * 下载cppjieba并编译安装。 https://github.com/aszxqw/cppjieba

  * 安装CppJiebaPy模块： python setup.py install

  * 调用方法： import cppjiebapy; cppjiebapy.cut

  * 测试：test/test_whoosh.py 

使用了正则对输入文本进行预处理，所以使用了宏-DNO_FILTER。若想预处理url链接等可以修改正则

__init__.py:
self.stage1_regex = re.compile('(\d+)|([a-zA-Z]+)', re.I|re.U) 为其它值。

借用swig实现Python对CppJieba的调用，没有使用Py++对整个库进行支持。

因为懒，所以目前只支持了MixSegment的模式，要支持其它模式也不难。

只支持精确分词模式

只在Linux下完成测试


#TODO

完整支持？

Support for windows？
