from dfa import DFA
from typing import Tuple
from os import system, name
from equiv import equivalence

class oracle:
    def __init__(self, M: DFA) -> None:
        self.M = M
        self.clear = ''#'cls' if name == 'nt' else 'clear'
        system(self.clear)
    
    # membership query
    def mq(self, s: str) -> bool:
        return self.M.move_string(s) in self.M.F

        # print(pretty(f'what is membership of {[s]} in:'))
        # self.M.print()

        # # should respond with 0 or 1
        # res = int(input('0 non-accept, 1 accept:'))
        # system(self.clear)
        # return res

    # equivalence query
    def eq(self, M_hat: DFA) -> Tuple[int, str]:
        # test for functional equivalence by hand (oops)
        print('are these DFAs equivalent?')
        print('M_hat')
        M_hat.print()
        print()

        print('M')
        self.M.print()
        print()

        if int(input('0 no, 1 yes:')) == 1:
            system(self.clear)
            return 1, None
        else:
            x = input('provide counterexample string:')
            system(self.clear)
            return 0, x