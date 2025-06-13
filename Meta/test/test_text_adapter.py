import sys

from engines.text import FormatTextIOAdapter
from engines.text import IntendWritingMethod
from engines.text import MarkedListWritingMethod

f = FormatTextIOAdapter(sys.stdout)

f.write('1')

with f.use(IntendWritingMethod()):
    f.write('2')

    with f.use(MarkedListWritingMethod()):
        f.write('3')
        f.write('4')

    f.write('5')

f.write('6')
