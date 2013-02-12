#!/usr/bin/env python

import os, sys
import commands
import subprocess

def doHadd(fList=None, label="", ana="anaPlots"):

    print "\n >>> Doing hadd for %s"%(label)

    cmd = []

    c = commands.getstatusoutput("ls ../haddOut/out%s_%s.root"%(label, ana))
    if "No such file" not in c[1]:
        print "\n\t***Removing old file %s\n"%label
        cmd.append("rm")
        cmd.append("../haddOut/out%s_%s.root"%(label, ana))
        subprocess.call(cmd)
        cmd = []

    for i in fList:
        cmd.append(i)
    cmd.insert(0, "../haddOut/out%s_%s.root"%(label, ana))
    cmd.insert(0, "hadd")
    subprocess.call(cmd)

parDir = "../results_27_Nov"
dirs = ["275_", "325_", "375_"]
lsOut = []

for d in dirs:
    tmp = commands.getstatusoutput("ls %s/%s/*root"%(parDir, d))
    tmp = tmp[1].split("\n")
    if len(tmp)>1: lsOut += tmp

fWJets = []
fQCD   = []
fZinv  = []
fSinT  = []
fDiBo  = []
fTTbar = []

for f in lsOut:
    if "WJet" in f:
        fWJets.append(f)
    if "QCD" in f:
        fQCD.append(f)
    if "ZJets" in f:
        fZinv.append(f)
    if "_T_" in f or "_Tbar_" in f:
        fSinT.append(f)
    if "_ZZ_" in f or "_WW_" in f or "_WZ_" in f:
        fDiBo.append(f)
    if "_TT_CT10_" in f:
        fTTbar.append(f)

if fWJets: doHadd(fWJets, "WJets")
if fQCD: doHadd(fQCD, "QCD")
if fZinv: doHadd(fZinv, "Zinv")
if fSinT: doHadd(fSinT, "SinT")
if fDiBo: doHadd(fDiBo, "DiBo")
if fTTbar: doHadd(fTTbar, "TTbar")

        
