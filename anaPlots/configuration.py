#!/usr/bin/env python
# encoding: utf-8
"""
configuration.py

Created by Chris Lucas on 2012-11-13.
Copyright (c) 2012 University of Bristol. All rights reserved.
"""

from sys import argv, exit
import ROOT as r

###-------------------------------------------------------------------###

def mode():
  
  anaMode = ["bTagEff", "anaPlots", "dev"][1]

  return anaMode

###-------------------------------------------------------------------###

def switches():
   
  switches={
          "runMode"       :["plotting", "yieldTables"][0],
          "plotMode"      :["anaPlots","standardPlots","comparisonPlots"][2],
          "runModeBTag"   :["charmFrac", "standardPlots", "charmPhi"][0],
          "signalSample"  :"T2cc_Scan_NoFilter",
          "HTcuts"        :["noCutInc", "standardHT","highHT","lowHT","parkedHT"][1],
          "jetMulti"      :["le3j","ge4j","inc"][0],
          "printLogy"     :[False, True][0],
          "norm"          :["None", "Unitary", "xSec", "lumi"][1],
          "lumiNorm"      :[1, 10, 11.7][0]
          }

  return switches

###-------------------------------------------------------------------###

def inFiles():
  """syntax is "Name":["path", scale]"""

  mcScale = 116.9 # corresponding to intL for had sample
  inDir = "/Users/cl7359/SUSY/charmStudy/ANALYSIS/rootfiles/"

  if mode()=="anaPlots":
    files = {
          "WJets"     :["%sanaPlots/outWJets_anaPlots.root"%inDir, mcScale],
          #"QCD"      :["%sanaPlots/outQCD_anaPlots.root"%inDir, mcScale],
          "SingleTop" :["%sanaPlots/outSinT_anaPlots.root"%inDir, mcScale],
          "TTJets"    :["%sanaPlots/outTTbar_anaPlots.root"%inDir, mcScale],
          "DiBoson"   :["%sanaPlots/outDiBo_anaPlots.root"%inDir, mcScale],
          }

  return files

###-------------------------------------------------------------------###

