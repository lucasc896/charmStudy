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
  return ["OP_analysisPlots", "OP_charmEffStudy"][0]


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


def makePlotOp(OP = (), cutTree = None, cut = None, label = "", alphaTMode=0.55):
  """docstring for makePlotOp"""
  out = []
  if OP[1] != None:
    plotpset = deepcopy(OP[1])
    plotpset.DirName = label
    op = eval(OP[0]+"(plotpset.ps())")
  else:
    op = eval(OP[0])
  out.append(op)
  if alphaTMode!=None:
    alpha = OP_CommonAlphaTCut(alphaTMode)
    out.append(alpha)
    cutTree.TAttach(cut, alpha)
    cutTree.TAttach(alpha, op)
  else:
    cutTree.TAttach(cut, op)
  return out
  pass

def AddBinedHist(cutTree = None, OP = (), cut = None, htBins = [],TriggerDict = None,lab = "", Muon=None, alphaTCut=None):
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
        pOps = makePlotOp(cutTree = cutTree, OP = OP, cut = upperCut if upper!=10000. else cut, label = "%s%d%s"%(lab,lower, "_%d"%upper if upper else ""), alphaTMode=alphaTCut)
        out.append(pOps)
  return out
  pass



# Common cut definitions
#Avaiable criteria for MC and for Data are at current slightly different Hence the making of two trees
#DataOnly!

# from icf.JetCorrections import *
# corPset =  CorrectionPset("ResidualJetEnergyCorrections.txt")
# corPset =  CorrectionPset("Spring10DataV2_L2L3Residual_AK5PF.txt")
# JetCorrections = JESCorrections( corPset.ps(),True )
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


json = JSONFilter("Json Mask", json_to_pset("Jsons/json_DCSONLY_23Aug_run2012C.txt") )
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



def MakeDataTree(Threshold,Muon = None,Split = None):
  out = []

  runModeName = runMode()


  if re.match("Muon_Add", str(Split)):
      secondJetET = OP_SecondJetOrMuEtCut(Threshold) 
  else:
      secondJetET = OP_SecondJetEtCut(Threshold)
  print "in MakeDataTree threshold: "+str(Threshold)
  HTBins = []
  if int(Threshold) is 100 : HTBins = [375.+100*i for i in range(6)]
  if int(Threshold) is 73 : HTBins = [275.,325.]
  if int(Threshold) is 86 : HTBins = [325.,375.]
  cutTreeData = Tree("Data")
  cutTreeData.Attach(json)
  cutTreeData.TAttach(json,json_ouput)
  cutTreeData.TAttach(json_ouput,NoiseFilt)
  cutTreeData.TAttach(NoiseFilt,MET_Filter)
  cutTreeData.TAttach(MET_Filter,GoodVertexMonster)
  if re.match("Muon_Add", str(Split)):
      cutTreeData.TAttach(GoodVertexMonster,LeadingJetOrMuEta)
      cutTreeData.TAttach(LeadingJetOrMuEta,secondJetET)
      cutTreeData.TAttach(secondJetET,oddJet)
  else:
      cutTreeData.TAttach(GoodVertexMonster,LeadingJetEta)
      cutTreeData.TAttach(LeadingJetEta,secondJetET)
      cutTreeData.TAttach(secondJetET,oddJet)
      
  cutTreeData.TAttach(oddJet,badMuonInJet)
  cutTreeData.TAttach(badMuonInJet,oddElectron)
  cutTreeData.TAttach(oddElectron,oddPhoton)
  cutTreeData.TAttach(oddPhoton,numComElectrons)
  cutTreeData.TAttach(numComElectrons,numComPhotons)
  cutTreeData.TAttach(numComPhotons,Tot_VertexCut)
  if Muon == None:
      cutTreeData.TAttach(Tot_VertexCut,htCut275)
      cutTreeData.TAttach(htCut275,ZeroMuon)
      cutTreeData.TAttach(ZeroMuon,recHitCut)
      cutTreeData.TAttach(recHitCut,VertexPtOverHT)
      cutTreeData.TAttach(VertexPtOverHT,DeadEcalCutData)
      cutTreeData.TAttach(DeadEcalCutData,MHT_METCut)
