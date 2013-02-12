#!/usr/bin/env python
"""
Created by Bryn Mathias on 2010-05-07.
Modified by Chris Lucas on 2013-02-07
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

from samples import *

from ra1objectid.vbtfElectronId_cff import *
from ra1objectid.vbtfMuonId_cff import *
from ra1objectid.ra3PhotonId_cff import *
from ra1objectid.ra3PhotonId2012_cff import *


# -----------------------------------------------------------------------------
# Utils

def ensure_dir(path):
    try:
      os.makedirs(path)
    except OSError as exc: # Python >2.5
      if exc.errno == errno.EEXIST:
        pass
      else: raise

# -----------------------------------------------------------------------------
# Samples
#import yours in your running script

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
default_ntuple.Taus=PSet(
Prefix="tau",
Suffix="Pat",
LooseID="TauIdbyTaNCfrOnePercent",
TightID="TauIdbyTaNCfrTenthPercent"
)
default_ntuple.Jets=PSet(
Prefix="ic5Jet",
Suffix="Pat",
Uncorrected=False,
)
default_ntuple.Photons=PSet(
Prefix="photon",
Suffix="Pat",
)

ic5_calo = deepcopy(default_ntuple)
ic5_calo.Jets.Prefix="ic5Jet"

ak5_calo = deepcopy(default_ntuple)
ak5_calo.Jets.Prefix="ak5Jet"

ak5_jpt = deepcopy(default_ntuple)
ak5_jpt.Jets.Prefix="ak5JetJPT"

ak5_pf = deepcopy(default_ntuple)
ak5_pf.Jets.Prefix="ak5JetPF"
ak5_pf.TerJets.Prefix="ak5Jet"

ak7_calo = deepcopy(default_ntuple)
ak7_calo.Jets.Prefix="ak7Jet"

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
default_cc.Muons.ModifyJetEnergy=True
default_cc.Muons.PtCut=10.0
default_cc.Muons.EtaCut=2.5
default_cc.Muons.TrkIsoCut=-1.
default_cc.Muons.CombIsoCut= 1.e6
default_cc.Muons.MuonJetDeltaR=0.5
default_cc.Muons.MuonIsoTypePtCutoff=0.
default_cc.Muons.RequireLooseIdForInitialFilter=False
default_cc.Electrons.PtCut=10.0
default_cc.Electrons.EtaCut=2.5
default_cc.Electrons.TrkIsoCut=-1.0
default_cc.Electrons.CombIsoCut=0.15
default_cc.Electrons.ElectronJetDeltaR=0.5
default_cc.Electrons.ElectronIsoTypePtCutoff=0.
default_cc.Electrons.ElectronLooseIdRequired=True
default_cc.Electrons.ElectronTightIdRequired=False
default_cc.Electrons.RequireLooseIdForInitialFilter=False
default_cc.Photons.EtCut=25.0
default_cc.Photons.EtaCut=2.5
default_cc.Photons.TrkIsoCut=2.0
default_cc.Photons.CaloIsoCut=0.2
default_cc.Photons.IDReq=3
default_cc.Photons.UseID=True
default_cc.Photons.PhotonJetDeltaR=0.5
default_cc.Photons.PhotonIsoTypePtCutoff=30.

# -----------------------------------------------------------------------------
# Definition of common objects

default_common = deepcopy(defaultConfig.Common)
default_common.ApplyXCleaning=True
default_common.Jets.PtCut=50.0
default_common.Jets.EtaCut=3.0
#default_common.Jets.EtaCut=5.0
default_common.Jets.ApplyID=True
default_common.Jets.TightID=False
default_common.Electrons.PtCut=10.0
default_common.Electrons.EtaCut=2.5
default_common.Electrons.TrkIsoCut=-1.
default_common.Electrons.CombIsoCut=0.15
default_common.Electrons.ApplyID = True
default_common.Electrons.TightID = False
default_common.Electrons.RequireLooseForOdd = True
default_common.Muons.PtCut=10.0
default_common.Muons.EtaCut=2.5
default_common.Muons.TrkIsoCut=-1.
default_common.Muons.CombIsoCut=0.15
default_common.Muons.ApplyID = True
default_common.Muons.TightID = True
default_common.Muons.RequireLooseForOdd = True
default_common.Photons.EtCut=25.0
# default_common.Photons.EtaCut=2.5
default_common.Photons.UseID=True
# the photon cuts are NOT read anyway
# default_common.Photons.TrkIsoRel=0.
# default_common.Photons.TrkIsoCut=99999.
# default_common.Photons.EcalIsoRel=0.
# default_common.Photons.EcalIsoCut=99999.
# default_common.Photons.HcalIsoRel=0.
# default_common.Photons.HcalIsoCut=99999.
# default_common.Photons.HadOverEmCut=0.5
# default_common.Photons.SigmaIetaIetaCut=0.5
##default_common.Photons.CaloIsoCut=99999.
default_common.Photons.IDReq = 3
default_common.Photons.RequireLooseForOdd = True

# -----------------------------------------------------------------------------
# Plotting PSets

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
)

genericPSet_data = PSet(
DirName       = "275_325Gev",
MinObjects    = 2,
MaxObjects    = 15,
isData        = True,
BTagAlgo      = 5,
BTagAlgoCut   = 0.679,
StandardPlots = True,
minDR         = 0.5,
threshold     = 50.,
)

# -----------------------------------------------------------------------------
# Define the custom muon ID

mu_2012 = PSet(
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

mu_2012_veto = PSet(
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

# -----------------------------------------------------------------------------
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

singleMuon = OP_NumComMuons("==", 1)
singleEle  = OP_NumComElectrons("==", 1)
doubleBTag = OP_NumCommonBtagJets("==", 2, 0.679, 5)

ht200trigger = 200.
ht200_Trigger = RECO_CommonHTCut(ht200trigger)
htTakeMu200_Trigger = RECO_CommonHTTakeMuCut(ht200trigger)

ht250trigger = 250.
ht250_Trigger = RECO_CommonHTCut(ht250trigger)
htTakeMu250_Trigger = RECO_CommonHTTakeMuCut(ht250trigger)

htCut225 = RECO_CommonHTCut(225.)
htTakeMuCut225 = RECO_CommonHTTakeMuCut(225.)

htCut275 = RECO_CommonHTCut(275.)
htTakeMuCut275 = RECO_CommonHTTakeMuCut(275.)

nullCut = RECO_CommonHTCut(0.)

DeadEcalCutData = OP_DeadECALCut(0.3,0.3,0.5,30.,10,0,"./deadRegionList_GR10_P_V10.txt")
DeadEcalCutMC =   OP_DeadECALCut(0.3,0.3,0.5,30.,10,0,"./deadRegionList_START38_V12.txt")

MHT_METCut = OP_MHToverMET(1.25,50.)
MHT_METReverseCut = OP_Reverse_MHToverMET(1.25,50.)
MHT_METCutMC = OP_MHToverMET(1.25,50.)

MET_Filter = OP_METFilters_2012()

MCPrint=MC_PrintGenParticleInfo("CHAIN")

jet_e2= OP_NumComJets("==",2)
jet_e3= OP_NumComJets("==",3)
jet_e4= OP_NumComJets("==",4)
jet_g3 = OP_NumComJets(">",3)
jet_g4= OP_NumComJets(">",4)
jet_ge4 = OP_NumComJets(">",3)
jet_le3 = OP_NumComJets("<",4)
jet_ge2  = OP_NumComJets(">",1)

jet_e2_du = OP_NumComJets("==",2)
jet_e3_du = OP_NumComJets("==",3)
jet_e4_du = OP_NumComJets("==",4)
jet_g3_du = OP_NumComJets(">",3)
jet_g4_du = OP_NumComJets(">",4)

VertexPtOverHT = OP_SumVertexPtOverHT(0.1)

json = JSONFilter("Json Mask", json_to_pset("Jsons/json_DCSONLY_190389-209151_17Jan2013_Thursday_Update1301.txt") )
recHitCut = OP_SumRecHitPtCut(30.)
ZeroMuon = OP_NumComMuons("<=",0)
json_ouput = JSONOutput("filtered")
OneMuon = OP_NumComMuons("==",1)
ZMassCut = RECO_2ndMuonMass(25.0, 91.2, False, "all")
PFMTCut30 = RECO_PFMTCut(30.0, -1.)
DiMuon = OP_NumComMuons("==",2)
ZMass_2Muons = RECO_2ndMuonMass(25.0, 91.2, True, "OS")
minDRMuonJetCut = RECO_MuonJetDRCut(0.5)
minDRMuonJetCutDiMuon = RECO_MuonJetDRCut(0.5)
Mu45PtCut = OP_LowerMuPtCut(30.0)
Mu50PtCut_HigHT = OP_LowerMuPtCut(50.0)
Mu50PtCut_LowHT275 = OP_LowerMuPtCut(50.0*275./375.)
Mu50PtCut_LowHT325 = OP_LowerMuPtCut(50.0*325./375.)
Mu50PtCut_HigHT_MuTrigPlateau = OP_LowerMuPtCut(50.0)
Mu50PtCut_LowHT275_MuTrigPlateau = OP_LowerMuPtCut(50.0)
Mu50PtCut_LowHT325_MuTrigPlateau = OP_LowerMuPtCut(50.0)
secondJetET = OP_SecondJetEtCut(0)
Tot_VertexCut = OP_TotVertexCut(0,100)

SMSMassCut_300 = OP_SSMmasscut(299., 301., 249., 251.)
SMSMassCut_200 = OP_SSMmasscut(199., 201., 119., 121.)

# -----------------------------------------------------------------------------
# Trigger Definitions

ht_triggers = {
    "275_325":["HLT_HT250_v*", ],
    "325_375":["HLT_HT300_v*", ],
    "375_475":["HLT_HT350_v*", ],
    "475_575":["HLT_HT450_v*", ],
    "575_675":["HLT_HT450_v*", ],
    "675_775":["HLT_HT450_v*", ],
    "775_875":["HLT_HT450_v*", ],
    "875":["HLT_HT450_v*", ],
}

triggers = {
    "275_325":["HLT_HT250_AlphaT0p55_v*", ],
    "325_375":["HLT_HT300_AlphaT0p53_v*", ],
    "375_475":["HLT_HT350_AlphaT0p52_v*", ],
    "475_575":["HLT_HT400_AlphaT0p51_v*", ],
    "575_675":["HLT_HT400_AlphaT0p51_v*", ],
    "675_775":["HLT_HT400_AlphaT0p51_v*", ],
    "775_875":["HLT_HT400_AlphaT0p51_v*", ],
    "875":["HLT_HT400_AlphaT0p51_v*", ],
    }

single_mu_triggers = {
    "275_325":["HLT_IsoMu24_eta2p1_v*", ],
    "325_375":["HLT_IsoMu24_eta2p1_v*", ],
    "375_475":["HLT_IsoMu24_eta2p1_v*", ],
    "475_575":["HLT_IsoMu24_eta2p1_v*", ],
    "575_675":["HLT_IsoMu24_eta2p1_v*", ],
    "675_775":["HLT_IsoMu24_eta2p1_v*", ],
    "775_875":["HLT_IsoMu24_eta2p1_v*", ],
    "875":["HLT_IsoMu24_eta2p1_v*", ],
}


di_mu_triggers = {
    "275_325":["HLT_Mu17_Mu8_v*", ],
    "325_375":["HLT_Mu17_Mu8_v*", ],
    "375_475":["HLT_Mu17_Mu8_v*", ],
    "475_575":["HLT_Mu17_Mu8_v*", ],
    "575_675":["HLT_Mu17_Mu8_v*", ],
    "675_775":["HLT_Mu17_Mu8_v*", ],
    "775_875":["HLT_Mu17_Mu8_v*", ],
    "875":["HLT_Mu17_Mu8_v*", ],
}


mu_triggers = {
    "275_325":["HLT_Mu5_HT200_v3","HLT_Mu5_HT200_v4","HLT_Mu8_HT200_v4","HLT_Mu15_HT200_v2","HLT_Mu15_HT200_v3","HLT_Mu15_HT200_v4","HLT_Mu30_HT200_v1","HLT_Mu30_HT200_v3","HLT_Mu40_HT200_v4","HLT_Mu40_HT300_v4","HLT_Mu40_HT300_v5",],
    "325_375":["HLT_Mu5_HT200_v3","HLT_Mu5_HT200_v4","HLT_Mu8_HT200_v4","HLT_Mu15_HT200_v2","HLT_Mu15_HT200_v3","HLT_Mu15_HT200_v4","HLT_Mu30_HT200_v1","HLT_Mu30_HT200_v3","HLT_Mu40_HT200_v4","HLT_Mu40_HT300_v4","HLT_Mu40_HT300_v5",],
    "375_475":["HLT_Mu5_HT200_v3","HLT_Mu5_HT200_v4","HLT_Mu8_HT200_v4","HLT_Mu15_HT200_v2","HLT_Mu15_HT200_v3","HLT_Mu15_HT200_v4","HLT_Mu30_HT200_v1","HLT_Mu30_HT200_v3","HLT_Mu40_HT200_v4","HLT_Mu40_HT300_v4","HLT_Mu40_HT300_v5",],
    "475_575":["HLT_Mu5_HT200_v3","HLT_Mu5_HT200_v4","HLT_Mu8_HT200_v4","HLT_Mu15_HT200_v2","HLT_Mu15_HT200_v3","HLT_Mu15_HT200_v4","HLT_Mu30_HT200_v1","HLT_Mu30_HT200_v3","HLT_Mu40_HT200_v4","HLT_Mu40_HT300_v4","HLT_Mu40_HT300_v5",],
    "575_675":["HLT_Mu5_HT200_v3","HLT_Mu5_HT200_v4","HLT_Mu8_HT200_v4","HLT_Mu15_HT200_v2","HLT_Mu15_HT200_v3","HLT_Mu15_HT200_v4","HLT_Mu30_HT200_v1","HLT_Mu30_HT200_v3","HLT_Mu40_HT200_v4","HLT_Mu40_HT300_v4","HLT_Mu40_HT300_v5",],
    "675_775":["HLT_Mu5_HT200_v3","HLT_Mu5_HT200_v4","HLT_Mu8_HT200_v4","HLT_Mu15_HT200_v2","HLT_Mu15_HT200_v3","HLT_Mu15_HT200_v4","HLT_Mu30_HT200_v1","HLT_Mu30_HT200_v3","HLT_Mu40_HT200_v4","HLT_Mu40_HT300_v4","HLT_Mu40_HT300_v5",],
    "775_875":["HLT_Mu5_HT200_v3","HLT_Mu5_HT200_v4","HLT_Mu8_HT200_v4","HLT_Mu15_HT200_v2","HLT_Mu15_HT200_v3","HLT_Mu15_HT200_v4","HLT_Mu30_HT200_v1","HLT_Mu30_HT200_v3","HLT_Mu40_HT200_v4","HLT_Mu40_HT300_v4","HLT_Mu40_HT300_v5",],
    "875":["HLT_Mu5_HT200_v3","HLT_Mu5_HT200_v4","HLT_Mu8_HT200_v4","HLT_Mu15_HT200_v2","HLT_Mu15_HT200_v3","HLT_Mu15_HT200_v4","HLT_Mu30_HT200_v1","HLT_Mu30_HT200_v3","HLT_Mu40_HT200_v4","HLT_Mu40_HT300_v4","HLT_Mu40_HT300_v5",],
}

egmu_triggers = {
    "275_325":["HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v*", "HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v*"],
    "325_375":["HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v*", "HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v*"],
    "375_475":["HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v*", "HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v*"],
    "475_575":["HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v*", "HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v*"],
    "575_675":["HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v*", "HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v*"],
    "675_775":["HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v*", "HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v*"],
    "775_875":["HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v*", "HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v*"],
    "875":["HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v*", "HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v*"],
}

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# Plotting Functions

def makePlotOp(OP = (), cutTree = None, cut = None, label = "", doAlphaTCut=False):
  """docstring for makePlotOp"""
  out = []
  if OP[1] != None:
    plotpset = deepcopy(OP[1])
    plotpset.DirName = label
    op = eval(OP[0]+"(plotpset.ps())")
  else:
    op = eval(OP[0])
  out.append(op)

  alpha = OP_CommonAlphaTCut(0.55)
  out.append(alpha)
  if doAlphaTCut:
    cutTree.TAttach(cut, alpha)
    cutTree.TAttach(alpha, op)
  else:
    cutTree.TAttach(cut, op)
  return out
  pass

# -----------------------------------------------------------------------------

def AddBinedHist(cutTree = None, OP = (), cut = None, htBins = [],TriggerDict = None,lab = "", Muon=None, alphaTCut=True):
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
        useprescale = False

        triggerps = PSet(Verbose = False,
        UsePreScaledTriggers = False,
        Triggers = [])

        triggerps.Triggers = TriggerDict["%d%s"%(lower, "_%d"%upper if upper else "")]
        Trigger = OP_MultiTrigger( triggerps.ps() )
        
        out.append(triggerps)
        out.append(Trigger)
        out.append(lowerCut)
        

        #cutTree.TAttach(cut,Trigger)
        #cutTree.TAttach(Trigger,lowerCut)
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
        if int(lower) == 275 and upper is None: continue
        if int(lower) == 325 and upper is None: continue
        if int(lower) == 375 and upper is None: continue
        if int(lower) == 675 and upper is None : continue
        lowerCutVal=""
        if Muon!=None:
            lowerCutVal=("RECO_CommonHTTakeMuCut(%d)"%lower)
        else:
            lowerCutVal=("RECO_CommonHTCut(%d)"%lower)
        lowerCut = eval(lowerCutVal)
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
        ###pOps = makePlotOp(cutTree = cutTree, OP = OP, cut = lowerCut, label = "%s%d_"%(lab,lower)) 
        pOps = makePlotOp(cutTree = cutTree, OP = OP, cut = upperCut if upper else lowerCut, label = "%s%d%s"%(lab,lower, "_%d"%upper if upper else ""), doAlphaTCut=alphaTCut)
        out.append(pOps)
  return out
  pass

# -----------------------------------------------------------------------------

def MakeDataTree(Threshold,Muon = None,Split = None):
  out = []

  secondJetET = OP_SecondJetEtCut(Threshold)

  print "in MakeDataTree threshold: "+str(Threshold)
  HTBins = []
  
  if int(Threshold) is 100 : HTBins = [375.+100*i for i in range(6)]
  if int(Threshold) is 73 : HTBins = [275.,325.]
  if int(Threshold) is 86 : HTBins = [325.,375.]
  
  cutTreeData = Tree("Data")
  cutTreeData.Attach(json)
  cutTreeData.TAttach(json,json_ouput)
  
  out.append(AddBinedHist(cutTree = cutTreeData,
  OP = ("OP_ISRSystematic",genericPSet_data), cut = json_ouput,
  htBins = HTBins,TriggerDict = egmu_triggers,lab ="debug1_", alphaTCut = False) ) 
  
  cutTreeData.TAttach(json_ouput,NoiseFilt)
  cutTreeData.TAttach(NoiseFilt,MET_Filter)
  cutTreeData.TAttach(MET_Filter,GoodVertexMonster)

  cutTreeData.TAttach(GoodVertexMonster,LeadingJetEta)
  cutTreeData.TAttach(LeadingJetEta,secondJetET)
  cutTreeData.TAttach(secondJetET,oddJet)
      
  cutTreeData.TAttach(oddJet,badMuonInJet)
  cutTreeData.TAttach(badMuonInJet,oddElectron)
  cutTreeData.TAttach(oddElectron,oddPhoton)
  cutTreeData.TAttach(oddPhoton,numComPhotons)
  cutTreeData.TAttach(numComPhotons,Tot_VertexCut)

  # select out required leptons
  #cutTreeData.TAttach(Tot_VertexCut, singleEle)
  #cutTreeData.TAttach(singleEle, singleMuon)
  #cutTreeData.TAttach(singleMuon, doubleBTag)
  #cutTreeData.TAttach(doubleBTag, htCut275)
  ### NOTE: also need veto on third bjet - loose WP
  cutTreeData.TAttach(Tot_VertexCut, doubleBTag)
  cutTreeData.TAttach(doubleBTag, singleMuon)
  cutTreeData.TAttach(singleMuon, singleEle)
  cutTreeData.TAttach(singleEle, htCut275)

  cutTreeData.TAttach(htCut275,ZeroMuon)
  cutTreeData.TAttach(ZeroMuon,recHitCut)
  cutTreeData.TAttach(recHitCut,VertexPtOverHT)
  cutTreeData.TAttach(VertexPtOverHT,DeadEcalCutData)
  cutTreeData.TAttach(DeadEcalCutData,MHT_METCut)

  cutTreeData.TAttach(DeadEcalCutData,MHT_METReverseCut)

  cutTreeData.TAttach(MHT_METCut,jet_e2) # jet n=2
  cutTreeData.TAttach(MHT_METCut,jet_e3) # jet n=3
  cutTreeData.TAttach(MHT_METCut,jet_e4) # jet n=4
  cutTreeData.TAttach(MHT_METCut,jet_g3) # jet n>3
  cutTreeData.TAttach(MHT_METCut,jet_g4) # jet n>4

  # make some plotting ops

  ## debug
 
  out.append(AddBinedHist(cutTree = cutTreeData,
        OP = ("OP_ISRSystematic",genericPSet_data), cut = oddPhoton,
        htBins = HTBins,TriggerDict = egmu_triggers,lab ="debug2_", alphaTCut = False) )  
  out.append(AddBinedHist(cutTree = cutTreeData,
        OP = ("OP_ISRSystematic",genericPSet_data), cut = singleMuon,
        htBins = HTBins,TriggerDict = egmu_triggers,lab ="debug3_", alphaTCut = False) )  



  ## Post-Object Selection
  out.append(AddBinedHist(cutTree = cutTreeData,
        OP = ("OP_ISRSystematic",genericPSet_data), cut = singleMuon,
        htBins = HTBins,TriggerDict = egmu_triggers,lab ="postObject_", alphaTCut = False) )  

  return (cutTreeData,secondJetET,out)

# -----------------------------------------------------------------------------

def MakeMCTree(Threshold, Muon = None, Split = None):
  out = []

  HTBins = []
  
  if int(Threshold) is 100 and Split == None : HTBins = [375+100*i for i in range(6)]
  if int(Threshold) is 100 and Split == "Had_One" : HTBins = [375+100*i for i in range(4)]
  if int(Threshold) is 100 and Split == "Had_Two" : HTBins = [675+100*i for i in range(3)]
  if int(Threshold) is 100 and Split == "Muon_One" : HTBins = [375,475]
  if int(Threshold) is 100 and Split == "Muon_Two" : HTBins = [475,575,675]
  if int(Threshold) is 100 and Split == "Muon_Three" : HTBins = [675,775,875]
  if int(Threshold) is 73 : HTBins = [275.,325.]
  if int(Threshold) is 86 : HTBins = [325.,375.]
  if int(Threshold) is 60 : HTBins = [225.,275.]

 
  ### add incl binning for thresh=100, split==None
  if int(Threshold) is 10 and Split == None : HTBins_inc = [0.,10000.]

  ### override the threshold arguement
  #Threshold=Threshold*1.1
  #Threshold=40.

  if Muon!=None:
      secondJetET = OP_SecondJetOrMuEtCut(Threshold)
  else:
      secondJetET = OP_SecondJetEtCut(Threshold)

  cutTreeMC = Tree("MC")

  runModeName = runMode()


  if Muon!=None:
      cutTreeMC.Attach(htTakeMu200_Trigger)
      cutTreeMC.TAttach(htTakeMu200_Trigger,NoiseFilt)
#      cutTreeMC.Attach(htTakeMu250_Trigger)
#      cutTreeMC.TAttach(htTakeMu250_Trigger,NoiseFilt)
      cutTreeMC.TAttach(NoiseFilt,GoodVertexMonster)
      cutTreeMC.TAttach(GoodVertexMonster,LeadingJetOrMuEta)
      cutTreeMC.TAttach(LeadingJetOrMuEta,secondJetET)
      cutTreeMC.TAttach(secondJetET,oddJet)
  else:
      cutTreeMC.Attach(nullCut)
      cutTreeMC.TAttach(nullCut, SMSMassCut_200)
      cutTreeMC.TAttach(SMSMassCut_200, jet_ge2)
      #cutTreeMC.TAttach(nullCut, jet_ge2)
      #cutTreeMC.TAttach(nullCut,SMSMassCut_300)
      #cutTreeMC.TAttach(SMSMassCut_300, jet_ge2)
#      cutTreeMC.TAttach(jet_ge2, ht250_Trigger)
#      cutTreeMC.TAttach(ht250_Trigger,NoiseFilt)
      cutTreeMC.TAttach(jet_ge2, ht200_Trigger)
      cutTreeMC.TAttach(ht200_Trigger,NoiseFilt)
      cutTreeMC.TAttach(NoiseFilt,GoodVertexMonster)
      cutTreeMC.TAttach(GoodVertexMonster,LeadingJetEta)
      cutTreeMC.TAttach(LeadingJetEta,secondJetET)
      cutTreeMC.TAttach(secondJetET,oddJet)

  cutTreeMC.TAttach(oddJet,badMuonInJet)
  cutTreeMC.TAttach(badMuonInJet,MCPrint)
  cutTreeMC.TAttach(MCPrint,oddElectron)
  cutTreeMC.TAttach(oddElectron,oddPhoton)
  cutTreeMC.TAttach(oddPhoton,numComElectrons)
  cutTreeMC.TAttach(numComElectrons,numComPhotons)
  cutTreeMC.TAttach(numComPhotons,MET_Filter)
  cutTreeMC.TAttach(MET_Filter,Tot_VertexCut)
 
  if Muon == None:
#    cutTreeMC.TAttach(Tot_VertexCut,htCut275)
#    cutTreeMC.TAttach(htCut275,ZeroMuon)
    cutTreeMC.TAttach(Tot_VertexCut,htCut225)
    cutTreeMC.TAttach(htCut225,ZeroMuon)
    cutTreeMC.TAttach(ZeroMuon,recHitCut)
    cutTreeMC.TAttach(recHitCut,VertexPtOverHT)
    cutTreeMC.TAttach(VertexPtOverHT,DeadEcalCutMC)
    cutTreeMC.TAttach(DeadEcalCutMC,MHT_METCut)

    cutTreeMC.TAttach(MHT_METCut,jet_le3)
    cutTreeMC.TAttach(MHT_METCut,jet_ge4) # jet ge4

    if int(Threshold) is 10 and Split == None :
      #pass
      out.append(AddBinedHist(cutTree = cutTreeMC,
      OP = (runModeName,genericPSet_mc), cut = SMSMassCut_200,
      htBins = HTBins_inc, TriggerDict = None, lab ="noCuts_", Muon=False, alphaTCut=False))
    else:
      out.append(AddBinedHist(cutTree = cutTreeMC,
      OP = (runModeName,genericPSet_mc), cut = MHT_METCut,
      htBins = HTBins, TriggerDict = None, lab ="inc_", Muon=False, alphaTCut=True))
      
      out.append(AddBinedHist(cutTree = cutTreeMC,
      OP = (runModeName,genericPSet_mc), cut = jet_le3,
      htBins = HTBins, TriggerDict = None, lab ="le3j_", Muon=False, alphaTCut=True ))
      
      out.append(AddBinedHist(cutTree = cutTreeMC,
      OP = (runModeName,genericPSet_mc), cut = jet_ge4,
      htBins = HTBins, TriggerDict = None, lab ="ge4j_", Muon=False, alphaTCut=True))

  else:
    cutTreeMC.TAttach(Tot_VertexCut,htCut275)
    cutTreeMC.TAttach(htCut275,Mu45PtCut)
    cutTreeMC.TAttach(Mu45PtCut,minDRMuonJetCut)
    cutTreeMC.TAttach(minDRMuonJetCut,recHitCut)
    cutTreeMC.TAttach(recHitCut,VertexPtOverHT)
    cutTreeMC.TAttach(VertexPtOverHT,DeadEcalCutMC)
    cutTreeMC.TAttach(DeadEcalCutMC,MHT_METCut)
    cutTreeMC.TAttach(MHT_METCut,OneMuon)
    cutTreeMC.TAttach(OneMuon,PFMTCut30)
    cutTreeMC.TAttach(PFMTCut30,ZMassCut)
#    cutTreeMC.TAttach(PFMTCut30,skim)
    cutTreeMC.TAttach(ZMassCut,jet_e2) # jet n=2
    cutTreeMC.TAttach(ZMassCut,jet_e3) # jet n=3
    cutTreeMC.TAttach(ZMassCut,jet_e4) # jet n=4
    cutTreeMC.TAttach(ZMassCut,jet_g3) # jet n>3
    cutTreeMC.TAttach(ZMassCut,jet_g4) # jet n>4

    cutTreeMC.TAttach(MHT_METCut,DiMuon)
    cutTreeMC.TAttach(DiMuon,ZMass_2Muons)
    cutTreeMC.TAttach(ZMass_2Muons,jet_e2_du) # jet n=2
    cutTreeMC.TAttach(ZMass_2Muons,jet_e3_du) # jet n=3
    cutTreeMC.TAttach(ZMass_2Muons,jet_e4_du) # jet n=4
    cutTreeMC.TAttach(ZMass_2Muons,jet_g3_du) # jet n>3
    cutTreeMC.TAttach(ZMass_2Muons,jet_g4_du) # jet n>4
    
    out.append(AddBinedHist(cutTree = cutTreeMC,
    OP = ("OP_charmEffStudy",genericPSet_mc), cut = ZMassCut,
    htBins = HTBins,TriggerDict = None, lab = "OneMuon_", Muon=True))

  
  return (cutTreeMC,secondJetET,out)


def run_analysis():

  thresholds = {
        "275":100.*275./375.,
        "325":100.*325./375.,
        "375":100.,
        }

  for bin, thresh in thresholds.iteritems():

    print bin,thresh

    vbtfMuonId_cff        = Muon_IDFilter( vbtfmuonidps.ps()  )
    vbtfElectronIdFilter  = Electron_IDFilter( vbtfelectronidWP95ps.ps() )
    ra3PhotonIdFilter     = Photon_IDFilter2012( ra3photonid2012ps.ps() )
    CustomEleID           = Electron_Egamma_Veto()
    CustomMuID            = OL_TightMuID(mu_2012_had.ps())

    #  Change the settings from golden to use the lowest scaled bin.
    default_common.Jets.PtCut=thresh/2.
    cutTree,blah,blah2 = MakeDataTree(thresh)

    def addCutFlowData(a) :
      a.AddMuonFilter("PreCC",CustomMuID)
      a.AddPhotonFilter("PreCC",ra3PhotonIdFilter)
      a.AddElectronFilter("PreCC",CustomEleID)
      a+=cutTree

    # AK5 Calo

    conf_ak5_caloData = deepcopy(defaultConfig)
    conf_ak5_caloData.Ntuple = deepcopy(ak5_calo)
    conf_ak5_caloData.XCleaning = deepcopy(default_cc)
    conf_ak5_caloData.Common = deepcopy(default_common)
    conf_ak5_caloData.Common.print_out()
    anal_ak5_caloData=Analysis("AK5Calo")
    addCutFlowData(anal_ak5_caloData)

    outDir = "../results_"+strftime("%d_%b/")+("%s_"%bin)
    ensure_dir(outDir)

    anal_ak5_caloData.Run(outDir,conf_ak5_caloData,MuEG_2012)

    del conf_ak5_caloData
    del anal_ak5_caloData



if __name__=='__main__':
    run_analysis()
