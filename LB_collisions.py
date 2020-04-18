from LB_globals import *



# def calculateMassAndVelocities():
#     # Sweep across the lattice to conserve mass and determine the pressures at each cell
#     for (i = 0 i < XDIM i++):
#         n1[i] = f1_0[i] + f1_1[i] + f1_2[i]         # 1st component mass density for this step
# 
#         if (n1[i] != 0):
#             u1[i] = (f1_1[i]-f1_2[i]) / n1[i]
# 
#             # Correction to the display of the mean fluid velocity
#             # Needed for the forcing methods (pressure method is good with the above)
#             uHat1[i] = u1[i] + 0.5/n1[i]*F1[i]
#         else:
#             u1[i] = 0
# 
# 
# def calculatePressures():
#     i
#     ip = 0
#     im = 0
#     omega = 1./oneOverTau
# 
#     # Functions to calculate pressures, partial and full
#     calculatePressurePartial()
#     calculatePressureTest()
# 
#     for (i = 0 i < XDIM i++):
#         pressureCCMinusVDW[i] = pressureCriticalConstants[i] - pressureVDWConstants[i]
# 
#     # For comparison, these loops calculate pressures in the same manner as Alexander's code
#     # Modified to include the gamma "modulation"
#     for (i = 0 i < XDIM i++):
#         ip=(i+1)%XDIM
#         im=(i+XDIM-1)%XDIM
# 
#         dni[i]=gradient(n1,i)
#         ddni[i]=laplace(n1,i)
# 
#         pni[i]=Pni(n1[i],dni[i],ddni[i])
#         p[i] = P(n1[i],dni[i],ddni[i])
# 
#         p[i] *= gammaP
#         pni[i] *= gammaP
# 
#     for (i = 0 i < XDIM i++):
#         ip=(i+1)%XDIM
#         im=(i+XDIM-1)%XDIM
# 
#         dpi[i]=gradient(pni,i)
#         ddpi[i]=laplace(p,i)
# 
#         Forces[i]=-dpi[i]
# 
#         pf[i]=p[i]-0.25*Forces[i]*Forces[i]/n1[i]-(1./omega-0.5)*Forces[i]*Forces[i]/n1[i]+0.25*ddpi[i]-1./12.*ddni[i]
#         PF[i]=p[i]+0.25*Forces[i]*Forces[i]/n1[i]+0.25*ddpi[i]-1./12.*ddni[i]
# 
# 
# def calculateChemicalPotentials():
#     if (useChemicalPotentialCriticalParameters):
#         for (i = 0 i < XDIM i++):
#             if (n1[i] != 0):
#                 mu1[i] = gammaMu * (-theta*log(1./n1[i]-1./(3*nc)) + theta/(1-(n1[i]/(3*nc))) - (9./4.)*tc*n1[i]/nc - kappa*laplace(n1,i))
#             else:
#                 mu1[i] = 0 # TODO: Is zeroing this out having an adverse effect?
# 
#             muCriticalConstants1[i] = mu1[i]
#     elif (!useChemicalPotentialCriticalParameters):
#         # These chemical potentials need density gradients, so calculate them separately
#         for (i = 0 i < XDIM i++):
#             tmp = 1.-b1*n1[i] #-b2*n2[i]
#             if (tmp < 0):
#                 lnExplosion = 1
#                 printf("LN EXPLOSION!!\t%f\n", tmp)
# 
#             mu1[i] = gammaMu * ( theta*log(n1[i]/(1.-b1*n1[i])) + theta*b1*n1[i]/(1.-b1*n1[i]) + theta - 2.*a1*n1[i] - kappa*laplace(n1,i) )
#             muVDWConstants1[i] = mu1[i]
# 
#     # These chemical potentials need density gradients, so calculate them separately
#     for (i = 0 i < XDIM i++):
#         muNonIdeal1[i] = mu1[i] - theta*log(n1[i])
#         muCCMinusVDW1[i] = muCriticalConstants1[i] - muVDWConstants1[i]


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
    print("collisionForcingNewChemicalPotentialGradient")