def sigFile():
  inDir = "/Users/cl7359/SUSY/charmStudy/ANALYSIS/rootfiles/"

  if mode()=="anaPlots":
    sigFile = {
            "T2cc_Scan_Filter"          :["%sanaPlots_225/outT2cc_Filter_anaPlots.root"%inDir, 100.],
            "T2cc_Scan_NoFilter"        :["%sanaPlots_225/outT2cc_NoFilter_anaPlots.root"%inDir, 100.],
            "T2bb_300"                  :["%sanaPlots_new/outT2bb_300_anaPlots.root"%inDir, 100.],
            "T2cc_160"                  :["%sanaPlots_225/outT2cc_160_anaPlots.root"%inDir, 100.],
            "T2cc_300"                  :["%sanaPlots_225/outT2cc_300_anaPlots.root"%inDir, 100.],
            "T2cc_220_145"              :["%sanaPlots_225/outT2cc_220_145_anaPlots.root"%inDir, 100.],
            "T2cc_220_170"              :["%sanaPlots_225/outT2cc_220_170_anaPlots.root"%inDir, 100.],
            "T2cc_220_195"              :["%sanaPlots_225/outT2cc_220_195_anaPlots.root"%inDir, 100.],
            "T2cc_200"                  :["%sanaPlots_225/outT2cc_200_anaPlots.root"%inDir, 100.],
            "T2cc_NF_200_120_cut"       :["%sanaPlots_225/outT2cc_Scan_NoFilter_200_120_cut_anaPlots.root"%inDir, 100.],
            "T2cc_NF_200_190_cut"       :["%sanaPlots_225/outT2cc_Scan_NoFilter_200_190_cut_anaPlots.root"%inDir, 100.],
            "T2cc_160_alphaT0p6"        :["%sanaPlots_225/outT2cc_160_anaPlots_alphaT0p6.root"%inDir, 100.],
            "T2cc_300_alphaT0p6"        :["%sanaPlots_225/outT2cc_300_anaPlots_alphaT0p6.root"%inDir, 100.],
            "T2cc_220_145_alphaT0p6"    :["%sanaPlots_225/outT2cc_220_145_anaPlots_alphaT0p6.root"%inDir, 100.],
            "T2cc_220_170_alphaT0p6"    :["%sanaPlots_225/outT2cc_220_170_anaPlots_alphaT0p6.root"%inDir, 100.],
            "T2cc_220_195_alphaT0p6"    :["%sanaPlots_225/outT2cc_220_195_anaPlots_alphaT0p6.root"%inDir, 100.],
            "T2cc_200_alphaT0p6"        :["%sanaPlots_225/outT2cc_200_anaPlots_alphaT0p6.root"%inDir, 100.],         
            "T2cc_160_flat50"           :["%sanaPlots_new/outT2cc_160_flat50_anaPlots.root"%inDir, 100.],
            "T2cc_300_flat50"           :["%sanaPlots_new/outT2cc_300_flat50_anaPlots.root"%inDir, 100.],
            "T2cc_220_145_flat50"       :["%sanaPlots_new/outT2cc_220_145_flat50_anaPlots.root"%inDir, 100.],
            "T2cc_220_170_flat50"       :["%sanaPlots_new/outT2cc_220_170_flat50_anaPlots.root"%inDir, 100.],
            "T2cc_220_195_flat50"       :["%sanaPlots_new/outT2cc_220_195_flat50_anaPlots.root"%inDir, 100.],
            "T2cc_160_flat50_up10"      :["%sanaPlots_new/outT2cc_160_flat50_up10_anaPlots.root"%inDir, 100.],
            "T2cc_300_flat50_up10"      :["%sanaPlots_new/outT2cc_300_flat50_up10_anaPlots.root"%inDir, 100.],
            "T2cc_220_145_flat50_up10"  :["%sanaPlots_new/outT2cc_220_145_flat50_up10_anaPlots.root"%inDir, 100.],
            "T2cc_220_170_flat50_up10"  :["%sanaPlots_new/outT2cc_220_170_flat50_up10_anaPlots.root"%inDir, 100.],
            "T2cc_220_195_flat50_up10"  :["%sanaPlots_new/outT2cc_220_195_flat50_up10_anaPlots.root"%inDir, 100.],
            "T2cc_160_flat50_up5"       :["%sanaPlots_new/outT2cc_160_flat50_up5_anaPlots.root"%inDir, 100.],
            "T2cc_300_flat50_up5"       :["%sanaPlots_new/outT2cc_300_flat50_up5_anaPlots.root"%inDir, 100.],
            "T2cc_220_145_flat50_up5"   :["%sanaPlots_new/outT2cc_220_145_flat50_up5_anaPlots.root"%inDir, 100.],
            "T2cc_220_170_flat50_up5"   :["%sanaPlots_new/outT2cc_220_170_flat50_up5_anaPlots.root"%inDir, 100.],
            "T2cc_220_195_flat50_up5"   :["%sanaPlots_new/outT2cc_220_195_flat50_up5_anaPlots.root"%inDir, 100.],
            "T2cc_160_flat50_down10"    :["%sanaPlots_new/outT2cc_160_flat50_down10_anaPlots.root"%inDir, 100.],
            "T2cc_300_flat50_down10"    :["%sanaPlots_new/outT2cc_300_flat50_down10_anaPlots.root"%inDir, 100.],
            "T2cc_220_145_flat50_down10":["%sanaPlots_new/outT2cc_220_145_flat50_down10_anaPlots.root"%inDir, 100.],
            "T2cc_220_170_flat50_down10":["%sanaPlots_new/outT2cc_220_170_flat50_down10_anaPlots.root"%inDir, 100.],
            "T2cc_220_195_flat50_down10":["%sanaPlots_new/outT2cc_220_195_flat50_down10_anaPlots.root"%inDir, 100.],
            "T2cc_160_flat50_down5"     :["%sanaPlots_new/outT2cc_160_flat50_down5_anaPlots.root"%inDir, 100.],
            "T2cc_300_flat50_down5"     :["%sanaPlots_new/outT2cc_300_flat50_down5_anaPlots.root"%inDir, 100.],
            "T2cc_220_145_flat50_down5" :["%sanaPlots_new/outT2cc_220_145_flat50_down5_anaPlots.root"%inDir, 100.],
            "T2cc_220_170_flat50_down5" :["%sanaPlots_new/outT2cc_220_170_flat50_down5_anaPlots.root"%inDir, 100.],
            "T2cc_220_195_flat50_down5" :["%sanaPlots_new/outT2cc_220_195_flat50_down5_anaPlots.root"%inDir, 100.],
            "T2cc_160_JES_up10"         :["%sanaPlots_new/outT2cc_160_JES_up10_anaPlots.root"%inDir, 100.],
            "T2cc_300_JES_up10"         :["%sanaPlots_new/outT2cc_300_JES_up10_anaPlots.root"%inDir, 100.],
            "T2cc_220_145_JES_up10"     :["%sanaPlots_new/outT2cc_220_145_JES_up10_anaPlots.root"%inDir, 100.],
            "T2cc_220_170_JES_up10"     :["%sanaPlots_new/outT2cc_220_170_JES_up10_anaPlots.root"%inDir, 100.],
            "T2cc_220_195_JES_up10"     :["%sanaPlots_new/outT2cc_220_195_JES_up10_anaPlots.root"%inDir, 100.],
            "T2cc_160_JES_up5"          :["%sanaPlots_new/outT2cc_160_JES_up5_anaPlots.root"%inDir, 100.],
            "T2cc_300_JES_up5"          :["%sanaPlots_new/outT2cc_300_JES_up5_anaPlots.root"%inDir, 100.],
            "T2cc_220_145_JES_up5"      :["%sanaPlots_new/outT2cc_220_145_JES_up5_anaPlots.root"%inDir, 100.],
            "T2cc_220_170_JES_up5"      :["%sanaPlots_new/outT2cc_220_170_JES_up5_anaPlots.root"%inDir, 100.],
            "T2cc_220_195_JES_up5"      :["%sanaPlots_new/outT2cc_220_195_JES_up5_anaPlots.root"%inDir, 100.],
            "T2cc_160_JES_down10"       :["%sanaPlots_new/outT2cc_160_JES_down10_anaPlots.root"%inDir, 100.],
            "T2cc_300_JES_down10"       :["%sanaPlots_new/outT2cc_300_JES_down10_anaPlots.root"%inDir, 100.],
            "T2cc_220_145_JES_down10"   :["%sanaPlots_new/outT2cc_220_145_JES_down10_anaPlots.root"%inDir, 100.],
            "T2cc_220_170_JES_down10"   :["%sanaPlots_new/outT2cc_220_170_JES_down10_anaPlots.root"%inDir, 100.],
            "T2cc_220_195_JES_down10"   :["%sanaPlots_new/outT2cc_220_195_JES_down10_anaPlots.root"%inDir, 100.],
            "T2cc_160_JES_down5"        :["%sanaPlots_new/outT2cc_160_JES_down5_anaPlots.root"%inDir, 100.],
            "T2cc_300_JES_down5"        :["%sanaPlots_new/outT2cc_300_JES_down5_anaPlots.root"%inDir, 100.],
            "T2cc_220_145_JES_down5"    :["%sanaPlots_new/outT2cc_220_145_JES_down5_anaPlots.root"%inDir, 100.],
            "T2cc_220_170_JES_down5"    :["%sanaPlots_new/outT2cc_220_170_JES_down5_anaPlots.root"%inDir, 100.],
            "T2cc_220_195_JES_down5"    :["%sanaPlots_new/outT2cc_220_195_JES_down5_anaPlots.root"%inDir, 100.],
            "T2cc_160_ISRRW"            :["%sanaPlots_new/outT2cc_160_ISRRW_anaPlots.root"%inDir, 100.],
            "T2cc_300_ISRRW"            :["%sanaPlots_new/outT2cc_300_ISRRW_anaPlots.root"%inDir, 100.],
            "T2cc_220_145_ISRRW"        :["%sanaPlots_new/outT2cc_220_145_ISRRW_anaPlots.root"%inDir, 100.],
            "T2cc_220_170_ISRRW"        :["%sanaPlots_new/outT2cc_220_170_ISRRW_anaPlots.root"%inDir, 100.],
            "T2cc_220_195_ISRRW"        :["%sanaPlots_new/outT2cc_220_195_ISRRW_anaPlots.root"%inDir, 100.],
            "T2cc_220_145_noCuts"        :["%sanaPlots_new/outT2cc_220_145_noCuts_anaPlots.root"%inDir, 100.],
            "T2cc_220_170_noCuts"        :["%sanaPlots_new/outT2cc_220_170_noCuts_anaPlots.root"%inDir, 100.],
            "T2cc_220_195_noCuts"        :["%sanaPlots_new/outT2cc_220_195_noCuts_anaPlots.root"%inDir, 100.],               
    }
  elif mode()=="bTagEff":
    sigFile={
          "T2cc_160"                :["%sbTagEff_Study/outT2cc_160_bTagEff.root"%inDir],
          "T2cc_300"                :["%sbTagEff_Study/outT2cc_300_bTagEff.root"%inDir],
          "T2cc_220_195"            :["%sbTagEff_Study/outT2cc_220_195_bTagEff.root"%inDir],
          "T2cc_220_170"            :["%sbTagEff_Study/outT2cc_220_170_bTagEff.root"%inDir],
          "T2cc_220_145"            :["%sbTagEff_Study/outT2cc_220_145_bTagEff.root"%inDir],
          "T2cc_220_195_pt50"       :["%sbTagEff_Study/outT2cc_220_195_pt50_bTagEff.root"%inDir],
          "T2cc_220_170_pt50"       :["%sbTagEff_Study/outT2cc_220_170_pt50_bTagEff.root"%inDir],
          "T2cc_220_145_pt50"       :["%sbTagEff_Study/outT2cc_220_145_pt50_bTagEff.root"%inDir],    
          "T2cc_220_195_JES_down10" :["%sbTagEff_Study/outT2cc_220_195_JES_down10_bTagEff.root"%inDir],
          "T2cc_220_170_JES_down10" :["%sbTagEff_Study/outT2cc_220_170_JES_down10_bTagEff.root"%inDir],
          "T2cc_220_145_JES_down10" :["%sbTagEff_Study/outT2cc_220_145_JES_down10_bTagEff.root"%inDir],    
          "T2cc_220_195_JES_up10"   :["%sbTagEff_Study/outT2cc_220_195_JES_up10_bTagEff.root"%inDir],
          "T2cc_220_170_JES_up10"   :["%sbTagEff_Study/outT2cc_220_170_JES_up10_bTagEff.root"%inDir],
          "T2cc_220_145_JES_up10"   :["%sbTagEff_Study/outT2cc_220_145_JES_up10_bTagEff.root"%inDir],
          "T2cc_220_195_noCuts"     :["%sbTagEff_Study/outT2cc_220_195_noCuts_bTagEff.root"%inDir],
          "T2cc_220_170_noCuts"     :["%sbTagEff_Study/outT2cc_220_170_noCuts_bTagEff.root"%inDir],
          "T2cc_220_145_noCuts"     :["%sbTagEff_Study/outT2cc_220_145_noCuts_bTagEff.root"%inDir],          
    }
  else:
    sigFile={}


  return sigFile

