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
hNames = ["stopGenPtVect", "commHT", "MHT"]
point = ["200_120", "200_190"][0]

parkedHTdirs = ["225_275", "275_325", "325_375", "375_475", "475_575", "575_675", "675_775", "775_875", "875"]
HTdirs = ["275_325", "325_375", "375_475", "475_575", "575_675", "675_775", "775_875", "875"]

trigEff = {
   "225": 0.82,
   "275": 0.93,
   "325": 0.97,
   "375": 0.99
}

iF  = r.TFile.Open("../../rootfiles/anaPlots_225/outT2cc_%s_anaPlots.root" % point)

c1 = r.TCanvas()

r.gStyle.SetOptStat(0)

for hName in hNames:
   hParked = None
   hParkedScaled = None

   for d in parkedHTdirs:
      d = "inc_"+d
      for i in range(5):
         h = iF.Get("%s/%s_%d" % (d, hName, i))

         if hParked is None:
            hParked = h.Clone()
         else:
            hParked.Add(h)

         # apply trigger scaling - currently on 225 bin!
         if "225" in d:
            h.Scale(trigEff["225"])

         if hParkedScaled is None:
            hParkedScaled = h.Clone()
         else:
            hParkedScaled.Add(h)

   hNormal = None

   for d in HTdirs:
      d = "inc_"+d
      for i in range(5):
         h = iF.Get("%s/%s_%d" % (d, hName, i))
         if hNormal is None:
            hNormal = h.Clone()
         else:
            hNormal.Add(h)

   hParked.Draw("hist")
   hNormal.Draw("histsame")
   hParkedScaled.Draw("histsame")

   #hParkedScaled.Scale(0.82)

   if normalise:
      hParked.Scale(1./hParked.GetEntries())
      hNormal.Scale(1./hNormal.GetEntries())
      hParkedScaled.Scale(1./hParkedScaled.GetEntries())

   hNormal.SetLineColor(r.kBlue)
   hNormal.SetLineWidth(2)

   hParked.SetLineColor(r.kRed)
   hParked.SetLineWidth(2)

   hParkedScaled.SetLineColor(r.kRed)
   hParkedScaled.SetLineWidth(2)
   hParkedScaled.SetLineStyle(2)

   hNormal.SetTitleSize(3, "x")
   hParked.SetTitleOffset(1.3, "y")

   #Log.info(hName)
   #Log.info("Normal: %s" % hNormal.Integral())
   #Log.info("Parked: %s" % hParked.Integral())

   hParked.SetTitle("T2cc %s" % point)

   lg = r.TLegend(0.52, 0.72, 0.94, 0.88)
   lg.AddEntry(hNormal, "2012 HTbinning - %d evts" % hNormal.Integral(), "L")
   lg.AddEntry(hParked, "Parked HTbinning - %d evts" % hParked.Integral(), "L")
   lg.AddEntry(hParkedScaled, "Parked HTbinning * trig. eff. - %d evts" % hParkedScaled.Integral(), "L")

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
