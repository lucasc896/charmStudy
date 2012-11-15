#!/usr/bin/env python
# encoding: utf-8
"""
make2DPlots.py

Created by Chris Lucas on 2012-11-07.
Copyright (c) 2012 University of Bristol. All rights reserved.
"""

from sys import argv, exit
from generalUtils import *

r.TH1.SetDefaultSumw2()
r.gROOT.SetBatch(True)

inFile = "../rootfiles/anaPlots/outT2bb_anaPlots.root"
inDir = "noCuts_0_10000"
hists = ["SMSvectGenPt",
      "SMSscalGenPt",
      "SMSdPhiLeadJetsGenPt"]

c1 = r.TCanvas()

rFile = r.TFile.Open(inFile)

for hT in hists:
  h = rFile.Get("%s/%s"%(inDir, hT))
  h.Draw("colz")
  c1.Print("%s.pdf"%hT)
