#!/usr/bin/env python
"""
Created by Bryn Mathias on 2010-05-07.
Modified by Chris Lucas on 2012-10-24
"""
# -----------------------------------------------------------------------------
# Necessary includes
import errno
import os
import re
import setupSUSY
from libFrameworkSUSY import *
from libHadronic import *
from libWPol import *
from libOneLepton import *
from lib_charmStudy import *
from icf.core import PSet,Analysis
from time import strftime
from icf.config import defaultConfig
from icf.utils import json_to_pset
from copy import deepcopy
# -----------------------------------------------------------------------------
# Samples
#import yours in your running script
def ensure_dir(path):
    try:
      os.makedirs(path)
    except OSError as exc: # Python >2.5
      if exc.errno == errno.EEXIST:
        pass
      else: raise

# -----------------------------------------------------------------------------


def runMode():
  return ["OP_analysisPlots", "OP_charmEffStudy", "OP_isoTrackPlots"][2]


# -----------------------------------------------------------------------------
# Reading the collections from the ntuple

default_ntuple = deepcopy(defaultConfig.Ntuple)
default_ntuple.Electrons=PSet(
Prefix="electron",
Suffix="Pat",
LooseID="EIDLoose",
TightID="EIDTight",
)
default_ntuple.Muons=PSet(
Prefix="muon",
Suffix="Pat",
LooseID="IsGlobalMuon",
TightID="IDGlobalMuonPromptTight",
)
default_ntuple.SecMuons=PSet(
    Prefix="muon",
    Suffix="PF")

# default_ntuple.Taus=PSet(
# Prefix="tau",
# Suffix="Pat",
# LooseID="TauIdbyTaNCfrOnePercent",
# TightID="TauIdbyTaNCfrTenthPercent"
# )
default_ntuple.Jets=PSet(
Prefix="ic5Jet",
Suffix="Pat",
Uncorrected=False,
)
default_ntuple.Photons=PSet(
Prefix="photon",
Suffix="Pat",
)

ak5_calo = deepcopy(default_ntuple)
ak5_calo.Jets.Prefix="ak5Jet"

ak5_pf = deepcopy(default_ntuple)
ak5_pf.Jets.Prefix="ak5JetPF"
ak5_pf.TerJets.Prefix="ak5Jet"

# -----------------------------------------------------------------------------
# Cross-cleaning settings

default_cc = deepcopy(defaultConfig.XCleaning)
default_cc.Verbose=False
default_cc.MuonJet=True
default_cc.ElectronJet=True
default_cc.PhotonJet=True
default_cc.ResolveConflicts=True
default_cc.Jets.PtCut=10.0
default_cc.Jets.EtaCut=10.0
default_cc.Muons.PtCut=10.0
default_cc.Muons.EtaCut=2.5
default_cc.Muons.MuonJetDeltaR=0.5
default_cc.Electrons.PtCut=10.0
default_cc.Electrons.EtaCut=2.5
default_cc.Electrons.ElectronJetDeltaR=0.5
default_cc.Photons.EtCut=25.0
default_cc.Photons.EtaCut=5.0
default_cc.Photons.IDReq=3
default_cc.Photons.UseID=True
default_cc.Photons.PhotonJetDeltaR=0.5
# -----------------------------------------------------------------------------
# Definition of common objects
default_common = deepcopy(defaultConfig.Common)
default_common.ApplyXCleaning=True
default_common.Jets.PtCut=50.0
default_common.Jets.EtaCut=3.0
default_common.Jets.ApplyID=True
default_common.Jets.TightID=False
default_common.Electrons.PtCut=10.0
default_common.Electrons.EtaCut=2.5
default_common.Electrons.ApplyID = True
default_common.Electrons.TightID = False
default_common.Electrons.RequireLooseForOdd = True
default_common.Muons.PtCut=10.0
default_common.Muons.EtaCut=2.5
default_common.Muons.ApplyID = True
default_common.Muons.TightID = False
default_common.Muons.RequireLooseForOdd = True
default_common.Photons.EtCut=25.0
default_common.Photons.EtaCut=2.5
default_common.Photons.UseID=True
default_common.Photons.IDReq = 3
default_common.Photons.RequireLooseForOdd = True
default_common.Btag.Corrections = "2013"
default_common.Btag.RA1_matching = False
default_common.SMS.Model = True

