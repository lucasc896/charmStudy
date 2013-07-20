#!/usr/bin/env python

import setupSUSY


###// Signal Samples //###
from montecarlo.Summer12.FNAL.SMS_T2cc_Filter_SumPt_130GeV_mStop_175to250_mLSP_95to240_8TeV_Pythia6Z_Summer12_START52_V9_FSIM_v1_V17_12_taus_0_scan_T2cc_beamHaloVars_0_clucasJob535 import *
from montecarlo.Summer12.FNAL.SMS_T2cc_NoFilter_mStop_175to250_mLSP_95to240_8TeV_Pythia6Z_Summer12_START52_V9_FSIM_v1_V17_12_taus_0_scan_T2cc_beamHaloVars_0_clucasJob539 import *
from montecarlo.Summer12.FNAL.SMS_MadGraph_2J_T2cc_NoFilter_mStop_100to250_mLSP_20to230_8TeV_Pythia6Zstar_Summer12_START52_V9_FSIM_v1_V17_12_taus_0_scan_T2cc_beamHaloVars_0_pdfSets_clucasJob566 import *
from montecarlo.Summer12.FNAL.SMS_Madgraph_T2cc_NoFilter_combined import *

from montecarlo.Summer12.FNAL.HCP.SMS_T2_Msquark_225to1200_mLSP_0to1200_8TeV_Pythia6Z_Summer12_START52_V9_FSIM_v1_V17_8_taus_0_scan_T2_beamHaloVars_0_yeshaqJob446 import *

from montecarlo.Summer12.FNAL.HCP.SMS_T2tt_FineBin_Mstop_225to1200_mLSP_0to1000_8TeV_Pythia6Z_Summer12_START52_V9_FSIM_v1_V17_8_taus_0_scan_T2tt_beamHaloVars_0_yeshaqJob445 import *

from montecarlo.Summer12.FNAL.HCP.SMS_T1tttt_Mgluino_350to2000_mLSP_0to1650_8TeV_Pythia6Z_Summer12_START52_V9_FSIM_v3_V17_8_taus_0_scan_T1tttt_beamHaloVars_0_yeshaqJob442 import *

from montecarlo.Summer12.FNAL.SMS_MadGraph_Pythia6Zstar_8TeV_T1ttcc_2J_mGo_1000_mStop_310_325_350_375_mLSP_300_Summer12_START52_V9_FSIM_v1_V17_22_taus_0_scan_T1ttcc_beamHaloVars_0_clucasJob676 import *

### some 3jet test samples
from montecarlo.Summer12.FNAL.SMS_8TeV_Pythia6Z_T2cc_3jets_mStop_200_mLSP_190_Summer12_START52_V9_FSIM_v1_V17_12_taus_0_scan_T2cc_beamHaloVars_0_pdfSets_clucasJob595 import *
from montecarlo.Summer12.FNAL.SMS_8TeV_Pythia6Z_T2cc_3jets_mStop_200_mLSP_120_Summer12_START52_V9_FSIM_v1_V17_12_taus_0_scan_T2cc_beamHaloVars_0_pdfSets_clucasJob596 import *

from T2cc_Skims import *
sig_T2cc_175_95 = [T2cc_175_95]
sig_T2cc_175_165 = [T2cc_175_165]


sig_T2cc_filter = [SMS_T2cc_Filter_SumPt_130GeV_mStop_175to250_mLSP_95to240_8TeV_Pythia6Z_Summer12_START52_V9_FSIM_v1_V17_12_taus_0_scan_T2cc_beamHaloVars_0_clucasJob535]
sig_T2cc_noFilter = [SMS_T2cc_NoFilter_mStop_175to250_mLSP_95to240_8TeV_Pythia6Z_Summer12_START52_V9_FSIM_v1_V17_12_taus_0_scan_T2cc_beamHaloVars_0_clucasJob539]
sig_T2cc_2J = [SMS_MadGraph_2J_T2cc_NoFilter_mStop_100to250_mLSP_20to230_8TeV_Pythia6Zstar_Summer12_START52_V9_FSIM_v1_V17_12_taus_0_scan_T2cc_beamHaloVars_0_pdfSets_clucasJob566]

