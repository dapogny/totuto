#!/usr/bin/pythonw
# -*-coding:Utf-8 -*

import subprocess
import inout
import os
import path
import sys
import numpy as np

#####################################################################################
#######   Regularization filter for the density function                      #######
#######       inputs: mesh (string): mesh of the computational domain         #######
#######               phi  (string): density function for design              #######
#######               nphi (string): filtered density function                #######
#####################################################################################

def regulFilter(mesh,phi,nphi) :
  
  # Set information in exchange file
  inout.setAtt(file=path.EXCHFILE,attname="MeshName",attval=mesh)
  inout.setAtt(file=path.EXCHFILE,attname="PhiName",attval=phi)
  inout.setAtt(file=path.EXCHFILE,attname="SolName",attval=nphi)
  
  # Call to FreeFem
  proc = subprocess.Popen(["{FreeFem} {elasticity} > /dev/null 2>&1".format(FreeFem=path.FREEFEM,elasticity=path.FFREGFILTER)],shell=True)
  proc.wait()

#####################################################################################
#####################################################################################

#####################################################################################
#######   Update of the density function                                      #######
#######       inputs: mesh (string): mesh of the computational domain         #######
#######               g (string): descent direction                           #######
#######               phi (string): density function for design               #######
#######               nphi (string): returned density function                #######
#######               dt (double): time step                                  #######
#####################################################################################

def updens(mesh,g,phi,nphi,dt) :
  
  # Set information in exchange file
  inout.setAtt(file=path.EXCHFILE,attname="MeshName",attval=mesh)
  inout.setAtt(file=path.EXCHFILE,attname="GradName",attval=g)
  inout.setAtt(file=path.EXCHFILE,attname="PhiName",attval=phi)
  inout.setAtt(file=path.EXCHFILE,attname="SolName",attval=nphi)
  inout.setAtt(file=path.EXCHFILE,attname="TimeStep",attval=dt)

  # Call to FreeFem
  proc = subprocess.Popen(["{FreeFem} {elasticity} > /dev/null 2>&1".format(FreeFem=path.FREEFEM,elasticity=path.FFUPDENS)],shell=True)
  proc.wait()

#####################################################################################
#####################################################################################