#      cutTreeData.TAttach(DeadEcalCutData,skim)
#      cutTreeData.TAttach(skim,MHT_METCut)

      cutTreeData.TAttach(DeadEcalCutData,MHT_METReverseCut)

      cutTreeData.TAttach(MHT_METCut,jet_e2) # jet n=2
      cutTreeData.TAttach(MHT_METCut,jet_e3) # jet n=3
      cutTreeData.TAttach(MHT_METCut,jet_e4) # jet n=4
      cutTreeData.TAttach(MHT_METCut,jet_g3) # jet n>3
      cutTreeData.TAttach(MHT_METCut,jet_g4) # jet n>4
      
      if Split == "Had_HTTrig":
          genericPSet_data.mode="Had_HTTrig"
          
          out.append(AddBinedHist(cutTree = cutTreeData,
          OP = ("TauFakeB",genericPSet_data), cut = ZeroMuon,
          htBins = HTBins,TriggerDict = ht_triggers,lab ="preselection_", split = Split) )

          #out.append(AddBinedHist(cutTree = cutTreeData,
          #OP = ("TauFakeB",genericPSet_data), cut = DeadEcalCutData,
          #htBins = HTBins,TriggerDict = ht_triggers,lab ="NoMHToverMET_", split = Split) )
#
          #out.append(AddBinedHist(cutTree = cutTreeData,
          #OP = ("TauFakeB",genericPSet_data), cut = MHT_METReverseCut,
          #htBins = HTBins,TriggerDict = ht_triggers,lab ="ReverseMHToverMET_", split = Split) )
#
          #out.append(AddBinedHist(cutTree = cutTreeData,
          #OP = ("TauFakeB",genericPSet_data), cut = MHT_METCut,
          #htBins = HTBins,TriggerDict = ht_triggers,lab ="", split = Split) )
#
          #out.append(AddBinedHist(cutTree = cutTreeData,
          #OP = ("TauFakeB",genericPSet_data), cut = jet_e2,
          #htBins = HTBins,TriggerDict = ht_triggers,lab ="TwoJet_", split = Split) )
#
          #out.append(AddBinedHist(cutTree = cutTreeData,
          #OP = ("TauFakeB",genericPSet_data), cut = jet_e3,
          #htBins = HTBins,TriggerDict = ht_triggers,lab ="ThreeJet", split = Split) )
#
          #out.append(AddBinedHist(cutTree = cutTreeData,
          #OP = ("TauFakeB",genericPSet_data), cut = jet_e4,
          #htBins = HTBins,TriggerDict = ht_triggers,lab ="FourJet", split = Split) )
#
          #out.append(AddBinedHist(cutTree = cutTreeData,
          #OP = ("TauFakeB",genericPSet_data), cut = jet_g3,
          #htBins = HTBins,TriggerDict = ht_triggers,lab ="MoreThreeJet", split = Split) )
#
          #out.append(AddBinedHist(cutTree = cutTreeData,
          #OP = ("TauFakeB",genericPSet_data), cut = jet_g4,
          #htBins = HTBins,TriggerDict = ht_triggers,lab ="MoreFourJet", split = Split) )

      else:
          genericPSet_data.mode="None"
          out.append(AddBinedHist(cutTree = cutTreeData,
          OP = (runModeName,genericPSet_data), cut = MHT_METCut,
          htBins = HTBins,TriggerDict = triggers,lab ="", Muon = None) )

          out.append(AddBinedHist(cutTree = cutTreeData,
          OP = (runModeName,genericPSet_data), cut = jet_e2,
          htBins = HTBins,TriggerDict = ht_triggers,lab ="TwoJet_", Muon = None) )

          out.append(AddBinedHist(cutTree = cutTreeData,
          OP = (runModeName,genericPSet_data), cut = jet_e3,
          htBins = HTBins,TriggerDict = ht_triggers,lab ="ThreeJet", Muon = None) )

          out.append(AddBinedHist(cutTree = cutTreeData,
          OP = (runModeName,genericPSet_data), cut = jet_e4,
          htBins = HTBins,TriggerDict = ht_triggers,lab ="FourJet", Muon = None) )

          out.append(AddBinedHist(cutTree = cutTreeData,
          OP = (runModeName,genericPSet_data), cut = jet_g3,
          htBins = HTBins,TriggerDict = ht_triggers,lab ="MoreThreeJet", Muon = None) )

          out.append(AddBinedHist(cutTree = cutTreeData,
          OP = (runModeName,genericPSet_data), cut = jet_g4,
          htBins = HTBins,TriggerDict = ht_triggers,lab ="MoreFourJet", Muon = None) )

      #print "genericPSet_data.mode := "+str(genericPSet_data.mode)
      #print "genericPSet_data.doZinvFromDY: "+str(genericPSet_data.doZinvFromDY)
  else:
    pass
      #if Split is None:
      #    genericPSet_data.mode="None"
      #elif re.match("Muon_Add", str(Split)):
      #    genericPSet_data.mode="Muon_Add"
      #else:
      #    genericPSet_data.mode=Split
