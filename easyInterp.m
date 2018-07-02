function [combined] = easyInterp(before, after, ninterp)

maxval = max(ninterp,1);

x3 = after(maxval + 1);
x2 = after(maxval);
x1 = before(end - maxval);
x0 = before(end - 1 - maxval);


% x3 = after(maxval + 1);
% x2 = after(maxval);
% x1 = before(end - maxval);
% x0 = x1;
% x1 = 0;


a0 = x3 - x2 - x0 + x1;
a1 = x0 - x1 - a0;
a2 = x2 - x0;
a3 = x1;

t = 0:(1/ninterp):(1-(1/ninterp));
values = a0*(t.^3) + a1*(t.^2) + a2*t + a3;
combined = [before, before(end), after];

end