sig_T2cc_full = [SMS_Madgraph_T2cc_NoFilter_combined]

sig_T2 = [SMS_T2_Msquark_225to1200_mLSP_0to1200_8TeV_Pythia6Z_Summer12_START52_V9_FSIM_v1_V17_8_taus_0_scan_T2_beamHaloVars_0_yeshaqJob446]

sig_T2tt = [SMS_T2tt_FineBin_Mstop_225to1200_mLSP_0to1000_8TeV_Pythia6Z_Summer12_START52_V9_FSIM_v1_V17_8_taus_0_scan_T2tt_beamHaloVars_0_yeshaqJob445]
sig_T1tttt = [SMS_T1tttt_Mgluino_350to2000_mLSP_0to1650_8TeV_Pythia6Z_Summer12_START52_V9_FSIM_v3_V17_8_taus_0_scan_T1tttt_beamHaloVars_0_yeshaqJob442]
sig_T1ttcc_300 = [SMS_MadGraph_Pythia6Zstar_8TeV_T1ttcc_2J_mGo_1000_mStop_310_325_350_375_mLSP_300_Summer12_START52_V9_FSIM_v1_V17_22_taus_0_scan_T1ttcc_beamHaloVars_0_clucasJob676]

sig_T2cc_3jet_200_190 = [SMS_8TeV_Pythia6Z_T2cc_3jets_mStop_200_mLSP_190_Summer12_START52_V9_FSIM_v1_V17_12_taus_0_scan_T2cc_beamHaloVars_0_pdfSets_clucasJob595]
sig_T2cc_3jet_200_120 = [SMS_8TeV_Pythia6Z_T2cc_3jets_mStop_200_mLSP_120_Summer12_START52_V9_FSIM_v1_V17_12_taus_0_scan_T2cc_beamHaloVars_0_pdfSets_clucasJob596]


#-------------------------------------------------------#
            ###// MonteCarlo Samples //###
            #//           HCP          //#
#-------------------------------------------------------#

## DY
from montecarlo.Summer12.FNAL.HCP.DYJetsToLL_Yossof_Skim import *
from montecarlo.Summer12.FNAL.HCP.DYJetsToLL_HT_200To400_TuneZ2Star_8TeV_madgraph_Summer12_DR53X_PU_S10_START53_V7A_v1_V17_5_taus_0_clucasJob364  import *
from montecarlo.Summer12.FNAL.HCP.DYJetsToLL_HT_400ToInf_TuneZ2Star_8TeV_madgraph_Summer12_DR53X_PU_S10_START53_V7A_v1_V17_5_taus_0_clucasJob364CombinkarageJob499 import *

mc_DY = [ DYJetsToLL_Yossof_Skim,
      DYJetsToLL_HT_200To400_TuneZ2Star_8TeV_madgraph_Summer12_DR53X_PU_S10_START53_V7A_v1_V17_5_taus_0_clucasJob364,
      DYJetsToLL_HT_400ToInf_TuneZ2Star_8TeV_madgraph_Summer12_DR53X_PU_S10_START53_V7A_v1_V17_5_taus_0_clucasJob364CombinkarageJob499]


## Photons
from montecarlo.Summer12.FNAL.HCP.GJets_HT_200To400_8TeV_madgraph_Summer12_DR53X_PU_S10_START53_V7A_v1_V17_5_taus_0_zmengJob369 import *
from montecarlo.Summer12.FNAL.HCP.GJets_HT_400ToInf_8TeV_madgraph_Summer12_DR53X_PU_S10_START53_V7A_v1_V17_5_taus_0_zmengJob369 import *

mc_Photon = [ GJets_HT_200To400_8TeV_madgraph_Summer12_DR53X_PU_S10_START53_V7A_v1_V17_5_taus_0_zmengJob369,
               GJets_HT_400ToInf_8TeV_madgraph_Summer12_DR53X_PU_S10_START53_V7A_v1_V17_5_taus_0_zmengJob369 ]


