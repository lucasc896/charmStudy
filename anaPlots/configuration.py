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
  
  anaMode = ["bTagEff", "anaPlots", "isoTrackPlots","dev"][1]

  return anaMode

###-------------------------------------------------------------------###

def switches():

  switches={
          "runMode"       :["plotting", "yieldTables"][0],
          "plotMode"      :["anaPlots","standardPlots","comparisonPlots"][2],
          "runModeBTag"   :["charmFrac", "standardPlots", "charmPhi"][0],
          "signalSample"  :"TTbar_isoTrack",
          "HTcuts"        :["noCutInc", "standardHT","highHT","lowHT","parkedHT"][3],
          "jetMulti"      :["le3j","ge4j","inc","after","before"][-1],
          "printLogy"     :[False, True][1],
          "norm"          :["None", "Unitary", "xSec", "lumi"][1],
          "lumiNorm"      :[1, 10, 11.7][2],
          "hiRes"         :[False, True][1], #Warning: Slow for png!
          "outFormat"     :["png", "pdf"][1], #PDF for combinations
          "BGcomp"        :[False, True][1], #option to decompose BG in tables - requires isoTrackPlots file
          }

  return switches

###-------------------------------------------------------------------###

def bMulti():
  bMulti = []
  bMultiAll = ["inc", "0b", "1b", "2b", "3b", "4b","ge1b","ge2b","ge3b","ge4b"]

  include = [0]

  for val in include:
    bMulti.append(bMultiAll[val])

  return bMulti

###-------------------------------------------------------------------###


def comparFiles():

  comparFiles = ["ZJets_Muon", "WJets_Muon"]

  return comparFiles

###-------------------------------------------------------------------###

def bgFile():
  """syntax is "Name":["path", scale]"""

  mcScale = switches()["lumiNorm"]*10. # corresponding to intL for had sample

  inDir = "/Users/chrislucas/SUSY/charmStudy/ANALYSIS/rootfiles/"

  if mode()=="anaPlots":
    files = {
          "WJets"     :["%sanaPlots_v3/outWJets_anaPlots.root"%inDir, mcScale],
          "ZJets"     :["%sanaPlots_v3/outZJets_anaPlots.root"%inDir, mcScale],
          "QCD"      :["%sanaPlots_v3/outQCD_anaPlots.root"%inDir, mcScale],
          "SingleTop" :["%sanaPlots_v3/outSinTop_anaPlots.root"%inDir, mcScale],
          "TTJets"    :["%sanaPlots_v3/outTTbar_anaPlots.root"%inDir, mcScale],
          "DiBoson"   :["%sanaPlots_v3/outDiBoson_anaPlots.root"%inDir, mcScale],
          }

  return files

###-------------------------------------------------------------------###

