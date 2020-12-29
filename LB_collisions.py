import LB_globals as lbg
import numpy


def calculateMassAndVelocities():
    # Sweep across the lattice to conserve mass and determine the pressures at each cell
    lbg.n1 = lbg.f1_0 + lbg.f1_1 + lbg.f1_2
    lbg.u1 = (lbg.f1_1 - lbg.f1_2) / lbg.n1
    lbg.uHat1 = lbg.u1 + 0.5 / lbg.n1 * lbg.F1
    
    # Density gradients needed elsewhere
    lbg.gradN1[1:-1] = lbg.n1
    lbg.gradN1[0] = lbg.n1[-1]
    lbg.gradN1[-1] = lbg.n1[0]
    lbg.gradN1 = numpy.gradient(lbg.gradN1)
    lbg.laplaceN1 = numpy.gradient(lbg.gradN1)


def calculatePressures():
    # Single component pressure
    lbg.pressure = lbg.n1*lbg.theta/(1-lbg.b1*lbg.n1) - lbg.a1*lbg.n1*lbg.n1 - \
        lbg.kappa*lbg.n1*lbg.laplaceN1[1:-1] + 0.5*lbg.kappa*lbg.gradN1[1:-1]*lbg.gradN1[1:-1]
        
    lbg.pressureNonIdeal1 = lbg.gammaP * (lbg.pressure - lbg.n1*lbg.theta)  # non-ideal part of pressure (vdw - ideal) provides a force
    
    lbg.gradPressureNonIdeal1[1:-1] = lbg.pressureNonIdeal1
    lbg.gradPressureNonIdeal1[0] = lbg.pressureNonIdeal1[-1]
    lbg.gradPressureNonIdeal1[-1] = lbg.pressureNonIdeal1[0]
    lbg.gradPressureNonIdeal1 = numpy.gradient(lbg.gradPressureNonIdeal1)


def calculateChemicalPotentials():
    if 1-lbg.b1*lbg.n1.any() < 0: print("LN EXPLOSION!!")
    lbg.mu1 = lbg.gammaMu * ( lbg.theta*numpy.log(lbg.n1/(1-lbg.b1*lbg.n1)) + lbg.theta*lbg.b1*lbg.n1/(1-lbg.b1*lbg.n1) + \
                              lbg.theta - 2*lbg.a1*lbg.n1 - lbg.kappa*lbg.laplaceN1[1:-1] )
    lbg.muNonIdeal1= lbg.mu1 - lbg.theta*numpy.log(lbg.n1)
    
    # Chemical potential gradients needed elsewhere
    lbg.gradMu1[1:-1] = lbg.mu1
    lbg.gradMu1[0] = lbg.mu1[-1]
    lbg.gradMu1[-1] = lbg.mu1[0]
    lbg.gradMu1 = numpy.gradient(lbg.gradMu1) 
    
    lbg.gradMuNonIdeal1[1:-1] = lbg.muNonIdeal1
    lbg.gradMuNonIdeal1[0] = lbg.muNonIdeal1[-1]
    lbg.gradMuNonIdeal1[-1] = lbg.muNonIdeal1[0]
    lbg.gradMuNonIdeal1 = numpy.gradient(lbg.gradMuNonIdeal1) 


def collisionForcingNewPressureGradient():
    calculateMassAndVelocities()
    calculatePressures()
    calculateChemicalPotentials()
#  
    # Forcing derived from pressure gradients... a la Gibbs-Duhem (pressure gradient - partial pressure - equals chemical potential gradients)
    # PGF plus gravity term for each component
    lbg.F1 = -lbg.gradPressureNonIdeal1[1:-1] + lbg.n1*lbg.g
#      
    # Correction to the equilibrium distribution that alters the actual PGF to pressure is constant in equilibirum
    lbg.psi1 = -lbg.oneOverTau * ( (lbg.tau-0.25)*lbg.F1*lbg.F1/lbg.n1 + (1/12)*lbg.laplaceN1[1:-1] )    # subtract psi, so minus sign relative to paper
     
    # Calculate particle densities at current lattice spot with forcing included    
    lbg.f1_0 += lbg.oneOverTau * ( (lbg.n1 - lbg.n1*lbg.theta - lbg.n1*lbg.u1*lbg.u1) - lbg.f1_0 ) - \
                                 ( 2*lbg.F1*lbg.u1 - lbg.psi1 )
    lbg.f1_1 += lbg.oneOverTau * ( 0.5*(lbg.n1*lbg.u1*lbg.u1 + lbg.n1*lbg.u1 + lbg.n1*lbg.theta) - lbg.f1_1 ) - \
                                 ( -lbg.F1*lbg.u1 - 0.5*lbg.F1 + 0.5*lbg.psi1 )
    lbg.f1_2 += lbg.oneOverTau * ( 0.5*(lbg.n1*lbg.u1*lbg.u1 - lbg.n1*lbg.u1 + lbg.n1*lbg.theta) - lbg.f1_2 ) - \
                                 ( -lbg.F1*lbg.u1 + 0.5*lbg.F1 + 0.5*lbg.psi1 )