## Top
from montecarlo.Summer12.FNAL.HCP.Tbar_s_channel_TuneZ2star_8TeV_powheg_tauola_Summer12_DR53X_PU_S10_START53_V7A_v1_V17_5_taus_0_zmengJob368  import *
from montecarlo.Summer12.FNAL.HCP.Tbar_t_channel_TuneZ2star_8TeV_powheg_tauola_Summer12_DR53X_PU_S10_START53_V7A_v1_V17_5_taus_0_zmengJob368 import *
from montecarlo.Summer12.FNAL.HCP.Tbar_tW_channel_DR_TuneZ2star_8TeV_powheg_tauola_Summer12_DR53X_PU_S10_START53_V7A_v1_V17_5_taus_0_zmengJob368 import *
from montecarlo.Summer12.FNAL.HCP.T_s_channel_TuneZ2star_8TeV_powheg_tauola_Summer12_DR53X_PU_S10_START53_V7A_v1_V17_5_taus_0_zmengJob368 import *
from montecarlo.Summer12.FNAL.HCP.T_t_channel_TuneZ2star_8TeV_powheg_tauola_Summer12_DR53X_PU_S10_START53_V7A_v1_V17_5_taus_0_zmengJob368 import *
from montecarlo.Summer12.FNAL.HCP.T_tW_channel_DR_TuneZ2star_8TeV_powheg_tauola_Summer12_DR53X_PU_S10_START53_V7A_v1_V17_5_taus_0_zmengJob368 import *

mc_sinT = [ Tbar_t_channel_TuneZ2star_8TeV_powheg_tauola_Summer12_DR53X_PU_S10_START53_V7A_v1_V17_5_taus_0_zmengJob368,
            Tbar_s_channel_TuneZ2star_8TeV_powheg_tauola_Summer12_DR53X_PU_S10_START53_V7A_v1_V17_5_taus_0_zmengJob368,
            Tbar_tW_channel_DR_TuneZ2star_8TeV_powheg_tauola_Summer12_DR53X_PU_S10_START53_V7A_v1_V17_5_taus_0_zmengJob368,
            T_s_channel_TuneZ2star_8TeV_powheg_tauola_Summer12_DR53X_PU_S10_START53_V7A_v1_V17_5_taus_0_zmengJob368,
            T_t_channel_TuneZ2star_8TeV_powheg_tauola_Summer12_DR53X_PU_S10_START53_V7A_v1_V17_5_taus_0_zmengJob368,
            T_tW_channel_DR_TuneZ2star_8TeV_powheg_tauola_Summer12_DR53X_PU_S10_START53_V7A_v1_V17_5_taus_0_zmengJob368 ]


## TTbar 
from montecarlo.Summer12.FNAL.HCP.TT_CT10_TuneZ2star_8TeV_powheg_tauola_Summer12_DR53X_PU_S10_START53_V7A_v1_V17_5_taus_0_clucasJob410 import *
from montecarlo.Summer12.FNAL.HCP.TT_CT10_TuneZ2star_8TeV_powheg_tauola_Summer12_DR53X_PU_S10_START53_V7A_v2_V17_5_taus_0_zmengJob404 import *

mc_TTbar = [ TT_CT10_TuneZ2star_8TeV_powheg_tauola_Summer12_DR53X_PU_S10_START53_V7A_v2_V17_5_taus_0_zmengJob404 ]

from montecarlo.Summer12.FNAL.TTJets_FullLeptMGDecays_8TeV_madgraph_Summer12_DR53X_PU_S10_START53_V7A_v2_V17_21_taus_0_clucasJob674 import *



## DiBoson
from montecarlo.Summer12.FNAL.HCP.WW_TuneZ2star_8TeV_pythia6_tauola_Summer12_DR53X_PU_S10_START53_V7A_v1_V17_5_taus_0_zmengJob370 import *
from montecarlo.Summer12.FNAL.HCP.WZ_TuneZ2star_8TeV_pythia6_tauola_Summer12_DR53X_PU_S10_START53_V7A_v1_V17_5_taus_0_zmengJob370 import *
from montecarlo.Summer12.FNAL.HCP.ZZ_TuneZ2star_8TeV_pythia6_tauola_Summer12_DR53X_PU_S10_START53_V7A_v1_V17_5_taus_0_zmengJob370 import *

