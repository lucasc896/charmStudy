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



    for i in range(len(nom[process])):

      try:
        eff = float(nom[process][i]/denomVals[i])
        # if "Other" in process:
          # print nom[process]
      except ZeroDivisionError:
        print "*** Error: Zero Division for", process
        eff=0.
      effOut[process].append(eff)
      outTxt += "& %.3f " % eff

    outTxt += r" \\"

  # makeTable(vals=effOut, label=label)

  return effOut

###-------------------------------------------------------------------###

def formatLabel(label=""):

  label = label.replace("GenHadTau", r"$\tau \to had$")
  label = label.replace("GenEle", r"$\tau/W/Z \to e$")
  label = label.replace("GenMu", r"$\tau/W/Z \to \mu$")
  label = label.replace("IT", "IT Matched ")
  label = label.replace("N", "")
  label = label.replace("isoTrack ", "")
  label = label.replace("All", "Cut")

  return label

###-------------------------------------------------------------------###

def makeTable(vals={}, label=""):
  
  out = ""
  out += printHeader(label = label)
  out += printHT()

  # user-defined order of table contents
  order = ["Cut", "Ele", "Mu", "Tau", "Other"]

  for ord in order:
    for key in vals:
      if ord in formatLabel(key):
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

def printCaption(label = ""):

  sample = switches()["sample"].replace("_", " ")

  outTxt = "\\caption{Single Isolated Track %s efficiencies for %s}\n" % (label, sample)

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

def printHeader(label = ""):
  outTxt = ""
  outTxt += "\\documentclass[a4paper,12pt]{article}\n"
  outTxt += "\\usepackage[margin=0.3in, landscape]{geometry}\n"
  outTxt += "\\begin{document}\n\n"
  outTxt += "\\begin{table}[lp{5cm}l]\n"
  outTxt += printCaption(label)
  outTxt += "\\begin{center}\n"
  outTxt += "\\begin{tabular}{ c|cccccccccc }\n"

  return outTxt

###-------------------------------------------------------------------###

def addDict(a={}, b={}):

  for val in b:
    a[val] = b[val]

  return a

###-------------------------------------------------------------------###
##                                                                     ##
###                       START OF MAIN CODE                          ###
##                                                                     ##
###-------------------------------------------------------------------###

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
      "Ele":[],
      "Mu":[],
      "HadTau":[],
}

matchedYld = {
      "Ele":[],
      "Mu":[],
      "HadTau":[],
      "Other":[],
}

vetoes = []

HTdirs = ["200_275", "275_325", "325_375", "375_475", "475_575", "575_675", "675_775", "775_875", "875_975", "975"]

HTBinEdges = []
for ht in HTdirs:
  val = float(ht.split("_")[0])
  HTBinEdges.append(val)

inFileName = "../../rootfiles/isoTrackPlots/out%s_isoTrackPlots.root" % switches()["sample"]
iF = r.TFile.Open(inFileName)


### genLevel, before SITV yields ###
for b in beforeYld:
  for ht in HTdirs:
    if b!="All":
      hName = "Gen%sN" % b
    else:
      hName = "n_Events"

    val = getYield(inFile=iF, hist=hName, dir=ht, bM=range(5) if b!="All" else [0])
    beforeYld[b].append(val)


### genLevel, after SITV yields ###
for a in afterYld:
  for ht in HTdirs:
    if a!="All":
      hName = "Gen%sN" % a
    else:
      hName = "n_Events"

    val = getYield(inFile=iF, hist=hName, dir=ht, dirPre="after", bM=range(5) if a!="All" else [0])
    afterYld[a].append(val)


# get total number of vetoes from the above
for b, a in zip(beforeYld["All"], afterYld["All"]):
  vetoes.append(b-a)


### yields for processes in events with atleast one SIT ###
for u in unmatchedYld:
  hName = "Gen%sNoMatchN" % u
  ctr = 0
  for ht in HTdirs:
    val = getYield(inFile=iF, hist=hName, dir=ht, bM=range(5))
    unmatchedYld[u].append(val)
    ctr+=1

### yields for processes matched to SIT ###
for m in matchedYld:
  hName = "ITGen%sN" % m
  ctr=0
  for ht in HTdirs:
    val = getYield(inFile=iF, hist=hName, dir=ht, bM=range(5))
    matchedYld[m].append(val)
    ctr+=1


totEff = printEff(nom=afterYld, denom=beforeYld, label="Total")
eventEff = printEff(nom=matchedYld, denom=beforeYld, vetoes=vetoes, label="Event")
procEff = printEff(nom=matchedYld, denom=beforeYld, label="Process")

# matchEff = printEff(nom=matchedYld, denom=unmatchedYld, label = "Matching")

# make some tables
makeTable(vals = addDict(totEff, procEff), label="Total")
makeTable(vals = eventEff, label="Event")

# make a dict for graph plotting
graphDict = {"Total Efficiency": [HTBinEdges, totEff["All"]]}

for p in procEff:
  if "Other" in p: continue
  graphDict["Process Efficiency - " + formatLabel(p)] = [HTBinEdges, procEff[p]]

# plot efficiency graph
myGrapher = gutils.grapher(inData=graphDict, multiGraph = True)
myGrapher.xTitle = "H_T (GeV)"
myGrapher.title = "SITV Efficiencies"
myGrapher.outFileBase = "%s_sitvEffs" % switches()["sample"]
myGrapher.paint()