skim_ps=PSet(
    SkimName = "myskim",
    DropBranches = False,
    Branches = [
        " keep * "
        ]
)
skim = SkimOp(skim_ps.ps())


#Plot the common plots!

genericPSet_mc = PSet(
DirName       = "275_325Gev",
MinObjects    = 2,
MaxObjects    = 15,
isData        = False,
BTagAlgo      = 5,
BTagAlgoCut   = 0.679,
StandardPlots = True,
minDR         = 0.5,
threshold     = 50.,
NoCutsMode    = False,
Debug         = False,
)

genericPSet_data = PSet(
DirName       = "175_225Gev",
MinObjects    = 2,
MaxObjects    = 15,
isData        = True,
BTagAlgo      = 5,
BTagAlgoCut   = 0.679,
StandardPlots = True,
minDR         = 0.5,
threshold     = 50.,
NoCutsMode    = False,
Debug         = False,
)


def makePlotOp(OP = (), cutTree = None, cut = None, label = ""):
  """docstring for makePlotOp"""
  out = []
  if OP[1] != None:
    plotpset = deepcopy(OP[1])
    plotpset.DirName = label
    if "noCut" in label:
      plotpset.NoCutsMode = True
    else:
      plotpset.NoCutsMode = False
    op = eval(OP[0]+"(plotpset.ps())")
  else:
    op = eval(OP[0])
  out.append(op)
  cutTree.TAttach(cut, op)
  return out
  pass

def AddBinedHist(cutTree = None, OP = (), cut = None, htBins = [],TriggerDict = None,lab = "", Muon=None):
  """docstring for AddBinedHist"""
  out = []

  if TriggerDict is not None:
    ## DATA
      for lower,upper in zip(htBins,htBins[1:]+[None]):
        if int(lower) == 275 and upper is None: continue
        if int(lower) == 325 and upper is None: continue
        if int(lower) == 375 and upper is None : continue
        if int(lower) == 675 and upper is None : continue
        # print "continue should have happened now"
        lowerCutVal=""
        if Muon!=None:
            lowerCutVal=("RECO_CommonHTTakeMuCut(%d)"%lower)
        else:
            lowerCutVal=("RECO_CommonHTCut(%d)"%lower)
        lowerCut = eval(lowerCutVal)
        
        # flips a bool in framework/.../CommonOps.cc to allow preScale > 1
        if TriggerDict == ht_triggers:
          useprescale = True
        else:
          useprescale = False

        triggerps = PSet(Verbose = False,
                      UsePreScaledTriggers = useprescale,
                      Triggers = [])

        triggerps.Triggers = TriggerDict["%d%s"%(lower, "_%d"%upper if upper else "")]
        Trigger = OP_MultiTrigger( triggerps.ps() )
        
        out.append(triggerps)
        out.append(Trigger)
        out.append(lowerCut)
        
        cutTree.TAttach(cut,lowerCut)

        if upper:
          upperCutVal=""
          if Muon!=None:
            upperCutVal=("RECO_CommonHTTakeMuLessThanCut(%d)"%upper)
          else:
            upperCutVal=("RECO_CommonHTLessThanCut(%d)"%upper)
          upperCut = eval(upperCutVal)
          out.append(upperCut)
          cutTree.TAttach(lowerCut,upperCut)
          cutTree.TAttach(upperCut,Trigger)

        if not upper:
          cutTree.TAttach(lowerCut,Trigger)

        pOps = makePlotOp(cutTree = cutTree, OP = OP, cut = Trigger, label = "%s%d%s"%(lab,lower, "_%d"%upper if upper else ""))
        out.append(pOps)
  else:
    ## MC
      for lower,upper in zip(htBins,htBins[1:]+[None]):
        # print lower, upper
        if int(lower) == 275 and upper is None: continue
        if int(lower) == 325 and upper is None: continue
        if int(lower) == 375 and upper is None: continue
        if int(lower) == 675 and upper is None : continue
        # print "  ", lower, upper
        lowerCutVal=""
        if Muon!=None:
            lowerCutVal=("RECO_CommonHTTakeMuCut(%d)"%lower)
        else:
            lowerCutVal=("RECO_CommonHTCut(%d)"%lower)
        lowerCut = eval(lowerCutVal)
        out.append(lowerCut)

        if lower == 200.:
          newAlphaT = OP_HadAlphaTCut(0.6)
          out.append(newAlphaT)
          cutTree.TAttach(cut, newAlphaT)
          cutTree.TAttach(newAlphaT, lowerCut)
        else:
          cutTree.TAttach(cut,lowerCut)
        if upper:
          upperCutVal=""
          if Muon!=None:
            upperCutVal=("RECO_CommonHTTakeMuLessThanCut(%d)"%upper)
          else:
            upperCutVal=("RECO_CommonHTLessThanCut(%d)"%upper)
          upperCut = eval(upperCutVal)
          out.append(upperCut)
          cutTree.TAttach(lowerCut,upperCut)
          pOps = makePlotOp(cutTree = cutTree, OP = OP, cut = upperCut if "noCut" not in lab else cut, label = "%s%d%s"%(lab,lower, "_%d"%upper if upper else ""))
        else:
          pOps = makePlotOp(cutTree = cutTree, OP = OP, cut = lowerCut if "noCut" not in lab else cut, label = "%s%d%s"%(lab,lower, "_%d"%upper if upper else ""))
        out.append(pOps)
  return out
  pass