#
# This pressure method based on the Holdych-new method cited in Alexander's thermodynamic consistency paper (with the Corr laplace(n) term)
# TODO: Works, but not stable like original C implementation... had to init with step profile and drop gamma-P to 0.85
#
def collisionPressureMethod():
    calculateMassAndVelocities()
    calculatePressures()
    calculateChemicalPotentials()

    # Calculate the pressure method correction A
#     print(lbg.pressureNonIdeal1)
    lbg.A = lbg.pressureNonIdeal1 + (lbg.tau-0.5)*lbg.pressureMethodCoefficient*(lbg.n1*lbg.u1*lbg.gradN1[1:-1] / (lbg.n1 + lbg.pressureMethodCorrection*lbg.laplaceN1[1:-1]))
    
#     a=f1-f2
#     A = a*a/n + n/3 + p + (1/omega-0.5)*(dn*a/(n+Corr*ddn)) 

    # Calculate particle densities at current lattice spot with pressure method correction included
    lbg.f1_0 += lbg.oneOverTau * ( (lbg.n1 - lbg.n1*lbg.theta - lbg.n1*lbg.u1*lbg.u1 - lbg.A) - lbg.f1_0 )
    lbg.f1_1 += lbg.oneOverTau * ( 0.5*(lbg.n1*lbg.u1*lbg.u1 + lbg.n1*lbg.u1 + lbg.n1*lbg.theta + lbg.A) - lbg.f1_1 )
    lbg.f1_2 += lbg.oneOverTau * ( 0.5*(lbg.n1*lbg.u1*lbg.u1 - lbg.n1*lbg.u1 + lbg.n1*lbg.theta + lbg.A) - lbg.f1_2 )


def collisionForcingNewChemicalPotentialGradient():
    calculateMassAndVelocities()
    calculatePressures()
    calculateChemicalPotentials()
  
    # Forcing derived from chemical potential gradients... a la Gibbs-Duhem (sum of both equals pressure gradient)
    if (lbg.useChemicalPotentialNonIdeal): # gradient of non-ideal mu
        lbg.F1 = -1*lbg.n1*lbg.gradMuNonIdeal1[1:-1] + lbg.n1*lbg.g
    else:   # gradient of FULL mu minus ideal pressure!
        lbg.F1 = -1*( lbg.n1*lbg.gradMu1[1:-1]-lbg.theta*lbg.gradN1[1:-1] ) + lbg.n1*lbg.g
  
    # Correction to the equilibrium distribution that alters the actual forcing
    lbg.psi1 = -lbg.oneOverTau * ( (lbg.tau-0.25)*lbg.F1*lbg.F1/lbg.n1 + (1/12)*lbg.laplaceN1[1:-1] )    # subtract psi, so minus sign relative to paper
  
    # Calculate particle densities at current lattice spot with forcing included
    lbg.f1_0 += lbg.oneOverTau * ( (lbg.n1 - lbg.n1*lbg.theta - lbg.n1*lbg.u1*lbg.u1) - lbg.f1_0 ) - \
                                 ( 2*lbg.F1*lbg.u1 - lbg.psi1 )
    lbg.f1_1 += lbg.oneOverTau * ( 0.5*(lbg.n1*lbg.u1*lbg.u1 + lbg.n1*lbg.u1 + lbg.n1*lbg.theta) - lbg.f1_1 ) - \
                                 ( -lbg.F1*lbg.u1 - 0.5*lbg.F1 + 0.5*lbg.psi1 )
    lbg.f1_2 += lbg.oneOverTau * ( 0.5*(lbg.n1*lbg.u1*lbg.u1 - lbg.n1*lbg.u1 + lbg.n1*lbg.theta) - lbg.f1_2 ) - \
                                 ( -lbg.F1*lbg.u1 + 0.5*lbg.F1 + 0.5*lbg.psi1 )
    

collision_dictionary = {
    "collisionForcingNewChemicalPotentialGradient" : collisionForcingNewChemicalPotentialGradient,
    "collisionForcingNewPressureGradient" : collisionForcingNewPressureGradient,
    "collisionPressureMethod" : collisionPressureMethod
}
collision_algorithm = collisionForcingNewChemicalPotentialGradient


def set_collision(collision):
    global collision_algorithm
    collision_algorithm = collision_dictionary[collision]
    
    
def streaming():
    lbg.f1_1 = numpy.roll(lbg.f1_1,1)
    lbg.f1_2 = numpy.roll(lbg.f1_2,-1)


def iteration():
    # Need to reset the critical and VDW constants each iteration
    # Keeps them all in sync if one is changed during a simulation
    lbg.pc = 3 *lbg.tc / 8
    lbg.nc = lbg.pc / ((3/8)*lbg.tc)
    lbg.a1 = (27/64) * (lbg.tc*lbg.tc/lbg.pc)
    lbg.b1 = lbg.tc /(8*lbg.pc)
 
    collision_algorithm()
    streaming()
