#!/usr/bin/env python
# encoding: utf-8

import ROOT as r
import generalUtils as gutils
import math as ma
from sys import argv
from sys import exit
from Log import *

r.gROOT.SetBatch(r.kTRUE)

def switches():

  switches={
          "sample"        :["WJets", "TTbar", "DY", "ZJets", "T2tt_500_1", "T2tt_825_500",
                            "T2tt_400_1", "T2cc_200_190", "T2cc_200_120", "Muon"][1],
          "HTcuts"        :["noCutInc", "standardHT","highHT","lowHT","parkedHT"][1],
          "HTdirs"        :["200_275", "275_325", "325_375", "375_475", "475_575", "575_675", "675_775", "775_875", "875_975", "975"],
          "jetMulti"      :["le3j","ge4j","inc"][2],
          "bMulti"        :["0b", "1b", "2b", "ge0b"][-1],
          "SITV"          :["before", "after"][0],
          "sele"          :["", "onemuon", "dimuon"][0],
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
      subStr = "after" if sitv else "before"
      string = subStr+dir#+"_"+switches()["jetMulti"]

    # print "%s/%s_%s" % (string, hist, b)
    h = inFile.Get("%s/%s_%s" % (string, hist, b))
    
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
    effOut[process]=[[],[]]

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



    for i in range(len(nom[process][0])):

      try:
        eff = float(nom[process][0][i]/denomVals[0][i])
      except ZeroDivisionError:
        print "*** Error: Zero Division for", process
        eff=0.

      ### calc the error
      if eff != 0.:
        n = nom[process][0][i]
        en = nom[process][1][i]
        d = denomVals[0][i]
        ed = denomVals[1][i]
        
        err = eff * ma.sqrt( ma.pow(en/n,2) + ma.pow(ed/d,2) )
      
      else:
        err = 0.


      effOut[process][0].append(eff)
      effOut[process][1].append(err)

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
        for val in vals[key][0]:
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
  
  out = {}
  keys = a.keys() + b.keys()
  
  for key in keys:
    out[key] = [[],[]]
    
    try:
      lista = a[key]
    except KeyError:
      noa = True
    else:
      noa = False

    try:
      listb = b[key]
    except KeyError:
      nob = True
    else:
      nob = False

    if noa and not nob:
      out[key][0] = b[key][0]
      out[key][1] = b[key][1]
    elif nob and not noa:
      out[key][0] = a[key][0]
      out[key][1] = a[key][1]
    else:
      if len(lista)!=len(listb):
        print "Error: lists diff length"
        exit()
      for vala, valb in zip(lista, listb):
        out[key][0].append(vala+valb)
        out[key][1].append(ma.sqrt( inverse(vala)+inverse(valb) ))

  return a

###-------------------------------------------------------------------###

def inverse(val=0.):

  try:
    tmpVal = 1./val
  except ZeroDivisionError:
    return 0.
  else:
    return tmpVal 

###-------------------------------------------------------------------###

###-------------------------------------------------------------------###
##                                                                     ##
###                       START OF MAIN CODE                          ###
##                                                                     ##
###-------------------------------------------------------------------###

def main(samp = ""):

  beforeYld = {
        "All":[[],[]],
        "Ele":[[],[]],
        "Mu":[[],[]],
        "HadTau":[[],[]],
        "Other":[[],[]],
  }

  afterYld = {
        "All":[[],[]],
        "Ele":[[],[]],
        "Mu":[[],[]],
        "HadTau":[[],[]],
  }

  unmatchedYld = {
        "Ele":[[],[]],
        "Mu":[[],[]],
        "HadTau":[[],[]],
  }

  matchedYld = {
        "Ele":[[],[]],
        "Mu":[[],[]],
        "HadTau":[[],[]],
        "Other":[[],[]],
        "NoMatch":[[],[]],
  }

  vetoes = [[],[]]
  nSIT = [[],[]]
  HTBinEdges = []
  HTdirs = switches()["HTdirs"]
  
  for ht in HTdirs:
    val = float(ht.split("_")[0])
    HTBinEdges.append(val)

  inFileName = "../../rootfiles/isoTrackPlots/out%s_%sisoTrackPlots.root" % (samp,"muonSele_" if "muon" in switches()["sele"] else "")
  iF = r.TFile.Open(inFileName)

  ### get btag multiplicity
  if switches()["bMulti"] == "0b":
    bMulti = [0]
  elif switches()["bMulti"] == "1b":
    bMulti = [1]
  elif switches()["bMulti"] == "2b":
    bMulti = [2]
  elif switches()["bMulti"] == "ge0b":
    bMulti = range(5)


  ### get number of SIT per ht bin
  for ht in HTdirs:
    val = getYield(inFile=iF, hist="anySIT", dir=ht, bM=bMulti)
    nSIT[0].append(val)
    nSIT[1].append(inverse( ma.sqrt(val) ))


  ### genLevel, before SITV yields ###
  for b in beforeYld:
    for ht in HTdirs:
      if b!="All":
        hName = "Gen%sN" % b
      else:
        hName = "n_Events"

      val = getYield(inFile=iF, hist=hName, dir=ht, bM=bMulti if b!="All" else [0])
      beforeYld[b][0].append(val)
      beforeYld[b][1].append(inverse( ma.sqrt(val) ))


  ### genLevel, after SITV yields ###
  for a in afterYld:
    for ht in HTdirs:
      if a!="All":
        hName = "Gen%sN" % a
      else:
        hName = "n_Events"

      val = getYield(inFile=iF, hist=hName, dir=ht, sitv=True, bM=bMulti if a!="All" else [0])
      afterYld[a][0].append(val)
      afterYld[a][1].append(inverse( ma.sqrt(val) ))


  ### get total number of vetoes from the above
  for b, a in zip(beforeYld["All"][0], afterYld["All"][0]):
    # print b
    vetoes[0].append(b-a)
    vetoes[1].append(ma.sqrt( inverse(a)+inverse(b) ))

  ### yields for processes in events with atleast one SIT ###
  for u in unmatchedYld:
    hName = "Gen%sNoMatchN" % u
    ctr = 0
    for ht in HTdirs:
      val = getYield(inFile=iF, hist=hName, dir=ht, bM=bMulti)
      unmatchedYld[u][0].append(val)
      unmatchedYld[u][1].append(inverse( ma.sqrt(val) ))
      ctr+=1


  ### yields for processes matched to SIT ###
  for m in matchedYld:
    hName = "ITGen%sN" % m
    if "NoMatch" in m:
      hName = "ITNoMatchN"
    ctr=0
    for ht in HTdirs:
      val = getYield(inFile=iF, hist=hName, dir=ht, bM=bMulti)
      matchedYld[m][0].append(val)
      matchedYld[m][1].append(inverse(ma.sqrt(val)))
      ctr+=1



  ### Calculate efficiencies
  totEff = printEff(nom=afterYld, denom=beforeYld, label="Total")
  eventEff = printEff(nom=matchedYld, denom=beforeYld, vetoes=vetoes, label="Event")
  procEff = printEff(nom=matchedYld, denom=beforeYld, vetoes=nSIT, label="Process")

  ### Make some tables
  makeTable(vals = addDict(totEff, procEff), sample = samp, label="Total")
  makeTable(vals = eventEff, sample = samp, label="Event")
  makeTable(vals = beforeYld, sample = samp, label="Processes")

  HT = [HTBinEdges, [5.] * len(HTBinEdges)]

  ### make a dict for graph plotting
  graphDict = {"Total Efficiency": [HT, totEff["All"]]}

  for p in procEff:
    graphDict["Process Fraction - " + formatLabel(p)] = [HT, procEff[p]]

  ### plot efficiency graph
  myGrapher = gutils.grapher(inData=graphDict, multiGraph = True)
  myGrapher.xTitle = "H_T (GeV)"
  myGrapher.title = "SITV Efficiencies"
  myGrapher.outFileBase = "%s_%ssitvEffs" % (samp, "muonSele_" if "muon" in switches()["sele"] else "")
  myGrapher.paint()

  return totEff["All"]

###-------------------------------------------------------------------###

allDict = {}

HTBinEdges = []
for ht in switches()["HTdirs"]:
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