# Common cut definitions

NoiseFilt= OP_HadronicHBHEnoiseFilter()
GoodVertexMonster = OP_GoodEventSelection()

#Standard Event Selection
LeadingJetEtaValue=2.5
LeadingJetEta = OP_FirstJetEta(LeadingJetEtaValue)

oddMuon = OP_OddMuon()
oddElectron = OP_OddElectron()
oddPhoton = OP_OddPhoton()
oddJet = OP_OddJet()
badMuonInJet = OP_BadMuonInJet()
numComElectrons = OP_NumComElectrons("<=",0)
numComPhotons = OP_NumComPhotons("<=",0)
ZeroMuon = OP_NumComMuons("<=",0)

ht150trigger = 150.
ht150_Trigger = RECO_CommonHTCut(ht150trigger)
htTakeMu200_Trigger = RECO_CommonHTTakeMuCut(ht150trigger)

ht250trigger = 250.
ht250_Trigger = RECO_CommonHTCut(ht250trigger)
htTakeMu250_Trigger = RECO_CommonHTTakeMuCut(ht250trigger)

htCut225 = RECO_CommonHTCut(225.)
htTakeMuCut225 = RECO_CommonHTTakeMuCut(225.)

htCut275 = RECO_CommonHTCut(275.)
htCut175 = RECO_CommonHTCut(175.)
htTakeMuCut275 = RECO_CommonHTTakeMuCut(275.)

DeadEcalCutData = OP_DeadECALCut(0.3,0.3,0.5,30.,10,0,"./deadEcal/deadRegionList_GR10_P_V10.txt")
DeadEcalCutMC =   OP_DeadECALCut(0.3,0.3,0.5,30.,10,0,"./deadEcal/deadRegionList_START38_V12.txt")

MHT_METCut = OP_MHToverMET(1.25,50.)
MHT_METReverseCut = OP_Reverse_MHToverMET(1.25,50.)
MHT_METCutMC = OP_MHToverMET(1.25,50.)

MET_Filter = OP_METFilters_2012()

json = JSONFilter("Json Mask", json_to_pset("./Jsons/Cert_190456-208686_8TeV_PromptReco_Collisions12_JSON.txt") )
recHitCut = OP_SumRecHitPtCut(30.)

jet_e2  = OP_NumComJets("==",2)
jet_e3  = OP_NumComJets("==",3)
jet_e4  = OP_NumComJets("==",4)
jet_g3  = OP_NumComJets(">",3)
jet_g4  = OP_NumComJets(">",4)
jet_ge4 = OP_NumComJets(">",3)
jet_le3 = OP_NumComJets("<",4)
jet_ge2 = OP_NumComJets(">",1)

jet_ge4_mu = OP_NumComJets(">",3)
jet_le3_mu = OP_NumComJets("<",4)


jet_e2_du = OP_NumComJets("==",2)
jet_e3_du = OP_NumComJets("==",3)
jet_e4_du = OP_NumComJets("==",4)
jet_g3_du = OP_NumComJets(">",3)
jet_g4_du = OP_NumComJets(">",4)

VertexPtOverHT = OP_SumVertexPtOverHT(0.1)

