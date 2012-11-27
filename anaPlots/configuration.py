#!/usr/bin/env python
# encoding: utf-8
"""
configuration.py

Created by Chris Lucas on 2012-11-13.
Copyright (c) 2012 University of Bristol. All rights reserved.
"""

from sys import argv, exit

#print options

###-------------------------------------------------------------------###

def mode():
  
  runMode = ["bTagEff", "anaPlots"][1]

  return runMode

###-------------------------------------------------------------------###

def switches():
  #generic switches
  switches={
          "runMode"       :["plotting", "yieldTables"][0],
          "plotMode"      :["anaPlots","standardPlots","comparisonPlots"][2],
          "signalSample"  :"T2cc_220_195",
          "HTcuts"        :["noCutInc", "standardHT","highHT","lowHT"][0],
          "jetMulti"      :["le3j","ge4j","inc"][2],
          "printLogy"     :[False, True][0],
          "unitNorm"      :[False,True][0],
          }

  return switches

###-------------------------------------------------------------------###

def inFiles():
  """syntax is "Name":["path", scale]"""

  mcScale = 116.9 # corresponding to intL for had sample
  inDir = "/Users/cl7359/SUSY/charmStudy/ANALYSIS/rootfiles/"

  if mode()=="anaPlots":
    files = {
          "WJets":    ["%sanaPlots/outWJets_anaPlots.root"%inDir, mcScale],
          #"QCD":      ["%sanaPlots/outQCD_anaPlots.root"%inDir, mcScale],
          "SingleTop":["%sanaPlots/outSinT_anaPlots.root"%inDir, mcScale],
          "TTJets":   ["%sanaPlots/outTTbar_anaPlots.root"%inDir, mcScale],
          "DiBoson":  ["%sanaPlots/outDiBo_anaPlots.root"%inDir, mcScale],
          }
  elif mode()=="bTagEff":
    files = {
          "file": ["%sbTagEff/some_file.root"%inDir, mcScale]
    }
  return files

###-------------------------------------------------------------------###

def sigFile():
  inDir = "/Users/cl7359/SUSY/charmStudy/ANALYSIS/rootfiles/"

  if mode()=="anaPlots":
    sigFile = {
            "T2cc_300"                :["%sanaPlots/outT2cc_300_anaPlots.root"%inDir, 100.],
            "T2cc_160"                :["%sanaPlots/outT2cc_160_anaPlots.root"%inDir, 100.],
            "T2bb_300"                :["%sanaPlots/outT2bb_300_anaPlots.root"%inDir, 100.],
            "T2cc_225-190"            :["%sanaPlots/outT2cc_225-190_anaPlots.root"%inDir, 100.],
            "T2cc_225-175"            :["%sanaPlots/outT2cc_225-175_anaPlots.root"%inDir, 100.],
            "T2cc_225-150"            :["%sanaPlots/outT2cc_225-150_anaPlots.root"%inDir, 100.],
            "T2cc_160_pt10"           :["%sanaPlots/outT2cc_160_pt10_anaPlots.root"%inDir, 100.],
            "T2cc_300_pt10"           :["%sanaPlots/outT2cc_300_pt10_anaPlots.root"%inDir, 100.],                            
            "T2cc_160_pt20"           :["%sanaPlots/outT2cc_160_pt20_anaPlots.root"%inDir, 100.],
            "T2cc_300_pt20"           :["%sanaPlots/outT2cc_300_pt20_anaPlots.root"%inDir, 100.],
            "T2cc_160_pt20_ISRRW"     :["%sanaPlots/outT2cc_160_pt20_ISRRW_anaPlots.root"%inDir, 100.],
            "T2cc_160_ISRRW"          :["%sanaPlots/outT2cc_160_ISRRW_anaPlots.root"%inDir, 100.],
            "T2cc_220_195"            :["%sanaPlots/outT2cc_220_195_anaPlots.root"%inDir, 100.],           
            "T2cc_220_170"            :["%sanaPlots/outT2cc_220_170_anaPlots.root"%inDir, 100.],           
            "T2cc_220_145"            :["%sanaPlots/outT2cc_220_145_anaPlots.root"%inDir, 100.],           
            "T2cc_220_195_pt20"       :["%sanaPlots/outT2cc_220_195_pt20_anaPlots.root"%inDir, 100.],           
            "T2cc_220_170_pt20"       :["%sanaPlots/outT2cc_220_170_pt20_anaPlots.root"%inDir, 100.],           
            "T2cc_220_145_pt20"       :["%sanaPlots/outT2cc_220_145_pt20_anaPlots.root"%inDir, 100.],
            "T2cc_220_195_ISRRW"      :["%sanaPlots/outT2cc_220_195_ISRRW_anaPlots.root"%inDir, 100.],           
            "T2cc_220_170_ISRRW"      :["%sanaPlots/outT2cc_220_170_ISRRW_anaPlots.root"%inDir, 100.],           
            "T2cc_220_145_ISRRW"      :["%sanaPlots/outT2cc_220_145_ISRRW_anaPlots.root"%inDir, 100.],
            "T2cc_220_195_noAlphaInc" :["%sanaPlots/outT2cc_220_195_noAlphaInc_anaPlots.root"%inDir, 100.],           
            "T2cc_220_170_noAlphaInc" :["%sanaPlots/outT2cc_220_170_noAlphaInc_anaPlots.root"%inDir, 100.],           
            "T2cc_220_145_noAlphaInc" :["%sanaPlots/outT2cc_220_145_noAlphaInc_anaPlots.root"%inDir, 100.],          
    }
  elif mode()=="bTagEff":
    sigFile={
          "T2cc_160"      :["%sbTagEff_Study/outT2cc_160_bTagEff.root"%inDir],
          "T2cc_300"      :["%sbTagEff_Study/outT2cc_300_bTagEff.root"%inDir],
          "T2cc_220_195"  :["%sbTagEff_Study/outT2cc_220_195_bTagEff.root"%inDir],
          "T2cc_220_170"  :["%sbTagEff_Study/outT2cc_220_170_bTagEff.root"%inDir],
          "T2cc_220_145"  :["%sbTagEff_Study/outT2cc_220_145_bTagEff.root"%inDir],
    }


  return sigFile