###-------------------------------------------------------------------###

def comparFiles():

  comparFiles = ["T2bb_300", "T2cc_300"]
  comparFiles = ["T2cc_220_195", "T2cc_220_170", "T2cc_220_145"]
  comparFiles = ["T2cc_Scan_Filter", "T2cc_Scan_NoFilter"]
  comparFiles = ["T2cc_200", "T2cc_NF_200_120_cut"]

  return comparFiles

###-------------------------------------------------------------------###

def inDirs():

  HTdirs = ["225_275", "275_325", "325_375", "375_475", "475_575", "575_675", "675_775", "775_875", "875"]

  if switches()["HTcuts"]=="parkedHT":
    HTdirs.insert(0, "225_275")
  
  dirs=[]

  if switches()["HTcuts"]=="noCutInc": dirs = ["noCuts_0_10000"]
  elif switches()["HTcuts"]=="standardHT":
    for d in HTdirs:
      if switches()["jetMulti"]=="le3j": dirs.append("le3j_"+d)
      if switches()["jetMulti"]=="ge4j": dirs.append("ge4j_"+d)
      if switches()["jetMulti"]=="inc":  dirs.append("inc_"+d)
  
  elif switches()["HTcuts"]=="highHT":
    for d in HTdirs[2:]:
      if switches()["jetMulti"]=="le3j": dirs.append("le3j_"+d)
      if switches()["jetMulti"]=="ge4j": dirs.append("ge4j_"+d)
      if switches()["jetMulti"]=="inc":  dirs.append("inc_"+d)
  
  elif switches()["HTcuts"]=="lowHT":
    for d in HTdirs[:2]:
      if switches()["jetMulti"]=="le3j": dirs.append("le3j_"+d)
      if switches()["jetMulti"]=="ge4j": dirs.append("ge4j_"+d)
      if switches()["jetMulti"]=="inc":  dirs.append("inc_"+d)

  return dirs