ht_triggers = {
    "175_275":["HLT_HT200_v1", "HLT_HT200_v2", "HLT_HT200_v3", "HLT_HT200_v4", "HLT_HT200_v6", ],
    "275_325":["HLT_HT250_v1", "HLT_HT250_v2", "HLT_HT250_v3", "HLT_HT250_v4", "HLT_HT250_v5", "HLT_HT250_v7", ],
    "325_375":["HLT_HT300_v1", "HLT_HT300_v2", "HLT_HT300_v3", "HLT_HT300_v4", "HLT_H300_v5", "HLT_HT300_v7", ],
    "375_475":["HLT_HT350_v1", "HLT_HT350_v2", "HLT_HT350_v3", "HLT_HT350_v4", "HLT_HT350_v5", "HLT_HT350_v7", ],
    "475_575":["HLT_HT450_v1", "HLT_HT450_v2", "HLT_HT450_v3", "HLT_HT450_v4", "HLT_HT450_v5", "HLT_HT450_v7", ],
    "575_675":["HLT_HT450_v1", "HLT_HT450_v2", "HLT_HT450_v3", "HLT_HT450_v4", "HLT_HT450_v5", "HLT_HT450_v7", ],
    "675_775":["HLT_HT450_v1", "HLT_HT450_v2", "HLT_HT450_v3", "HLT_HT450_v4", "HLT_HT450_v5", "HLT_HT450_v7", ],
    "775_875":["HLT_HT450_v1", "HLT_HT450_v2", "HLT_HT450_v3", "HLT_HT450_v4", "HLT_HT450_v5", "HLT_HT450_v7", ],
    "875":["HLT_HT450_v1", "HLT_HT450_v2", "HLT_HT450_v3", "HLT_HT450_v4", "HLT_HT450_v5", "HLT_HT450_v7", ],
}

triggers = {
    # "175_275":["HLT_HT200_AlphaT0p57_v*", ],
    "200_225":["HLT_HT200_AlphaT0p57_v*", ],
    "225_275":["HLT_HT200_AlphaT0p57_v*", ],
    "275_325":["HLT_HT250_AlphaT0p55_v*", ],
    "325_375":["HLT_HT300_AlphaT0p53_v*", ],
    "375_475":["HLT_HT350_AlphaT0p52_v*", ],
    "475_575":["HLT_HT400_AlphaT0p51_v*", ],
    "575_675":["HLT_HT400_AlphaT0p51_v*", ],
    "675_775":["HLT_HT400_AlphaT0p51_v*", ],
    "775_875":["HLT_HT400_AlphaT0p51_v*", ],
    "875":["HLT_HT400_AlphaT0p51_v*", ],
    }

json_output = JSONOutput("filtered")
OneMuon = OP_NumComMuons("==",1)
ZMassCut = RECO_2ndMuonMass(25.0, 91.2, False, "all")
PFMTCut30 = RECO_PFMTCut(30.0, -1.)
DiMuon = OP_NumComMuons("==",2)
ZMass_2Muons = RECO_2ndMuonMass(25.0, 91.2, True, "OS")
minDRMuonJetCut = RECO_MuonJetDRCut(0.5)
minDRMuonJetCutDiMuon = RECO_MuonJetDRCut(0.5)
Mu45PtCut = OP_LowerMuPtCut(30.0)
Tot_VertexCut = OP_TotVertexCut(0,100)

Leading_MuPtCut = OP_LowerMuPtCut(30.)


SMSMassCut_300 = OP_SMSmasscut(299., 301., 249., 251.)
SMSMassCut_200 = OP_SMSmasscut(199., 201., 119., 121.)

SMSMassCut_100_20 = OP_SMSmasscut(99., 101., 19., 21.)
SMSMassCut_100_40 = OP_SMSmasscut(99., 101., 39., 41.)
SMSMassCut_100_60 = OP_SMSmasscut(99., 101., 59., 61.)
SMSMassCut_100_70 = OP_SMSmasscut(99., 101., 69., 71.)
SMSMassCut_100_80 = OP_SMSmasscut(99., 101., 79., 81.)
SMSMassCut_100_90 = OP_SMSmasscut(99., 101., 89., 91.)

