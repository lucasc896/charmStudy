#!/usr/bin/env python
# encoding: utf-8
"""
tables.py

Created by Chris Lucas on 2012-11-14.
Copyright (c) 2012 University of Bristol. All rights reserved.
"""

from sys import argv, exit
from generalUtils import *
from Log import *
import configuration as conf
import math
from collections import OrderedDict

###-------------------------------------------------------------------###

def getbMultis(bM=""):
  bMultiHists = {
    "0b":["_0"],
    "1b":["_1"],
    "2b":["_2"],
    "3b":["_3"],
    "4b":["_4"],
    "ge1b":["_1", "_2", "_3", "_4", "_5"],
    "ge2b":["_2", "_3", "_4", "_5"],
    "ge3b":["_3", "_4", "_5"],
    "ge4b":["_4", "_5"],
    "inc":["_0", "_1", "_2", "_3", "_4", "_5"],}

  return bMultiHists[bM]

###-------------------------------------------------------------------###

def getSMPred(bM="inc", jM="inc"):

  zerobtagDict={
          "225-275":[0., 0., 0., 0.],
          "275-325":[6235., 100., 1010., 34.],
          "325-375":[2900., 60., 447., 19.],
          "375-475":[1955., 34., 390., 19.],
          "475-575":[558., 14., 250., 12.],
          "575-675":[186., 11., 111., 9.],
          "675-775":[51.3, 3.4, 53.3, 4.3],
          "775-875":[21.2, 2.3, 18.5, 2.4],
          "875-inf":[16.1, 1.7, 19.4, 2.5],
  }

  onebtagDict={
          "225-275":[0., 0., 0., 0.],
          "275-325":[1162, 37., 521., 25.],
          "325-375":[481., 18., 232., 15.],
          "375-475":[341., 15., 188., 12.],
          "475-575":[86.7, 4.2, 106., 6.],
          "575-675":[24.8, 2.8, 42.1, 4.1],
          "675-775":[7.2, 1.1, 17.9, 2.2],
          "775-875":[3.3, 0.7, 9.8, 1.5],
          "875-inf":[2.1, 0.5, 6.8, 1.2],
  }
  twobtagDict={
          "225-275":[0., 0., 0., 0.],
          "275-325":[224., 15., 208., 17.],
          "325-375":[98.2, 8.4, 103., 9.],
          "375-475":[59., 5.2, 85.9, 7.2],
          "475-575":[12.8, 1.6, 51.7, 4.6],
          "575-675":[3., 0.9, 19.9, 3.4],
          "675-775":[.5, 0.2, 6.8, 1.2],
          "775-875":[0.1, 0.1, 1.7, 0.7],
          "875-inf":[0.1, 0., 1.3, 0.4],
  }
  threebtagDict={
          "225-275":[0., 0., 0., 0.],
          "275-325":[0., 0., 25.3, 5.],
          "325-375":[0., 0., 11.7, 1.7],
          "375-475":[0., 0., 6.7, 1.4],
          "475-575":[0., 0., 3.9, 0.8],
          "575-675":[0., 0., 2.3, 0.6],
          "675-775":[0., 0., 1.2, 0.3],
          "775-875":[0., 0., 0.3, 0.2],
          "875-inf":[0., 0., 0.1, 0.1],
  }
  fourbtagDict={
          "225-275":[0., 0., 0., 0.],
          "275-325":[0., 0., 0.9, 0.4],
          "325-375":[0., 0., 0.3, 0.2],
          "375-475":[0., 0., 0.6, 0.3],
          "475-575":[0., 0., 0., 0.],
          "575-675":[0., 0., 0., 0.],
          "675-775":[0., 0., 0., 0.],
          "775-875":[0., 0., 0., 0.],
          "875-inf":[0., 0., 0., 0.],
  }
  inclbtagDict={
          "225-275":[0., 0., 0., 0.],
          "275-325":[0., 0., 0., 0.],
          "325-375":[0., 0., 0., 0.],
          "375-475":[0., 0., 0., 0.],
          "475-575":[0., 0., 0., 0.],
          "575-675":[0., 0., 0., 0.],
          "675-775":[0., 0., 0., 0.],
          "775-875":[0., 0., 0., 0.],
          "875-inf":[0., 0., 0., 0.], 
  }

  HTbins = [
          "225-275",
          "275-325",
          "325-375",
          "375-475",
          "475-575",
          "575-675",
          "675-775",
          "775-875",
          "875-inf",
        ]


  #sum all dictionaries to make inclusive dict
  for i in HTbins:
    for k in range(4):
      if k==0 or k==2:
        inclbtagDict[i][k]+=zerobtagDict[i][k]
        inclbtagDict[i][k]+=onebtagDict[i][k]
        inclbtagDict[i][k]+=twobtagDict[i][k]
        inclbtagDict[i][k]+=threebtagDict[i][k]
        inclbtagDict[i][k]+=fourbtagDict[i][k]
      if k==1 or k==3:
        inclbtagDict[i][k]+=zerobtagDict[i][k]*zerobtagDict[i][k]
        inclbtagDict[i][k]+=onebtagDict[i][k]*onebtagDict[i][k]
        inclbtagDict[i][k]+=twobtagDict[i][k]*twobtagDict[i][k]
        inclbtagDict[i][k]+=threebtagDict[i][k]*threebtagDict[i][k]
        inclbtagDict[i][k]+=fourbtagDict[i][k]*fourbtagDict[i][k]
    inclbtagDict[i][1]=math.sqrt(inclbtagDict[i][1])
    inclbtagDict[i][3]=math.sqrt(inclbtagDict[i][3])

  zerobtagDict  = OrderedDict(sorted(zerobtagDict.items(), key=lambda t: t[0]))
  onebtagDict   = OrderedDict(sorted(onebtagDict.items(), key=lambda t: t[0]))
  twobtagDict   = OrderedDict(sorted(twobtagDict.items(), key=lambda t: t[0]))
  threebtagDict = OrderedDict(sorted(threebtagDict.items(), key=lambda t: t[0]))
  fourbtagDict  = OrderedDict(sorted(fourbtagDict.items(), key=lambda t: t[0]))
  inclbtagDict  = OrderedDict(sorted(inclbtagDict.items(), key=lambda t: t[0]))

  if bM=="0b":
    smDict = zerobtagDict
  if bM=="1b":
    smDict = onebtagDict
  if bM=="inc":
    smDict = inclbtagDict
  
  for key, val in smDict.iteritems():
    if jM=="le3j": val = val[:2]
    if jM=="le3j": val = val[2:]
    if jM=="inc":
      val[0]=val[0]+val[2]
      val[1]=math.sqrt(val[1]*val[1] + val[3]*val[3])

  return smDict

