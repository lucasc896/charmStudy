#!/usr/bin/env python

import os
import sys
import commands
import subprocess
from time import time

###-------------------------------------------------------------------###


def oldRemove(label="", ana="anaPlots"):

    cmd = []

    c = commands.getstatusoutput("ls ../haddOut/out%s_%s.root" % (label, ana))
    if "No such file" not in c[1]:
        cmd.append("rm")
        cmd.append("-v")
        cmd.append("../haddOut/out%s_%s.root" % (label, ana))
        if query_yes_no("Remove out%s_%s.root" % (label, ana)):
            subprocess.call(cmd)
        cmd = []

###-------------------------------------------------------------------###


def doHadd(fList=None, label="", ana="anaPlots"):

    print "\n >>> Doing hadd for %s"%(label)

    cmd = []

    cmd.append("hadd")
    cmd.append("-v")
    cmd.append("1")
    # cmd.append("-f")
    cmd.append("../haddOut/out%s_%s.root"%(label, ana))

    for i in fList:
        cmd.append(i)

    subprocess.call(cmd)

###-------------------------------------------------------------------###

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes":True,   "y":True,  "ye":True,
             "no":False,     "n":False}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")

###-------------------------------------------------------------------###           

def main():

    baseTime = time()

    parDir = sys.argv[1]
    lsOut = []

    samps = {
        "WJets":    ["WJet", "wj_lv_"],
        "QCD":      ["_QCD_"],
        "ZJets":    ["ZJets"],
        "SinTop":  ["_T_", "_Tbar_"],
        "DiBoson":  ["_ZZ_", "_WW_", "_WZ_"],
        "TTbar":    ["_TT_CT10_"],
	    "DY":	    ["DYJets"],
        "Photon":   ["GJets"],
        }

    haddDict = {}
     
    for key, val in samps.iteritems():
        oldRemove(key)
        tmp = commands.getstatusoutput("ls %s/*/*%s*.root" % (parDir, val[0]))
        if tmp[0]==0:
            haddDict[key] = tmp[1].split("\n")

    for s in haddDict:
        doHadd(haddDict[s], s, ana="isoTrackPlots")
        

###-------------------------------------------------------------------###
###-------------------------------------------------------------------###

if __name__=='__main__':

    if len(sys.argv)>1:
        main()
    else:
        print "\n >>> Error: Pass a directory as an arguement."
        print "\te.g. './hadd MC.py <dirPath>'\n"

