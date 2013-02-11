#!/usr/bin/env python
# encoding: utf-8
"""
makeAnaPlots.py

Created by Chris Lucas on 2012-11-13.
Copyright (c) 2012 University of Bristol. All rights reserved.
"""

import sys
from Log import *
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
  
  Log.info("\n >>> Making Analysis Plots\n")

  files       = conf.inFiles()
  dirs        = conf.inDirs()
  bMulti      = conf.bMulti()
  hists       = conf.anaHists()
  sigSamp     = conf.switches()["signalSample"]
  sigFile     = conf.sigFile()

  c1 = r.TCanvas()

  sigXSec = conf.getXSec()

  sigNorm = 0.01*conf.switches()["lumiNorm"]*sigXSec

  for hT, pDet in hists.iteritems():
    for b in bMulti:
      if debug: Log.debug(hT)
      if sigSamp:
        sFile=r.TFile().Open(sigFile[sigSamp][0])
        if debug: Log.debug(sFile)
        hS = getPlotsFromFile(hT, dirs, getbMultis(b), sFile, sigNorm)
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
      a1.xRange = pDet["xRange"]
      a1.yRange = pDet["yRange"]
      a1.xRebin = pDet["rebinX"]
      a1.yRebin = pDet["rebinY"]
      a1.canvTitle = hT
      a1.oFileName = oFileName
      a1.sigTitle = sigSamp
      if conf.switches()["printLogy"]: a1.PrintLogy = True
      a1.drawStack()
      del a1
 
###-------------------------------------------------------------------###

def runStandPlots(printPlots=True, comparSamp=None, debug=False, doLogy=False):

  if printPlots: Log.info("\n >>> Making Standard Plots\n")

  dirs        = conf.inDirs()
  bMulti      = conf.bMulti()
  hists       = conf.anaHists()
  sinHists    = conf.sinHists()
  sFile       = conf.sigFile()
  sigSamp     = conf.switches()["signalSample"]
  jMulti      = conf.switches()["jetMulti"]

  # override the global signal sample if running comparison plots
  if comparSamp: sigSamp = comparSamp

  if debug: Log.debug(sFile[sigSamp][0])
  
  normVal = None
  if conf.switches()["norm"]=="Unitary":
    normVal = 1.
  elif conf.switches()["norm"]=="xSec" or conf.switches()["norm"]=="lumi":
    #FIXME
    if "T2cc_160" in sigSamp:
      normVal = conf.getXSecNorm(160)
    if "T2cc_220_" in sigSamp:
      normVal = conf.getXSecNorm(220)
    if "T2cc_300" in sigSamp:
      normVal = conf.getXSecNorm(300)

  rFile = r.TFile.Open(sFile[sigSamp][0])
  if debug: Log.debug(str(rFile))

  c1 = r.TCanvas()

  outHists = []

  #plot b-Multi plots
  for hT, pDet in hists.iteritems():
    for b in bMulti:
      histList = []
      for d in dirs:
        for suf in getbMultis(b):
          if debug: Log.debug("%s/%s%s"%(d, hT, suf))
          h = rFile.Get("%s/%s%s"%(d, hT, suf))
          histList.append(h)
      
      aPlot = anaPlot(histList, "%s_%s"%(hT, b))
      if debug: aPlot.Debug=True
      if doLogy: aPlot.SetLogy = True
      if conf.switches()["norm"]=="lumi": aPlot.xSecNorm=True
      hTot = aPlot.makeSinglePlot(rebinX=pDet["rebinX"], rebinY=pDet["rebinY"], norm=normVal)
      del aPlot
      
      doRanges(hTot, pDet)

      if "TH2D" in str( type(hTot) ):
        hTot.Draw("colz")
      elif "TH1D" in str( type(hTot) ):
        hTot.Draw("hist")

      outHists.append(hTot)  

      if printPlots:
        if "noCut" not in conf.switches()["HTcuts"]:
          c1.Print("plotDump/%s_%s_%s_%s.png"%(sigSamp, hT, b, jMulti))
        else:
          c1.Print("plotDump/%s_%s_%s_%s.png"%(sigSamp, hT, b, "noCuts"))   
  
  #plot single plots
  for hT, pDet in sinHists.iteritems():
    histList = []
    for d in dirs:
      if debug: Log.debug("%s/%s"%(d, hT))
      h = rFile.Get("%s/%s"%(d, hT))
      histList.append(h)
    
    aPlot = anaPlot(histList, hT)
    if debug: aPlot.Debug=True
    if doLogy: aPlot.SetLogy=True
    hTot = aPlot.makeSinglePlot(rebinX=pDet["rebinX"], rebinY=pDet["rebinY"], norm=normVal)
    del aPlot
    
    doRanges(hTot, pDet)

    if "TH2" in str( type(hTot) ): 
      hTot.Draw("colz")
    elif "TH1" in str( type(hTot) ):
      hTot.Draw("hist")

    outHists.append(hTot)  
    
    if printPlots:
        if "noCut" not in conf.switches()["HTcuts"]:
          c1.Print("plotDump/%s_%s_%s.png"%(sigSamp, hT, jMulti))
        else:
          c1.Print("plotDump/%s_%s_%s.png"%(sigSamp, hT, "noCuts"))
  
  return outHists

###-------------------------------------------------------------------###

def runComparPlots(debug=False, doLogy=False):

  if doLogy:
    Log.info("Making Comparison Plots (SetLogy=True)")
  else:
    Log.info("Making Comparison Plots")

  compFiles   = conf.comparFiles()
  if debug: Log.debug(str(compFiles))

  if len( conf.bMulti() )>1:
    Log.error("Only run comparison plots with one bMultiplicity")
    sys.exit()

  hList=[]
  for f in compFiles:
    hList.append( runStandPlots(printPlots=False, comparSamp=f, debug=debug, doLogy=doLogy) )

  for i in range( len(hList[0]) ):
    hComp = []
    for k in range( len(hList) ):
      hComp.append(hList[k][i])
    comparPlots(hComp, debug=debug, doLogy=doLogy)

