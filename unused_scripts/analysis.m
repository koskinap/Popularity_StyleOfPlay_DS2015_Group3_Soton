A = mergeddata(:,5:15);
f = mergeddata(:,16);

w = inv(A'*A)*A'*f;
