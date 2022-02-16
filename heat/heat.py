from torch import tensor,nn,fft,diag,ones,float64
import torchsde
from math import pi

class Heat(nn.Module):

    def __init__(self,nu,alpha,N):

        super().__init__()

        # parameters
        # FIXME: I don't know if there's an advantage to these fancy torch Parameter classes
        # the documentation says that you can iterate over all parameters, somehow
        self.nu    = nn.Parameter(tensor(nu), requires_grad=False)      # viscosity / Reynolds
        self.alpha = nn.Parameter(tensor(alpha), requires_grad=False)       # noise intensity
        self.N     = nn.Parameter(tensor(N), requires_grad=False)               # number of modes
        self.dx    = 1./float(N)                                                # spacing
        if N%2!=0:
            raise ValueError('N must be even')
        self.nucte = nn.Parameter(tensor(4.*pi**2*nu), requires_grad=False) # noise intensity
        self.wavenumbers = 2*pi*fft.fftfreq(self.N, d=self.dx)                    # wavenumbers vector

        self.noise_type = 'additive'
        # TODO: which is better, additive or diagonal?
        self.sde_type = 'ito'

    # Drift
    # f = - 4 * pi^2 * nu * k^2 * y
    def f(self, t, y):
        return -self.nucte*self.wavenumbers*y  # shape (batch_size, state_size)

    # Diffusion
    # g = alpha * f
    def g(self, t, y):

        return diag(ones((self.N,), dtype=float64)*self.alpha)
