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
    lbg.pressure = lbg.n1*lbg.theta/(1-lbg.b1*lbg.n1) - lbg.a1*lbg.n1*lbg.n1 - \
        lbg.kappa*lbg.n1*lbg.laplaceN1[1:-1] + 0.5*lbg.kappa*lbg.gradN1[1:-1]*lbg.gradN1[1:-1]


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
    print("collisionForcingNewPressureGradient")
#     i = 0
# 
#     iterations++
# 
#     calculateMassAndVelocities()
#     calculatePressures()
#     calculateChemicalPotentials()
# 
#     # Forcing derived from pressure gradients... a la Gibbs-Duhem (pressure gradient - partial pressure - equals chemical potential gradients)
#     for (i = 0 i < XDIM i++):
#         # PGF plus gravity term for each component
#         F1[i] = -1.*gradient(pressureNonIdeal1,i) + n1[i]*g
# 
#     # Correction for the effective pressure that is exerted by including the gradient terms
#     # This correction does not change the PGF it only effects what is displayed in a variable separate from the actual pressure
#     for (i = 0 i < XDIM i++):
#         # TODO: the corrected pressure has a bug in the boundary conditions
#         if (n1[i] != 0):
#             correctionsPressureDisplay1[i] = -( tau-(1./4.) )*F1[i]*F1[i]/n1[i] + (1./4.)*( laplace(pressure1,i)-theta*laplace(n1,i) )
#         else:
#             correctionsPressureDisplay1[i] = 0
#         
#         pressureCorrected1[i] = pressure1[i] + correctionsPressureDisplay1[i]    # used to display the effective pressure, not to calculate forces
#         pressureGradPMethod[i] = pressure[i]
# 
#         muGradPMethod[i] = mu1[i]
#     
#     for (i = 0 i < XDIM i++):
#         F1GradPMethod[i] = F1[i]
#         F1GradPGradMuDifference[i] = F1GradPMethod[i] - F1GradMuMethod[i]
#     
#     for (i = 0 i < XDIM i++):
#         # Correction to the equilibrium distribution that alters the actual PGF to pressure is constant in equilibirum
#         if (n1[i] !=0):
#             psi1[i] = -oneOverTau * ( (tau-(1./4.))*F1[i]*F1[i]/n1[i] + (1./12.)*laplace(n1,i) )    # subtract psi, so minus sign relative to paper
#         else:
#             psi1[i] = 0
# 
#         # Calculate particle densities at current lattice spot with forcing included
#         f1_0[i] += oneOverTau * ( (n1[i] - n1[i]*theta - n1[i]*u1[i]*u1[i]) - f1_0[i] ) - ( 2.*F1[i]*u1[i] - psi1[i] )
#         f1_1[i] += oneOverTau * ( (1./2.)*(n1[i]*u1[i]*u1[i]+n1[i]*u1[i]+n1[i]*theta)-f1_1[i] ) - ( -F1[i]*u1[i] - (1./2.)*F1[i] + (1./2.)*psi1[i] )
#         f1_2[i] += oneOverTau * ( (1./2.)*(n1[i]*u1[i]*u1[i]-n1[i]*u1[i]+n1[i]*theta)-f1_2[i] ) - ( -F1[i]*u1[i] + (1./2.)*F1[i] + (1./2.)*psi1[i] )


#
# This pressure method based on the Holdych-new method cited in Alexander's thermodynamic consistency paper (with the Corr laplace(n) term)
#
def collisionPressureMethod():
    print("collisionPressureMethod")
#     i = 0
# 
#     iterations++
# 
#     calculateMassAndVelocities()
#     calculatePressures()
#     calculateChemicalPotentials()
# 
#     for (i = 0 i < XDIM i++):
#         pressurePressureMethod[i] = pressure[i]
#         muPressureMethod[i] = mu1[i]
# 
#         # Calculate the pressure method correction A
#         A[i] = pressureNonIdeal1[i] + (tau-0.5)*pressureMethodCoefficient*(n1[i]*u1[i]*gradient(n1,i) / (n1[i] + pressureMethodCorrection*laplace(n1,i)))
# 
#         # Calculate particle densities at current lattice spot with pressure method correction included
#         f1_0[i] += oneOverTau * ( (n1[i] - n1[i]*theta - n1[i]*u1[i]*u1[i] - A[i]) - f1_0[i] )
#         f1_1[i] += oneOverTau * ( (1./2.)*(n1[i]*u1[i]*u1[i] + n1[i]*u1[i] + n1[i]*theta + A[i]) - f1_1[i] )
#         f1_2[i] += oneOverTau * ( (1./2.)*(n1[i]*u1[i]*u1[i] - n1[i]*u1[i] + n1[i]*theta + A[i]) - f1_2[i] )


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
#         if (n1[i] !=0):
    lbg.psi1 = -lbg.oneOverTau * ( (lbg.tau-0.25)*lbg.F1*lbg.F1/lbg.n1 + (1/12)*lbg.laplaceN1[1:-1] )    # subtract psi, so minus sign relative to paper
#         else:
#             psi1[i] = 0
  
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
