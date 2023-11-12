#!/usr/bin/pythonw
# -*-coding:Utf-8 -*

import subprocess
import inout
import os
import path
import sys
import numpy as np

###################################################################################################################
#######                               Numerical solver for conductivity                                     #######
#######               inputs: mesh (string): mesh of the computational domain                               #######
#######                       phir (string): regularized density function                                   #######
#######                       u    (string): output elastic displacement                                    #######
###################################################################################################################

def conductivity(mesh,phir,u) :
  
  # Set information in exchange file
  inout.setAtt(file=path.EXCHFILE,attname="MeshName",attval=mesh)
  inout.setAtt(file=path.EXCHFILE,attname="PhiRName",attval=phir)
  inout.setAtt(file=path.EXCHFILE,attname="SolName",attval=u)
  
  # Call to FreeFem
  proc = subprocess.Popen(["{FreeFem} {elasticity} > /dev/null 2>&1".format(FreeFem=path.FREEFEM,elasticity=path.FFCONDUC)],shell=True)
  proc.wait()

###################################################################################################################
###################################################################################################################

###################################################################################################################
#######                        Evaluation of the mean temperature and its gradient                          #######
#######           Inputs: mesh (string): mesh of the computational domain                                   #######
#######                   phir (string): regularized density function                                       #######
#######                   u    (string): temperature                                                        #######
#######                   g    (string): gradient of elastic compliance                                     #######
###################################################################################################################

def MTGrad(mesh,phir,u,g) :
  
  # Set information in exchange file
  inout.setAtt(file=path.EXCHFILE,attname="MeshName",attval=mesh)
  inout.setAtt(file=path.EXCHFILE,attname="PhiRName",attval=phir)
  inout.setAtt(file=path.EXCHFILE,attname="SolName",attval=u)
  inout.setAtt(file=path.EXCHFILE,attname="MTGradName",attval=g)

  # Call to FreeFem
  proc = subprocess.Popen(["{FreeFem} {MT} > /dev/null 2>&1".format(FreeFem=path.FREEFEM,MT=path.FFMT)],shell=True)
  proc.wait()
  
  # Return compliance
  [MT] = inout.getrAtt(file=path.EXCHFILE,attname="MT")
  
  return MT

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
#####         Calculation of the (normalized) descent direction via the Augmented Lagrangian algorithm        #####
#####             Inputs : mesh: (string) mesh                                                                #####
#####                      phi   (string): regularized density function                                       #####
#####                      gMT:  (string) gradient of mean temperature                                        #####
#####                      gV:   (string) gradient of Volume                                                  #####
#####                      g:    (string for) output total gradient                                           #####
###################################################################################################################

def descentAL(mesh,phi,gMT,gV,g) :

  inout.setAtt(file=path.EXCHFILE,attname="MeshName",attval=mesh)
  inout.setAtt(file=path.EXCHFILE,attname="MTGradName",attval=gMT)
  inout.setAtt(file=path.EXCHFILE,attname="volGradName",attval=gV)
  inout.setAtt(file=path.EXCHFILE,attname="GradName",attval=g)
  
  # Velocity extension - regularization via FreeFem
  proc = subprocess.Popen(["{FreeFem} {ffdescent} > /dev/null 2>&1".format(FreeFem=path.FREEFEM,ffdescent=path.FFDESCENTAL)],shell=True)
  proc.wait()

###################################################################################################################
###################################################################################################################

###################################################################################################################
#####                Evaluation of the merit function in the Null Space optimization algorithm                #####
#####      Inputs :  MT:    (real) Mean temperature of shape                                                  #####
#####                vol:   (real) volume of shape                                                            #####
#####      Outputs : merit: (real) value of the merit of shape                                                #####
###################################################################################################################

def evalObjAL(MT,vol) :

  # Read parameters in the exchange file
  [lmo] = inout.getrAtt(file=path.EXCHFILE,attname="lmAL")
  [muo] = inout.getrAtt(file=path.EXCHFILE,attname="penAL")
  [vtarg] = inout.getrAtt(file=path.EXCHFILE,attname="VolumeTarget")

  merit = MT - lmo*(vol-vtarg) + 0.5*muo*(vol-vtarg)**2

  return merit

###################################################################################################################
###################################################################################################################
