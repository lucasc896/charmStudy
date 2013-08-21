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
          "sample"        :["WJets", "TTbar", "DY", "ZJets", "T2tt_500_1", "T2tt_825_500",
                            "T2tt_400_1", "T2cc_200_190", "T2cc_200_120"][1],
          "HTcuts"        :["noCutInc", "standardHT","highHT","lowHT","parkedHT"][1],
          "jetMulti"      :["le3j","ge4j","inc"][-2],
          "SITV"          :["before", "after"][0],
          "sele"          :["", "onemuon", "dimuon"][1],
          "norm"          :["None", "Unitary", "xSec", "lumi"][0],
          }

  return switches

###-------------------------------------------------------------------###

def getYield(inFile=None, hist="", dir="", sitv=False, bM=[0]):

  ent = 0
  for b in bM:
    if "muon" in switches()["sele"]:
      subStr = "sitv_" if sitv else ""
      string = switches()["sele"]+"_"+subStr+dir+"_"+switches()["jetMulti"]
    else:
      subStr = "after_" if sitv else "before_"
      string = subStr+dir+"_"+switches()["jetMulti"]

    h = inFile.Get("%s/%s_%s" % (string, hist, b))
    
    # print "%s/%s_%s" % (string, hist, b)
    ent += h.GetEntries()

  return ent

###-------------------------------------------------------------------###

# def getNSIT(inFile=None, hist="anySIT", dir="", sitv=False, bM=[0]):

#   nSIT = 0

#   for b in bM:
#     if "muon" in switches()["sele"]:
#       subStr = "sitv_" if sitv else ""
#       string = switches()["sele"]+"_"+subStr+dir+"_"+switches()["jetMulti"]
#     else:
#       subStr = "after_" if sitv else "before_"
#       string = subStr+dir+"_"+switches()["jetMulti"]

#     h = inFile.Get("%s/%s_%s" % (string, hist, b))

#     for i in range(h.GetNbinsX()):
#       x = h.GetBinLowEdge(i)
#       n = h.GetBinContent(i)
      
#       # cut out nSIT=0 and underflow bins
#       if x<1.: continue
      
#       #nSIT += n*x
#     nSIT += h.GetEntries()
#   # print dir, nSIT
#   return nSIT


###-------------------------------------------------------------------###

def printEff(nom={}, denom={}, vetoes=[], label=""):

  effOut = {}
  passList = []

  if "Total" in label:
    passList = ["All"]
  else:
    passList = ["Ele", "Mu", "HadTau", "Other", "NoMatch"]

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
        # print nom[process][i], denomVals[i]
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
  # label = label.replace("N", "")
  label = label.replace("isoTrack ", "")
  label = label.replace("All", "Cut")



  return label

###-------------------------------------------------------------------###

def makeTable(vals={}, sample = "", label=""):
  
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

  f = open("yields/yieldTable_%s_%s.tex" % (sample, label), "w")
  f.write(out)
  f.close()

###-------------------------------------------------------------------###

def printCaption(samp = "", label = ""):

  sample = samp.replace("_", " ")

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

###-------------------------------------------------------------------###
##                                                                     ##
###                       START OF MAIN CODE                          ###
##                                                                     ##
###-------------------------------------------------------------------###

def main(samp = ""):

  beforeYld = {
        "All":[],
        "Ele":[],
        "Mu":[],
        "HadTau":[],
        "Other":[],
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
        "NoMatch":[],
  }

  vetoes = []

  nSIT = []

  HTdirs = ["200_275", "275_325", "325_375", "375_475", "475_575", "575_675", "675_775", "775_875", "875_975", "975"]

  HTBinEdges = []
  for ht in HTdirs:
    val = float(ht.split("_")[0])
    HTBinEdges.append(val)

  inFileName = "../../rootfiles/isoTrackPlots/out%s_%sisoTrackPlots.root" % (samp,"muonSele_" if "muon" in switches()["sele"] else "")
  iF = r.TFile.Open(inFileName)

  # get number of SIT per ht bin
  for ht in HTdirs:
    nSIT.append(getYield(inFile=iF, hist="anySIT", dir=ht, bM=range(5)))

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

      val = getYield(inFile=iF, hist=hName, dir=ht, sitv=True, bM=range(5) if a!="All" else [0])
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
    if "NoMatch" in m:
      hName = "ITNoMatchN"
    ctr=0
    for ht in HTdirs:
      val = getYield(inFile=iF, hist=hName, dir=ht, bM=range(5))
      matchedYld[m].append(val)
      ctr+=1

  totEff = printEff(nom=afterYld, denom=beforeYld, label="Total")
  eventEff = printEff(nom=matchedYld, denom=beforeYld, vetoes=vetoes, label="Event")
  procEff = printEff(nom=matchedYld, denom=beforeYld, vetoes=nSIT, label="Process")

  # matchEff = printEff(nom=matchedYld, denom=unmatchedYld, label = "Matching")

  # make some tables
  makeTable(vals = addDict(totEff, procEff), sample = samp, label="Total")
  # makeTable(vals = eventEff, sample = samp, label="Event")
  # makeTable(vals = beforeYld, sample = samp, label="Processes")

  # make a dict for graph plotting
  graphDict = {"Total Efficiency": [HTBinEdges, totEff["All"]]}

  for p in procEff:
    # if "Other" in p: continue
    graphDict["Process Fraction - " + formatLabel(p)] = [HTBinEdges, procEff[p]]

  # plot efficiency graph
  myGrapher = gutils.grapher(inData=graphDict, multiGraph = True)
  myGrapher.xTitle = "H_T (GeV)"
  myGrapher.title = "SITV Efficiencies"
  myGrapher.outFileBase = "%s_%ssitvEffs" % (samp, "muonSele_" if "muon" in switches()["sele"] else "")
  myGrapher.paint()

  return totEff["All"]

###-------------------------------------------------------------------###

allDict = {}

# get a better way of doing this...
HTdirs = ["200_275", "275_325", "325_375", "375_475", "475_575", "575_675", "675_775", "775_875", "875_975", "975"]

HTBinEdges = []
for ht in HTdirs:
  val = float(ht.split("_")[0])
  HTBinEdges.append(val)

if "list" in str(type(switches()["sample"])):
  for s in switches()["sample"]:
    eff = main(s)
    allDict[s] = [HTBinEdges, eff]
  
  myGrapher = gutils.grapher(inData=allDict, multiGraph = True)
  myGrapher.xTitle = "H_T (GeV)"
  myGrapher.title = "Total SITV Efficiencies"
  myGrapher.outFileBase = "total_sitvEffs"
  myGrapher.paint()

else:
  main(switches()["sample"])

