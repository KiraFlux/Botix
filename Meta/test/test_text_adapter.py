import sys

from engines.text import FormatTextIOAdapter
from engines.text import _MarkedListWritingMethod
from engines.text import _NumericListWritingMethod

f = FormatTextIOAdapter(sys.stdout)

f.write('Нумерованный список с отступом')

with f.use(_NumericListWritingMethod()):
    f.write('Элемент списка')

    with f.use(_MarkedListWritingMethod()):
        f.write('Элемент списка')
        f.write('Элемент списка')

    f.write('Элемент списка')
