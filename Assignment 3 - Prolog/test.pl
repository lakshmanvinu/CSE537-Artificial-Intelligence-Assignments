% Input Format

users(5).
roles(4).
perms(3).

ur(1,1).
ur(2,1).
ur(3,2).
ur(4,3).
ur(5,4).

rh(1,2).
rh(2,1).
rh(2,3).

rp(1,1).
rp(2,2).
rp(3,3).
rp(4,1).
rp(4,2).
rp(4,3).

% Output Format

% authorized_roles(1,R).
% authorized_roles(2,R).
% authorized_roles(3,R).
% authorized_roles(4,R).
% authorized_roles(5,R).

% authorized_permissions(1,P).
% authorized_permissions(2,P).
% authorized_permissions(3,P).
% authorized_permissions(4,P).
% authorized_permissions(5,P).

% minRoles(S).