#!/usr/bin/pythonw
# -*-coding:Utf-8 -*

import os
import sys
import path
import inout
import mechtools
import totools
import inigeom
import subprocess
import numpy as np

##########################################################################################
##################                      START PROGRAM                  ###################
##########################################################################################
print("********************************************************************")
print("******************         Start of TODemo           ***************")
print("********************************************************************")

# Initialize folders and exchange files
inout.iniWF()

# Test the links with external C libraries
inout.testLib()

# Create computational mesh and initial density function
inigeom.iniGeom(path.MESH,path.step(0,"phi.sol"))

# Regularization filter
totools.regulFilter(path.MESH,path.step(0,"phi.sol"),path.step(0,"phiR.sol"))

# Resolution of the linear elasticity system
mechtools.conductivity(path.MESH,path.step(0,"phiR.sol"),path.step(0,"u.sol"))

# Evaluation of the initial objective and constraint functions
newMT  = mechtools.MTGrad(path.MESH,path.step(0,"phiR.sol"),path.step(0,"u.sol"),path.step(0,"MT.grad.sol"))
newvol = mechtools.volumeGrad(path.MESH,path.step(0,"phiR.sol"),path.step(0,"vol.grad.sol"))

# Initial values for the parameters of the augmented Lagrangian
lmo = 0.01*(newvol-path.VTARG)/path.VTARG;
muo = 0.8*(newvol/path.VTARG)*abs(lmo);

# Main loop
coef = 0.1          # Maximum change in the values of the density within 1 iteration
for n in range(0,path.MAXIT) :

  print("Iteration {}".format(n))
  scurphi       = path.step(n,"phi.sol")
  snewphi       = path.step(n+1,"phi.sol")
  scurphiR      = path.step(n,"phiR.sol")
  snewphiR      = path.step(n+1,"phiR.sol")
  scuru         = path.step(n,"u.sol")
  snewu         = path.step(n+1,"u.sol")
  scurgrad      = path.step(n,"grad.sol")
  scurMTgrad    = path.step(n,"MT.grad.sol")
  snewMTgrad    = path.step(n+1,"MT.grad.sol")
  scurvolgrad   = path.step(n,"vol.grad.sol")
  snewvolgrad   = path.step(n+1,"vol.grad.sol")
  MT            = newMT
  vol           = newvol
  
  # Set parameters of the Augmented Lagrangian
  inout.setAtt(file=path.EXCHFILE,attname="lmAL",attval=lmo)
  inout.setAtt(file=path.EXCHFILE,attname="penAL",attval=muo)
    
  # Update Heaviside filter parameter
  if path.doHeavReg(n) :
    path.HEAVREG = path.HEAVREG + 2.0
    inout.setAtt(file=path.EXCHFILE,attname="HeavisideRegularization",attval=path.HEAVREG)
    mechtools.conductivity(path.MESH,scurphiR,scuru)
    MT  = mechtools.MTGrad(path.MESH,scurphiR,scuru,scurMTgrad)
    vol = mechtools.volumeGrad(path.MESH,scurphiR,scurvolgrad)

  # Calculation of the descent direction
  mechtools.descentAL(path.MESH,scurphi,scurMTgrad,scurvolgrad,scurgrad)
  
  # Evaluation of initial merit
  merit = mechtools.evalObjAL(MT,vol)
  
  # Line search procedure
  print("  Line search procedure")
  for k in range(0,path.MAXITLS) :
    print("  k = {}".format(k))
    
    # Update of the design
    print("    Update of density")
    totools.updens(path.MESH,scurgrad,scurphi,snewphi,coef)
    
    # Regularization filter
    totools.regulFilter(path.MESH,snewphi,snewphiR)
  
    # Resolution of the linear elasticity system
    print("    Resolution of the conductivity equation")
    mechtools.conductivity(path.MESH,snewphiR,snewu)

    # Evaluation of the new merit
    print("    Evaluation of the new design")
    newMT    = mechtools.MTGrad(path.MESH,snewphiR,snewu,snewMTgrad)
    newvol   = mechtools.volumeGrad(path.MESH,snewphiR,snewvolgrad)
    newmerit = mechtools.evalObjAL(newMT,newvol)

    # Decision
    # Iteration accepted
    if ( ( newmerit < merit + path.TOL*abs(merit) ) or ( k == 2 ) or ( coef < path.MINCOEF) ) :
      coef = min(path.MAXCOEF,1.1*coef)
      print("    Iteration {} - subiteration {} accepted: Mean Temperature {} - Volume {}\n".format(n,k,newMT,newvol))
      break
    # Iteration rejected
    else :
      print("    Iteration {} - subiteration {} rejected".format(n,k))
      coef = max(path.MINCOEF,0.6*coef)
      
  # Update of the coefficients of the Augmented Lagrangian
  lmo = lmo - muo*(newvol-path.VTARG);
  if  ( n != 0 ) and ( n%3 == 0 ) and ( n <= 70 ) :
    muo = muo*1.4


##########################################################################################
##################                      END PROGRAM                    ###################
##########################################################################################

print("********************************************************************")
print("******************          End of TODemo            ***************")
print("********************************************************************")