SMSMassCut_175_95 = OP_SMSmasscut(174., 176., 94., 96.)
SMSMassCut_175_115 = OP_SMSmasscut(174., 176., 114., 116.)
SMSMassCut_175_135 = OP_SMSmasscut(174., 176., 134., 136.)
SMSMassCut_175_145 = OP_SMSmasscut(174., 176., 144., 146.)
SMSMassCut_175_155 = OP_SMSmasscut(174., 176., 154., 156.)
SMSMassCut_175_165 = OP_SMSmasscut(174., 176., 164., 166.)

SMSMassCut_200_120 = OP_SMSmasscut(199., 202., 119., 122.)
SMSMassCut_200_190 = OP_SMSmasscut(199., 202., 189., 192.)

SMSStopMassCut_100 = OP_SMSmasscut(99., 101., 0., 500.)
SMSStopMassCut_175 = OP_SMSmasscut(175., 176., 0., 500.)
SMSStopMassCut_250 = OP_SMSmasscut(249., 251., 0., 500.)

#some delta mass cuts
SMSdMassCut_10 = OP_SMSdmasscut(0., 1000., 8., 15.)
SMSdMassCut_20 = OP_SMSdmasscut(0., 1000., 18., 25.)
SMSdMassCut_30 = OP_SMSdmasscut(0., 1000., 28., 35.)
SMSdMassCut_40 = OP_SMSdmasscut(0., 1000., 38., 45.)
SMSdMassCut_60 = OP_SMSdmasscut(0., 1000., 58., 65.)
SMSdMassCut_80 = OP_SMSdmasscut(0., 1000., 78., 85.)

#null op to start tree
count_total = OP_Count("count_total")

# genLevel VectSumPt of stop pair cut
stopVectPt_le100 = OP_StopGenVectPtSumCut(100.)


# test definition of isoTrackVeto

isoTrackPset = PSet(
            PtCut = 10., 
            MaxEta = 2.2,
            dZCut = 0.05, #cm
            trkIsoOverPtCut = 0.1,
            Verbose = False)

isoTrackVeto = OP_IsoTrackVeto(isoTrackPset.ps())



def MakeDataTree(Threshold,Muon = None):
  out = []

  runModeName = runMode()

  ### temporary hack - kill me if still here in June.
  ### June update - it's still here...
  Split = None

  if re.match("Muon_Add", str(Split)):
      secondJetET = OP_SecondJetOrMuEtCut(Threshold) 
  else:
      secondJetET = OP_SecondJetEtCut(Threshold)
  print "in MakeDataTree threshold: "+str(Threshold)
  HTBins = []
  if int(Threshold) is 100 : HTBins = [375.+100*i for i in range(6)]
  if int(Threshold) is 73 : HTBins = [200.,225.,275.,325.]
  if int(Threshold) is 86 : HTBins = [325.,375.]

  # define HTbinning for 2013 analysis
  if int(Threshold) is 85:
    HTBins = [175., 275., 325.]+[375.+100*i for i in range(6)]
    HadronicAlphaT = OP_HadAlphaTCut(0.5)
  elif int(Threshold) is 60:
    HTBins = [225., 275.]
    HadronicAlphaT = OP_HadAlphaTCut(0.6)
  else:
    HadronicAlphaT = OP_HadAlphaTCut(0.55)   
  out.append(HadronicAlphaT)

  cutTreeData = Tree("Data")
  cutTreeData.Attach(json)
  cutTreeData.TAttach(json,json_output)
  cutTreeData.TAttach(json_output,jet_ge2)
  cutTreeData.TAttach(jet_ge2,NoiseFilt)
  cutTreeData.TAttach(NoiseFilt,MET_Filter) 
  cutTreeData.TAttach(MET_Filter,GoodVertexMonster)
  cutTreeData.TAttach(GoodVertexMonster,LeadingJetEta)
  cutTreeData.TAttach(LeadingJetEta,secondJetET)
  cutTreeData.TAttach(secondJetET,oddJet)
  cutTreeData.TAttach(oddJet,badMuonInJet)
  cutTreeData.TAttach(badMuonInJet,oddElectron)
  cutTreeData.TAttach(oddElectron,oddPhoton)
  cutTreeData.TAttach(oddPhoton,numComElectrons)
  cutTreeData.TAttach(numComElectrons,numComPhotons) 
  
  if Muon == None:
      cutTreeData.TAttach(numComPhotons,ZeroMuon)
      cutTreeData.TAttach(ZeroMuon, HadronicAlphaT)
      cutTreeData.TAttach(HadronicAlphaT, DeadEcalCutData)
      cutTreeData.TAttach(DeadEcalCutData,VertexPtOverHT)
      cutTreeData.TAttach(VertexPtOverHT,recHitCut)

      myTriggerDict = triggers

      cutTreeData.TAttach(recHitCut, MHT_METCut)

      # branch into jet multi for before MHToMET
      cutTreeData.TAttach(MHT_METCut, jet_le3)
      cutTreeData.TAttach(MHT_METCut, jet_ge4)

      out.append(AddBinedHist(cutTree = cutTreeData,
      OP = ("OP_analysisPlots", genericPSet_data), cut=MHT_METCut,
      htBins = HTBins, TriggerDict = myTriggerDict, lab = "inc_", Muon=None))
      out.append(AddBinedHist(cutTree = cutTreeData,
      OP = ("OP_analysisPlots", genericPSet_data), cut=jet_le3,
      htBins = HTBins, TriggerDict = myTriggerDict, lab = "le3j_", Muon=None))
      out.append(AddBinedHist(cutTree = cutTreeData,
      OP = ("OP_analysisPlots", genericPSet_data), cut=jet_ge4,
      htBins = HTBins, TriggerDict = myTriggerDict, lab = "ge4j_", Muon=None))


      # cutTreeData.TAttach(MHT_METCut,isoTrackVeto)
      # cutTreeData.TAttach(isoTrackVeto, jet_e2_du)
      # cutTreeData.TAttach(isoTrackVeto, jet_e3_du)
      # cutTreeData.TAttach(isoTrackVeto, jet_e4_du)
      
      # out.append(AddBinedHist(cutTree = cutTreeData,
      # OP = ("OP_analysisPlots",genericPSet_data), cut = isoTrackVeto,
      # htBins = HTBins, TriggerDict = myTriggerDict, lab ="after", Muon=None))

    


  else:
    pass

  return (cutTreeData,secondJetET,out)


