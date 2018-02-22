#  -*- coding: UTF-8 -*-
#  File: __init__.py

if False:
    from .base import *
    from .common import *
    from .format import *
    from .image import *
    from .parallel_map import *
    from .parallel import *
    from .raw import *
    from .remote import *
    from . import imgaug
    from . import dataset
    from . import dftools


from pkgutil import iter_modules
import os
import os.path
from ..utils.develop import LazyLoader

__all__ = []


def _global_import(name):
    p = __import__(name, globals(), locals(), level=1)
    lst = p.__all__ if '__all__' in dir(p) else dir(p)
    if lst:
        del globals()[name]
        for k in lst:
            if not k.startswith('__'):
                globals()[k] = p.__dict__[k]
                __all__.append(k)


__SKIP = set(['dftools', 'dataset', 'imgaug'])
_CURR_DIR = os.path.dirname(__file__)
for _, module_name, __ in iter_modules(
        [os.path.dirname(__file__)]):
    srcpath = os.path.join(_CURR_DIR, module_name + '.py')
    if not os.path.isfile(srcpath):
        continue
    if not module_name.startswith('_') and \
            module_name not in __SKIP:
        _global_import(module_name)


globals()['dataset'] = LazyLoader('dataset', globals(), 'tensorpack.dataflow.dataset')
globals()['imgaug'] = LazyLoader('imgaug', globals(), 'tensorpack.dataflow.imgaug')

del LazyLoader

__all__.extend(['imgaug', 'dftools', 'dataset'])