#
      #if Split == "Muon_SingleMuTrig":
      #    cutTreeData.TAttach(Tot_VertexCut,htCut275)
      #    cutTreeData.TAttach(htCut275,Mu45PtCut)
      #    cutTreeData.TAttach(Mu45PtCut,minDRMuonJetCut)
      #    cutTreeData.TAttach(minDRMuonJetCut,recHitCut)
      #    cutTreeData.TAttach(recHitCut,VertexPtOverHT)
      #    cutTreeData.TAttach(VertexPtOverHT,DeadEcalCutData)
      #    cutTreeData.TAttach(DeadEcalCutData,MHT_METCut)
#
      #    cutTreeData.TAttach(MHT_METCut,OneMuon)
      #    cutTreeData.TAttach(OneMuon,PFMTCut30)
      #    cutTreeData.TAttach(PFMTCut30,ZMassCut)
      #    cutTreeData.TAttach(ZMassCut,jet_e2) # jet n=2
      #    cutTreeData.TAttach(ZMassCut,jet_e3) # jet n=3
      #    cutTreeData.TAttach(ZMassCut,jet_e4) # jet n=2
      #    cutTreeData.TAttach(ZMassCut,jet_g3) # jet n>3
      #    cutTreeData.TAttach(ZMassCut,jet_g4) # jet n>4
      #
      #    cutTreeData.TAttach(MHT_METCut,DiMuon)
      #    cutTreeData.TAttach(DiMuon,ZMass_2Muons)
      #    cutTreeData.TAttach(ZMass_2Muons,jet_e2_du) # jet n=2
      #    cutTreeData.TAttach(ZMass_2Muons,jet_e3_du) # jet n=3
      #    cutTreeData.TAttach(ZMass_2Muons,jet_e4_du) # jet n=4
      #    cutTreeData.TAttach(ZMass_2Muons,jet_g3_du) # jet n>3
      #    cutTreeData.TAttach(ZMass_2Muons,jet_g4_du) # jet n>4
      
	  #out.append(AddBinedHist(cutTree = cutTreeData,
    #      OP = ("TauFakeB",genericPSet_data), cut = ZMassCut,
    #      htBins = HTBins,TriggerDict = single_mu_triggers,lab = "OneMuon_", split = genericPSet_data.mode ) )
#
	  #out.append(AddBinedHist(cutTree = cutTreeData,
    #      OP = ("TauFakeB",genericPSet_data), cut = jet_e2,
    #      htBins = HTBins,TriggerDict = single_mu_triggers,lab = "TwoJet_OneMuon_", split = genericPSet_data.mode ) )
#
	  #out.append(AddBinedHist(cutTree = cutTreeData,
    #      OP = ("TauFakeB",genericPSet_data), cut = jet_e3,
    #      htBins = HTBins,TriggerDict = single_mu_triggers,lab = "ThreeJet_OneMuon_", split = genericPSet_data.mode ) )
#
	  #out.append(AddBinedHist(cutTree = cutTreeData,
    #      OP = ("TauFakeB",genericPSet_data), cut = jet_e4,
    #      htBins = HTBins,TriggerDict = single_mu_triggers,lab = "FourJet_OneMuon_", split = genericPSet_data.mode ) )
#
	  #out.append(AddBinedHist(cutTree = cutTreeData,
    #      OP = ("TauFakeB",genericPSet_data), cut = jet_g3,
    #      htBins = HTBins,TriggerDict = single_mu_triggers,lab = "MoreThreeJet_OneMuon_", split = genericPSet_data.mode ) )
