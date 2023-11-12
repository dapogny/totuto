#!/usr/bin/pythonw
# -*-coding:Utf-8 -*

import subprocess
import inout
import os
import path
import sys
import numpy as np

###################################################################################################################
#######                               Numerical solver for elasticity                                       #######
#######               inputs: mesh (string): mesh of the computational domain                               #######
#######                       phir (string): regularized density function                                   #######
#######                       u    (string): output elastic displacement                                    #######
###################################################################################################################

def elasticity(mesh,phir,u) :
  
  # Set information in exchange file
  inout.setAtt(file=path.EXCHFILE,attname="MeshName",attval=mesh)
  inout.setAtt(file=path.EXCHFILE,attname="PhiRName",attval=phir)
  inout.setAtt(file=path.EXCHFILE,attname="SolName",attval=u)
  
  # Call to FreeFem
  proc = subprocess.Popen(["{FreeFem} {elasticity} > /dev/null 2>&1".format(FreeFem=path.FREEFEM,elasticity=path.FFELAS)],shell=True)
  proc.wait()

###################################################################################################################
###################################################################################################################

###################################################################################################################
#######                        Evaluation of the elastic compliance and its gradient                        #######
#######           Inputs: mesh (string): mesh of the computational domain                                   #######
#######                   phir (string): regularized density function                                       #######
#######                   u    (string): elastic displacement                                               #######
#######                   g    (string): gradient of elastic compliance                                     #######
###################################################################################################################

def complianceGrad(mesh,phir,u,g) :
  
  # Set information in exchange file
  inout.setAtt(file=path.EXCHFILE,attname="MeshName",attval=mesh)
  inout.setAtt(file=path.EXCHFILE,attname="PhiRName",attval=phir)
  inout.setAtt(file=path.EXCHFILE,attname="SolName",attval=u)
  inout.setAtt(file=path.EXCHFILE,attname="CpGradName",attval=g)

  # Call to FreeFem
  proc = subprocess.Popen(["{FreeFem} {compliance} > /dev/null 2>&1".format(FreeFem=path.FREEFEM,compliance=path.FFCPLY)],shell=True)
  proc.wait()
  
  # Return compliance
  [cply] = inout.getrAtt(file=path.EXCHFILE,attname="Compliance")
  
  return cply

###################################################################################################################
###################################################################################################################

###################################################################################################################
#######                        Evaluation of the volume and its gradient                                    #######
#######       Inputs: mesh (string): mesh of the computational domain                                       #######
#######               phir (string): regularized density function                                           #######
#######               g    (string): gradient of volume                                                     #######
###################################################################################################################

def volumeGrad(mesh,phir,g) :
  
  # Set information in exchange file
  inout.setAtt(file=path.EXCHFILE,attname="MeshName",attval=mesh)
  inout.setAtt(file=path.EXCHFILE,attname="PhiRName",attval=phir)
  inout.setAtt(file=path.EXCHFILE,attname="VolGradName",attval=g)
    
  # Call to FreeFem
  proc = subprocess.Popen(["{FreeFem} {volume} > /dev/null 2>&1".format(FreeFem=path.FREEFEM,volume=path.FFVOL)],shell=True)
  proc.wait()
  
  # Return volume
  [vol] = inout.getrAtt(file=path.EXCHFILE,attname="Volume")
  
  return vol

###################################################################################################################
###################################################################################################################

###################################################################################################################
#####         Calculation of the (normalized) descent direction via the Null Space optimization algorithm     #####
#####             Inputs : mesh: (string) mesh ;                                                              #####
#####                      gCp:  (string) gradient of Compliance                                              #####
#####                      gV:   (string) gradient of Volume                                                  #####
#####                      g:    (string for) output total gradient                                           #####
###################################################################################################################

def descentNS(mesh,gCp,gV,g) :

  inout.setAtt(file=path.EXCHFILE,attname="MeshName",attval=mesh)
  inout.setAtt(file=path.EXCHFILE,attname="CpGradName",attval=gCp)
  inout.setAtt(file=path.EXCHFILE,attname="volGradName",attval=gV)
  inout.setAtt(file=path.EXCHFILE,attname="GradName",attval=g)
  
  # Velocity extension - regularization via FreeFem
  proc = subprocess.Popen(["{FreeFem} {ffdescent} > /dev/null 2>&1".format(FreeFem=path.FREEFEM,ffdescent=path.FFDESCENTNS)],shell=True)
  proc.wait()

###################################################################################################################
###################################################################################################################

###################################################################################################################
#####                Evaluation of the merit function in the Null Space optimization algorithm                #####
#####      Inputs :  Cp:    (real) compliance of shape                                                        #####
#####                vol:   (real) volume of shape                                                            #####
#####      Outputs : merit: (real) value of the merit of shape                                                #####
###################################################################################################################

def evalObjNS(Cp,vol) :

  # Read parameters in the exchange file
  [alphaJ] = inout.getrAtt(file=path.EXCHFILE,attname="alphaJ")
  [alphaG] = inout.getrAtt(file=path.EXCHFILE,attname="alphaG")
  [ell] = inout.getrAtt(file=path.EXCHFILE,attname="Lagrange")
  [m] = inout.getrAtt(file=path.EXCHFILE,attname="Penalty")
  [vtarg] = inout.getrAtt(file=path.EXCHFILE,attname="VolumeTarget")

  merit = alphaJ*(Cp - ell*(vol-vtarg)) + 0.5*alphaG/m*(vol-vtarg)**2

  return merit

###################################################################################################################
###################################################################################################################