def sigFile():
  inDir = "/Users/chrislucas/SUSY/charmStudy/ANALYSIS/rootfiles/"

  if mode()=="anaPlots":
    sigFile = {
            "T2cc_mSt200_dev"           :["%sdev/outT2cc_anaPlots.root"%inDir, 100.],
            "T2cc"                      :["%sanaPlots_v3/outT2cc_anaPlots.root"%inDir, 100.],
            "T2cc_mSt200_mL120"         :["%sanaPlots_v3/outT2cc_200_120_anaPlots_v3.root"%inDir, 100.],
            "T2cc_mSt200_mL190"         :["%sanaPlots_v3/outT2cc_200_190_anaPlots_v3.root"%inDir, 100.],
            "T2cc_3jet_mSt200_mL120"    :["%sanaPlots_v3/outT2cc_3jet_200_120_anaPlots_v3.root"%inDir, 100.],
            "T2cc_3jet_mSt200_mL190"    :["%sanaPlots_v3/outT2cc_3jet_200_190_anaPlots_v3.root"%inDir, 100.],
            "T2cc_aT0p6"                :["%sanaPlots_225/outT2cc_aT0p6_anaPlots.root"%inDir, 100.],
            "T2cc_ISRRW"                :["%sanaPlots_v3/outT2cc_ISRRW13_anaPlots.root"%inDir, 100.],
            "T2cc_ISRRW_delta10"        :["%sanaPlots_225/outT2cc_ISRRW13_delta10_anaPlots.root"%inDir, 100.],
            "T2cc_ISRRW_delta20"        :["%sanaPlots_225/outT2cc_ISRRW13_delta20_anaPlots.root"%inDir, 100.],
            "T2cc_ISRRW_delta30"        :["%sanaPlots_225/outT2cc_ISRRW13_delta30_anaPlots.root"%inDir, 100.],
            "T2cc_ISRRW_delta40"        :["%sanaPlots_225/outT2cc_ISRRW13_delta40_anaPlots.root"%inDir, 100.],
            "T2cc_ISRRW_delta60"        :["%sanaPlots_225/outT2cc_ISRRW13_delta60_anaPlots.root"%inDir, 100.],
            "T2cc_ISRRW_delta80"        :["%sanaPlots_225/outT2cc_ISRRW13_delta80_anaPlots.root"%inDir, 100.],
            "T2cc_ISRRW_mSt100_mL20"    :["%sanaPlots_225/outT2cc_ISRRW13_100_20_anaPlots.root"%inDir, 100.],
            "T2cc_ISRRW_mSt100_mL40"    :["%sanaPlots_225/outT2cc_ISRRW13_100_40_anaPlots.root"%inDir, 100.],
            "T2cc_ISRRW_mSt100_mL60"    :["%sanaPlots_225/outT2cc_ISRRW13_100_60_anaPlots.root"%inDir, 100.],
            "T2cc_ISRRW_mSt100_mL70"    :["%sanaPlots_225/outT2cc_ISRRW13_100_70_anaPlots.root"%inDir, 100.],
            "T2cc_ISRRW_mSt100_mL80"    :["%sanaPlots_225/outT2cc_ISRRW13_100_80_anaPlots.root"%inDir, 100.],
            "T2cc_ISRRW_mSt100_mL90"    :["%sanaPlots_225/outT2cc_ISRRW13_100_90_anaPlots.root"%inDir, 100.],
            "T2cc_ISRRW_mSt175_mL95"    :["%sanaPlots_v3/outT2cc_ISRRW13_175_95_anaPlots.root"%inDir, 100.],
            "T2cc_ISRRW_mSt175_mL135"   :["%sanaPlots_225/outT2cc_ISRRW13_175_135_anaPlots.root"%inDir, 100.],
            "T2cc_ISRRW_mSt175_mL165"   :["%sanaPlots_225/outT2cc_ISRRW13_175_165_anaPlots.root"%inDir, 100.],            
            "T2cc_ISRRW_mSt100"         :["%sanaPlots_225/outT2cc_ISRRW13_Stop100_anaPlots.root"%inDir, 100.],
            "T2cc_ISRRW_mSt175"         :["%sanaPlots_225/outT2cc_ISRRW13_Stop175_anaPlots.root"%inDir, 100.],
            "T2cc_ISRRW_mSt250"         :["%sanaPlots_225/outT2cc_ISRRW13_Stop250_anaPlots.root"%inDir, 100.],
            "T2cc_ISRRW_mSt100_Vect100" :["%sanaPlots_225/outT2cc_ISRRW13_Stop100_Vect100_anaPlots.root"%inDir, 100.],
            "T2cc_ISRRW_mSt175_Vect100" :["%sanaPlots_225/outT2cc_ISRRW13_Stop175_Vect100_anaPlots.root"%inDir, 100.],
            "T2cc_ISRRW_mSt250_Vect100" :["%sanaPlots_225/outT2cc_ISRRW13_Stop250_Vect100_anaPlots.root"%inDir, 100.],
            "T1ttcc"                    :["%sanaPlots_v3/outT1ttcc_300_anaPlots.root"%inDir, 100.],
            "HT_2012_PSRW"              :["%sanaPlots_v3/outHT_2012_PSRW_anaPlots.root"%inDir, 100.],
            "HT_2012"                   :["%sanaPlots_v3/outHT_2012_anaPlots.root"%inDir, 100.],
            "HT_Parked"                 :["%sanaPlots_v3/outParkedHT_OliverThresh_anaPlots.root"%inDir, 100.],
            "WJets_Muon"                :["%sanaPlots_v3/outWJets_MuonSele_anaPlots.root"%inDir, 100.],
            "ZJets_Muon"                :["%sanaPlots_v3/outZJets_MuonSele_anaPlots.root"%inDir, 100.],
            "TEST"       :["%sanaPlots_v3/outTEST.root"%inDir, 100.],

    }
  elif mode()=="bTagEff":
    sigFile={
          "T2cc_ISRRW"          :["%sbTagEff_v2/outT2cc_ISRRW13_bTagEff.root"%inDir],
          "T2cc_ISRRW_175_95"   :["%sbTagEff_v2/outT2cc_ISRRW13_175_95_bTagEff.root"%inDir],
          "T2cc_ISRRW_175_165"  :["%sbTagEff_v2/outT2cc_ISRRW13_175_165_bTagEff.root"%inDir],
          "T2cc_ISRRW_175_145"  :["%sbTagEff_v2/outT2cc_ISRRW13_175_145_bTagEff.root"%inDir],
    } 
  elif mode()=="isoTrackPlots":
    sigFile={
          "TTbar_isoTrack"            :["%sisoTrackPlots/outTTbar_isoTrackPlots.root"%inDir, 100.],
          "TTbar_FullLept_isoTrack"   :["%sisoTrackPlots/outTTbar_FullLept_isoTrackPlots.root"%inDir, 100.],
          "WJets_isoTrack"            :["%sisoTrackPlots/outWJets_isoTrackPlots.root"%inDir, 100.],
          "ZJets_isoTrack"            :["%sisoTrackPlots/outZJets_isoTrackPlots.root"%inDir, 100.],
          "T2tt_isoTrack"             :["%sisoTrackPlots/outT2tt_isoTrackPlots.root"%inDir, 100.],
          "T2cc_isoTrack"             :["%sisoTrackPlots/outT2cc_isoTrackPlots.root"%inDir, 100.],
          "T1tttt_isoTrack"           :["%sisoTrackPlots/outT1tttt_isoTrackPlots.root"%inDir, 100.],
          "T2cc_175_165_isoTrack"     :["%sanaPlots_v3/outT2cc_175_165_isoTrackTest_anaPlots.root"%inDir, 100.],
          "T2cc_175_95_isoTrack"      :["%sanaPlots_v3/outT2cc_175_95_isoTrackTest_anaPlots.root"%inDir, 100.],
    }

  else:
    sigFile={}


  return sigFile

