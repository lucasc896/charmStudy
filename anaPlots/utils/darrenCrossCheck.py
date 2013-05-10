#!/usr/bin/env python
# encoding: utf-8

import ROOT as r

r.gROOT.SetBatch(0)
r.gStyle.SetOptStat(0)

dirs = ["noWeight", "reweight", "reweightGenCuts"]
colors = [r.kBlue, r.kRed, r.kGreen]
samps = ["175_165", "175_95"]
htbins = [275., 325.] + [375.+100*i for i in range(6)]
htNames = []

for i in range(len(htbins)):
   tmp = str(htbins[i])[0:3]
   if (i+1) < len(htbins):
      tmp += "_"+str(htbins[i+1])[0:3]
   htNames.append(tmp)

dirTemp = "smsScan_ge0b_ge2j_AlphaT55_"


c1 = r.TCanvas()

for s in samps:

   lg = r.TLegend(0.6, 0.6, 0.89, 0.89)

   ctr = 0
   for d, col in zip(dirs, colors):
      iF = r.TFile.Open("../../rootfiles/t2ccCompare/%s/AK5Calo_T2cc_had_2012_100.0_bt0.0_MChi-1.0_wLeptVeto_T2cc_%s_0.root" % (d, s))
      hist = None
      for ht in htNames:
         h = iF.Get(dirTemp+ht+"/"+"HT_all")
         if hist == None:
            hist = h.Clone()
         else:
            hist.Add(h)

      hist.Rebin(20)
      hist.SetLineColor(col)
      hist.GetXaxis().SetRangeUser(0., 1200.)
      if ctr == 0:
         hist.Draw("hist")
      else:
         hist.Draw("histsame")
      ctr += 1
      lg.AddEntry(hist, d, "L")

   lg.SetFillColor(0)
   lg.SetLineColor(0)
   lg.Draw()

   c1.Print("out_htCompare_%s.pdf" % s)

   

