# uncompyle6 version 2.9.10
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.10 (default, Feb  6 2017, 23:53:20) 
# [GCC 4.2.1 Compatible Apple LLVM 8.0.0 (clang-800.0.34)]
# Embedded file name: fix_xreadlines.py
"""Fix "for x in f.xreadlines()" -> "for x in f".

This fixer will also convert g(f.xreadlines) into g(f.__iter__)."""
from .. import fixer_base
from ..fixer_util import Name

class FixXreadlines(fixer_base.BaseFix):
    BM_compatible = True
    PATTERN = "\n    power< call=any+ trailer< '.' 'xreadlines' > trailer< '(' ')' > >\n    |\n    power< any+ trailer< '.' no_call='xreadlines' > >\n    "

    def transform(self, node, results):
        no_call = results.get('no_call')
        if no_call:
            no_call.replace(Name(u'__iter__', prefix=no_call.prefix))
        else:
            node.replace([ x.clone() for x in results['call'] ])