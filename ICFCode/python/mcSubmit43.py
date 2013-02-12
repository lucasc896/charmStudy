#!/usr/bin/env python
import setupSUSY
from libFrameworkSUSY import *
#from libbryn import *
from libHadronic import *
from libOneLepton import *
from lib_charmStudy import *
from icf.core import PSet,Analysis
from time import strftime
import icf.utils as Utils
from batchGolden import *
from ra1objectid.vbtfElectronId_cff import *
from ra1objectid.vbtfMuonId_cff import *
from ra1objectid.ra3PhotonId_cff import *
from ra1objectid.ra3PhotonId2012_cff import *
from samples import *
from sys import argv
from utils import *

myDict = {
   "ISR/h_ISRWeight_lastPt_150_100.txt":sig_T2cc_160,
   "ISR/h_ISRWeight_lastPt_300_250.txt":sig_T2cc_300,
   "ISR/h_ISRWeight_lastPt_225_200.txt":sig_T2cc_220_195,
   "ISR/h_ISRWeight_lastPt_225_175.txt":sig_T2cc_220_170,
   "ISR/h_ISRWeight_lastPt_225_150.txt":sig_T2cc_220_145,
}

#for key, val in myDict.iteritems():

ISR_pset = PSet(
JetPt_Low = EffToPSet(readBtagWeight("ISR/h_ISRWeight_lastPt_225_150.txt")).GenPt,
JetPt_High = EffToPSet(readBtagWeight("ISR/h_ISRWeight_lastPt_225_150.txt")).GenEta,
Variation  = EffToPSet(readBtagWeight("ISR/h_ISRWeight_lastPt_225_150.txt")).Pt_Eta_Eff,
)

ISR_reweight = SMS_ISR_Reweighting(ISR_pset.ps())

default_common.Jets.PtCut              = 50.*(325./375.)

cutTreeMC, junkVar,junkVar2            = MakeMCTree(100.*(325./375.),Muon = None)
vbtfMuonId_cff                         = Muon_IDFilter( vbtfmuonidps.ps()  )
ra3PhotonIdFilter                      = Photon_IDFilter2012( ra3photonid2012ps.ps() )
CustomEleID                            = Electron_Egamma_Veto()
CustomMuID                             = OL_TightMuID(mu_2012.ps())


def addCutFlowMC(b) :
  #b.AddWeightFilter("Weight", vertex_reweight)
#  b.AddWeightFilter("Weight", pileup_reweight)
  #b.AddWeightFilter("Weight", ISR_reweight)  

  b.AddMuonFilter("PreCC",CustomMuID)
  b.AddPhotonFilter("PreCC",ra3PhotonIdFilter)
  b.AddElectronFilter("PreCC",CustomEleID)
  b+=cutTreeMC

#AK5 Calo
conf_ak5_caloMC           = deepcopy(defaultConfig)
conf_ak5_caloMC.Ntuple    = deepcopy(ak5_calo)
conf_ak5_caloMC.XCleaning = deepcopy(default_cc)
conf_ak5_caloMC.Common    = deepcopy(default_common)
conf_ak5_caloMC.Common.print_out()
anal_ak5_caloMC           =Analysis("AK5Calo")
addCutFlowMC(anal_ak5_caloMC)


outDir = "../results_"+strftime("%d_%b/325_/")
ensure_dir(outDir)

samp_mc = mc_TTbar + mc_WJets + mc_QCD + mc_DiBo + mc_sinT
samp_sig = sig_T2cc_160 + sig_T2cc_300
samp_sig = sig_T2cc_220_195 + sig_T2cc_220_170 + sig_T2cc_220_145 + sig_T2cc_300 + sig_T2cc_160

anal_ak5_caloMC.Run(outDir,conf_ak5_caloMC,sig_T2cc_noFilter)
