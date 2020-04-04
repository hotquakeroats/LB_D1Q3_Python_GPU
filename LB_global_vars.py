import numpy


XDIM = 201  # lattice length

#
# Arrays for physical properties along the lattice
#

# Equilibrium distribution of each component velocities
f1_0 = numpy.zeros(XDIM)   # the static vector
f1_1 = numpy.zeros(XDIM)   # +1 lattice space
f1_2 = numpy.zeros(XDIM)   # -1 lattice space

psi1 = numpy.zeros(XDIM) 

# Number densities of each component
n1 = numpy.zeros(XDIM)   # 1st component mass/density

# *freeEnergyArray = 

# Component and bulk velocities
u1 =  numpy.zeros(XDIM)
uHat1 =  numpy.zeros(XDIM)

# Component thermodynamic properties
mu1 = numpy.zeros(XDIM)    # chemical potential
muNonIdeal1 = numpy.zeros(XDIM)
muCriticalConstants1 = numpy.zeros(XDIM)
muVDWConstants1 = numpy.zeros(XDIM)
muCCMinusVDW1 = numpy.zeros(XDIM)
muGradPMethod = numpy.zeros(XDIM)
muGradMuMethod = numpy.zeros(XDIM)
muPressureMethod = numpy.zeros(XDIM)

pressure = numpy.zeros(XDIM)
pressure1 = numpy.zeros(XDIM)
pressureNonIdeal1 = numpy.zeros(XDIM)
pressureCorrected1 = numpy.zeros(XDIM)
pressureGradPMethod = numpy.zeros(XDIM)
pressureGradMuMethod = numpy.zeros(XDIM)
pressurePressureMethod = numpy.zeros(XDIM)
pressureCriticalConstants = numpy.zeros(XDIM)
pressureVDWConstants = numpy.zeros(XDIM)
pressureCCMinusVDW = numpy.zeros(XDIM)
correctionsPressure1 = numpy.zeros(XDIM)
correctionsPressureDisplay1 = numpy.zeros(XDIM)
pressureTest = numpy.zeros(XDIM)
pressureTestZero = numpy.zeros(XDIM)
pressureTest1 = numpy.zeros(XDIM)
pressureTest2 = numpy.zeros(XDIM)
pressureTest3 = numpy.zeros(XDIM)
pressureTest4 = numpy.zeros(XDIM)
pressureTest5 = numpy.zeros(XDIM)
pressureTest6 = numpy.zeros(XDIM)

dni = numpy.zeros(XDIM)
ddni = numpy.zeros(XDIM)
dpi = numpy.zeros(XDIM)
ddpi = numpy.zeros(XDIM)
p = numpy.zeros(XDIM)
pni = numpy.zeros(XDIM)
pf = numpy.zeros(XDIM)
#pff = numpy.zeros(XDIM)
PF = numpy.zeros(XDIM)

# Friction forces for each component velocity
F1_0 = numpy.zeros(XDIM)
F1_1 = numpy.zeros(XDIM)
F1_2 = numpy.zeros(XDIM)

# Forces on each component =  potential and friction
F1 = numpy.zeros(XDIM)
F1GradPMethod = numpy.zeros(XDIM)
F1GradMuMethod = numpy.zeros(XDIM)
F1GradPGradMuDifference = numpy.zeros(XDIM)
Forces = numpy.zeros(XDIM)

A = numpy.zeros(XDIM)  # pressure method change to the density distributions

gradP = numpy.zeros(XDIM)
rhoGradMu = numpy.zeros(XDIM)
gradPMinusRhoGradMu = numpy.zeros(XDIM)

# Graph/GUI variables
u1g = numpy.zeros(XDIM)
#pg1 = numpy.zeros(XDIM)
tg = numpy.zeros(XDIM)
#mu1g = numpy.zeros(XDIM)


#
# Externs
#

# Initial densities of each component
n1_liquid = 1.27
n1_vapor = 0.6

# Total amount of each component
rho1 = 0.0
excludedVolume1 = 0.0 

theoreticalRhoVapor = 0.0
theoreticalRhoLiquid = 0.0
interfaceWidth = 2.0

# freeEnergyArraySize = 0

# Evaporation constants
dn = 0.0 # delta n for evaporation
epos = 0  # lattice position at which evaporation occurs

# Equations of motion constants
T0 = 0.33333333     # initial theta from write-up
theta = 1/3
n0 = 1.0
Amp = 0.01
tau = 1.0
oneOverTau = 1.0    # 1/tau from write-up (relaxation constant)
g = 0               # gravitational acceleration term
lmbda = 1.0        # friction (F12) coefficient
gammaP = 1.0        # pressure coefficient to control the rate of forcing per time step
gammaMu = 1.0       # chemical potential coefficient to control the rate of forcing per time step
kappa = 0.1         # coefficient of gradient corrections
a1 = 0.1
b1 = 1/3
dummy = 1
quenchDepth = 0.6   # depth of tc/theta ratio for calculating phase diagrams
pressureMethodCorrection = 0        # coefficient of laplace correction in the pressure method
pressureMethodCoefficient = 7/3     # coefficient of the Holdych correction in the pressure method 
                                    # u*gradRho + u*gradRho(transpose) + theta*u*gradRho (2 1/3)

# Critical point traits
tc = 0.34
nc = 1.0
pc = 1.0

usePressureCoupled = False
usePressureCriticalParameters = False    # chooses between tc,pc,nc and a,b VDW constants; default use VDW constants
useChemicalPotentialCriticalParameters = False  # default use VDW constants
useChemicalPotentialsCoupled = False  # chooses between independent or coupled mu's
useChemicalPotentialNonIdeal = False    # default use full mu (not non-ideal part)
lnExplosion = False
useBoundaryConditionsPeriodic = True    # default periodic BCs
autoKappaGammaMu = True

# GUI
ulreq = 0
ugreq = 0
pgreq = 0
tgreq = 0
mu1greq = 0 # graph requests
next_step = 0
Pause = 1
done = False
step_size = 10
iterations = 0
collectData = 0
wall = XDIM * 0.5
phase_iterations = 0