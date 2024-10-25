% Prolog Algorithm containing rules to match generated scansions to patterns we believe are found on the disk

% This has been removed from other functions because I cannot figure out how to make it work
% Calling this function with I equal to a variable will cause an error
checkSpecIndex([H|_], 0, C) :- H = C.
checkSpecIndex([_|T], I, C) :- I1 is I - 1, checkSpecIndex(T, I1, C).

rightWay(S, I):-
    L = [['l','u','u','d','l','l','d','l','x'], 
        ['l','l','d','l','l','d','l','x']],
    I = 0; I = 1,
    append([_, P, _], S),
    member(P, L),
    checkSpecIndex(L, I, P).

wrongWay(S, I):-
    L = [['l','l','d','l','l','d','l','l','d'], 
        ['l','s','s','d','l','l','d','l','l','d'], 
        ['l','s','s','d','l','l','d','l','s','s','d'],
        ['l','l','d','l','l','d','l','s','s','d']],
    I = 0; I = 1; I = 2; I = 3,
    append([_, P, _], S),
    member(P, L),
    checkSpecIndex(L, I, P).
wrongWay(S, I):-
    L = [['x','l','l','d','l','l','d','l','l','d'], 
        ['x','l','s','s','d','l','l','d','l','l','d'], 
        ['x','l','s','s','d','l','l','d','l','s','s','d'],
        ['x','l','l','d','l','l','d','l','s','s','d']],
    I = 0; I = 1; I = 2; I = 3,
    append([_, P, _], S),
    member(P, L),
    checkSpecIndex(L, I, P).