###-------------------------------------------------------------------###

def inDirs():

  HTdirs = ["200_275", "275_325", "325_375", "375_475", "475_575", "575_675", "675_775", "775_875", "875_975", "975"]

  if switches()["HTcuts"]=="parkedHT":
    HTdirs.insert(0, "200_275")
  
  dirs=[]
  iterList=[]

  if switches()["jetMulti"]=="le3j":    pre = "le3j_"
  if switches()["jetMulti"]=="ge4j":    pre = "ge4j_"
  if switches()["jetMulti"]=="inc":     pre = "inc_"
  if switches()["jetMulti"]=="before":  pre = "before"
  if switches()["jetMulti"]=="after":   pre = "after"  


  if switches()["HTcuts"]=="noCutInc": dirs = ["noCuts_0_10000"]
  elif switches()["HTcuts"]=="standardHT" or switches()["HTcuts"]=="parkedHT":
    iterList = HTdirs
  elif switches()["HTcuts"]=="highHT":
    iterList = HTdirs[3:]
  elif switches()["HTcuts"]=="lowHT":
    iterList = HTdirs[:2]

  for i in iterList:
    dirs.append(pre+i)

  return dirs

###-------------------------------------------------------------------###

def sinHists():
  if mode()=="anaPlots":
    singleHists={
        "n_Events_1"           :plotDetails(),
        # "n_Jets"               :plotDetails(xRange=[0.,8.]),
        # "n_evWeight"         :plotDetails(xRange=[0.,10.]), 
        # "n_Jets_charm"               :plotDetails(xRange=[0.,8.]),
        # "n_Jets_ISR"               :plotDetails(xRange=[0.,8.]),
        # "n_BTagged_Jets_all"   :plotDetails(xRange=[0.,6.]),
        # "tmpDR"           :plotDetails(rebX=10),
        # "matchPtDiff"     :plotDetails(rebX=10),
    }
  elif mode()=="bTagEff":
    singleHists={
            "n_Jets"         :plotDetails(),
            # "n_JetsMatchB"   :plotDetails(),
            # "n_JetsMatchC"   :plotDetails(),
            # "n_JetsMatchL"   :plotDetails(),
            # "jetFlavour_0"   :plotDetails(),
            # "jetFlavour_1"   :plotDetails(),
            # "jetFlavour_2"   :plotDetails(),
            # "jetFlavour_3"   :plotDetails(),
            # "n_Truth_B"      :plotDetails(),
            # "n_Truth_C"      :plotDetails(),
    }
  else:
    singleHists={}
  
  return singleHists

