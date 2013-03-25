#!/usr/bin/env python
# encoding: utf-8
"""
parkedPlots.py

Created by Chris Lucas on 2013-03-25.
Copyright (c) 2012 University of Bristol. All rights reserved.
"""

import ROOT as r

r.gROOT.SetBatch(r.kTRUE)

normalise = [False, True][0]
hNames = ["stopGenPtVect", "commHT", "MHT"]
point = ["200_120", "200_190"][1]

parkedHTdirs = ["225_275", "275_325", "325_375", "375_475", "475_575", "575_675", "675_775", "775_875", "875"]
HTdirs = ["275_325", "325_375", "375_475", "475_575", "575_675", "675_775", "775_875", "875"]

iF  = r.TFile.Open("../../rootfiles/anaPlots_225/outT2cc_ISRRW13_%s_anaPlots.root" % point)

c1 = r.TCanvas()

r.gStyle.SetOptStat(0)

for hName in hNames:
   hParked = None
   for d in parkedHTdirs:
      d = "inc_"+d
      for i in range(5):
         h = iF.Get("%s/%s_%d" % (d, hName, i))
         if hParked == None:
            hParked = h.Clone()
         else:
            hParked.Add(h)
   
   hNormal = None
   for d in HTdirs:
      d = "inc_"+d
      for i in range(5):
         h = iF.Get("%s/%s_%d" % (d, hName, i))
         if hNormal == None:
            hNormal = h.Clone()
         else:
            hNormal.Add(h)
   hParked.Draw("hist")
   hNormal.Draw("histsame")
   
   if normalise:
      hParked.Scale(1./hParked.GetEntries())
      hNormal.Scale(1./hNormal.GetEntries())
   
   hNormal.SetLineColor(r.kBlue)
   hNormal.SetLineWidth(2)
   
   hParked.SetLineColor(r.kRed)
   hParked.SetLineWidth(2)
   
   hNormal.SetTitleSize(3,"x")
   hParked.SetTitleOffset(1.3,"y")
   
   hParked.SetTitle("T2cc %s" % point)
   
   lg = r.TLegend(0.58, 0.75, 0.88, 0.88)
   lg.AddEntry(hParked, "Parked HTbinning", "L")
   lg.AddEntry(hNormal, "2012 HTbinning", "L")
   
   lg.SetFillColor(0)
   lg.SetFillStyle(0)
   lg.SetLineColor(0)
   lg.SetLineStyle(0)
   lg.Draw()
   
   r.gPad.SetLeftMargin(0.12)
   r.gPad.SetRightMargin(0.05)
   r.gPad.SetTopMargin(0.05)
   r.gPad.SetBottomMargin(0.12)
   
   c1.Print("compareParked_T2cc_%s_%s_inc_inc%s.pdf" % (point, hName, "_norm" if normalise else ""))
