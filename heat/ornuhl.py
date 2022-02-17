from torch import tensor,nn,fft,full_like
import torchsde
from math import pi

class OrnUhl(nn.Module):

    def __init__(self,nu,alpha,N):

        super().__init__()

        # parameters
        # FIXME: I don't know if there's an advantage to these fancy torch Parameter classes
        # the documentation says that you can iterate over all parameters, somehow
        self.nu    = nn.Parameter(tensor(nu), requires_grad=False)              # viscosity / Reynolds
        self.alpha = nn.Parameter(tensor(alpha), requires_grad=False)           # noise intensity
        self.N     = nn.Parameter(tensor(N), requires_grad=False)               # number of modes
        self.dx    = 1./float(N)                                                # spacing
        if N%2!=0:
            raise ValueError('N must be even')
        self.wavenumbers = 2*pi*fft.fftfreq(self.N, d=self.dx)                  # wavenumbers vector

        self.noise_type = 'diagonal'
        # TODO: which is better, additive or diagonal?
        # TODO: I don't know how to create additive noise
        self.sde_type = 'ito'

    # Drift
    # f = - 4 * pi^2 * nu * k^2 * y
    def f(self, t, y):
        return -self.nu*y  # shape (batch_size, state_size)

    # Diffusion
    # g = alpha * dW/dt
    def g(self, t, y):

        # FIXME: additive noise below does not work
        #return diag(full((self.N,),self.alpha))
        return full_like(y,self.alpha)

    def squared(self, y):
        """
        Compute solution squared
        """
        return y*y

    def gradient_squared(self):

        return 1.

    def spectrum(self,t):

        return 1.