#!/usr/bin/env python

import os, sys
import commands
import subprocess
from time import time

###-------------------------------------------------------------------###


def oldRemove(label="", ana="anaPlots"):

    cmd = []

    c = commands.getstatusoutput("ls ../haddOut/out%s_%s.root"%(label, ana))
    if "No such file" not in c[1]:
        cmd.append("rm")
        cmd.append("../haddOut/out%s_%s.root"%(label, ana))
        #if query_yes_no("Remove out%s_%s.root" % (label, ana)):
        #    subprocess.call(cmd)
        subprocess.call(cmd)
        cmd = []

###-------------------------------------------------------------------###


def doHadd(fList=None, label="", ana="anaPlots"):

    print "\n >>> Doing hadd for %s"%(label)

    cmd = []

    cmd.append("hadd")
    cmd.append("-v")
    cmd.append("1")
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

    parDir = sys.argv[1]
    dirs = ["225_", "275_", "325_", "375_"]
    lsOut = []

    samps = {
        "WJets":    ["WJet"],
        "QCD":      ["_QCD_"],
        "ZJets":    ["ZJets"],
        "SingTop":  ["_T_", "_Tbar_"],
        "DiBoson":  ["_ZZ_", "_WW_", "_WZ_"],
        "TTbar":    ["_TT_CT10_"],
        }

    haddDict = {}

    # get list of root files
    for d in dirs:
        tmp = commands.getstatusoutput("ls %s/%s/*root" % (parDir, d))
        tmp = tmp[1].split("\n")
        if len(tmp)>1: lsOut += tmp

    # would save time if could remove non-present samples

    # group all files into samples within hadd dict
    # slow!!
    for f in lsOut:
        found = False
        for key, val in samps.iteritems():
            oldRemove(key)
            if key not in haddDict:
                haddDict[key] = []
            for v in val:
                if v in f:
                    if len(haddDict[key]) < 3:haddDict[key].append(f)
                    found = True
            if found: break

    # do some hadd'ing!
    for key, val in haddDict.iteritems():
        if len(val) > 0:
            doHadd(val, key)

            
###-------------------------------------------------------------------###
###-------------------------------------------------------------------###

if __name__=='__main__':

    if len(sys.argv)>1:
        main()
    else:
        print "\n >>> Error: Pass a directory as an arguement."
        print "\te.g. './hadd MC.py <dirPath>'\n"