###-------------------------------------------------------------------###

def comparFiles():

  comparFiles = ["T2cc_220_195_pt20", "T2cc_220_170_pt20", "T2cc_220_145_pt20"]
  #comparFiles = ["T2cc_220_170_pt20", "T2cc_160_pt20", "T2cc_300_pt20"]
  comparFiles = ["T2cc_220_195", "T2cc_220_170", "T2cc_220_145", "T2cc_300", "T2cc_160"]
  comparFiles = ["T2cc_160", "T2cc_300", "T2cc_220_145", "T2cc_220_170", "T2cc_220_195"]
  return comparFiles

###-------------------------------------------------------------------###

def inDirs():

  if switches()["HTcuts"]=="noCutInc": return ["noCuts_0_10000"]
  if switches()["HTcuts"]=="standardHT":
    if switches()["jetMulti"]=="inc":
      dirs=["inc_275_325", "inc_325_375", "inc_375_475", "inc_475_575", "inc_575_675", "inc_675_775", "inc_775_875", "inc_875"]
    if switches()["jetMulti"]=="le3j":
      dirs=["le3j_275_325", "le3j_325_375", "le3j_375_475", "le3j_475_575", "le3j_575_675", "le3j_675_775", "le3j_775_875", "le3j_875"]  
    if switches()["jetMulti"]=="ge4j":
      dirs=["ge4j_275_325", "ge4j_325_375", "ge4j_375_475", "ge4j_475_575", "ge4j_575_675", "ge4j_675_775", "ge4j_775_875", "ge4j_875"] 
  if switches()["HTcuts"]=="highHT":
    if switches()["jetMulti"]=="le3j":
      dirs=["le3j_375_475", "le3j_475_575", "le3j_575_675", "le3j_675_775", "le3j_775_875", "le3j_875"]
  if switches()["HTcuts"]=="lowHT":
    dirs = dirs[:2]

  return dirs

###-------------------------------------------------------------------###

def bMulti():
  bMulti=[]
  bMultiAll=["inc", "0b", "1b", "2b", "3b", "4b","ge1b","ge2b","ge3b","ge4b"]

  include=[0]

  for val in include:
    bMulti.append(bMultiAll[val])

  return bMulti

###-------------------------------------------------------------------###

def sinHists():
  if mode()=="anaPlots":
    singleHists={
          "stopGenPtScal":40,
          "stopGenPtVect":20,
          "delPhi_vs_scalGenPt":4,
          "dPhiStopCharm":2,
          "dPhiStopStop":2,
          "dPhiNeutCharm":2,
          "dPhiCharmCharm":2,
          "dPhiStopNeut":2,
          "n_Events_1":1,
          "n_Jets":1,
          "n_BTagged_Jets_all":1,
    }
  elif mode()=="bTagEff":
    singleHists={
          "n_Jets":1,
          "n_JetsMatchB":1,
          "n_JetsMatchC":1,
          "n_JetsMatchL":1,
          "jetFlavour_0":1,
          "jetFlavour_1":1,
          "jetFlavour_2":1,
          "jetFlavour_3":1,
          "n_Truth_B":1,
          "n_Truth_C":1,
    }
  
  return singleHists

###-------------------------------------------------------------------###

def anaHists():  
  
  if mode()=="anaPlots":
    hists={
      "MET":20,
      "MHT":20,
      "commHT":20,
      "hadronicAlphaTZoom":5,
      "leadJetdelPhi":2,
      "MHToverMET":2,
      "jetPt":20,
      "leadJetPt":20,
      "subLeadJetPt":20,
      #"alphaT_vs_HT":1,
    }
  elif mode()=="bTagEff":
    hists={}
  
  return hists

###-------------------------------------------------------------------###

def histRanges():
  rangeDict={
         "stopGenPtScal"        :[0., 1000.],
         "stopGenPtVect"        :[0., 500.],
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
         "n_BTagged_Jets_all"   :[0., 5.],
         "n_Jets"               :[0., 10.],
  }

  return rangeDict