#
	  #out.append(AddBinedHist(cutTree = cutTreeData,
    #      OP = ("TauFakeB",genericPSet_data), cut = jet_g4,
    #      htBins = HTBins,TriggerDict = single_mu_triggers,lab = "MoreFourJet_OneMuon_", split = genericPSet_data.mode ) )


    #      out.append(AddBinedHist(cutTree = cutTreeData,
    #      OP = ("TauFakeB",genericPSet_data), cut = ZMass_2Muons,
    #      htBins = HTBins,TriggerDict = single_mu_triggers,lab = "DiMuon_", split = genericPSet_data.mode ) )
#
    #      out.append(AddBinedHist(cutTree = cutTreeData,
    #      OP = ("TauFakeB",genericPSet_data), cut = jet_e2_du,
    #      htBins = HTBins,TriggerDict = single_mu_triggers,lab = "TwoJet_DiMuon_", split = genericPSet_data.mode ) )
#
    #      out.append(AddBinedHist(cutTree = cutTreeData,
    #      OP = ("TauFakeB",genericPSet_data), cut = jet_e3_du,
    #      htBins = HTBins,TriggerDict = single_mu_triggers,lab = "ThreeJet_DiMuon_", split = genericPSet_data.mode ) )
#
    #      out.append(AddBinedHist(cutTree = cutTreeData,
    #      OP = ("TauFakeB",genericPSet_data), cut = jet_e4_du,
    #      htBins = HTBins,TriggerDict = single_mu_triggers,lab = "FourJet_DiMuon_", split = genericPSet_data.mode ) )
#
    #      out.append(AddBinedHist(cutTree = cutTreeData,
    #      OP = ("TauFakeB",genericPSet_data), cut = jet_g3_du,
    #      htBins = HTBins,TriggerDict = single_mu_triggers,lab = "MoreThreeJet_DiMuon_", split = genericPSet_data.mode ) )
#
    #      out.append(AddBinedHist(cutTree = cutTreeData,
    #      OP = ("TauFakeB",genericPSet_data), cut = jet_g4_du,
    #      htBins = HTBins,TriggerDict = single_mu_triggers,lab = "MoreFourJet_DiMuon_", split = genericPSet_data.mode ) )
##
     #     print "mode  data="+str(genericPSet_data.mode)+" "+str(Split)
     # elif Split == "Muon_Add_SingleMuTrigPlateau":
     #     cutTreeData.TAttach(Tot_VertexCut,htTakeMuCut275)
     #     if int(Threshold) is 73:
     #         cutTreeData.TAttach(htTakeMuCut275,Mu50PtCut_LowHT275_MuTrigPlateau)
     #         cutTreeData.TAttach(Mu50PtCut_LowHT275_MuTrigPlateau,minDRMuonJetCut)
     #     elif int(Threshold) is 86:
     #         cutTreeData.TAttach(htTakeMuCut275,Mu50PtCut_LowHT325_MuTrigPlateau)
     #         cutTreeData.TAttach(Mu50PtCut_LowHT325_MuTrigPlateau,minDRMuonJetCut)
     #     elif int(Threshold) is 100:
     #         cutTreeData.TAttach(htTakeMuCut275,Mu50PtCut_HigHT_MuTrigPlateau)
     #         cutTreeData.TAttach(Mu50PtCut_HigHT_MuTrigPlateau,minDRMuonJetCut)
     #     cutTreeData.TAttach(minDRMuonJetCut,recHitCut)
     #     cutTreeData.TAttach(recHitCut,VertexPtOverHT)
     #     cutTreeData.TAttach(VertexPtOverHT,DeadEcalCutData)
     #     cutTreeData.TAttach(DeadEcalCutData,MHTTakeMu_METTakeMuCut)
#
     #     cutTreeData.TAttach(MHTTakeMu_METTakeMuCut,OneMuon)
     #     cutTreeData.TAttach(OneMuon,PFMTCut30)
     #     cutTreeData.TAttach(PFMTCut30,ZMassCut)
#
     #     cutTreeData.TAttach(MHT_METCut,DiMuon)
     #     cutTreeData.TAttach(DiMuon,ZMass_2Muons)
      
	  #out.append(AddBinedHist(cutTree = cutTreeData,
    #      OP = ("TauFakeB",genericPSet_data), cut = ZMassCut,
    #      htBins = HTBins,TriggerDict = single_mu_triggers,lab = "OneMuon_", split = genericPSet_data.mode ) )
