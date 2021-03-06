#!/usr/bin/env python
# encoding: utf-8
"""
bTagPlots.py

Created by Chris Lucas on 2012-10-28.
Copyright (c) 2012 University of Bristol. All rights reserved.
"""

from generalUtils import *
import configuration as conf
from Log import *

r.gROOT.SetBatch(True)


def runOldBtagAna():
   """function to keep old analysis alive"""

   inList = {
         "TTbar_CSVM": ("_375_",
                     ["jet_response_0",
            "bMatched_response_0",
            "cMatched_response_0",
            "lMatched_response_0"],
            "../rootfiles/bTagEff_Study/outTTbar_bTagEff.root",
            [0., .07], [0.001, .2]),

      "TTbar_CSVMVA": ("_375_",
            ["jet_response_1",
            "bMatched_response_1",
            "cMatched_response_1",
            "lMatched_response_1"],
            "../rootfiles/bTagEff_Study/outTTbar_bTagEff.root",
            [0., .07], [0.001, .2]),
        
      "TTbar_JetBProb": ("_375_",
            ["jet_response_3",
            "bMatched_response_3",
            "cMatched_response_3",
            "lMatched_response_3"],
            "../rootfiles/bTagEff_Study/outTTbar_bTagEff.root",
            [0., .03], [0.001, .03]),
        
      "TTbar_JetProb": ("_375_",
            ["jet_response_2",
            "bMatched_response_2",
            "cMatched_response_2",
            "lMatched_response_2"],
            "../rootfiles/bTagEff_Study/outTTbar_bTagEff.root",
            [0., .025], [0.001, 0.03]),
    
      "TTbar_TrkCountHiPu": ("_375_",
            ["jet_response_4",
            "bMatched_response_4",
            "cMatched_response_4",
            "lMatched_response_4"],
            "../rootfiles/bTagEff_Study/outTTbar_bTagEff.root",
            [0., .01], [0.001, 0.01]), 
   }

   for key, val in inList.items():
      histList = []
      rFile = r.TFile.Open(val[2])
      for hist in val[1]:
         histDir = "%s/%s" % (val[0], hist)
         h = rFile.Get(histDir)
         hInt = h.GetEntries()
         h.Scale(1./hInt)
         histList.append(h)

      c1 = Print("bTagEff_%s.pdf" % key)

      multi = multiPlot(hists=histList)
      multi.hTitles = ["All", "bMatched", "cMatched", "lMatched"]

      multi.yRange = val[3]

      if "CSVM" in key:
         multi.xRange = [0., 1.]
         multi.DrawLine([.898, .679, .244])
      elif "Prob" in key:
         multi.xRange = [0., 2.5]
         multi.DrawLine([0.790, 0.545, 0.275])
      elif "BProb" in key:
         multi.xRange = [0., 4.]
      elif "Trk" in key:
         multi.xRange = [0., 4.]
         multi.DrawLine([3.41])
      else:
         mutli.xRange = [0., 1.]

      multi.canvTitle = key
      c1.PrintCanvas(multi.makeMultiPlot())

      #do logY version
      multi.yRange = val[4]
      multi.SetLogy = True

      c1.PrintCanvas(multi.makeMultiPlot())

      del multi
      c1.close()

###-------------------------------------------------------------------###


def runStandPlots(debug=False):

   print "\n >>> Making Analysis Plots\n"

   dirs        = conf.inDirs()
   sinHists    = conf.sinHists()
   sFile       = conf.sigFile()
   sigSamp     = conf.switches()["signalSample"]
   jMulti      = conf.switches()["jetMulti"]
   bMulti      = conf.bMulti()

   if debug: print sFile[sigSamp][0]

   normVal = None
   if conf.switches()["norm"] == "Unitary":
      normVal = 1.

   rFile = r.TFile.Open(sFile[sigSamp][0])
   if debug: print rFile

   c1 = r.TCanvas()

   for hT, pDet in sinHists.iteritems():
      hList = []
      for d in dirs:
         h = rFile.Get("%s/%s" % (d, hT))
         if debug: print h
         hList.append(h)
      aPlot = anaPlot(hList, hT)
      if debug: aPlot.Debug=True
      hTot = aPlot.makeSinglePlot(rebinX=1, norm=normVal)
      del aPlot

      doRanges(hTot, pDet)

      if "TH2D" in str(type(hTot)):
         hTot.Draw("colz")
      elif "TH1D" in str(type(hTot)):
         hTot.Draw("hist")

      if "noCut" not in conf.switches()["HTcuts"]:
         c1.Print("plotDump/bTagEff_%s_%s_%s.png" % (sigSamp, hT, bMulti[0]))
      else:
         c1.Print("plotDump/bTagEff_%s_%s_noCuts.png" % (sigSamp, hT))

   pass

###-------------------------------------------------------------------###