def MakeMCTree(Threshold, Muon = None):
  out = []

  HTBins = []

  runModeName = runMode()
  HadronicAlphaT = OP_HadAlphaTCut(0.55)

  if int(Threshold) is 100: HTBins = [375+100*i for i in range(7)]
  if int(Threshold) is 73 : HTBins = [200.,275.,325.]
  if int(Threshold) is 86 : HTBins = [325.,375.]
  if int(Threshold) is 60 :
    HTBins = [225.,275.]
    HadronicAlphaT = OP_HadAlphaTCut(0.6)

  if int(Threshold) is 85 :
    HTBins = [175., 275., 325.]+[375.+100*i for i in range(6)]
    print HTBins
    HadronicAlphaT = OP_HadAlphaTCut(0.5)
  out.append(HadronicAlphaT)
 
  ### add incl binning for thresh=100, split==None
  HTBins_inc = [0.,10000.]

  if Muon!=None:
      secondJetET = OP_SecondJetOrMuEtCut(Threshold)
  else:
      secondJetET = OP_SecondJetEtCut(Threshold)

  cutTreeMC = Tree("MC")

  SMScut_ = None
  # SMScut_ = SMSMassCut_175_95
  # SMScut_ = SMSMassCut_175_115
  # SMScut_ = SMSMassCut_175_135
  # SMScut_ = SMSMassCut_175_145
  # SMScut_ = SMSMassCut_175_155
  # SMScut_ = SMSMassCut_175_165

  # SMScut_ = SMSMassCut_200_120
  # SMScut_ = SMSMassCut_200_190

  # SMScut_ = SMSStopMassCut_100
  # SMScut_ = SMSStopMassCut_175
  # SMScut_ = SMSStopMassCut_250

  cutTreeMC.Attach(count_total)

  if SMScut_:
    cutTreeMC.TAttach(count_total, SMScut_)
    cutTreeMC.TAttach(SMScut_,jet_ge2)
  else:
    cutTreeMC.TAttach(count_total,jet_ge2)

  cutTreeMC.TAttach(jet_ge2, ht150_Trigger)
  cutTreeMC.TAttach(ht150_Trigger, NoiseFilt)
  cutTreeMC.TAttach(NoiseFilt, GoodVertexMonster)
  cutTreeMC.TAttach(GoodVertexMonster, MET_Filter)
  cutTreeMC.TAttach(MET_Filter, LeadingJetEta)
  cutTreeMC.TAttach(LeadingJetEta, secondJetET )
  cutTreeMC.TAttach(secondJetET, oddJet)
  cutTreeMC.TAttach(oddJet, badMuonInJet)
  cutTreeMC.TAttach(badMuonInJet, oddElectron)
  cutTreeMC.TAttach(oddElectron, oddPhoton)
  cutTreeMC.TAttach(oddPhoton, numComElectrons)
  cutTreeMC.TAttach(numComElectrons, numComPhotons)

  if Muon == None: 
    ## HADRONIC SELECTION ##

    cutTreeMC.TAttach(numComPhotons, ZeroMuon)
    cutTreeMC.TAttach(ZeroMuon, HadronicAlphaT),
    cutTreeMC.TAttach(HadronicAlphaT, DeadEcalCutMC) 
    cutTreeMC.TAttach(DeadEcalCutMC, VertexPtOverHT)
    cutTreeMC.TAttach(VertexPtOverHT, recHitCut)
    cutTreeMC.TAttach(recHitCut, MHT_METCut) 

    cutTreeMC.TAttach(MHT_METCut,jet_le3)
    cutTreeMC.TAttach(MHT_METCut,jet_ge4)

    if "Track" in runModeName:

      cutTreeMC.TAttach(MHT_METCut, isoTrackVeto)

      out.append(AddBinedHist(cutTree = cutTreeMC,
      OP = (runModeName,genericPSet_mc), cut = MHT_METCut,
      htBins = HTBins, TriggerDict = None, lab ="before", Muon=None))

      out.append(AddBinedHist(cutTree = cutTreeMC,
      OP = (runModeName,genericPSet_mc), cut = isoTrackVeto,
      htBins = HTBins, TriggerDict = None, lab ="after", Muon=None))

    elif "analysis" in runModeName:
      
      out.append(AddBinedHist(cutTree = cutTreeMC,
      OP = (runModeName,genericPSet_mc), cut =  SMScut_ if SMScut_ else count_total,
      htBins = HTBins_inc, TriggerDict = None, lab ="noCuts_", Muon=None))
       
      out.append(AddBinedHist(cutTree = cutTreeMC,
      OP = (runModeName,genericPSet_mc), cut = MHT_METCut,
      htBins = HTBins, TriggerDict = None, lab ="inc_", Muon=None))
      
      out.append(AddBinedHist(cutTree = cutTreeMC,
      OP = (runModeName,genericPSet_mc), cut = jet_le3,
      htBins = HTBins, TriggerDict = None, lab ="le3j_", Muon=None))
      
      out.append(AddBinedHist(cutTree = cutTreeMC,
      OP = (runModeName,genericPSet_mc), cut = jet_ge4,
      htBins = HTBins, TriggerDict = None, lab ="ge4j_", Muon=None))


  else:
    ## MUON SELECTION ##

    cutTreeMC.TAttach(numComPhotons,DeadEcalCutData)
    cutTreeMC.TAttach(DeadEcalCutData,Leading_MuPtCut)

