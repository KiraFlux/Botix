import sys

from engines.text import FormatTextIOAdapter
from engines.text import MarkedListWritingMethod
from engines.text import NumericListWritingMethod

f = FormatTextIOAdapter(sys.stdout)

f.write('Нумерованный список с отступом')

with f.use(NumericListWritingMethod()):
    f.write('Элемент списка')

    with f.use(MarkedListWritingMethod()):
        f.write('Элемент списка')
        f.write('Элемент списка')

    f.write('Элемент списка')
