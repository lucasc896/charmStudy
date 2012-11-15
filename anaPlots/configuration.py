#!/usr/bin/env python
# encoding: utf-8
"""
configuration.py

Created by Chris Lucas on 2012-11-13.
Copyright (c) 2012 University of Bristol. All rights reserved.
"""

from sys import argv, exit


def mode():
  runMode = ["plotting", "yieldTables"][0]

  return runMode


def switches():
  switches={
          "plotMode"      :["anaPlots","standardPlots","comparisonPlots"][0],
          "signalSample"  :"T2cc_300"
          }

  return switches


def inFiles():
  """syntax is "Name":["path", scale]"""

  mcScale = 116.9 # corresponding to intL for had sample
  inDir = "/Users/cl7359/SUSY/charmStudy/ANALYSIS/rootfiles/anaPlots/"

  files = {
        "WJets":    ["%soutWJets_anaPlots.root"%inDir, mcScale],
        #"QCD":      ["%soutQCD_anaPlots.root"%inDir, mcScale],
        "SingleTop":["%soutSinT_anaPlots.root"%inDir, mcScale],
        "TTJets":   ["%soutTTbar_anaPlots.root"%inDir, mcScale],
        "DiBoson":  ["%soutDiBo_anaPlots.root"%inDir, mcScale],
        }

  return files


def sigFile():
  sigFile = {
          "T2cc_300":["../rootfiles/anaPlots/outT2cc_300_anaPlots.root", 100.],
          "T2cc_160":["../rootfiles/anaPlots/outT2cc_160_anaPlots.root", 100.],
          "T2bb_300":["../rootfiles/anaPlots/outT2bb_300_anaPlots.root", 100.],
  }

  return sigFile

def comparFiles():
  comparFiles = ["T2cc_160", "T2cc_300"]

  return comparFiles


def inDirs():
  dirs=["noCuts_0_10000"]
  #dirs=["_275_325", "_325_375", "_375_475", "_475_575", "_575_675", "_675_775", "_775_875", "_875"]
  return dirs


def bMulti():
  bMulti=[]
  bMultiAll=["inc", "0b", "1b", "2b", "3b", "4b","ge1b","ge2b","ge3b","ge4b"]
  
  #make selection here
  include=[0, 1, 2]

  for val in include:
    bMulti.append(bMultiAll[val])

  return bMulti


def sinHists():
  singleHists={"stopGenPtScal":10,
        "stopGenPtVect":10,
        "delPhi_vs_scalGenPt":4,
        "dPhiStopCharm":1,
        "dPhiNeutCharm":1,
        "dPhiStopNeut":1,
        "n_Events_1":1}
  
  return singleHists


def anaHists():  
  hists={#"MET":10,
    "MHT":10,
    "commHT":20,
    "hadronicAlphaTZoom":1,
    #"leadJetdelPhi":1,
    #"MHToverMET":1,
    #"jetPt":10,
    #"leadJetPt":10,
    #"subLeadJetPt":10}
    }
    
  return hists