###-------------------------------------------------------------------###

def getDataYields(bM="inc", debug=False):

  dirs        = conf.inDirs()
  sigSamp     = conf.switches()["signalSample"]
  sigFile     = conf.sigFile()

  if debug: Log.debug(sigFile[sigSamp][0])

  sFile = r.TFile.Open(sigFile[sigSamp][0])

  yieldDict = {}

  scale=1.

#  if "200_190" in sigSamp:
#    scale=494749.
#  elif "200_120" in sigSamp:
#    scale=601852.

#  scale=float(601852./90000.)

  Log.warning("Tables filled with scale factor %d"%scale)

  for d in dirs:
    ent=0
    dirTitle = d[4:].replace("_","-")
    if d=="inc_875": dirTitle="875-inf"
    for suf in getbMultis(bM):
      if debug: Log.debug("Getting %s/commHT%s"%(d, suf))
      h = sFile.Get("%s/commHT%s"%(d, suf))
      ent += h.GetEntries()
      if debug: Log.debug(str(ent))
    ent /= scale  
    yieldDict[dirTitle[1:]]=[ent, math.sqrt(ent)]

  return OrderedDict(sorted(yieldDict.items(), key=lambda t: t[0]))

###-------------------------------------------------------------------###

def printHeader():
  outTxt=""
  outTxt += "\\documentclass[a4paper,12pt]{article}\n"
  outTxt += "\\usepackage[margin=0.3in, landscape]{geometry}\n"
  outTxt += "\\begin{document}\n\n"
  outTxt += "\\begin{table}[lp{5cm}l]\n"

  return outTxt

###-------------------------------------------------------------------###

def printCaption(bM, jM):

  if jM=="le3j":
    label = "$N_{jet} \\leq 3$"
  elif jM=="ge4j":
    label = "$N_{jet} \\leq 3$"
  else:
    label = "all jets"

  outTxt = "\\caption{Yields for $\\alpha_T>$ 0.55 (%s b-jets, %s)}\n"%(bM, label)
  #add a bit more eventually

  return outTxt

###-------------------------------------------------------------------###

def printEnd():
  outTxt  = "\n\n\n"
  outTxt += "\\end{tabular}\n"
  outTxt += "\\end{center}\n"
  outTxt += "\\end{table}\n"
  outTxt += "\\end{document}"

  return outTxt

###-------------------------------------------------------------------###

def printHT():

  return " HT Bins (GeV) & 225-275 & 275-325 & 325-375 & 375-475 & 475-575 & 575-675 & 675-775 & 775-875 & 875-$\\inf$ \\\\ \n"

###-------------------------------------------------------------------###

def makeTable(bM="inc", debug=False):
  
  sigSamp  = conf.switches()["signalSample"]
  jM       = conf.switches()["jetMulti"]

  Log.info("\tBin: %s %s\n"%(bM, jM))

  smPred = getSMPred(bM, jM)
  dYield = getDataYields(bM, debug=debug)

  if debug: Log.debug("Opening: tableDump/yieldTable_%s_%s_%s.tex"%(sigSamp, jM, bM))

  f = open("tableDump/yieldTable_%s_%s_%s.tex"%(sigSamp, jM, bM), "w")
  outTxt = ""
  outTxt += printHeader()
  outTxt += printCaption(bM, jM)

  outTxt += "\\begin{center}\n"
  outTxt += "\\begin{tabular}{ c|ccccccccc }\n"

  outTxt += printHT()

  outTxt +="\\hline"

  print "\n*** SM BG Pred ***"

  outTxt += " SM BG Pred "

  for key, val in smPred.iteritems():
    print "%s\t%f \\pm %f"%(key, val[0], val[1])
    outTxt += "& %.1f $^{\pm %.1f }$ "%(val[0], val[1])

  outTxt += " \\\\"

  print "\n*** %s Yields"%(sigSamp)
  outTxt += "\n\n%s "%sigSamp.replace("_"," ")

  totYield = 0
  for key, val in dYield.iteritems():
    print "%s\t%f \\pm %f"%(key, val[0], val[1])
    outTxt += "& %.1f $^{\pm %.1f }$ "%(val[0], val[1])
    totYield += val[0]

  print "\n*** Total Yield for %s: %d ***\n"%(sigSamp, totYield)
  outTxt += "\ntotal: %f"%totYield
  outTxt += " \\\\"

  outTxt += printEnd()

  f.write(outTxt)

###-------------------------------------------------------------------###

def printTable(debug=False):
  
  bMulti = conf.bMulti()

  for b in bMulti:
    makeTable(b, debug=debug)
