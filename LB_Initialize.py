import LB_globals
import numpy


def initializeRandom():
    LB_globals.n1 = LB_globals.n0 + LB_globals.Amp*(numpy.random.rand(LB_globals.XDIM)-0.5)

def initializeSteps():

    interface = 0.5 * LB_globals.XDIM
    transition = 0.0
    rhoA1 = LB_globals.n1_vapor     # theoreticalRhoVapor
    rhoA2 = LB_globals.n1_liquid    # theoreticalRhoLiquid

    for i in range(LB_globals.XDIM):
        if (i < interface-0.25*LB_globals.XDIM):
            transition = 0.5 + 0.5*numpy.tanh((i%LB_globals.XDIM)/LB_globals.interfaceWidth)
            LB_globals.n1[i] = (1.0-transition)*rhoA2 + transition*rhoA1
        elif (interface-0.25*LB_globals.XDIM <= i <= interface+0.25*LB_globals.XDIM):
            transition = 0.5 + 0.5*numpy.tanh((i-interface)/LB_globals.interfaceWidth)
            LB_globals.n1[i] = (1.0-transition)*rhoA1 + transition*rhoA2
        else:   # TODO: drops straight from liquid to vapor density before end of lattice
            transition = 0.5 + 0.5*numpy.tanh(((i-LB_globals.XDIM)%LB_globals.XDIM)/LB_globals.interfaceWidth)
            LB_globals.n1[i] = (1.0-transition)*rhoA2 + transition*rhoA1

def initialize():
    u = 0

    LB_globals.iterations = 0
    LB_globals.rho1 = 0
    LB_globals.excludedVolume1 = 0

    LB_globals.pc = 3.*LB_globals.tc/8.    # This is needed to put the original critical parameter formulation on equal footing with the VDW constant formulation
    LB_globals.nc = LB_globals.pc / ((3./8.)*LB_globals.tc)

    # Reset the values of the VDW constants for each component
    LB_globals.a1 = (27./64.)*(LB_globals.tc*LB_globals.tc/LB_globals.pc)
    LB_globals.b1 = LB_globals.tc/(8.*LB_globals.pc)

#     if (initializeProfile == initializeSteps):
#         if (getTheoreticalDensities() and autoKappaGammaMu):
#             interfaceWidth = 1.0 / sqrt(4.0*theoreticalRhoVapor*fabs(tc-theta))
#             kappa = 1.0 / (8.0 * theta * theoreticalRhoVapor)
#             gammaMu = 1.0 / (6.0 * kappa * theoreticalRhoLiquid)
#             gammaMu /= 10.0
#             printf("kappa = %f\tgammaMu = %f\twidth = %f\n", kappa, gammaMu, interfaceWidth)


    if (LB_globals.useDensityProfileStep):
        initializeSteps()
        print("step")
    else:
        initializeRandom()
        print("random")

    LB_globals.u1 = numpy.zeros(LB_globals.XDIM)
    LB_globals.uHat1 = numpy.zeros(LB_globals.XDIM)

    # Initialize 1st component
    LB_globals.f1_0 = LB_globals.n1 - LB_globals.n1*LB_globals.T0 - LB_globals.n1*u*u   # zero velocity
    LB_globals.f1_1 = (1./2) * (LB_globals.n1*u*u + LB_globals.n1*u + LB_globals.n1*LB_globals.T0)  # +1 velocity (moving right)
    LB_globals.f1_2 = (1./2) * (LB_globals.n1*u*u - LB_globals.n1*u + LB_globals.n1*LB_globals.T0)  # -1 velocity (moving left)

    LB_globals.mu1 = numpy.zeros(LB_globals.XDIM)
    LB_globals.muNonIdeal1 = numpy.zeros(LB_globals.XDIM)

    LB_globals.A = numpy.zeros(LB_globals.XDIM)

    LB_globals.pressure = numpy.zeros(LB_globals.XDIM)
    LB_globals.pressure1 = numpy.zeros(LB_globals.XDIM)
    LB_globals.pressureNonIdeal1 = numpy.zeros(LB_globals.XDIM)
    LB_globals.pressureCorrected1 = numpy.zeros(LB_globals.XDIM)
    LB_globals.p = numpy.zeros(LB_globals.XDIM)
    LB_globals.pni = numpy.zeros(LB_globals.XDIM)
    LB_globals.pf = numpy.zeros(LB_globals.XDIM)
    LB_globals.PF = numpy.zeros(LB_globals.XDIM)
    LB_globals.ddni = numpy.zeros(LB_globals.XDIM)
    
    # Set the total density and excluded volume constants for the VDW equations
    LB_globals.excludedVolume1 = numpy.sum(LB_globals.n1) * LB_globals.b1
# end function initialize()

# if __name__ == "__main__":
#     print(LB_globals.n1.shape)
#     initializeRandom()
#     print(LB_globals.n1)
    