# HACK
    # cutTreeMC.TAttach(Leading_MuPtCut, OneMuon)
    cutTreeMC.TAttach(Leading_MuPtCut,jet_le3_mu)
    cutTreeMC.TAttach(Leading_MuPtCut,jet_ge4_mu)

    out.append(AddBinedHist(cutTree = cutTreeMC,
    OP = (runModeName,genericPSet_mc), cut =  SMScut_ if SMScut_ else count_total,
    htBins = HTBins_inc, TriggerDict = None, lab ="noCuts_", Muon=True))
     
    out.append(AddBinedHist(cutTree = cutTreeMC,
    OP = (runModeName,genericPSet_mc), cut = Leading_MuPtCut,
    htBins = HTBins, TriggerDict = None, lab ="onemuon_inc_", Muon=True))
    
    out.append(AddBinedHist(cutTree = cutTreeMC,
    OP = (runModeName,genericPSet_mc), cut = jet_le3_mu,
    htBins = HTBins, TriggerDict = None, lab ="onemuon_le3j_", Muon=True))
    
    out.append(AddBinedHist(cutTree = cutTreeMC,
    OP = (runModeName,genericPSet_mc), cut = jet_ge4_mu,
    htBins = HTBins, TriggerDict = None, lab ="onemuon_ge4j_", Muon=True))

    # cutTreeMC.TAttach(Leading_MuPtCut,minDRMuonJetCut)

    # cutTreeMC.TAttach(minDRMuonJetCut,OneMuon)
    # cutTreeMC.TAttach(OneMuon,PFMTCut30)
    # cutTreeMC.TAttach(PFMTCut30,ZMassCut)
    
    # QCD one muon position
     
    # cutTreeMC.TAttach(ZMassCut,MHT_METCut)

    # one muon position
    
    # cutTreeMC.TAttach(minDRMuonJetCut,DiMuon)
    # cutTreeMC.TAttach(DiMuon,ZMass_2Muons)
    # cutTreeMC.TAttach(ZMass_2Muons,MHT_METCutDiMuon)

    # dimuon position
  
  return (cutTreeMC,secondJetET,out)


