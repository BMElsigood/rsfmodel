import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
from math import exp,log
from collections import namedtuple

class RateState(object):
    def __init__(self):
        # Rate and state model parameters
        self.mu0 = 0
        self.a = 0
        self.b = 0
        self.dc = 0
        self.k = 0
        self.v = 0
        self.vlp = 0
        self.model_time = [] # List of times we want answers at
        # Results of running the model
        self._dispHist = []
        self.results = namedtuple("results",["time","displacement","velocity","friction","state1"])
        self.results.time = []
        self.results.displacement = []
        self.results.velocity = []
        self.results.friction = []
        self.results.state1 = []
        # Integrator settings
        self.abserr = 1.0e-12
        self.relerr = 1.0e-12

    def _integrationStep(self, w, t, p):
        """
        Do the calculation for a time-step
        """
        mu, theta, self.v = w
        mu0, vlp, a, b, dc, k = p
        self.v = self.v * exp((mu - mu0 - b * log(self.v * theta / dc)) / a)
        self._vHist.append(self.v)

        dmu_dt = k * (vlp - self.v)
        dtheta_dt = 1. - self.v * theta / dc

        return [dmu_dt,dtheta_dt]

    def solve(self):
        """
        Runs the integrator to actually solve the model and returns a
        named tuple of results.
        """
        # Parameters for the model
        p = [self.mu0,self.vlp,self.a,self.b,self.dc,self.k]

        # Initial conditions at t = 0
        # mu = reference friction value, theta = dc/v, velocity = v
        w0 = [self.mu0,self.dc/self.v,self.v]

        # Append initial value to velocity history
        self._vHist = [self.v]

        # Solve it
        wsol = integrate.odeint(self._integrationStep, w0, self.model_time, args=(p,),
                                atol=self.abserr, rtol=self.relerr)

        self.results.friction = wsol[:,0]
        self.results.state1 = wsol[:,1]
        self.results.velocity = np.array(self._vHist)

        return self.results
