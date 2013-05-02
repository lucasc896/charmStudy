#!/usr/bin/env python
import setupSUSY
import commands
import itertools
import os

from libFrameworkSUSY import *
from libHadronic import *
from libOneLepton import *
from lib_charmStudy import *
from icf.core import PSet, Analysis
from time import strftime
from batchGolden import *
from ra1objectid.vbtfElectronId_cff import *
from ra1objectid.vbtfMuonId_cff import *
from ra1objectid.ra3PhotonId_cff import *
from ra1objectid.ra3PhotonId2012_cff import *
from samples import *
from utils import *

###-------------------------------------------------------------------###
###-------------------------------------------------------------------###


switches = {
    'sample': ["sig_T2cc_full", "sig_T2cc_3jet_200_120", "mc_TTbar", "mc_WJets",
                "mc_sinT", "mc_DiBo", "mc_QCD", "sig_T2cc_175_95"][-1],
    'sele': ["had", "muon"][:1],
    'thresh': [(30.0, 60.0), (36.7, 73.7), (43.3, 86.7), (50.0, 100.0)][1:],
    'isr': [False, True][1],
    'jes': ["", "-ve", "+ve"][0],
    'pu': [False, True][0],
    'year': [2011, 2012][-1:],
}
bins = {
    30.0: "225",
    36.7: "275",
    43.3: "325",
    50.0: "375",
}

###-------------------------------------------------------------------###


def uniqueStr(sample, sele, thresh, jes, isr, pu, year):

    s = '{sample}_{sel}_{year}_{thr}_jes-{jes}_isr-{isr}'.format(
            sample=sample, sel=sele, thr=thresh[1], jes=jes,
            isr=isr, year=year)

    return s

###-------------------------------------------------------------------###


def run_analysis(sample, sele, thresh, isr, jes, pu, year):

    ISR_pset = PSet(
        JetPt_Low=EffToPSet(readBtagWeight("ISR/2013_ISRWeights_Official.txt")).GenPt,
        JetPt_High=EffToPSet(readBtagWeight("ISR/2013_ISRWeights_Official.txt")).GenEta,
        Variation=EffToPSet(readBtagWeight("ISR/2013_ISRWeights_Official.txt")).Pt_Eta_Eff,
    )

    ISR_reweight = SMS_ISR_Reweighting(ISR_pset.ps())
    JES_reweight = JESUncert(jes)

    default_common.Jets.PtCut   = thresh[0]

    cutTreeMC, junkVar, junkVar2 = MakeMCTree(thresh[1], Muon=None if "had" in sele else True)
    ra3PhotonIdFilter            = Photon_IDFilter2012(ra3photonid2012ps.ps())
    RA4EleID                     = CutBasedElId2012(el_id_2012_RA4.ps())
    CustomMuID                   = OL_TightMuID(mu_2012_had.ps())

    outDir = "results_"+strftime("%d_%b")+"/%s_" % bins[thresh[0]]
    scratchDir = commands.getoutput("echo $_CONDOR_SCRATCH_DIR")
    if len(scratchDir) > 0:
      outDir = scratchDir + "/" + outDir
    ensure_dir(outDir)

    #AK5 Calo
    conf_ak5_caloMC           = deepcopy(defaultConfig)
    conf_ak5_caloMC.Ntuple    = deepcopy(ak5_calo)
    conf_ak5_caloMC.XCleaning = deepcopy(default_cc)
    conf_ak5_caloMC.Common    = deepcopy(default_common)
    conf_ak5_caloMC.Common.print_out()

    anal_ak5_caloMC = Analysis("AK5Calo_{ustr}".format(ustr=uniqueStr(sample,
                                          sele, thresh, jes, isr, pu, year)))

    # add weights and IDs
    if pu:
        anal_ak5_caloMC.AddWeightFilter("Weight", pileup_reweight)
    if isr:
        anal_ak5_caloMC.AddWeightFilter("Weight", ISR_reweight)
    if jes:
        anal_ak5_caloMC.AddJetFilter("PreCC", JES_reweight)
    anal_ak5_caloMC.AddMuonFilter("PreCC", CustomMuID)
    anal_ak5_caloMC.AddPhotonFilter("PreCC", ra3PhotonIdFilter)
    anal_ak5_caloMC.AddElectronFilter("PreCC", RA4EleID)

    anal_ak5_caloMC += cutTreeMC

    anal_ak5_caloMC.Run(outDir, conf_ak5_caloMC, eval(sample))

###-------------------------------------------------------------------###


def main():

    # check ISR weighting only applied to sigSamps
    if switches["isr"] and "sig" not in switches["sample"]:
        print "\n\t>>> ERROR: Cannot run ISR reweighting on non-signal samples\n"
        exit()

    variables_to_iterate = ['sample', 'sele', 'thresh', 'isr', 'jes', 'pu',
                            'year']

    # convert all switch entries to lists
    for key, val in switches.iteritems():
        if "list" not in str(type(val)):
            switches[key] = [val]

    # create list of lists to iterate
    variable_values = [switches[x] for x in variables_to_iterate]
    # create list of every combination of elements from list
    argument_set = list(itertools.product(*variable_values))
    # create list of dictionaries for each unique run config
    arg_list = [dict(zip(variables_to_iterate, x)) for x in argument_set]

    for kwargs in arg_list:
        run_analysis(**kwargs)

###-------------------------------------------------------------------###

if __name__ == '__main__':
    main()