mc_DiBo = [ ZZ_TuneZ2star_8TeV_pythia6_tauola_Summer12_DR53X_PU_S10_START53_V7A_v1_V17_5_taus_0_zmengJob370,
            WZ_TuneZ2star_8TeV_pythia6_tauola_Summer12_DR53X_PU_S10_START53_V7A_v1_V17_5_taus_0_zmengJob370, 
            WW_TuneZ2star_8TeV_pythia6_tauola_Summer12_DR53X_PU_S10_START53_V7A_v1_V17_5_taus_0_zmengJob370 ]


## WJets
#from montecarlo.Summer12.FNAL.HCP.WJetsToLNu_Yossof_Skim import *
from montecarlo.Summer12.FNAL.HCP.wj_lv_skim_v2 import *
from montecarlo.Summer12.FNAL.HCP.WJetsToLNu_TuneZ2Star_8TeV_madgraph_tarball_Summer12_DR53X_PU_S10_START53_V7A_v1_V17_5_taus_0_clucasJob363 import *
from montecarlo.Summer12.FNAL.HCP.wj_lv_incl_v2_job673 import *
from montecarlo.Summer12.FNAL.HCP.WJetsToLNu_HT_150To200_8TeV_madgraph_Summer12_DR53X_PU_S10_START53_V7C_v1_V17_5_taus_0_agapitosJob663 import *
from montecarlo.Summer12.FNAL.HCP.WJetsToLNu_HT_200To250_8TeV_madgraph_Summer12_DR53X_PU_S10_START53_V7C_v1_V17_5_taus_0_agapitosJob672 import *
from montecarlo.Summer12.FNAL.HCP.WJetsToLNu_HT_250To300_8TeV_madgraph_v2_Summer12_DR53X_PU_S10_START53_V7A_v1_V17_5_taus_0_karageJob498 import *
from montecarlo.Summer12.FNAL.HCP.WJetsToLNu_HT_300To400_8TeV_madgraph_v2_Summer12_DR53X_PU_S10_START53_V7A_v1_V17_5_taus_0_karageJob498 import *
from montecarlo.Summer12.FNAL.HCP.WJetsToLNu_HT_400ToInf_8TeV_madgraph_v2_Summer12_DR53X_PU_S10_START53_V7A_v1_V17_5_taus_0_karageJob498 import *

mc_WJets = [ wj_lv_skim_v2,
            WJetsToLNu_HT_150To200_8TeV_madgraph_Summer12_DR53X_PU_S10_START53_V7C_v1_V17_5_taus_0_agapitosJob663,
            WJetsToLNu_HT_200To250_8TeV_madgraph_Summer12_DR53X_PU_S10_START53_V7C_v1_V17_5_taus_0_agapitosJob672,
            WJetsToLNu_HT_250To300_8TeV_madgraph_v2_Summer12_DR53X_PU_S10_START53_V7A_v1_V17_5_taus_0_karageJob498,
            WJetsToLNu_HT_300To400_8TeV_madgraph_v2_Summer12_DR53X_PU_S10_START53_V7A_v1_V17_5_taus_0_karageJob498,
            WJetsToLNu_HT_400ToInf_8TeV_madgraph_v2_Summer12_DR53X_PU_S10_START53_V7A_v1_V17_5_taus_0_karageJob498 ]

