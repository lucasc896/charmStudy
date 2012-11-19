#!/usr/bin/env python
# encoding: utf-8
"""
tables.py

Created by Chris Lucas on 2012-11-14.
Copyright (c) 2012 University of Bristol. All rights reserved.
"""

from sys import argv, exit
from generalUtils import *
import configuration as conf
import math
from collections import OrderedDict


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


def getSMPred():

  zerobtagDict={
          "275-325":[.0, .0, .0, .0],
          "325-375":[.0, .0, .0, .0],
          "375-475":[.0, .0, .0, .0],
          "475-575":[.0, .0, .0, .0],
          "575-675":[.0, .0, .0, .0],
          "675-775":[.0, .0, .0, .0],
          "775-875":[.0, .0, .0, .0],
          "875-inf":[.0, .0, .0, .0],
  }

  zerobtagDict = OrderedDict(sorted(zerobtagDict.items(), key=lambda t: t[0]))

  onebtagDict={
          "275-325":[.0, .0, .0, .0],
          "325-375":[.0, .0, .0, .0],
          "375-475":[.0, .0, .0, .0],
          "475-575":[.0, .0, .0, .0],
          "575-675":[.0, .0, .0, .0],
          "675-775":[.0, .0, .0, .0],
          "775-875":[.0, .0, .0, .0],
          "875-inf":[.0, .0, .0, .0],
  }
  twobtagDict={
          "275-325":[.0, .0, .0, .0],
          "325-375":[.0, .0, .0, .0],
          "375-475":[.0, .0, .0, .0],
          "475-575":[.0, .0, .0, .0],
          "575-675":[.0, .0, .0, .0],
          "675-775":[.0, .0, .0, .0],
          "775-875":[.0, .0, .0, .0],
          "875-inf":[.0, .0, .0, .0],
  }
  threebtagDict={
          "275-325":[.0, .0, .0, .0],
          "325-375":[.0, .0, .0, .0],
          "375-475":[.0, .0, .0, .0],
          "475-575":[.0, .0, .0, .0],
          "575-675":[.0, .0, .0, .0],
          "675-775":[.0, .0, .0, .0],
          "775-875":[.0, .0, .0, .0],
          "875-inf":[.0, .0, .0, .0],
  }
  fourbtagDict={
          "275-325":[.0, .0, .0, .0],
          "325-375":[.0, .0, .0, .0],
          "375-475":[.0, .0, .0, .0],
          "475-575":[.0, .0, .0, .0],
          "575-675":[.0, .0, .0, .0],
          "675-775":[.0, .0, .0, .0],
          "775-875":[.0, .0, .0, .0],
          "875-inf":[.0, .0, .0, .0],
  }

  inclDict={
          "275-325":[.0, .0, .0, .0],
          "325-375":[.0, .0, .0, .0],
          "375-475":[.0, .0, .0, .0],
          "475-575":[.0, .0, .0, .0],
          "575-675":[.0, .0, .0, .0],
          "675-775":[.0, .0, .0, .0],
          "775-875":[.0, .0, .0, .0],
          "875-inf":[.0, .0, .0, .0], 
  }   

  return {"0b":zerobtagDict, "1b":onebtagDict, "2b":twobtagDict, "3b":threebtagDict, "4b":fourbtagDict, "inc":inclDict}


def getDataYields(bM="inc"):

  dirs        = conf.inDirs()
  sigSamp     = conf.switches()["signalSample"]
  sigFile     = conf.sigFile()

  sFile = r.TFile.Open(sigFile[sigSamp][0])

  yieldDict = {}
  ent = 0

  for d in dirs:
    dirTitle = d[4:].replace("_","-")
    if d=="inc_875": dirTitle="875-inf"
    for suf in getbMultis(bM):
      h = sFile.Get("%s/commHT%s"%(d, suf))
      print "%s/commHT_%s"%(d, suf)
      ent += h.GetEntries()
    yieldDict[dirTitle]=[ent, math.sqrt(ent)]

  return OrderedDict(sorted(yieldDict.items(), key=lambda t: t[0]))


def printHeader():
  outTxt=""
  outTxt += "\\documentclass[a4paper,12pt]{article}\n"
  outTxt += "\\usepackage[margin=0.3in]{geometry}\n"
  outTxt += "\\begin{document}\n\n"
  outTxt += "\\begin{table}[lp{5cm}l]\n"

  return outTxt


def printCaption(bM):
  outTxt = "\\caption{Yields for $\alpha_T>$ 0.55 (%s b-jets)}\n"%bM
  #add a bit more eventually

  return outTxt


def printEnd():
  outTxt  = "\n\n\\hline\n"
  outTxt += "\\end{tabular}\n"
  outTxt += "\\end{flushleft}\n"
  outTxt += "\\end{table}\n"
  outTxt += "\\end{document}"

  return outTxt


def makeTable(bM="inc"):
  
  sigSamp     = conf.switches()["signalSample"]

  smPred = getSMPred()
  dYield = getDataYields(bM)

  f = open("yieldTable_%s.tex"%bM, "w")
  outTxt = ""
  outTxt += printHeader()
  outTxt += printCaption(bM)

  outTxt += "\\begin{flushleft}\n"
  outTxt += "\\begin{tabular}{ c|cccccccc }\n"
  outTxt += "\\hline"

  print "\n*** SM BG Pred ***"

  outTxt += "SM BG Pred "

  for sKey, sVal in smPred[bM].iteritems():
    print "%s\t%f \\pm %f"%(sKey, sVal[0], sVal[1])
    outTxt += "& %.1f $^{\pm %.1f }$ "%(sVal[0], sVal[1])

  outTxt += " \\\\"

  print "\n*** %s Yields"%(sigSamp)
  outTxt += "\n\n%s "%sigSamp.replace("_"," ")

  for key, val in dYield.iteritems():
    print "%s\t%f \\pm %f"%(key, val[0], val[1])
    outTxt += "& %.1f $^{\pm %.1f }$ "%(val[0], val[1])

  outTxt += " \\\\"

  outTxt += printEnd()

  f.write(outTxt)

def printTable():

  bMulti = conf.bMulti()

  for b in bMulti:
    makeTable(b)
