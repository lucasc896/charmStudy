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

  print inclbtagDict

  return {"0b":zerobtagDict, "1b":onebtagDict, "2b":twobtagDict, "3b":threebtagDict, "4b":fourbtagDict, "inc":inclbtagDict}


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