## Zinv
from montecarlo.Summer12.FNAL.HCP.ZJetsToNuNu_50_HT_100_TuneZ2Star_8TeV_madgraph_Summer12_DR53X_PU_S10_START53_V7A_v1_V17_5_taus_0_clucasJob407CombinkarageJob500 import *
from montecarlo.Summer12.FNAL.HCP.ZJetsToNuNu_100_HT_200_TuneZ2Star_8TeV_madgraph_Summer12_DR53X_PU_S10_START53_V7A_v1_V17_5_taus_0_clucasJob365 import *
from montecarlo.Summer12.FNAL.HCP.ZJetsToNuNu_200_HT_400_TuneZ2Star_8TeV_madgraph_Summer12_DR53X_PU_S10_START53_V7A_v1_V17_5_taus_0_clucasJob365CombinkarageJob500 import * 
from montecarlo.Summer12.FNAL.HCP.ZJetsToNuNu_400_HT_inf_TuneZ2Star_8TeV_madgraph_Summer12_DR53X_PU_S10_START53_V7A_v1_V17_5_taus_0_clucasJob365CombinkarageJob500 import *

mc_ZJets = [ ZJetsToNuNu_50_HT_100_TuneZ2Star_8TeV_madgraph_Summer12_DR53X_PU_S10_START53_V7A_v1_V17_5_taus_0_clucasJob407CombinkarageJob500,
            ZJetsToNuNu_100_HT_200_TuneZ2Star_8TeV_madgraph_Summer12_DR53X_PU_S10_START53_V7A_v1_V17_5_taus_0_clucasJob365,
            ZJetsToNuNu_200_HT_400_TuneZ2Star_8TeV_madgraph_Summer12_DR53X_PU_S10_START53_V7A_v1_V17_5_taus_0_clucasJob365CombinkarageJob500,
            ZJetsToNuNu_400_HT_inf_TuneZ2Star_8TeV_madgraph_Summer12_DR53X_PU_S10_START53_V7A_v1_V17_5_taus_0_clucasJob365CombinkarageJob500 ]

## QCD
from montecarlo.Summer12.FNAL.HCP.QCD_Pt_5to15_TuneZ2star_8TeV_pythia6_Summer12_PU_S7_START52_V9_v1_V17_5_taus_0_agapitosJobXXX import *
from montecarlo.Summer12.FNAL.HCP.QCD_Pt_0to5_TuneZ2star_8TeV_pythia6_Summer12_PU_S7_START52_V9_v1_V17_5_taus_0_agapitosJobXXX import *
from montecarlo.Summer12.FNAL.HCP.QCD_Pt_1000to1400_TuneZ2star_8TeV_pythia6_Summer12_PU_S7_START52_V9_v1_V17_5_taus_0_agapitosJobXXX import *
from montecarlo.Summer12.FNAL.HCP.QCD_Pt_1800_TuneZ2star_8TeV_pythia6_Summer12_PU_S7_START52_V9_v1_V17_5_taus_0_agapitosJobXXX import *
from montecarlo.Summer12.FNAL.HCP.QCD_Pt_30to50_TuneZ2star_8TeV_pythia6_Summer12_PU_S7_START52_V9_v1_V17_5_taus_0_agapitosJobXXX import *
from montecarlo.Summer12.FNAL.HCP.QCD_Pt_15to30_TuneZ2star_8TeV_pythia6_Summer12_PU_S7_START52_V9_v1_V17_5_taus_0_agapitosJobXXX import *
from montecarlo.Summer12.FNAL.HCP.QCD_Pt_120to170_TuneZ2star_8TeV_pythia6_Summer12_PU_S7_START52_V9_v1_V17_5_taus_0_agapitosJobXXX import *
from montecarlo.Summer12.FNAL.HCP.QCD_Pt_300to470_TuneZ2star_8TeV_pythia6_Summer12_PU_S7_START52_V9_v1_V17_5_taus_0_agapitosJobXXX import *
from montecarlo.Summer12.FNAL.HCP.QCD_Pt_1400to1800_TuneZ2star_8TeV_pythia6_Summer12_PU_S7_START52_V9_v1_V17_5_taus_0_agapitosJobXXX import *
from montecarlo.Summer12.FNAL.HCP.QCD_Pt_600to800_TuneZ2star_8TeV_pythia6_Summer12_PU_S7_START52_V9_v1_V17_5_taus_0_agapitosJobXXX import *
from montecarlo.Summer12.FNAL.HCP.QCD_Pt_470to600_TuneZ2star_8TeV_pythia6_Summer12_PU_S7_START52_V9_v1_V17_5_taus_0_agapitosJobXXX import *
from montecarlo.Summer12.FNAL.HCP.QCD_Pt_80to120_TuneZ2star_8TeV_pythia6_Summer12_PU_S7_START52_V9_v1_V17_5_taus_0_agapitosJobXXX import *
from montecarlo.Summer12.FNAL.HCP.QCD_Pt_170to300_TuneZ2star_8TeV_pythia6_Summer12_PU_S7_START52_V9_v1_V17_5_taus_0_agapitosJobXXX import *
from montecarlo.Summer12.FNAL.HCP.QCD_Pt_50to80_TuneZ2star_8TeV_pythia6_Summer12_PU_S7_START52_V9_v1_V17_5_taus_0_agapitosJobXXX import *
from montecarlo.Summer12.FNAL.HCP.QCD_Pt_800to1000_TuneZ2star_8TeV_pythia6_Summer12_PU_S7_START52_V9_v1_V17_5_taus_0_agapitosJobXXX import *