#
    #      out.append(AddBinedHist(cutTree = cutTreeData,
    #      OP = ("TauFakeB",genericPSet_data), cut = ZMass_2Muons,
    #      htBins = HTBins,TriggerDict = single_mu_triggers,lab = "DiMuon_", split = genericPSet_data.mode ) )
    #      print "mode  data="+str(genericPSet_data.mode)+" "+str(Split)
    #      print "genericPSet_data.doZinvFromDY: "+str(genericPSet_data.doZinvFromDY)
    #  else:
    #      print "do nothing: here data, single/di muon selection"


#      cutTreeData.TAttach(minDRMuonJetCut,DiMuon)
#      cutTreeData.TAttach(DiMuon,ZMass_2Muons)

      # avobe here does one big inclusive bin!
      # Now lets start binning in HT bins
      # So we can HADD the files at the end and get a chorent set to save the book keeping nightmare:
      # we arrange the HT bins so they are not repoduced though out threshold runs.

#      out.append(AddBinedHist(cutTree = cutTreeData,
#      OP = ("TauFakeB",genericPSet_data), cut = ZMass_2Muons,
#      htBins = HTBins,TriggerDict = (mu_triggers if Split == "Muon_All" else triggers),lab = "DiMuon_") ) 
    
  return (cutTreeData,secondJetET,out)


def MakeMCTree(Threshold, Muon = None, Split = None):
  out = []

  HTBins = []

  alphaTVal = 0.55
  
  if int(Threshold) is 100 and Split == None : HTBins = [375+100*i for i in range(6)]
  if int(Threshold) is 100 and Split == "Had_One" : HTBins = [375+100*i for i in range(4)]
  if int(Threshold) is 100 and Split == "Had_Two" : HTBins = [675+100*i for i in range(3)]
  if int(Threshold) is 100 and Split == "Muon_One" : HTBins = [375,475]
  if int(Threshold) is 100 and Split == "Muon_Two" : HTBins = [475,575,675]
  if int(Threshold) is 100 and Split == "Muon_Three" : HTBins = [675,775,875]
  if int(Threshold) is 73 : HTBins = [275.,325.]
  if int(Threshold) is 86 : HTBins = [325.,375.]
  if int(Threshold) is 60 :
    HTBins = [225.,275.]
    alphaTVal = 0.6
 
  ### add incl binning for thresh=100, split==None
  HTBins_inc = [0.,10000.]

  ### override the threshold arguement
  #Threshold=Threshold*1.1
  #Threshold=40.

  if Muon!=None:
      secondJetET = OP_SecondJetOrMuEtCut(Threshold)
  else:
      secondJetET = OP_SecondJetEtCut(Threshold)

  cutTreeMC = Tree("MC")

  runModeName = runMode()

  SMScut_ = None

  #SMScut_ = SMSdMassCut_10
  #SMScut_ = SMSdMassCut_20
  #SMScut_ = SMSdMassCut_30
  #SMScut_ = SMSdMassCut_40
  #SMScut_ = SMSdMassCut_60
  #SMScut_ = SMSdMassCut_80

  #SMScut_ = SMSMassCut_100_20
  #SMScut_ = SMSMassCut_100_40
  #SMScut_ = SMSMassCut_100_60
  #SMScut_ = SMSMassCut_100_70
  #SMScut_ = SMSMassCut_100_80
  #SMScut_ = SMSMassCut_100_90

  #SMScut_ = SMSMassCut_175_95
  #SMScut_ = SMSMassCut_175_115
  #SMScut_ = SMSMassCut_175_135
  #SMScut_ = SMSMassCut_175_145
  #SMScut_ = SMSMassCut_175_155
  #SMScut_ = SMSMassCut_175_165

  #SMScut_ = SMSMassCut_200_120
  #SMScut_ = SMSMassCut_200_190

  #SMScut_ = SMSMassCut_250_20
  #SMScut_ = SMSMassCut_250_40
  #SMScut_ = SMSMassCut_250_60
  #SMScut_ = SMSMassCut_250_70
  #SMScut_ = SMSMassCut_250_80
  #SMScut_ = SMSMassCut_250_90

  #SMScut_ = SMSStopMassCut_100
  #SMScut_ = SMSStopMassCut_175
  #SMScut_ = SMSStopMassCut_250


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
      cutTreeMC.Attach(count_total)

      if SMScut_:
        cutTreeMC.TAttach(count_total, SMScut_)
        cutTreeMC.TAttach(SMScut_,jet_ge2)
      else:
        cutTreeMC.TAttach(count_total,jet_ge2)

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
    
    if int(Threshold) is 100:
      out.append(AddBinedHist(cutTree = cutTreeMC,
      OP = (runModeName,genericPSet_mc), cut =  SMScut_ if SMScut_ else count_total,
      htBins = HTBins_inc, TriggerDict = None, lab ="noCuts_", Muon=False, alphaTCut=None))
      
    out.append(AddBinedHist(cutTree = cutTreeMC,
    OP = (runModeName,genericPSet_mc), cut = MHT_METCut,
    htBins = HTBins, TriggerDict = None, lab ="inc_", Muon=False, alphaTCut=alphaTVal))
    
    out.append(AddBinedHist(cutTree = cutTreeMC,
    OP = (runModeName,genericPSet_mc), cut = jet_le3,
    htBins = HTBins, TriggerDict = None, lab ="le3j_", Muon=False, alphaTCut=alphaTVal ))
    
    out.append(AddBinedHist(cutTree = cutTreeMC,
    OP = (runModeName,genericPSet_mc), cut = jet_ge4,
    htBins = HTBins, TriggerDict = None, lab ="ge4j_", Muon=False, alphaTCut=alphaTVal))

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



