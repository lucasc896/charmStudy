#!/usr/bin/env python
# encoding: utf-8



"""
jetMeanDeltaM.py

Created by Chris Lucas on 2013-03-12.
Copyright (c) 2012 University of Bristol. All rights reserved.
"""

import ROOT as r


dirs = ["ge4j_275_325", "ge4j_325_375", "ge4j_375_475", "ge4j_475_575", "ge4j_575_675", "ge4j_675_775", "ge4j_775_875", "ge4j_875"]
dirs_no = ["noCuts_0_10000"]
delta = [10, 20, 30, 40, 60, 80]

g1 = r.TGraph(len(delta))
g2 = r.TGraph(len(delta))
c1 = r.TCanvas()

r.gPad.SetRightMargin(0.05)
r.gPad.SetLeftMargin(0.09)
r.gPad.SetTopMargin(0.08)
r.gPad.SetBottomMargin(0.09)

ctr=0
for dVal in delta:

   iF = r.TFile.Open("../../rootfiles/anaPlots_225/outT2cc_ISRRW13_delta%d_anaPlots.root"%dVal)
   
   hT = None
   for d in dirs:
      h = iF.Get("%s/jetPt_0"%d)
      if hT==None:
         hT = h.Clone()
      else:
         hT.Add(h)
   
   print dVal, hT.GetMean()
   g1.SetPoint( ctr, dVal, hT.GetMean() )

   hT = None
   for d in dirs_no:
      h = iF.Get("%s/jetPt_0"%d)
      if hT==None:
         hT = h.Clone()
      else:
         hT.Add(h)
   
   print dVal, hT.GetMean()
   g2.SetPoint( ctr, dVal, hT.GetMean() )
   
   ctr+=1

g1.SetMarkerSize(3)
g1.SetMarkerStyle(34)
g1.SetMarkerColor(r.kGreen-3)
c1.SetGridy(1)

#g1.Draw("AP")

g2.SetMarkerSize(3)
g2.SetMarkerStyle(34)
g2.SetMarkerColor(r.kBlue-3)

g2.SetTitle("")
#g2.GetXaxis().SetTitle("deltaM (GeV)")
#g2.GetYaxis().SetTitle("Mean Jet Pt (GeV)")
#g2.Draw("AP")

mg = r.TMultiGraph()
mg.Add(g1)
mg.Add(g2)

mg.Draw("AP")

mg.SetTitle("")
mg.GetXaxis().SetTitle("deltaM (GeV)")
mg.GetYaxis().SetTitle("Mean Jet Pt (GeV)")

c1.Print("meanJetPt.pdf")