mc_QCD = [ QCD_Pt_1000to1400_TuneZ2star_8TeV_pythia6_Summer12_PU_S7_START52_V9_v1_V17_5_taus_0_agapitosJobXXX,
            QCD_Pt_1800_TuneZ2star_8TeV_pythia6_Summer12_PU_S7_START52_V9_v1_V17_5_taus_0_agapitosJobXXX,
            QCD_Pt_120to170_TuneZ2star_8TeV_pythia6_Summer12_PU_S7_START52_V9_v1_V17_5_taus_0_agapitosJobXXX,
            QCD_Pt_300to470_TuneZ2star_8TeV_pythia6_Summer12_PU_S7_START52_V9_v1_V17_5_taus_0_agapitosJobXXX,
            QCD_Pt_1400to1800_TuneZ2star_8TeV_pythia6_Summer12_PU_S7_START52_V9_v1_V17_5_taus_0_agapitosJobXXX,
            QCD_Pt_600to800_TuneZ2star_8TeV_pythia6_Summer12_PU_S7_START52_V9_v1_V17_5_taus_0_agapitosJobXXX,
            QCD_Pt_470to600_TuneZ2star_8TeV_pythia6_Summer12_PU_S7_START52_V9_v1_V17_5_taus_0_agapitosJobXXX,
            QCD_Pt_80to120_TuneZ2star_8TeV_pythia6_Summer12_PU_S7_START52_V9_v1_V17_5_taus_0_agapitosJobXXX,
            QCD_Pt_170to300_TuneZ2star_8TeV_pythia6_Summer12_PU_S7_START52_V9_v1_V17_5_taus_0_agapitosJobXXX,
            QCD_Pt_800to1000_TuneZ2star_8TeV_pythia6_Summer12_PU_S7_START52_V9_v1_V17_5_taus_0_agapitosJobXXX ]


#-------------------------------------------------------#
               ###// Data Samples //###
               #//       HCP        //#
#-------------------------------------------------------#

## Hadronic
from data.Run2012.FNAL.HCP.HTMHT_Run2012B_13Jul2012_v1_V17_5_taus_0_yeshaqJob462 import *
from data.Run2012.FNAL.HCP.HTMHT_Run2012C_24Aug2012_v1_V17_5_taus_0_yeshaqJob468 import *
from data.Run2012.FNAL.HCP.HTMHT_Run2012C_PromptReco_v2_V17_5_taus_0_yeshaqJob472 import *
from data.Run2012.FNAL.BeyondHCP.HTMHT_Run2012D_PromptReco_v1_V17_5_taus_0_yeshaqJob508 import *
from data.Run2012.FNAL.BeyondHCP.HTMHT_Run2012D_PromptReco_v1_V17_5_taus_0_yeshaqJob527 import *
from data.Run2012.FNAL.HCP.HTMHT_Run2012B_13Jul2012_v1_V17_5_taus_0_yeshaqJob358  import *
from data.Run2012.FNAL.HCP.HTMHT_Run2012C_24Aug2012_v1_V17_5_taus_0_yeshaqJob361 import *
from data.Run2012.FNAL.HCP.HTMHT_Run2012C_PromptReco_v2_V17_5_taus_0_yeshaqJob360 import *

