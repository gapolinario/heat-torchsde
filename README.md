**NOT WORKING**

Virtual environment:
`conda activate hsde`

Apparently this will not work.
As per the documentation, we can solve the following SDE:
dy(t) = f(t, y(t)) dt + g(t, y(t)) dW(t)

Notice, there is no mention of "solving an SPDE"
A letter P makes a huge difference when talking about differential equations
Except in computational complexity, where the N makes a huge difference

I'd need F(dW) for the code to work, or to apply the laplacian in real space,
but then it wouldn't be spectral anymore
