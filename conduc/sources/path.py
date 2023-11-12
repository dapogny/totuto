#!/usr/bin/pythonw
# -*-coding:Utf-8 -*

import os
import sys

# Global parameters
REFDIR        = 1
MESHSIZ       = 0.01
EPS           = 1e-10 # Precision parameter
ALPHA         = 0.005 # Regularization parameter for velocity extension / regularization
MAXIT         = 200
MAXITLS       = 3   # Maximum number of iterations in the line search procedure
MAXCOEF       = 0.2
MINCOEF       = 0.005
TOL           = 0.005
VTARG         = 0.2
HEAVREG       = 3.0
SIMPP         = 3.0

# Paths to folders
RES     = "./res/"       # Directory for results
TESTDIR = RES + "test/"  # Directory for test of libraries
SCRIPT  = "./sources/"   # Directory for sources

# Call for the executables of external codes
FREEFEM = "FreeFem++ -nw"

# Path to FreeFem scripts
FFTEST         = SCRIPT + "testFF.edp"
FFINIMSH       = SCRIPT + "inimsh.edp"
FFINIDENS      = SCRIPT + "inidens.edp"
FFCONDUC       = SCRIPT + "conductivity.edp"
FFMT           = SCRIPT + "MT.edp"
FFVOL          = SCRIPT + "volume.edp"
FFDESCENTAL    = SCRIPT + "descentAL.edp"
FFUPDENS     = SCRIPT + "updens.edp"
FFREGFILTER  = SCRIPT + "regfilter.edp"

# Names of output and exchange files
TESTMESH = TESTDIR + "test.mesh"
TESTPHI  = TESTDIR + "test.phi.sol"
TESTSOL  = TESTDIR + "test.grad.sol"
EXCHFILE = RES + "exch.data"
LOGFILE  = RES + "log.data"
STEP     = RES + "step"
TMPSOL   = "./res/temp.sol"
MESH     = RES + "box.mesh"

# Shortcut for various file types
def step(n,typ) :
  return STEP + "." + str(n) + "." + typ
  
# Decision to increase Heaviside regularization
def doHeavReg(it) :
  if ( it >= 50 and it <= 200 and it % 20 == 0 ) :
    return 1
  else :
    return 0
