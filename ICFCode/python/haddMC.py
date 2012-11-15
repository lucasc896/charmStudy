#!/usr/bin/env python

import os, sys
import commands
import subprocess

def doHadd(fList=None, label="", ana="anaPlots"):

    print " >>> Doing hadd for %s"%(label)

    myStr=""
    for i in fList:
        myStr += " %s"%i 
        #myStr.append(i)

    #print myStr
    cmd = ["hadd", "../haddOut/out%s_%s.root"%(label, ana), myStr]
    #subprocess.call(cmd)

    print cmd



tmp = commands.getstatusoutput("ls ../results_14_Nov_06/375_/*root")
tmp = tmp[1:]
tmp = tmp[0].split("\n")

fWJets = []
fQCD   = []
fZinv  = []
fSinT  = []
fDiBo  = []
fTTbar = []

for f in tmp:
    if "WJet" in f:
        fWJets.append(f)
    if "QCD" in f:
        fQCD.append(f)
    if "ZJets" in f:
        fZinv.append(f)
    if "_T_" or "_Tbar_" in f:
        fSinT.append(f)
    if "_ZZ_" or "_WW_" or "_WZ_" in f:
        fDiBo.append(f)
    if "_TTJets" in f:
        fTTbar.append(f)

if fWJets: doHadd(fWJets, "WJets")
if fQCD: doHadd(fQCD, "QCD")
if fZinv: doHadd(fZinv, "Zinv")
if fSinT: doHadd(fSinT, "SinT")
if fDiBo: doHadd(fDiBo, "DiBo")
if fTTbar: doHadd(fTTbar, "TTbar")

        
