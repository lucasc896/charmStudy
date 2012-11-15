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

default_common.Jets.PtCut              = 50.*(275./375.)

cutTreeMC, junkVar,junkVar2            = MakeMCTree(100.*(275./375.), Muon=None)
vbtfMuonId_cff                         = Muon_IDFilter( vbtfmuonidps.ps()  )
ra3PhotonIdFilter                      = Photon_IDFilter2012( ra3photonid2012ps.ps() )
CustomEleID                            = Electron_Egamma_Veto()
CustomMuID                             = OL_TightMuID(mu_2012.ps())


def addCutFlowMC(b) :
  #b.AddWeightFilter("Weight", vertex_reweight)
#  b.AddWeightFilter("Weight", pileup_reweight)
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


outDir = "../results_"+strftime("%d_%b/275_")
ensure_dir(outDir)

samp = mc_TTbar + mc_WJets + mc_QCD + mc_DiBo + mc_sinT

anal_ak5_caloMC.Run(outDir,conf_ak5_caloMC,samp)
