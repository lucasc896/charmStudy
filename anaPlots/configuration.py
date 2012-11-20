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
          "plotMode"      :["anaPlots","standardPlots","comparisonPlots"][1],
          "signalSample"  :"T2cc_160",
          "HTcuts"        :["fullInc", "hadrInc", "standardHT","highHT","lowHT"][0],
          "jetMulti"      :["le3j","ge4j","inc"][0],
          "PrintLogy"     :[True, False][0],
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
          "T2cc_300":     ["../rootfiles/anaPlots/outT2cc_300_anaPlots.root", 100.],
          "T2cc_160":     ["../rootfiles/anaPlots/outT2cc_160_anaPlots.root", 100.],
          "T2bb_300":     ["../rootfiles/anaPlots/outT2bb_300_anaPlots.root", 100.],
          "T2cc_225-190": ["../rootfiles/anaPlots/outT2cc_225-190_anaPlots.root", 100.],
          "T2cc_225-175": ["../rootfiles/anaPlots/outT2cc_225-175_anaPlots.root", 100.],
          "T2cc_225-150": ["../rootfiles/anaPlots/outT2cc_225-150_anaPlots.root", 100.],                    
  }

  return sigFile

def comparFiles():
  comparFiles = ["T2cc_160", "T2cc_300"]

  return comparFiles


def inDirs():

  if switches()["HTcuts"]=="fullInc": return ["noCuts_0_10000"]
  if switches()["HTcuts"]=="standardHT":
    if switches()["jetMulti"]=="inc":
      dirs=["inc_275_325", "inc_325_375", "inc_375_475", "inc_475_575", "inc_575_675", "inc_675_775", "inc_775_875", "inc_875"]
    if switches()["jetMulti"]=="le3j":
      dirs=["le3j_275_325", "le3j_325_375", "le3j_375_475", "le3j_475_575", "le3j_575_675", "le3j_675_775", "le3j_775_875", "le3j_875"]  
    if switches()["jetMulti"]=="ge4j":
      dirs=["ge4j_275_325", "ge4j_325_375", "ge4j_375_475", "ge4j_475_575", "ge4j_575_675", "ge4j_675_775", "ge4j_775_875", "ge4j_875"] 
  if switches()["HTcuts"]=="highHT":
    dirs = dirs[2:]
  if switches()["HTcuts"]=="lowHT":
    dirs = dirs[:2]

  return dirs


def bMulti():
  bMulti=[]
  bMultiAll=["inc", "0b", "1b", "2b", "3b", "4b","ge1b","ge2b","ge3b","ge4b"]

  include=[0, 1, 2]

  for val in include:
    bMulti.append(bMultiAll[val])

  return bMulti


def sinHists():
  singleHists={"stopGenPtScal":10,
        "stopGenPtVect":10,
        "delPhi_vs_scalGenPt":4,
        "dPhiStopCharm":2,
        "dPhiStopStop":2,
        "dPhiNeutCharm":2,
        "dPhiStopNeut":2,
        "n_Events_1":1}
  
  return singleHists


def anaHists():  
  hists={"MET":20,
    "MHT":20,
    "commHT":20,
    "hadronicAlphaTZoom":4,
    "leadJetdelPhi":2,
    "MHToverMET":5,
    "jetPt":20,
    "leadJetPt":20,
    "subLeadJetPt":20
    }

  return hists


def histRanges():
  rangeDict={
         "stopGenPtScal"        :[0., 1000.],
         "stopGenPtVect"        :[0., 1000.],
         "delPhi_vs_scalGenPt"  :[0., 1000.],
         "dPhiStopCharm"        :[0., 3.2],
         "dPhiNeutCharm"        :[0., 3.2],
         "dPhiStopNeut"         :[0., 3.2],
         "dPhiStopCharm"        :[0., 3.2],
         "n_Events_1"           :[0., 1.],
         "MET"                  :[0., 500.],
         "MHT"                  :[0., 500.],
         "commHT"               :[0., 700.],
         "hadronicAlphaTZoom"   :[0.,  1.5],
         "leadJetdelPhi"        :[0., 3.2],
         "MHToverMET"           :[0., 8.],
         "jetPt"                :[0., 500.],
         "leadJetPt"            :[0., 500.],
         "subLeadJetPt"         :[0., 400.],         
  }

  return rangeDict