vertex_reweight_PUS4 = GoodVertexReweighting(
PSet(GoodVertexWeights = [1.0, 0.071182041228993354, 0.3788533298983548, 0.70212224756460717, 0.95912926863057879,
 1.1063323506805849, 1.1826257455177471, 1.2297382718782017, 1.2772830447358376, 1.4266446590805815, 1.5732065775636328, 
 1.8401056375971667, 2.1784909215394999, 2.506266882602076, 3.3335988825191176, 4.687787057503483, 6.8602191807881647, 
 11.198474011060968, 14.883466002768214, 20.878255333866864, 1.0, 1.0, 1.0, 1.0, 1.0]).ps())

vertex_reweight_PUS6 = GoodVertexReweighting(
PSet(GoodVertexWeights =[1.0, 0.6747792521746856, 1.0448420078821972, 1.3055015002285708, 1.3983895957384924, 1.4093911155782819, 1.3850308438481276, 1.3018072225453758, 1.1623455679439036, 1.0517773707737472, 0.89838694986924372, 0.76765214151467354, 0.63185640954246791, 0.49262105848611853, 0.42787145593782405, 0.3847054078776958, 0.35778382190253444, 0.34148368315539618, 0.28535617241618649, 0.24963682196802897, 0.15231738209843554, 0.10766396055685283, 0.066294358386045707, 0.039350814964675719, 0.071293966061105704] ).ps())

vertex_reweight_PUS_MC7TeVData8TeV = GoodVertexReweighting(
PSet(GoodVertexWeights = [ 0.0, 0.00188151, 0.00878233, 0.0420452, 0.098297, 0.166391, 0.323089, 0.551869, 0.767407, 1.39418, 1.95776, 3.26008, 5.06286, 8.15389, 16.6012, 27.5545, 49.8479, 64.8275, 229.833, 592.366, 1501.81, 1812.08, 4010.64, 3220.56, 3192.77, 2644.38, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0,0, 0, 0, 0, 0 ]).ps())

#For onemuon 3.9/fb golden 15June2012
vertex_reweight_PUS_MC8TeVData8TeV = GoodVertexReweighting(
PSet(GoodVertexWeights = [ 0., 2.13881, 6.19557, 4.38383, 9.65705, 10.5397, 11.0608, 8.87249, 6.3986, 5.61017, 4.59699, 3.81157, 2.22687, 2.00172, 1.59634, 1.3718, 0.938535, 0.81193, 0.671217, 0.502157, 0.432198, 0.338219, 0.279123, 0.23935, 0.191275, 0.148133, 0.104935, 0.106231, 0.0679703, 0.0599905, 0.0580532, 0.0279169, 0.0253552, 0.0384467, 0.00802036, 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., ]).ps())

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

