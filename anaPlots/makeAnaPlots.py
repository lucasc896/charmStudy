#!/usr/bin/env python
# encoding: utf-8
"""
makeAnaPlots.py

Created by Chris Lucas on 2012-11-13.
Copyright (c) 2012 University of Bristol. All rights reserved.
"""

from sys import argv, exit
from generalUtils import *
import configuration as conf
import tables as tbl

r.TH1.SetDefaultSumw2()
r.gROOT.SetBatch(True)

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

def runAnaPlots(debug=False):
  
  if debug: print "\n\tDEBUG: In runAnaPlots.\n"
  print "\n >>> Making Analysis Plots\n"

  files       = conf.inFiles()
  dirs        = conf.inDirs()
  bMulti      = conf.bMulti()
  hists       = conf.anaHists()
  sigSamp     = conf.switches()["signalSample"]
  sigFile     = conf.sigFile()


  for hT, rVal in hists.iteritems():
    for b in bMulti:
      if debug: print hT
      if sigSamp:
        sFile=r.TFile().Open(sigFile[sigSamp][0])
        if debug: print sFile
        hS = getPlotsFromFile(hT, dirs, getbMultis(b), sFile, sigFile[sigSamp][1])
      else: hS=None

      bgHists=[]
      bgTitles=[]
      for sName, iF in files.iteritems():
        rFile = r.TFile().Open(iF[0])
        h = getPlotsFromFile(hT, dirs, getbMultis(b), rFile, iF[1])
        bgHists.append(h)
        bgTitles.append(sName)

      oFileName="plotDump/Stack_%s_%s.png"%(hT, b)

      a1 = stackPlots(bgHists, bgTitles, hS)
      if debug: a1.Debug=True
      if conf.switches()["printLogy"]: a1.PrintLogy = True
      a1.drawStack(hT, rVal, oFileName, sigTitle=sigSamp)
      del a1
 
###-------------------------------------------------------------------###

def runStandPlots(printPlots=True, comparSamp=None, debug=False):

  if debug: print "\n\tDEBUG: In runStandPlots.\n"
  if printPlots: print "\n >>> Making Standard Plots\n"

  dirs        = conf.inDirs()
  bMulti      = conf.bMulti()
  hists       = conf.anaHists()
  sinHists    = conf.sinHists()
  sFile       = conf.sigFile()
  sigSamp     = conf.switches()["signalSample"]
  histRanges  = conf.histRanges()
  jMulti      = conf.switches()["jetMulti"]
#  debug       = conf.switches()["debug"]

  # override the global signal sample if running comparison plots
  if comparSamp: sigSamp = comparSamp

  if debug: print sFile[sigSamp][0]
  
  normVal = None
  if conf.switches()["unitNorm"]:
    normVal = 1.

  rFile = r.TFile.Open(sFile[sigSamp][0])
  if debug: print rFile

  c1 = r.TCanvas()

  outHists = []

  #plot b-Multi plots
  for hT, rVal in hists.iteritems():
    for b in bMulti:
      histList = []
      for d in dirs:
        for suf in getbMultis(b):
          if debug: print "%s/%s%s"%(d, hT, suf)
          h = rFile.Get("%s/%s%s"%(d, hT, suf))
          histList.append(h)
      aPlot = anaPlot(histList, "%s_%s"%(hT, b))
      if debug: aPlot.Debug=True
      hTot = aPlot.makeSinglePlot(rVal, normVal)
      del aPlot
      if "TH2D" in str( type(hTot) ):
        hTot.Draw("colz")
      else:
        hTot.Draw("hist")
      if hT in histRanges:
        ranges = histRanges[hT]
        hTot.GetXaxis().SetRangeUser(ranges[0], ranges[1])
      outHists.append(hTot)  
      if printPlots:
        if "noCut" not in conf.switches()["HTcuts"]:
          c1.Print("plotDump/%s_%s_%s_%s.png"%(sigSamp, hT, b, jMulti))
        else:
          c1.Print("plotDump/%s_%s_%s_%s.png"%(sigSamp, hT, b, "noCuts"))   
  
  #plot single plots
  for hT, rVal in sinHists.iteritems():
    histList = []
    for d in dirs:
      if debug: print "%s/%s"%(d, hT)
      h = rFile.Get("%s/%s"%(d, hT))
      histList.append(h)
    
    aPlot = anaPlot(histList, hT)
    if debug: aPlot.Debug=True
    hTot = aPlot.makeSinglePlot(rVal, normVal)
    del aPlot
    
    if "TH2D" in str( type(hTot) ):
      hTot.Draw("colz")
    else:
      hTot.Draw("hist")
    if hT in histRanges:
      ranges = histRanges[hT]
      hTot.GetXaxis().SetRangeUser(ranges[0], ranges[1])  
    
    outHists.append(hTot)  
    
    if printPlots:
        if "noCut" not in conf.switches()["HTcuts"]:
          c1.Print("plotDump/anaPlots_%s_%s_%s_%s.png"%(sigSamp, hT, b, jMulti))
        else:
          c1.Print("plotDump/%s_%s_%s_%s.png"%(sigSamp, hT, b, "noCuts"))
  
  return outHists

###-------------------------------------------------------------------###

def runComparPlots(debug=False):

  if debug: print "\n\tDEBUG: In runAnaPlots.\n"
  print "\n >>> Making Comparison Plots\n"

  files       = conf.inFiles()
  dirs        = conf.inDirs()
  bMulti      = conf.bMulti()
  hists       = conf.anaHists()
  sinHists    = conf.sinHists()
  sFile       = conf.sigFile()
  compFiles   = conf.comparFiles()

  if debug: print compFiles

  if len(bMulti)>1:
    print "\t*** Only run comparison plots with one bMultiplicity\n"
    sys.exit()

  hList=[]
  for f in compFiles:
    hList.append( runStandPlots(printPlots=False, comparSamp=f, debug=debug) )

  if len(hList)==2:
    for h1, h2 in zip(hList[0], hList[1]):
      hComp=[]
      hComp.append(h1)
      hComp.append(h2)
      comparPlots(hComp, debug=debug)

  if len(hList)==3:
    for h1, h2, h3 in zip(hList[0], hList[1], hList[2]):
      hComp=[]
      hComp.append(h1)
      hComp.append(h2)
      hComp.append(h3)    
      comparPlots(hComp, debug=debug)
  if len(hList)==5:
    for h1, h2, h3, h4, h5 in zip(hList[0], hList[1], hList[2], hList[3], hList[4]):
      hComp=[]
      hComp.append(h1)
      hComp.append(h2)
      hComp.append(h3)
      hComp.append(h4)
      hComp.append(h5)  
      comparPlots(hComp, debug=debug)
