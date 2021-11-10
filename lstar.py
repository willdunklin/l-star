from oracle import oracle
from tree import Tree
from dfa import DFA

# M_star = DFA()
alphabet = ['0', '1']

def lstar(o: oracle) -> DFA:
    b = o.mq('')

    M = DFA(
        Q=[''],
        delta={
            ('', '0'): '',
            ('', '1'): '',
        },
        start='',
        F=[] if b == 0 else ['']
    )

    done, x = o.eq(M)
    # if done, halt
    if done == 1:
        return M
    
    T = Tree('')

    # incorporate x into tree
    if not b:
        T.left = Tree('')
        T.right = Tree(x)
    else:
        T.left = Tree(x)
        T.right = Tree('')

    # loop infinite (bounded for now)
    for _ in range(10):
        M = make_dfa(T, o)
        
        done, x = o.eq(M)
        # if done, halt
        if done == 1:
            return M

        T = update_tree(x, T, M, o)


def make_dfa(T: Tree, o: oracle) -> DFA:
    Q = []
    delta = {}
    F = []

    leaves = T.get_leaves()
    for path, leaf in leaves:
        s = leaf.string 
        # append the string to list of states
        if not s in Q:
            Q.append(s)

        # if the leaf is a right child, add to accepting
        if o.mq(s) and not s in F:
            F.append(s)
        
        # add state to transition table
        for c in alphabet:
            # find destination through shift of s.c
            d = sift(s+c, T, o).string
            delta[(s, c)] = d # add rule
    
    return DFA(
        Q=Q,
        delta=delta,
        start='',
        F=F
    )
    

def sift(s: str, T: Tree, o: oracle) -> Tree:
    # start with curr at root node
    curr = T

    # traverse down to leaf
    while not curr.is_leaf():
        # get the distinguishing string d from the current intermediate node
        d = curr.string
        
        # if s.d is accepted, traverse right
        if o.mq(s + d):
            curr = curr.right
        # otherwise traverse left
        else:
            curr = curr.left

    # return the leaf node
    return curr


def update_tree(x: str, T: Tree, M: DFA, o: oracle) -> Tree:
    state = ''
    state_hat = ''
    j = 0
    
    for i in range(len(x) + 1):
        prefix = x[:i]
        state = sift(prefix, T, o).string
        state_hat = M.move_string(prefix)

        if state != state_hat:
            j = i
            break

    # want to find the leaf (and subsequent path to that leaf)
    path = T.find_leaf(M.move_string(x[:j-1]))

    # d is the differentiating string b/w state and state_hat in T
    d, _ = T.closest_ancestor(state, state_hat)

    # want to do surgery on the tree
    T_prime = T
    for dir in path:
        if dir == 0:
            T = T.left
        else:
            T = T.right
    
    prev = T.string

    # create new node
    T.string = x[j-1] + d
    # add the following as its 2 children 
    # the order is dependent on the side the node we just moved is
    if path[-1] == 0:
        T.left = Tree(prev)
        T.right = Tree(x[:j-1])
    else:
        T.left = Tree(x[:j-1])
        T.right = Tree(prev)
    
    # return the full tree (post-op)
    return T_prime


if __name__ == '__main__':
    o = oracle(
        DFA(
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
    )
    M = lstar(o)
    print()
    print('Completed DFA via Lstar:')
    M.print()
    # T = Tree('', left=Tree('0', left=Tree(''), right=Tree('10')), right=Tree('1'))
    # M = make_dfa(T, o)
    # M.print()
    # print()