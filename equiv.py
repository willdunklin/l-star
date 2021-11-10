from dfa import DFA

def equivalence(A: DFA, B: DFA) -> str:
    # find the semantic difference of the languages
    # L(M)  = [x | x in (M.S)* if M.move_string(x) in M.F]
    # L(M') = [x | x in (M.S)* if M.move_string(x) not in M.F]
    # L(P)  = L(M) ∩ L(N) 
    #     P.Q = M.Q x N.Q
    #     P.delta = logical extension
    #     P.start = (M.start, N.start)
    #     P.F = [s in P.Q if s[0] in M.F AND s[1] in N.F]
    # 
    # L(C) = [L(A) ∩ L(B')] + [L(A') ∩ L(B)]

    alpha = A.S
    Q = {}
    delta = {}
    start = (A.start, B.start)

    for a in A.Q:
        for b in B.Q:
            state = (a,b)
            Q[state] = False
            for c in alpha:
                # transition to corresponding state pair
                delta[(state, c)] = (A.delta[(a, c)], B.delta[(b, c)])

    # L(A) ∩ L(B') case
    symm_diff =  [s for s in Q.keys() if (s[0] in A.F) and (s[1] not in B.F)]
    # L(A') ∩ L(B) case
    symm_diff += [s for s in Q.keys() if (s[0] not in A.F) and (s[1] in B.F)]

    # cx = list of counterexamples
    cx = explore(Q, alpha, delta, start, symm_diff)

    if len(cx) == 0:
        # there are no counterexamples
        return None

    # return the smallest counterexample
    return min(cx, key=len)

def explore(Q: dict, alpha: list, delta: dict, start: tuple, F: list) -> list:
    work = [(start, '')]
    vistited = []

    # bfs
    while len(work) != 0:
        # pop from front of queue
        state, string = work.pop(0)
        for c in alpha:
            dest = delta[(state, c)]
            
            # if this node has been vistited, mark as such
            if Q[dest]:
                continue
            
            # mark the state as visited 
            Q[dest] = True

            # add the next state to visit + its access string to work
            work.append((dest, string + c))
            vistited.append((dest, string + c))

    return [string for (state, string) in vistited if state in F]