from data.Run2012.FNAL.HCP.HT_Run2012A_13Jul2012_v1_V17_5_taus_0_yeshaqJob358 import *
from data.Run2012.FNAL.HCP.HT_Run2012A_recover_06Aug2012_v1_V17_5_taus_0_yeshaqJob359 import *
from data.Run2012.FNAL.HCP.HT_Run2012A_13Jul2012_v1_V17_5_taus_0_yeshaqJob463 import *
from data.Run2012.FNAL.HCP.HT_Run2012A_recover_06Aug2012_v1_V17_5_taus_0_yeshaqJob475 import *

## HTMHT Parked
from data.Run2012.FNAL.BeyondHCP.HTMHTParked_Run2012B_22Jan2013_v1_V17_5_taus_0_yeshaqJob649 import *
from data.Run2012.FNAL.BeyondHCP.HTMHTParked_Run2012C_22Jan2013_v1_V17_5_taus_0_yeshaqJob649 import *
from data.Run2012.FNAL.BeyondHCP.HTMHTParked_Run2012D_22Jan2013_v1_V17_5_taus_0_yeshaqJob649 import *


#data_Had_2012 = [ HTMHT_Run2012B_13Jul2012_v1_V17_5_taus_0_yeshaqJob358,  HTMHT_Run2012C_24Aug2012_v1_V17_5_taus_0_yeshaqJob361,
#                  HTMHT_Run2012C_PromptReco_v2_V17_5_taus_0_yeshaqJob360, HTMHT_Run2012D_PromptReco_v1_V17_5_taus_0_yeshaqJob508,
#                  HTMHT_Run2012B_13Jul2012_v1_V17_5_taus_0_yeshaqJob462, HTMHT_Run2012C_24Aug2012_v1_V17_5_taus_0_yeshaqJob468,
#                  HTMHT_Run2012C_PromptReco_v2_V17_5_taus_0_yeshaqJob472, HTMHT_Run2012D_PromptReco_v1_V17_5_taus_0_yeshaqJob527,
#                  HT_Run2012A_13Jul2012_v1_V17_5_taus_0_yeshaqJob358, HT_Run2012A_recover_06Aug2012_v1_V17_5_taus_0_yeshaqJob359,
#                  HT_Run2012A_13Jul2012_v1_V17_5_taus_0_yeshaqJob463, HT_Run2012A_recover_06Aug2012_v1_V17_5_taus_0_yeshaqJob475 ]

data_Had_2012 = [HTMHT_Run2012B_13Jul2012_v1_V17_5_taus_0_yeshaqJob358]

# HTMHTParked_Run2012B_22Jan2013_v1_V17_5_taus_0_yeshaqJob649.File = HTMHTParked_Run2012B_22Jan2013_v1_V17_5_taus_0_yeshaqJob649.File[0:20]
data_ParkedHad_2012 = [ HTMHTParked_Run2012B_22Jan2013_v1_V17_5_taus_0_yeshaqJob649,
                        HTMHTParked_Run2012C_22Jan2013_v1_V17_5_taus_0_yeshaqJob649,
                        HTMHTParked_Run2012D_22Jan2013_v1_V17_5_taus_0_yeshaqJob649, ]

# TTJets_FullLeptMGDecays_8TeV_madgraph_Summer12_DR53X_PU_S10_START53_V7A_v2_V17_21_taus_0_clucasJob674.File = TTJets_FullLeptMGDecays_8TeV_madgraph_Summer12_DR53X_PU_S10_START53_V7A_v2_V17_21_taus_0_clucasJob674.File[10:20]
mc_test = [ TTJets_FullLeptMGDecays_8TeV_madgraph_Summer12_DR53X_PU_S10_START53_V7A_v2_V17_21_taus_0_clucasJob674 ]
