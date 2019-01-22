% --------------- UTILITY METHODS ----------------- %
% --------------------------------------------------- %
% Checks if an element has already been added to list
% If yes, process next element
% Else, add to list

check_visited([], L, L).
check_visited([H|T], Vi, L) :-
	(member(H,Vi)
	->	check_visited(T, Vi, L)
	;	check_visited(T, [H|Vi], L)
	).

% --------------------------------------------------- %
% Calculate descendant roles of a role
% To avoid infinte recursive calls and cycles,
% maintain a visited list.

descendant_roles([],V,V).
descendant_roles([H|T],V,L) :-
	(member(H, V)
	->	descendant_roles(T,V,L)
	; 	(rh(H,_)
		->  setof(Z, rh(H,Z), L1),
			check_visited(L1, T, T2),
			descendant_roles(T2, [H|V], L)
		;	descendant_roles(T, [H|V], L)
		)
	).

% --------------------------------------------------- %
% Calculate the user roles from the fact -
% ur(X,Y)
% Add check to handle invalid cases

user_roles(X, L) :-
	users(Z),
	%to check if input is a valid user
	(X =< Z
	%to check if input user has roles
	-> 	(ur(X,_)
		->  setof(Y,ur(X,Y),L)
		; 	L = [],
			write('User '),write(X),write(' has no roles')
		)
	; 	L = [],
		write('Invalid user. Max users = '),write(Z)
	).

% --------------------------------------------------- %
% Calculate permissions of each of the roles
% Keep visited to remove duplicate entries
% Return list of permissions of all roles

calc_perms([],V,V).
calc_perms([H|T],V,L) :-
	(rp(H,_)
	->	setof(Z, rp(H,Z), L1),
		check_visited(L1, V, V1),
		calc_perms(T, V1, L)
	;	calc_perms(T, V, L)
	).

% --------------------------------------------------- %
% Returns a list of authorized_permissions each user has
% Keeps visited to check for duplicate entries of authorized_permissions
% Sorts the list of permissions before checking dor duplicates

all_perms([],V,V).
all_perms([H|T],V,L) :-
	authorized_permissions(H,La),
	sort(La,La1),
	check_visited([La1], V, Vn),
	all_perms(T, Vn, L).

% --------------------------------------------------- %
% Predicate to check if a fact of the form ur(X,Y) exists
all_users(X) :-
	ur(X, _).

% -----------------PREDICATE METHODS----------------- %
% --------------------------------------------------- %
% Authorized_roles is calculated by first computing user roles
% Then check descendant roles of each of the user roles
% Return sorted list of all roles.

authorized_roles(X, L) :- 
	user_roles(X, L1),
	%if user_roles is not empty, call descendant_roles of user_roles
	(L1 \= []
	->	descendant_roles(L1,[],Lu),
		sort(Lu,L)
	;	L = []
	).

% --------------------------------------------------- %
% Authorized_permissions is calculated by first calculating 
% authorized_roles of the user and identidying all the 
% permissions for each of the authorized_roles

authorized_permissions(X, L) :-
	authorized_roles(X, L1),
	(L1 \= []
	->	calc_perms(L1,[],Lu),
		sort(Lu,L)
	;	L = [],
		write('User '),write(X),write(' has no permissions')
	).

% --------------------------------------------------- %
% Calculates minRoles by maintaining a set of permissions of 
% each user and returning the count of the number of entries in the set

minRoles(S) :-
	setof(X, all_users(X), Lu),
	(Lu \= []
	->	all_perms(Lu,[],Lp),
		length(Lp,S)
	;	S = 0,
		write('Users have no permissions')
	).
% --------------------------------------------------- %