#     i = 0
#  
#     iterations++
#  
#     calculateMassAndVelocities()
#     calculatePressures()
#     calculateChemicalPotentials()
#  
#     for (i = 0 i < XDIM i++):
#         pressureGradMuMethod[i] = pressure[i]
#         muGradMuMethod[i] = mu1[i]
#  
#     # Forcing derived from chemical potential gradients... a la Gibbs-Duhem (sum of both equals pressure gradient)
#     if (useChemicalPotentialNonIdeal): # gradient of non-ideal mu
#         for (i = 0 i < XDIM i++):
#             F1[i] = -1.*n1[i]*gradient(muNonIdeal1,i) + n1[i]*g
#     else:
#         for (i = 0 i < XDIM i++): # gradient of FULL mu minus ideal pressure!
#             F1[i] = -1. * ( n1[i]*gradient(mu1,i)-theta*gradient(n1,i) ) + n1[i]*g
#  
#     for (i = 0 i < XDIM i++):
#         F1GradMuMethod[i] = F1[i]
#         F1GradPGradMuDifference[i] = F1GradPMethod[i] - F1GradMuMethod[i]
#      
#  
#     compareGradPRhoGradMu()
#  
#     for (i = 0 i < XDIM i++):
#         # Correction to the equilibrium distribution that alters the actual forcing
#         if (n1[i] !=0):
#             psi1[i] = -oneOverTau * ( (tau-(1./4.))*F1[i]*F1[i]/n1[i] + (1./12.)*laplace(n1,i) )    # subtract psi, so minus sign relative to paper
#         else:
#             psi1[i] = 0
#  
#         # Calculate particle densities at current lattice spot with forcing included
#         f1_0[i] += oneOverTau * ( (n1[i] - n1[i]*theta - n1[i]*u1[i]*u1[i]) - f1_0[i] ) - ( 2.*F1[i]*u1[i] - psi1[i] )
#         f1_1[i] += oneOverTau * ( (1./2.)*(n1[i]*u1[i]*u1[i]+n1[i]*u1[i]+n1[i]*theta)-f1_1[i]) - ( -F1[i]*u1[i] - (1./2.)*F1[i] + (1./2.)*psi1[i] )
#         f1_2[i] += oneOverTau * ( (1./2.)*(n1[i]*u1[i]*u1[i]-n1[i]*u1[i]+n1[i]*theta)-f1_2[i]) - ( -F1[i]*u1[i] + (1./2.)*F1[i] + (1./2.)*psi1[i] )
    

# TODO: dynamic kappa, gammaP/gammaMu values
# TODO: sync up changes from this single component code with the multi-component code
# TODO: look at relative stability among the 3 methods (pressure, gradP, gradMu)
# TODO: even/odd lattice problem comments for thesis
# def streaming():
# 
#     tmp
# 
#     # Original wrap-around end points 
# 
#     tmp=f1_1[XDIM-1]                                   # save right end point
#     memmove(&f1_1[1],&f1_1[0],(XDIM-1)*sizeof(double)) # shift all cells +1
#     f1_1[0]=tmp                                        # rotate former end to first lattice cell
#     tmp=f1_2[0]                                        # save left end point
#     memmove(&f1_2[0],&f1_2[1],(XDIM-1)*sizeof(double)) # shift all cells -1
#     f1_2[XDIM-1]=tmp                                   # rotate former first lattice cell to end
# 
#     # Walls at the end points 
#     # Bounce from lattice origin (0)
#     if (!useBoundaryConditionsPeriodic):
#         tmp = f1_1[0]
#         f1_1[0] = f1_2[XDIM-1]
#         f1_2[XDIM-1]=tmp
# 
#     # Switching cells to simulate wall between lattice spots [wall-1]|[wall] 
#     # TODO: this works for wall == 1 (correct) through wall == XDIM (bug)... should be restricted to wall == 1 through XDIM-1
#     if (wall > 0):
#         tmp = f1_1[wall]
#         f1_1[wall] = f1_2[(wall-1+XDIM)%XDIM]
#         f1_2[(wall-1+XDIM)%XDIM] = tmp


collision_dictionary = {
    "collisionForcingNewChemicalPotentialGradient" : collisionForcingNewChemicalPotentialGradient,
    "collisionForcingNewPressureGradient" : collisionForcingNewPressureGradient,
    "collisionPressureMethod" : collisionPressureMethod
}
collision_algorithm = collisionForcingNewChemicalPotentialGradient


def set_collision(collision):
    global collision_algorithm
    collision_algorithm = collision_dictionary[collision]


def iteration():
    # Need to reset the critical and VDW constants each iteration
    # Keeps them all in sync if one is changed during a simulation
    pc = 3*tc/8
    nc = pc / ((3/8)*tc)
    a1 = (27/64)*(tc*tc/pc)
    b1 = tc/(8*pc)
# 
    collision_algorithm()
#     streaming()
