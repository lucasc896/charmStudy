#!/usr/bin/env python
# encoding: utf-8
"""
intellHad.py

Created by Chris Lucas on 2012-12-14.
Copyright (c) 2012 University of Bristol. All rights reserved.
"""

import commands
import subprocess
from optparse import OptionParser
from sys import exit

###-------------------------------------------------------------------###

parser = OptionParser()

parser.add_option("-n", "--nSplit",
                  type="int", dest="nSplit", default=10,
                  help="number of groups to split into")
parser.add_option("-r", "--run",
                  action="store_true", dest="doRun", default=False,
                  help="run the hadd process")

(options, args) = parser.parse_args()

###-------------------------------------------------------------------###

def doSplit(fList=[], nSplit=None):
   print "\n\t"+"*"*20
   print "  File list split into groups of %d."%nSplit
   print "\t   (%d hadd jobs.)"%(len(fList)/nSplit)
   print "\t"+"*"*20+"\n"

   print "* Run with '-r' option to hadd files."

   return [fList[x:x+nSplit] for x in xrange(0, len(fList), nSplit)]

###-------------------------------------------------------------------###

rootDir = "../../bryn/results_17_Dec_14/"
subDirs = [
#      "ht275NoUpper",
#      "ht325NoUpper",
      "ht375NoUpper"
      ]

protoName = "Triggers_SinMu_ABCD_"
oProtoName = "outSinMu_ABCD_trigEffs"
outTmp = ""

for d in subDirs:
   print "\n>>> Checking directory: %s/%s"%(rootDir,d)
   outTmp += commands.getstatusoutput("ls %s/%s/*root"%(rootDir,d))[1]
   print "\tFound %d files."%( len(outTmp.split("\n")) )
   outTmp += "\n"

# split fileList into list of splits
sList = doSplit(outTmp.split("\n"), options.nSplit)


outList = []

for n in range( len(sList) ):
   cmd = ["hadd"]
   cmd.append("%s/%s_%d.root"%("/".join(rootDir.split("/")), oProtoName, n))   
   outList.append("%s/%s_%d.root"%("/".join(rootDir.split("/")), oProtoName, n))

   for k in range( len(sList[n]) ):
      cmd.append("%s"%sList[n][k])

   if options.doRun: subprocess.call(cmd)


cmd = ["hadd", "%s/%s.root"%("/".join(rootDir.split("/")), oProtoName)]

for o in outList:
   cmd.append(o)

# hadd intermediate files
if options.doRun: subprocess.call(cmd)

# remove intermediate files
cmd = cmd[2:]
cmd.insert(0, "rm")

if options.doRun: subprocess.call(cmd)