###-------------------------------------------------------------------###

def bMulti():
  bMulti=[]
  bMultiAll=["inc", "0b", "1b", "2b", "3b", "4b","ge1b","ge2b","ge3b","ge4b"]

  include=[1]

  for val in include:
    bMulti.append(bMultiAll[val])

  return bMulti

###-------------------------------------------------------------------###

def sinHists():
  if mode()=="anaPlots":
    singleHists={
         "stopGenPtScal"       :plotDetails(xRange=[0.,1000.], rebX=4),
         "stopGenPtVect"       :plotDetails(xRange=[0.,600.], rebX=2),
         "delPhi_vs_scalGenPt" :plotDetails(xRange=[0., 900.], yRange=[0., 3.2], rebX=5), 
         "dPhiStopCharm"       :plotDetails(xRange=[0.,3.2], rebX=2),
         "dPhiStopStop"        :plotDetails(xRange=[0.,3.2], rebX=2),
         "dPhiNeutCharm"       :plotDetails(xRange=[0.,3.2], rebX=2),
         "dPhiCharmCharm"      :plotDetails(xRange=[0.,3.2], rebX=2),
         "dPhiStopNeut"        :plotDetails(xRange=[0.,3.2], rebX=2),
         #"n_Events_1"          :plotDetails(),
         "n_Jets"              :plotDetails(xRange=[0.,8.]),
         "n_BTagged_Jets_all"  :plotDetails(xRange=[0.,6.]),
    }
  elif mode()=="bTagEff":
    singleHists={
            #"n_Jets"         :plotDetails(),
          #"n_JetsMatchB"   :plotDetails(),
          #"n_JetsMatchC"   :plotDetails(),
          #"n_JetsMatchL"   :plotDetails(),
          #"jetFlavour_0"   :plotDetails(),
          #"jetFlavour_1"   :plotDetails(),
          #"jetFlavour_2"   :plotDetails(),
          #"jetFlavour_3"   :plotDetails(),
          #"n_Truth_B"      :plotDetails(),
          #"n_Truth_C"      :plotDetails(),
    }
  else:
    singleHists={}
  
  return singleHists

