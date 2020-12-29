import LB_globals as lbg
import numpy


def initializeRandom():
    lbg.n1 = lbg.n0 + lbg.Amp*(numpy.random.rand(lbg.XDIM)-0.5)


def initializeSteps():

    interface = 0.5 * lbg.XDIM
    transition = 0.0
    rhoA1 = lbg.n1_vapor     # theoreticalRhoVapor
    rhoA2 = lbg.n1_liquid    # theoreticalRhoLiquid

    for i in range(lbg.XDIM):
        if (i < interface-0.25*lbg.XDIM):
            transition = 0.5 + 0.5*numpy.tanh((i%lbg.XDIM)/lbg.interfaceWidth)
            lbg.n1[i] = (1.0-transition)*rhoA2 + transition*rhoA1
        elif (interface-0.25*lbg.XDIM <= i <= interface+0.25*lbg.XDIM):
            transition = 0.5 + 0.5*numpy.tanh((i-interface)/lbg.interfaceWidth)
            lbg.n1[i] = (1.0-transition)*rhoA1 + transition*rhoA2
        else:
            transition = 0.5 + 0.5*numpy.tanh(((i-lbg.XDIM)%lbg.XDIM)/lbg.interfaceWidth)
            lbg.n1[i] = (1.0-transition)*rhoA1 + transition*rhoA2
            

def initialize():
    u = 0

    lbg.iterations = 0
    lbg.rho1 = 0
    lbg.excludedVolume1 = 0

    lbg.pc = 3.*lbg.tc/8.    # This is needed to put the original critical parameter formulation on equal footing with the VDW constant formulation
    lbg.nc = lbg.pc / ((3./8.)*lbg.tc)

    # Reset the values of the VDW constants for each component
    lbg.a1 = (27./64.)*(lbg.tc*lbg.tc/lbg.pc)
    lbg.b1 = lbg.tc/(8.*lbg.pc)

    if (lbg.useDensityProfileStep):
        initializeSteps()
    else:
        initializeRandom()

    lbg.u1 = numpy.zeros(lbg.XDIM)
    lbg.uHat1 = numpy.zeros(lbg.XDIM)

    # Initialize 1st component
    lbg.f1_0 = lbg.n1 - lbg.n1*lbg.T0 - lbg.n1*u*u   # zero velocity
    lbg.f1_1 = (1./2) * (lbg.n1*u*u + lbg.n1*u + lbg.n1*lbg.T0)  # +1 velocity (moving right)
    lbg.f1_2 = (1./2) * (lbg.n1*u*u - lbg.n1*u + lbg.n1*lbg.T0)  # -1 velocity (moving left)

    lbg.mu1 = numpy.zeros(lbg.XDIM)
    lbg.muNonIdeal1 = numpy.zeros(lbg.XDIM)

    lbg.A = numpy.zeros(lbg.XDIM)

    lbg.pressure = numpy.zeros(lbg.XDIM)
    lbg.pressure1 = numpy.zeros(lbg.XDIM)
    lbg.pressureNonIdeal1 = numpy.zeros(lbg.XDIM)
    lbg.pressureCorrected1 = numpy.zeros(lbg.XDIM)
    lbg.p = numpy.zeros(lbg.XDIM)
    lbg.pni = numpy.zeros(lbg.XDIM)
    lbg.pf = numpy.zeros(lbg.XDIM)
    lbg.PF = numpy.zeros(lbg.XDIM)
    lbg.ddni = numpy.zeros(lbg.XDIM)
    
    # Set the total density and excluded volume constants for the VDW equations
    lbg.excludedVolume1 = numpy.sum(lbg.n1) * lbg.b1
# end function initialize()

# if __name__ == "__main__":
#     print(lbg.n1.shape)
#     initializeRandom()
#     print(lbg.n1)
    
