% Prolog Algorithm containing rules to match generated scansions to patterns we believe are found on the disk

% Theory for check index rule
% checkIndex(S, P, I, L) This rule finds the index I of the pattern P of L length
%   constructList(S, I, C, L) This rule recursively creates a list C of L length starting at I index
%   P = C

rightWay(S, I):- 
    P = ['l','u','u','d','l','l','d','l','x'],
    append([_, P, _], S),
    checkIndex(S, P, I, L),
    L = 9.
rightWay(S, I):- 
    P = ['l','l','d','l','l','d','l','x'],
    append([_, P, _], S),
    checkIndex(S, P, I, L),
    L = 8.


wrongWay(S, I):- 
    P = ['x','l','l','d','l','l','d','l','l','d'],
    append([_, P, _], S),
    checkIndex(S, P, I, L),
    L = 10.
wrongWay(S, I):- 
    P = ['l','l','d','l','l','d','l','l','d'],
    append([P, _], S),
    checkIndex(S, P, I, L),
    L = 9.

wrongWay(S, I):- 
    P = ['x','l','s','s','d','l','l','d','l','l','d'],
    append([_, P, _], S),
    checkIndex(S, P, I, L),
    L = 11.
wrongWay(S, I):- 
    P = ['l','s','s','d','l','l','d','l','l','d'],
    append([P, _], S),
    checkIndex(S, P, I, L),
    L = 10.

wrongWay(S, I):- 
    P = ['x','l','s','s','d','l','l','d','l','s','s','d'],
    append([_, P, _], S),
    checkIndex(S, P, I, L),
    L = 12.
wrongWay(S, I):- 
    P = ['l','s','s','d','l','l','d','l','s','s','d'],
    append([P, _], S),
    checkIndex(S, P, I, L),
    L = 11.

wrongWay(S, I):- 
    P = ['x','l','l','d','l','l','d','l','s','s','d'],
    append([_, P, _], S),
    checkIndex(S, P, I, L),
    L = 11.
wrongWay(S, I):- 
    P = ['l','l','d','l','l','d','l','s','s','d'],
    append([P, _], S),
    checkIndex(S, P, I, L),
    L = 10.