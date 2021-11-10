import re
remove_brackets = re.compile(r'\[(.*?)\]')

# DFA M = (set of states Q, alphabet SIGMA, transition function delta, start state s_0, accept states F)
class DFA:
    def __init__(self, Q: list, delta: dict, start: str, F: list, S: list=['0','1']) -> None:
        # initialize variables
        self.Q: list = Q # set of states
        self.S: list = S # alphabet
        self.delta: dict = delta # transition function
        self.start: str = start # start state
        self.F: list = F # accepting states
        # track the current state of the dfa
        self.current: str = self.start # current state

        # check that DFA is legal
        self.semantic_check()

    def invert(self):
        # result
        R = self
        # invert accepting/rejecting
        R.F = [s for s in self.Q if s not in self.F]
        return R

    # consume character and update current state via delta
    def move(self, char: str) -> bool:
        # skip empty char
        if char == '':
            return self.current in self.F

        # if the char is not in the alphabet, raise an exception
        if not char in self.S:
            raise Exception(f'DFA not defined for character {char}')

        self.current = self.delta[(self.current, char)]
        return self.current in self.F

    # repeat move for all chars in string
    def move_string(self, string: str) -> str:
        self.current = self.start
        for char in string:
            self.move(char)
        return self.current

    def semantic_check(self):
        # check for semantics
        for (s, c), d in self.delta.items():
            if s not in self.Q:
                raise Exception(pretty(f'rule {[s]}+{[c]} -> {[d]} invalid\n    {[s]} not in Q'))
            if c not in self.S:
                raise Exception(pretty(f'rule {[s]}+{[c]} -> {[d]} invalid\n    {[c]} not in S'))
            if d not in self.Q:
                raise Exception(pretty(f'rule {[s]}+{[c]} -> {[d]} invalid\n    {[d]} not in Q'))
        
        # not checking if delta has multiple outputs from one char
        # although isnt this solved with the fact delta is dict?

        for s in self.Q:
            for c in self.S:
                if (s, c) not in self.delta:
                    raise Exception(pretty(f'state {[s]} has no transition for symbol {[c]}'))

        if self.start not in self.Q:
            raise Exception(pretty(f'start state {[self.start]} not in Q'))

        for s in self.F:
            if s not in self.Q:
                raise Exception(pretty(f'accepting state {[s]} not in Q'))

    # diplay functions
    def display(self) -> None:
        print(pretty(f'{[self.current]}'))

    def print(self) -> None:
        # print('DFA')
        print(pretty(f'    curr:      {[self.current]}'))
        print(pretty(f'    states:    {self.Q}'))
        # print(pretty(f'    alphabet:  {self.S}'))
        print(f'    delta:     ')
        self.print_delta()
        print(pretty(f'    start:     {[self.start]}'))
        print(pretty(f'    accpeting: {self.F}'))

    def print_delta(self) -> None:
        for (s, c), d, in self.delta.items():
            print(pretty(f'       = {[s]}({c}) -> {[d]}'))



# def create_transition(transitions: list) -> dict:
#     try:
#         delta = {}
#         for start, dest, char in transitions:
#             delta[(start, char)] = dest
#         return delta
#     except:
#         raise Exception('pair list is malformatted')

def pretty(s: str) -> str:
    return ''.join(remove_brackets.split(s))