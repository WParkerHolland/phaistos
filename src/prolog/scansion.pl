% Prolog Algorithm containing rules to match generated scansions to patterns we believe are found on the disk

checkSpecIndex([H|_], 0, C) :- H = C.
checkSpecIndex([_|T], I, C) :- I1 is I - 1, checkSpecIndex(T, I1, C).

rightWay(S, I):-
    append([_, P, _], S),
    L = [['l','u','u','d','l','l','d','l','x'], ['l','l','d','l','l','d','l','x']],
    member(P, L),
    checkSpecIndex(L, I, P).

wrongWay(S, I):-
    append([P, _], S),
    L = [['l','l','d','l','l','d','l','l','d'], 
        ['l','s','s','d','l','l','d','l','l','d'], 
        ['l','s','s','d','l','l','d','l','s','s','d'],
        ['l','l','d','l','l','d','l','s','s','d']],
    member(P, L),
    checkSpecIndex(L, I, P).
wrongWay(S, I):-
    append([_, P, _], S),
    L = [['x','l','l','d','l','l','d','l','l','d'], 
        ['x','l','s','s','d','l','l','d','l','l','d'], 
        ['x','l','s','s','d','l','l','d','l','s','s','d'],
        ['x','l','l','d','l','l','d','l','s','s','d']],
    member(P, L),
    checkSpecIndex(L, I, P).