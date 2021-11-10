from equiv import equivalence, explore
from dfa import DFA


M = DFA(
    Q=['a', 'b', 'c'],
    delta={
        ('a', '0'): 'a',
        ('a', '1'): 'b',

        ('b', '0'): 'c',
        ('b', '1'): 'a',

        ('c', '0'): 'b',
        ('c', '1'): 'c',
    },
    start='a',
    F=['b']
)

N = DFA(
    Q=['', '1', '10'],
    delta={
        ('', '0'): '',
        ('', '1'): '1',

        ('1', '0'): '10',
        ('1', '1'): '',

        ('10', '0'): '1',
        ('10', '1'): '10',
    },
    start='',
    F=['1']
)


M.print()
N.print()

res = equivalence(M, N)
if res == None:
    print('equivalent!')
else:
    print('not equivalent:', res)