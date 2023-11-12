#!/usr/bin/pythonw
# -*-coding:Utf-8 -*

import os
import sys

# Global parameters
REFDIR        = 1
REFNEU        = 2
MESHSIZ       = 0.02
EPS           = 1e-10 # Precision parameter
ALPHA         = 0.03 # Regularization parameter for velocity extension / regularization
MAXIT         = 200
MAXITLS       = 3   # Maximum number of iterations in the line search procedure
MAXCOEF       = 0.2
MINCOEF       = 0.005
TOL           = 0.005
VTARG         = 0.7
HEAVREG       = 3.0 # 3.0
SIMPP         = 3.0

# Parameters for the Null Space optimization algorithm
AJ            = 1.0
AG            = 0.02
ITMAXNORMXIJ  = 200

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
FFELAS         = SCRIPT + "elasticity.edp"
FFCPLY         = SCRIPT + "compliance.edp"
FFVOL          = SCRIPT + "volume.edp"
FFDESCENTNS    = SCRIPT + "descentNS.edp"
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
  return 0
