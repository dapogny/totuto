#!/usr/bin/pythonw
# -*-coding:Utf-8 -*

import path
import subprocess
import os
import inout
import sys
import numpy as np

###################################################################################
#######         Create computational mesh and initial density Function      #######
#######         Inputs:  mesh = (string) path to mesh;                      #######
#######                  sol  = (string) path to ls function                #######
###################################################################################
def iniGeom(mesh,sol) :
  
  # Fill in exchange file
  inout.setAtt(file=path.EXCHFILE,attname="MeshName",attval=mesh)
  inout.setAtt(file=path.EXCHFILE,attname="PhiName",attval=sol)

  # Call to FreeFem for creating the background mesh
  log = open(path.LOGFILE,'a')
  proc = subprocess.Popen(["{FreeFem} {file} > /dev/null 2>&1".format(FreeFem=path.FREEFEM,file=path.FFINIMSH)],shell=True,stdout=log)
  proc.wait()
  log.close()

  # Call to FreeFem for creating the initial density function
  log = open(path.LOGFILE,'a')
  proc = subprocess.Popen(["{FreeFem} {file} > /dev/null 2>&1".format(FreeFem=path.FREEFEM,file=path.FFINIDENS)],shell=True,stdout=log)
  proc.wait()
  log.close()

###################################################################################
###################################################################################
