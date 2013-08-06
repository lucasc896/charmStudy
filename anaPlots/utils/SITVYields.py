#!/usr/bin/env python
# encoding: utf-8

import ROOT as r
import generalUtils as gutils
from sys import argv
from sys import exit
from Log import *

r.gROOT.SetBatch(r.kTRUE)

def switches():

  switches={
          "sample"        :["WJets", "TTbar", "DY", "ZJets", "T2cc_200_120"][2],
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
    # print "%s/%s_%s" % (dir, hist, b)
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

def printEff(nom={}, denom={}, vetoes=[], label=""):

  effOut = {}
  passList = []

  if "Total" in label:
    passList = ["All"]
  else:
    passList = ["Ele", "Mu", "HadTau", "Other"]

  for process in nom:

    # check if process in passList
    if process not in passList:
      continue

    outTxt = formatLabel(process) + " Efficiency "
    effOut[process]=[]

    # if "Other" not in one of the dicts, skip
    try:
      tmp = nom[process]
      if not vetoes:
        tmp = denom[process]
    except KeyError:
      if "Other" in process:
        continue

    if vetoes:
      denomVals = vetoes
    else:
      denomVals = denom[process]



    for i in range(len(denomVals)):

      try:
        eff = float(nom[process][i]/denomVals[i])
        # if "Other" in process:
          # print nom[process]
      except ZeroDivisionError:
        # print "*** Error: Zero Division for", process
        eff=0.
      effOut[process].append(eff)
      outTxt += "& %.3f " % eff

    outTxt += r" \\"

  makeTable(vals=effOut, label=label)

  return effOut

###-------------------------------------------------------------------###

def printTotal(before={}, matched={}):
  pass

###-------------------------------------------------------------------###

def formatLabel(label=""):

  # label = label.replace("TauEle", r"$\tau \to e \nu$")
  # label = label.replace("TauMu", r"$\tau \to \mu \nu$")
  label = label.replace("GenHadTau", r"$\tau \to had$")
  label = label.replace("GenEle", r"$\tau/W/Z \to e$")
  label = label.replace("GenMu", r"$\tau/W/Z \to \mu$")
  label = label.replace("IT", "IT Matched ")
  label = label.replace("N", "")
  # label = label.replace("VEle", r"$W/Z \to e \nu$")
  # label = label.replace("VMu", r"$W/Z \to \mu \nu$")
  label = label.replace("isoTrack ", "")
  label = label.replace("All", "Cut")

  return label

###-------------------------------------------------------------------###

def makeTable(vals={}, label=""):
  
  out = ""

  out += printHeader()
  out += printHT()

  for key in vals:
    out += formatLabel(key) + " "
    for val in vals[key]:
      out += "& %.3f " % val
    out += r"\\"
    out += "\n"

  out += printEnd()

  f = open("yieldTable_%s_%s.tex" % (switches()["sample"], label), "w")
  f.write(out)
  f.close()

###-------------------------------------------------------------------###

def printCaption():

  sample = switches()["sample"].replace("_", " ")

  outTxt = "\\caption{Single Isolated Track yields for %s}\n" % sample
  #add a bit more eventually

  return outTxt

###-------------------------------------------------------------------###

def printEnd():

  outTxt = "\n\n\n"
  outTxt += "\\end{tabular}\n"
  outTxt += "\\end{center}\n"
  outTxt += "\\end{table}\n"
  outTxt += "\\end{document}"

  return outTxt

###-------------------------------------------------------------------###

def printHT():

  HTline = " HT Bins (GeV) & 200-275 & 275-325 & 325-375 & 375-475 & 475-575 & 575-675 & 675-775 & 775-875 & 875-975 & 975-$\\inf$ \\\\ \n"
  HTline += "\hline\n"

  return HTline

###-------------------------------------------------------------------###

def printHeader():
  outTxt = ""
  outTxt += "\\documentclass[a4paper,12pt]{article}\n"
  outTxt += "\\usepackage[margin=0.3in, landscape]{geometry}\n"
  outTxt += "\\begin{document}\n\n"
  outTxt += "\\begin{table}[lp{5cm}l]\n"
  outTxt += printCaption()
  outTxt += "\\begin{center}\n"
  outTxt += "\\begin{tabular}{ c|cccccccccc }\n"

  return outTxt

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

unmatchedYld = {
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
      "Other":[],
}

vetoes = []

HTdirs = ["200_275", "275_325", "325_375", "375_475", "475_575", "575_675", "675_775", "775_875", "875_975", "975"]

inFileName = "../../rootfiles/isoTrackPlots/out%s_isoTrackPlots.root" % switches()["sample"]
iF = r.TFile.Open(inFileName)
print "\n", inFileName

### generic, before SITV yields ###
for b in beforeYld:
  for ht in HTdirs:
    if b!="All":
      hName = "Gen%sN" % b
    else:
      hName = "n_Events"

    val = getYield(inFile=iF, hist=hName, dir=ht, bM=range(5) if b!="All" else [0])
    beforeYld[b].append(val)

### generic, after SITV yields ###
for a in afterYld:
  for ht in HTdirs:
    if a!="All":
      hName = "Gen%sN" % a
    else:
      hName = "n_Events"

    val = getYield(inFile=iF, hist=hName, dir=ht, dirPre="after", bM=range(5) if a!="All" else [0])
    afterYld[a].append(val)

# get total number of vetoes
for b, a in zip(beforeYld["All"], afterYld["All"]):
  vetoes.append(b-a)

# zero out unecessary entries
for i in range(len(HTdirs)):
  unmatchedYld["All"].append(0)
  matchedYld["All"].append(0)

### yields for processes in events with atleast one SIT ###
for u in unmatchedYld:
  if u=="All": continue
  hName = "Gen%sNoMatchN" % u
  ctr = 0
  for ht in HTdirs:
    val = getYield(inFile=iF, hist=hName, dir=ht, bM=range(5) if b!="All" else [0])
    unmatchedYld[u].append(val)
    unmatchedYld["All"][ctr] += val
    ctr+=1

### yields for processes matched to SIT ###
for m in matchedYld:
  if m=="All": continue
  hName = "ITGen%sN" % m
  ctr=0
  for ht in HTdirs:
    val = getYield(inFile=iF, hist=hName, dir=ht, bM=range(5) if b!="All" else [0])
    matchedYld[m].append(val)
    matchedYld["All"][ctr] += val
    ctr+=1



if "p" in argv[1]:
  printPurity(before=beforeYld, matched=matchedYld)

if "e" in argv[1]:
  # print "\n>>> Total Efficiency"
  # totEff = printEff(nom=afterYld, denom=beforeYld, label="Total")
  # print totEff
  print "\n>>> Process Efficiency"
  procEff = printEff(nom=matchedYld, denom=beforeYld, vetoes=vetoes, label="Process")
  print procEff["HadTau"]

  # print "\n>>> Matching Efficiency"
  # printEff(nom=matchedYld, denom=unmatchedYld)

if "t" in argv[1]:
  printTotal(before=beforeYld, matched=matchedYld)

HTBinEdges = []
for ht in HTdirs:
  val = float(ht.split("_")[0])
  HTBinEdges.append(val)

# gutils.grapher([HTBinEdges, totEff["Ele"]])