def jetCharmFrac(debug=False):

   dirs     = conf.inDirs()
   inFiles  = conf.comparFiles()
   sFile    = conf.sigFile()

   if debug: Log.debug(str(sFile))

   c1 = r.TCanvas()
   mg = r.TMultiGraph()
   #lg = r.TLegend(0.6, 0.17, 0.85, 0.42)
   lg = r.TLegend(0.6, 0.65, 0.85, 0.88)

   c1.SetCanvasSize(1000, 1000)

   colours = [r.kRed, r.kBlue, r.kViolet]

   for iF, col in zip(inFiles, colours):
      hList = []
      g = r.TGraph(4)
      rFile = r.TFile().Open(sFile[iF][0])
      if debug: Log.debug(">> %s" % iF)

      for i in range(4):
         ctr = 0
         for d in dirs:
            if debug:
               Log.debug("%s/jetFlavourICF_%d" % (d, i))
            h = rFile.Get("%s/jetFlavourICF_%d" % (d, i))
            if debug:
               Log.debug(str(h))
            if ctr == 0: hT = h.Clone()
            else: hT.Add(h)
            ctr+=1
         hList.append(hT)

      ctr1 = 0
      for hT in hList:
         try:
            charmFrac = hT.GetBinContent(5)/hT.GetEntries()
         except ZeroDivisionError:
            Log.warning("Zero Entries in hist")
            charmFrac = 0.
         g.SetPoint(ctr1, ctr1, charmFrac)

         myDict = {
               0: "first",
               1: "second",
               2: "third",
               3: "fourth",
               }

         Log.info("Frac of gen charm %s jets: %.2f (from %d charmJets)" %
                  (myDict[ctr1], charmFrac, hT.GetBinContent(5)))
         ctr1 += 1

      g.Draw("P")
      g.SetMarkerStyle(29)
      g.SetMarkerSize(8)

      entTitle = iF

      # work out a better way of doing this
      #if "195" in iF: g.SetMarkerColor(r.kRed)
      #if "195_pt50" in iF: g.SetMarkerColor(r.kRed-2)
      #if "170" in iF: g.SetMarkerColor(r.kBlue)
      #if "170_pt50" in iF: g.SetMarkerColor(r.kBlue-2)
      #if "145" in iF: g.SetMarkerColor(r.kViolet)
      #if "145_pt50" in iF: g.SetMarkerColor(r.kViolet+2)
      #if "300" in iF: g.SetMarkerColor(r.kGreen-2)
      #if "160" in iF: g.SetMarkerColor(r.kOrange)

      g.SetMarkerColor(col)

      #if "_ISRRW_" in iF and "JES+ve" in iF:
      #   entTitle = "T2cc_JES+ve"
      #elif "_ISRRW_" in iF and "JES-ve" in iF:
      #   entTitle = "T2cc_JES-ve"
      #elif "_ISRRW" in iF:
      #   entTitle = "T2cc_noJES"
      #else: entTitle=iF

#      if "_delta10" in iF:
#         entTitle = "T2cc delta10"

      lg.AddEntry(g, entTitle, "P")
      mg.Add(g)

   mg.SetTitle("Charm Fraction; Jet Rank (pT ordered); genCharm Frac.")
   mg.Draw("AP")

   for i in range(len(hList)):
      bin = mg.GetXaxis().FindBin(i)
      mg.GetXaxis().SetBinLabel(bin, myDict[i])

   mg.GetXaxis().LabelsOption("d")
   mg.GetXaxis().SetLabelSize(0.05)
   mg.GetXaxis().SetTitleOffset(1.35)
   mg.GetYaxis().SetRangeUser(0., 1.0)
   mg.GetYaxis().SetTitleOffset(1.40)

   lg.SetFillColor(0)
   lg.Draw()
   c1.SetGrid(1)
   c1.Print("plotDump/total_charmFrac.%s" % conf.switches()["outFormat"])

###-------------------------------------------------------------------###


def doCharmPhiStudy(debug=False):

   dirs        = conf.inDirs()
   sFile       = conf.sigFile()
   sigSamp     = conf.switches()["signalSample"]
   jMulti      = conf.switches()["jetMulti"]
   inFiles     = conf.comparFiles()

   if debug: print inFiles

   r.gStyle.SetOptStat(0)

   iHists = ["noCLeadJetdR", "noCLeadJetdPhi"]
   colors = [r.kRed, r.kBlue, r.kViolet-1]

   c1 = r.TCanvas()

   for iF in inFiles:
      rFile = r.TFile().Open(sFile[iF][0])

      for iH in iHists:
         lg = r.TLegend(.75, .68, .89, .89)
         hList = []
         for i in range(3):
            ctr = 0
            for d in dirs:
               h = rFile.Get("%s/%s_%d" % (d, iH, i))
               if ctr == 0:
                  hT = h.Clone()
               else:
                  hT.Add(h)
               ctr += 1

            normalise(hT)
            hT.Rebin(5)
            # why do i need this?!
            hList.append(hT)

         hOrder = getHistOrder(hList)

         ctr1 = 0
         for k in hOrder:
            if ctr1 == 0:
               hList[k].Draw("hist")
            else:
               hList[k].Draw("histsame")
            hList[k].SetLineColor(colors[ctr1])
            hList[k].SetLineWidth(2)
            #hList[k].Rebin(5)
            # temp
            if "dPhi" in iH:
               hList[k].GetXaxis().SetTitle("DeltaPhi")
            lg.AddEntry(hList[k], "Jet %d" % ctr1, "L")
            ctr1 += 1

         lg.SetFillColor(0)
         lg.SetLineColor(0)
         lg.Draw()
         c1.Print("plotDump/%s_%s.png" % (iF, iH))
