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

def runAnaPlots():
  
  print "\n >>> Making Analysis Plots\n"

  files       = conf.inFiles()
  dirs        = conf.inDirs()
  bMulti      = conf.bMulti()
  hists       = conf.anaHists()
  sigSamp     = conf.switches()["signalSample"]
  sigFile     = conf.sigFile()

  sFile=r.TFile().Open(sigFile[sigSamp][0])

  for hT, rVal in hists.iteritems():
    for b in bMulti:
      bgHists=[]
      bgTitles=[]
      for sName, iF in files.iteritems():
        rFile = r.TFile().Open(iF[0])
        h = getPlotsFromFile(hT, dirs, getbMultis(b), rFile, iF[1])
        bgHists.append(h)
        bgTitles.append(sName)

      hS = getPlotsFromFile(hT, dirs, getbMultis(b), sFile, sigFile[sigSamp][1])

      oFileName="Stack_%s_%s.png"%(hT, b)

      a1 = stackPlots(bgHists, bgTitles, hS)
      a1.drawStack(hT, rVal, oFileName, sigTitle=sigSamp)
      del a1
###-------------------------------------------------------------------###

def runStandPlots(printPlots=True, comparSamp=None):

  if printPlots: print "\n >>> Making Standard Plots\n"

  dirs        = conf.inDirs()
  bMulti      = conf.bMulti()
  hists       = conf.anaHists()
  sinHists    = conf.sinHists()
  sFile       = conf.sigFile()
  sigSamp     = conf.switches()["signalSample"]

  # override the global signal sample if running comparison plots
  if comparSamp: sigSamp = comparSamp

  rFile = r.TFile.Open(sFile[sigSamp][0])
  c1 = r.TCanvas()

  outHists = []

  #plot b-Multi plots
  for hT, rVal in hists.iteritems():
    for b in bMulti:
      histList = []
      for d in dirs:
        for suf in getbMultis(b):
          h = rFile.Get("%s/%s%s"%(d, hT, suf))
          histList.append(h)
      aPlot = anaPlot(histList, "%s_%s"%(hT, b))
      hTot = aPlot.makeSinglePlot(rVal, 1.)
      if "TH2D" in str( type(hTot) ):
        hTot.Draw("colz")
      else:
        hTot.Draw("hist")
      outHists.append(hTot)  
      if printPlots: c1.Print("%s_%s_%s.png"%(sigSamp, hT, bMulti[0]))    
      del aPlot   
  
  #plot single plots
  for hT, rVal in sinHists.iteritems():
    histList = []
    for d in dirs:
      h = rFile.Get("%s/%s"%(d, hT))
      histList.append(h)
    aPlot = anaPlot(histList, hT)
    hTot = aPlot.makeSinglePlot(rVal, 1.)
    if "TH2D" in str( type(hTot) ):
      hTot.Draw("colz")
    else:
      hTot.Draw("hist")
    outHists.append(hTot)  
    if printPlots: c1.Print("%s_%s_%s.png"%(sigSamp, hT, bMulti[0]))
    del aPlot
  
  return outHists
###-------------------------------------------------------------------###

def runComparPlots():

  print "\n >>> Making Comparison Plots\n"

  files       = conf.inFiles()
  dirs        = conf.inDirs()
  bMulti      = conf.bMulti()
  hists       = conf.anaHists()
  sinHists    = conf.sinHists()
  sFile       = conf.sigFile()
  compFiles   = conf.comparFiles()


  ch0 = runStandPlots(printPlots=False, comparSamp=compFiles[0])
  ch1 = runStandPlots(printPlots=False, comparSamp=compFiles[1])

  for h0, h1 in zip(ch0, ch1):
    comparPlot(h0, h1)