# Define the custom muon ID

mu_2012_mu = PSet(
        MuID = "Tight",
        MinPt = 10.,
        MaxEta = 2.1,
        MaxIsolation = 0.12,
        GlobalChi2 = 10,
        MaxGlbTrkDxy = 0.2,
        MinNumTrkLayers = 6,
        Match2GlbMu = 1,
        NumPixelHits = 1,
        MaxInrTrkDz = 0.5
              )

mu_2012_had = PSet(
    MuID = "Tight",
    MinPt = 10.,
    MaxEta = 2.5,
    MaxIsolation = 0.12,
    GlobalChi2 = 10,
    MaxGlbTrkDxy = 0.2,
    MinNumTrkLayers = 6,
    Match2GlbMu = 1,
    NumPixelHits = 1,
    MaxInrTrkDz = 0.5
)

# Define the custom eleID (taken from RA4)

el_id_2012_RA4 = PSet(
      IsData           = False,
      QCDEstimation    = False,
      ScEtaMax         = 2.5,
      RecoPfPtDifMax   = 10.,
      PtMin_eb         = 20.,
      PfRelIso_eb      = 0.15,
      HoE_eb           = 0.12,
      TrkDphi_eb       = 0.06,
      TrkDeta_eb       = 0.004,
      SigmaIetaIeta_eb = 0.01 ,
      ConvRejection_eb = True ,
      MissingHits_eb   = 1 ,
      Dxy_eb           = 0.02 ,
      Dz_eb            = 0.1 ,
      EoP_eb           = 0.05 ,
      PtMin_ee         = 20.,
      PfRelIso_ee      = 0.15,
      HoE_ee           = 0.10 ,
      TrkDphi_ee       = 0.03 ,
      TrkDeta_ee       = 0.007 ,
      SigmaIetaIeta_ee = 0.03 ,
      ConvRejection_ee = True ,
      MissingHits_ee   = 1 ,
      Dxy_ee           = 0.02 ,
      Dz_ee            = 0.1 ,
      EoP_ee           = 0.05,
      PF_Electron      = False,
)

PU_2012 = [3.3526156883828602, 5.0000390543531159, 5.0000387186660964, 5.0000387864635014, 5.0000390502495184, 5.0000389494780535, 
  3.4145539861479008, 1.7907397611093883, 1.5290439653662495, 1.5740788042135916, 1.6530978708241377, 1.6462211050178599, 
  1.5287603131779848, 1.350159932499021, 1.1605480712613019, 1.0167357240277282, 0.94570196626791592, 0.92969500964238916, 
  0.94911635831102081, 0.98744363579509253, 1.0189148078013086, 1.0293893415021849, 1.0212259726950803, 1.000824346166683, 
  0.97311858818444352, 0.94213734571363006, 0.91015183950802869, 0.87804921585398921, 0.84564433493107471, 0.81305212352685896, 
  0.7803616157059774, 0.74750993300650936, 0.71409776929773849, 0.68074164080016197, 0.64779490297963582, 0.61464959710449685, 
  0.58197264454021658, 0.55012656573179264, 0.51876819929979823, 0.48823394292261296, 0.45864392634163109, 0.43010947665090771, 
  0.40265257271948524, 0.37615982828793132, 0.35110986448841147, 0.32716124272580405, 0.30431197427324258, 0.28274399234289738, 
  0.26242234978760065, 0.24325970866189159]

pileup_reweight = PileUpReweighting(PSet(PileUpWeights = PU_2012).ps())