###-------------------------------------------------------------------###

def anaHists():  
  
  if mode()=="anaPlots":
    hists={
      # "MET"                   :plotDetails(xRange=[0.,900.], rebX=2),
      # "MHT"                   :plotDetails(xRange=[0.,900.],rebX=2),
      "commHT"                :plotDetails(xRange=[275.,1500.], rebX=1),
      "genPartonHT"           :plotDetails(xRange=[275.,1200.], rebX=1),
      # # "HT_charm"                :plotDetails(xRange=[0.,1000.], rebX=2),
      # # "HT_ISR"                :plotDetails(xRange=[0.,1000.], rebX=2),
      # "hadronicAlphaTZoom"    :plotDetails(xRange=[0.3, 1.5], rebX=2),
      # "leadJetdelPhi"        :plotDetails(xRange=[0.,3.2], rebX=2),
      # "MHToverMET"            :plotDetails(xRange=[0.,2.], rebX=1),
      # # "MHToverHT"            :plotDetails(xRange=[0.,2.], rebX=1),
      # "jetPt"                 :plotDetails(xRange=[0.,800.], rebX=1),
      # "leadJetPt"             :plotDetails(xRange=[0.,800.], rebX=1),
      # "subLeadJetPt"          :plotDetails(xRange=[0.,800.], rebX=1),
      # "thirdJetPt"            :plotDetails(xRange=[0., 300.], rebX=1),
      # "leadISRJetPt"            :plotDetails(xRange=[0., 300.], rebX=1),
      # "subLeadISRJetPt"            :plotDetails(xRange=[0., 300.], rebX=1),
      # "fourthJetPt"           :plotDetails(xRange=[0., 200.], rebX=1),
      # "fivePlusJetPt"           :plotDetails(xRange=[0., 200.], rebX=1),
      # "alphaT_vs_HT"          :plotDetails(xRange=[175.,875.], yRange=[.5,.8], rebX=1, rebY=1),
      # "leadTwoJetsPt"         :plotDetails(xRange=[0.,800.], rebX=2),
      # "stopGenPtScal"         :plotDetails(xRange=[0.,1000.], rebX=2),
      # "stopGenPtVect"         :plotDetails(xRange=[0.,600.], rebX=2),
      # "delPhi_vs_scalGenPt"   :plotDetails(xRange=[0., 900.], yRange=[0., 3.2], rebX=5), 
      # "dPhiStopCharm"         :plotDetails(xRange=[0.,3.2], rebX=1),
      # "dPhiStopStop"          :plotDetails(xRange=[0.,3.2], rebX=1),
      # "dPhiNeutCharm"         :plotDetails(xRange=[0.,3.2], rebX=1),
      # "dPhiCharmCharm"        :plotDetails(xRange=[0.,3.2], rebX=1),
      # "dPhiStopNeut"          :plotDetails(xRange=[0.,3.2], rebX=2),
      # "dPhiLeadJetMHT"        :plotDetails(xRange=[0.,3.2], rebX=1),
      # "leadJetdelPhi"         :plotDetails(xRange=[0.,3.2], rebX=1),
      # "dPhiSubLeadJetMHT"        :plotDetails(xRange=[0.,3.2], rebX=1),
      # "charmJetPt_0"          :plotDetails(xRange=[0., 350.], rebX=1),
      # "charmJetPt_1"          :plotDetails(xRange=[0., 350.], rebX=1),
    }
  if mode()=="isoTrackPlots":
    hists = {
      "nIsoTrack"       :plotDetails(),
      "ITGenEleN"       :plotDetails(),    
      "ITGenElePt"      :plotDetails(),
      "ITGenEleEta"     :plotDetails(),
      "ITGenMuN"        :plotDetails(),
      "ITGenMuPt"       :plotDetails(),
      "ITGenMuEta"      :plotDetails(),
      "ITGenHadTauN"        :plotDetails(),
      "ITGenHadTauPt"       :plotDetails(),
      "ITGenHadTauEta"      :plotDetails(),
      "ITGenOtherN"        :plotDetails(),
      "ITGenOtherPt"       :plotDetails(),
      "ITGenOtherEta"      :plotDetails(),
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







# 
