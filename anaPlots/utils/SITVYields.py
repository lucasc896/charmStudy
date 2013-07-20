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

def getYield(inFile=None, hist="", dir="", dirPre="before", bM=[0]):

  ent = 0
  dir = dirPre + dir
  for b in bM:
    h = inFile.Get("%s/%s_%s" % (dir, hist, b))
    # print hist
    ent += h.GetEntries()
  
  return ent

###-------------------------------------------------------------------###

def printPurity(before={}, matched={}):
  print ""

  totVeto = matched["All"]

  for m in matched:
    if m=="All": continue
    outTxt = formatLabel(m) + " Purity"
    for i in range(len(matched[m])):
      pur = float(matched[m][i]/totVeto[i])
      outTxt += "& %.3f " % pur
    
    print outTxt
  print ""
###-------------------------------------------------------------------###

def printEff(before={}, matched={}):
  print ""

  for process in before:
    outTxt = formatLabel(process) + " Efficiency"
    for i in range(len(matched[process])):
      eff = float(matched[process][i]/beforeYld[process][i])
      print process, matched[process][i], beforeYld[process][i]
      outTxt += "& %.3f " % eff

    print outTxt
  print""

###-------------------------------------------------------------------###

def printTotal(before={}, matched={}):
  pass

###-------------------------------------------------------------------###

def formatLabel(label=""):

  # label = label.replace("TauEle", r"$\tau \to e \nu$")
  # label = label.replace("TauMu", r"$\tau \to \mu \nu$")
  label = label.replace("GenTauHad", r"$\tau \to had$")
  label = label.replace("GenHadTau", r"$\tau \to had$")
  label = label.replace("GenEle", r"$\tau/W/Z \to e$")
  label = label.replace("GenMu", r"$\tau/W/Z \to \mu$")
  label = label.replace("IT", "IT Matched ")
  label = label.replace("N", "")
  # label = label.replace("VEle", r"$W/Z \to e \nu$")
  # label = label.replace("VMu", r"$W/Z \to \mu \nu$")
  label = label.replace("isoTrack ", "")

  return label

###-------------------------------------------------------------------###

if len(argv)<2:
  print "Whoah there young bucky...specificy a command line option, yeah?"
  exit()


beforeYld = {
      "All":[],
      "Ele":[],
      "Mu":[],
      "HadTau":[],
}

afterYld = {
      "All":[],
      "Ele":[],
      "Mu":[],
      "HadTau":[],
}

matchedYld = {
      "All":[],
      "Ele":[],
      "Mu":[],
      "HadTau":[],
}

HTdirs = ["200_275", "275_325", "325_375", "375_475", "475_575", "575_675", "675_775", "775_875", "875_975", "975"]

iF = r.TFile.Open("../../rootfiles/isoTrackPlots/outWJets_isoTrackPlots.root")

for b in beforeYld:
  for ht in HTdirs:
    if b!="All":
      hName = "Gen%sN" % (b if b!="HadTau" else "TauHad")
    else:
      hName = "n_Events"

    val = getYield(inFile=iF, hist=hName, dir=ht, bM=range(5) if b!="All" else [0])
    beforeYld[b].append(val)

for a in afterYld:
  for ht in HTdirs:
    if a!="All":
      hName = "Gen%sN" % (a if a!="HadTau" else "TauHad")
    else:
      hName = "n_Events"

    val = getYield(inFile=iF, hist=hName, dir=ht, dirPre="after", bM=range(5) if a!="All" else [0])
    afterYld[a].append(val)

for i in range(len(HTdirs)):
  matchedYld["All"].append(0)

for m in matchedYld:
  if m=="All": continue
  hName = "ITGen%sN" % m
  ctr=0
  for ht in HTdirs:
    val = getYield(inFile=iF, hist=hName, dir=ht, bM=range(5) if b!="All" else [0])
    matchedYld[m].append(val)
    matchedYld["All"][ctr] += val
    ctr+=1

print beforeYld
print ""
print afterYld
print ""
print matchedYld

if "p" in argv[1]:
  printPurity(before=beforeYld, matched=matchedYld)

if "e" in argv[1]:
  printEff(before=beforeYld, matched=matchedYld)

if "t" in argv[1]:
  printTotal(before=beforeYld, matched=matchedYld)
