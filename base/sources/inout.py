#!/usr/bin/pythonw
# -*-coding:Utf-8 -*

import path
import subprocess
import os
import sys
import numpy

###########################################################################################
############              Set the field attname in file                        ############
############      Inputs: file    (str) path of exchange file                  ############
############              attname (str) field of exchange file to fill         ############
############              attval  (str) object to print                        ############
###########################################################################################

def setAtt(file="none",attname="none",attval="none"):
  """ Set the value attval in the field attname of file """
  
  # Open file
  ff = open(file,"r")
  content = ff.read()
  contentl = content.lower()
  lst = content.split()
  lstl = contentl.split()
  ff.close()
  
  isfnd = 0
  # Travel file
  for i,elt in enumerate(lstl) :
    if elt == attname.lower() :
      isfnd = 1
      ind = i+1
      lst[ind] = str(attval)
      break

  # If attname has been found, rewrite file out of the updated list
  if isfnd :
    with open(file,"w") as ff :
      for i,elt in enumerate(lst) :
        ff.write(elt+"\n")
        if ( i % 2 == 1 ) :
            ff.write("\n")

  # If attname has not been found, append at the end of the file
  else :
    with open(file,"a") as ff :
      ff.write(attname+"\n"+str(attval)+"\n\n")

###########################################################################################
###########################################################################################

###########################################################################################
############             Get real value associated to kwd                       ###########
############      Inputs: file    (str) path of exchange file                   ###########
############              attname (str) field of exchange file to consult       ###########
############              npar    (int) number of real parameters to obtain     ###########
###########################################################################################

def getrAtt(file="none",attname="none",npar=1) :
  """ Get real value associated to keyword kwd in file """
  
  # Open file
  ff = open(file,"r")
  content = ff.read()
  content = content.lower()
  lst = content.split()
  ff.close()
  
  # Travel file
  rval = []
  for i,elt in enumerate(lst) :
    if elt == attname.lower() :
      for j in range(1,npar+1) :
        rval.append(float(lst[i+j]))

  return ( rval )

###########################################################################################
###########################################################################################

###########################################################################################
############                      Initialize folders and files                  ###########
###########################################################################################

def iniWF():

  # Create and clear ./res folder for results depending on the situation
  proc = subprocess.Popen(["mkdir -p {folder}".format(folder=path.RES)],shell=True)
  proc.wait()
  proc = subprocess.Popen(["rm -rf {folder}*".format(folder=path.RES)],shell=True)
  proc.wait()
  
  # Create and clear ./testdir folder for results depending on the situation
  proc = subprocess.Popen(["mkdir -p {folder}".format(folder=path.TESTDIR)],shell=True)
  proc.wait()
  proc = subprocess.Popen(["rm -rf {folder}*".format(folder=path.TESTDIR)],shell=True)
  proc.wait()

  # For vizualization
  proc = subprocess.Popen(["cp {ini} {dup}".format(ini="DEFAULT.medit",dup=path.RES+"DEFAULT.medit")],shell=True)
  proc.wait()

  # Create exchange file
  ff = open(path.EXCHFILE,'w')
  ff.close()
  
  # Create log file
  ff = open(path.LOGFILE,'w')
  ff.close()
  
  # Add global information (e.g. about Dirichlet and Neumann boundaries)
  setAtt(file=path.EXCHFILE,attname="Dirichlet",attval=path.REFDIR)
  setAtt(file=path.EXCHFILE,attname="Neumann",attval=path.REFNEU)
  setAtt(file=path.EXCHFILE,attname="Regularization",attval=path.ALPHA)
  setAtt(file=path.EXCHFILE,attname="CoefficientObjective",attval=path.AJ)
  setAtt(file=path.EXCHFILE,attname="CoefficientConstraint",attval=path.AG)
  setAtt(file=path.EXCHFILE,attname="MaxNormXiJ",attval=0.0)
  setAtt(file=path.EXCHFILE,attname="MeshSize",attval=path.MESHSIZ)
  setAtt(file=path.EXCHFILE,attname="VolumeTarget",attval=path.VTARG)
  setAtt(file=path.EXCHFILE,attname="HeavisideRegularization",attval=path.HEAVREG)
  setAtt(file=path.EXCHFILE,attname="SimpPen",attval=path.SIMPP)

###########################################################################################
###########################################################################################

###########################################################################################
#############        Test calls to external C libraries and softwares           ###########
###########################################################################################

def testLib():

  log = open(path.LOGFILE,'a')

  # Test call to FreeFem
  setAtt(file=path.EXCHFILE,attname="MeshName",attval=path.TESTMESH)
  setAtt(file=path.EXCHFILE,attname="PhiName",attval=path.TESTPHI)
  setAtt(file=path.EXCHFILE,attname="SolName",attval=path.TESTSOL)
  
  proc = subprocess.Popen(["{FreeFem} {test} > /dev/null 2>&1".format(FreeFem=path.FREEFEM,test=path.FFTEST)],shell=True)
  proc.wait()
  
  if ( proc.returncode == 0 ) :
    print("FreeFem installation working.")
  else :
    print("Problem with FreeFem installation.")
    exit()

  # Test command line gsed
  proc = subprocess.Popen(["gsed 's/MeshVersionFormatted/MeshVersion/g' {SolName} > /dev/null 2>&1".format(SolName=path.TESTSOL)],shell=True)
  proc.wait()
  proc = subprocess.Popen(["gsed 's/MeshVersion/MeshVersionFormatted/g' {SolName} > /dev/null 2>&1".format(SolName=path.TESTSOL)],shell=True)
  proc.wait()
  
  if ( proc.returncode == 0 ) :
    print("gsed command line working.")
  else :
    print("Problem with gsed command line.")
    exit()
  
  print("All external libraries working.")
  log.close()
  
###########################################################################################
###########################################################################################
