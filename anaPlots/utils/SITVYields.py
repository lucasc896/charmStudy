#!/usr/bin/env python
# encoding: utf-8

import ROOT as r
from sys import argv
from sys import exit
from Log import *

def switches():

  switches={
          "signalSample"  :"TTbar_isoTrack",
          "HTcuts"        :["noCutInc", "standardHT","highHT","lowHT","parkedHT"][1],
          "jetMulti"      :["le3j","ge4j","inc","after","before"][-1],
          "norm"          :["None", "Unitary", "xSec", "lumi"][0],
          }

  return switches

###-------------------------------------------------------------------###

def getYield(inFile=None, hist="", dir="", bM=[0]):

  ent = 0
  dir = "before" + dir
  for b in bM:
    h = inFile.Get("%s/%s_%s" % (dir, hist, b))
    # print hist
    ent += h.GetEntries()
  
  return ent

###-------------------------------------------------------------------###

def printPurity(before={}, veto={}):
  print ""

  totVeto = veto["All"]

  for v in veto:
    if v=="All": continue
    outTxt = formatLabel(v) + " Purity"
    for i in range(len(veto[v])):
      pur = float(veto[v][i]/totVeto[i])
      outTxt += "& %.3f " % pur
    
    print outTxt
  print ""
###-------------------------------------------------------------------###

def printEff(before={}, veto={}):
  pass

###-------------------------------------------------------------------###

def printTotal(before={}, veto={}):
  pass

###-------------------------------------------------------------------###

def formatLabel(label=""):

  label = label.replace("TauEle", r"$\tau \to e \nu$")
  label = label.replace("TauMu", r"$\tau \to \mu \nu$")
  label = label.replace("TauHad", r"$\tau \to had$")
  label = label.replace("VEle", r"$W/Z \to e \nu$")
  label = label.replace("VMu", r"$W/Z \to \mu \nu$")

  return label

###-------------------------------------------------------------------###

if len(argv)<2:
  print "Whoah there young bucky...specificy a command line option, yeah?"
  exit()


beforeYld = {
      "All":[],
      "TauEle":[],
      "TauMu":[],
      "TauHad":[],
      "VEle":[],
      "VMu":[],
}

vetoYld = {
      "All":[],
      "TauEle":[],
      "TauMu":[],
      "TauHad":[],
      "VEle":[],
      "VMu":[],
}

HTdirs = ["175_275", "275_325", "325_375", "375_475", "475_575", "575_675", "675_775", "775_875", "875"]

iF = r.TFile.Open("../../rootfiles/isoTrackPlots/outTTbar_isoTrackPlots.root")

for b in beforeYld:
  for ht in HTdirs:
    hName = "n_Events%s" % (b if b!="All" else "")
    val = getYield(inFile=iF, hist=hName, dir=ht, bM=range(5) if b!="All" else [0])
    beforeYld[b].append(val)

for i in range(len(HTdirs)):
  vetoYld["All"].append(0)

for v in vetoYld:
  if v=="All": continue
  hName = "n_Events%sITMatched" % (v if v!="All" else "")
  ctr=0
  for ht in HTdirs:
    val = getYield(inFile=iF, hist=hName, dir=ht, bM=range(5) if b!="All" else [0])
    vetoYld[v].append(val)
    vetoYld["All"][ctr] += val
    ctr+=1


if "p" in argv[1]:
  printPurity(before=beforeYld, veto=vetoYld)

if "e" in argv[1]:
  printEff(before=beforeYld, veto=vetoYld)

if "t" in argv[1]:
  printTotal(before=beforeYld, veto=vetoYld)