###-------------------------------------------------------------------###

def anaHists():  
  
  if mode()=="anaPlots":
    hists={
      "MET"               :plotDetails(xRange=[0.,900.], rebX=2),
      "MHT"               :plotDetails(xRange=[0.,900.],rebX=2),
      "commHT"            :plotDetails(xRange=[150.,1000.], rebX=2),
      "hadronicAlphaTZoom":plotDetails(xRange=[0., 1.5], rebX=5),
      "leadJetdelPhi"     :plotDetails(xRange=[0.,3.2], rebX=2),
      "MHToverMET"        :plotDetails(xRange=[0.,2.], rebX=1),
      "jetPt"             :plotDetails(xRange=[0.,500.], rebX=2),
      "leadJetPt"         :plotDetails(xRange=[0.,800.], rebX=2),
      "subLeadJetPt"      :plotDetails(xRange=[0.,500.], rebX=2),
      #"alphaT_vs_HT"     :plotDetails(xRange=[0.,1.6], yRange=[0.,600.], rebX=2, rebY=2),
      #"leadTwoJetsPt"     :plotDetails(xRange=[0.,300.], rebX=2),
    }
  elif mode()=="bTagEff":
    hists={}
  else:
    hists={}
  
  return hists

###-------------------------------------------------------------------###

def plotDetails(xRange=None, yRange=None, rebX=1, rebY=1):
  """docString for making plotDetails dict"""
  myDict={}
  myDict["xRange"]=xRange
  myDict["yRange"]=yRange
  myDict["rebinX"] =rebX
  myDict["rebinY"] =rebY

  return myDict

###-------------------------------------------------------------------###

def getXSecNorm(mStop=None):

  prodXSec = {
        160:58.01,
        220:11.18,
        300:1.996,
        600:0.02480,
  }

  stopXSec = prodXSec[mStop]

  if switches()["norm"]=="xSec":
    #normFact=prodXSec[mStop]*switches()["xSecNorm"]*1000.
    normFact=1.
    print "\nERROR: Normalisation by xSec feature not yet enabled/written at all. My bad.\n"
    exit()
  elif switches()["norm"]=="lumi":
    targLumi = switches()["lumiNorm"]
    normFact=targLumi/(100000./stopXSec)
    print normFact

  return normFact

###-------------------------------------------------------------------###

def getXSec():

  sigSamp = switches()["signalSample"]

  prodXSec = {
        160:58.01,
        220:11.18,
        300:1.996,
        600:0.02480,
  }

  if "T2cc_160" in sigSamp:
    sigXSec = prodXSec[160]
  elif "T2cc_220_" in sigSamp:
    sigXSec = prodXSec[220]
  elif "T2cc_300" in sigSamp:
    sigXSec = prodXSec[300]
  elif "T2cc_600" in sigSamp:
    sigXSec = prodXSec[600]
  else:
    print "> ERROR: Could not get signal xSec value."
    print ">>> This could be a sample naming issue."
    sys.exit()

  print "> Setting signal xSec to %.2fpb\n"%sigXSec

  return sigXSec







