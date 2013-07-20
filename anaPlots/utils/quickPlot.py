#!/usr/bin/env python
# encoding: utf-8
"""
parkedPlots.py

Created by Chris Lucas on 2013-03-25.
Copyright (c) 2012 University of Bristol. All rights reserved.
"""

import ROOT as r
from Log import *

r.gROOT.SetBatch(r.kTRUE)

normalise = [False, True][0]
hNames = ["stopGenPtVect", "commHT", "MHT", "tmpDR"][-1:]

HTdirs = ["275_325", "325_375", "375_475", "475_575", "575_675", "675_775", "775_875", "875"][2:]


iF  = r.TFile.Open("/tmp/AK5Calo_mc_test_had_2012_100.0_jes-_isr-False_TTJets_FullLeptMGDecays_8TeV_madgraph_Summer12_DR53X_PU_S10_START53_V7A_v2_V17_21_taus_0_clucasJob674.root")

c1 = r.TCanvas()

r.gStyle.SetOptStat(0)

for hName in hNames:
   myHist = None

   for d in HTdirs:
      d = "before"+d
      for i in range(1):
         print "%s/%s" % (d, hName)
         h = iF.Get("%s/%s" % (d, hName))

         if myHist is None:
            myHist = h.Clone()
         else:
            myHist.Add(h)

   hNormal = None
   myHist.Draw("hist")
   myHist.RebinX(10)

   if normalise:
      myHist.Scale(1./myHist.GetEntries())

   myHist.SetLineColor(r.kRed)
   myHist.SetLineWidth(2)


   myHist.SetTitleOffset(1.3, "y")


   r.gPad.SetLeftMargin(0.12)
   r.gPad.SetRightMargin(0.05)
   r.gPad.SetTopMargin(0.05)
   r.gPad.SetBottomMargin(0.12)

   c1.Print("myQuickHist_%s.pdf" % (hName))