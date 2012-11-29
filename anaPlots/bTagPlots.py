#!/usr/bin/env python
# encoding: utf-8
"""
bTagPlots.py

Created by Chris Lucas on 2012-10-28.
Copyright (c) 2012 University of Bristol. All rights reserved.
"""

from sys import argv
from generalUtils import *
import configuration as conf

r.gROOT.SetBatch(True)

def runOldBtagAna():
   """function to keep old analysis alive"""

   if len(argv) > 1:
      cmd = argv[1]

   inList = {
      "TTbar_CSVM":("_375_",
        ["jet_response_0",
        "bMatched_response_0",
        "cMatched_response_0",
        "lMatched_response_0"],
        "../rootfiles/bTagEff_Study/outTTbar_bTagEff.root",
        [0., .07], [0.001, .2]),

      "TTbar_CSVMVA":("_375_",
        ["jet_response_1",
            "bMatched_response_1",
            "cMatched_response_1",
            "lMatched_response_1"],
            "../rootfiles/bTagEff_Study/outTTbar_bTagEff.root",
            [0., .07], [0.001, .2]),
        
      "TTbar_JetBProb":("_375_",
            ["jet_response_3",
            "bMatched_response_3",
            "cMatched_response_3",
            "lMatched_response_3"],
            "../rootfiles/bTagEff_Study/outTTbar_bTagEff.root",
            [0., .03], [0.001, .03]),
        
      "TTbar_JetProb":("_375_",
            ["jet_response_2",
            "bMatched_response_2",
            "cMatched_response_2",
            "lMatched_response_2"],
            "../rootfiles/bTagEff_Study/outTTbar_bTagEff.root",
            [0., .025], [0.001, 0.03]),
    
      "TTbar_TrkCountHiPu":("_375_",
            ["jet_response_4",
            "bMatched_response_4",
            "cMatched_response_4",
            "lMatched_response_4"],
            "../rootfiles/bTagEff_Study/outTTbar_bTagEff.root",
            [0., .01], [0.001, 0.01]), 
    }
    
    
   for key, val in inList.items():
      histList = []
      rFile = r.TFile.Open( val[2] )
      for hist in val[1]:
         histDir = "%s/%s"%(val[0], hist)
         h = rFile.Get( histDir )
         hInt = h.GetEntries()
         h.Scale(1./hInt)
         histList.append( h )
   
      c1 = Print("bTagEff_%s.pdf"%key)
      
      multi = multiPlot( hists=histList )
      multi.hTitles = ["All", "bMatched", "cMatched", "lMatched"]
   
      multi.yRange = val[3]
   
      if "CSVM" in key:
         multi.xRange = [0., 1.]
         multi.DrawLine([.898,.679,.244])
      elif "Prob" in key:
         multi.xRange = [0., 2.5]
         multi.DrawLine([0.790,0.545,0.275])
      elif "BProb" in key:
         multi.xRange = [0., 4.]
      elif "Trk" in key:
         multi.xRange = [0., 4.]
         multi.DrawLine([3.41])
      else:
         mutli.xRange = [0., 1.]
   
      multi.canvTitle = key
      c1.PrintCanvas( multi.makeMultiPlot() )
      
      #do logY version
      multi.yRange = val[4]
      multi.SetLogy = True
      
      c1.PrintCanvas( multi.makeMultiPlot() )
      
      del multi
      c1.close()


def runStandPlots(debug=False):
   
   print "\n >>> Making Analysis Plots\n"

   dirs        = conf.inDirs()
   hists       = conf.anaHists()
   sinHists    = conf.sinHists()
   sFile       = conf.sigFile()
   sigSamp     = conf.switches()["signalSample"]
   histRanges  = conf.histRanges()
   jMulti      = conf.switches()["jetMulti"]
   bMulti      = conf.bMulti()

   if debug: print sFile[sigSamp][0]
  
   normVal = None
   if conf.switches()["norm"]:
      normVal = 1.

   rFile = r.TFile.Open(sFile[sigSamp][0])
   if debug: print rFile

   c1 = r.TCanvas()

   for hT in sinHists:
      hList=[]
      for d in dirs:
         h = rFile.Get("%s/%s"%(d, hT))
         if debug: print h
         hList.append(h)
      aPlot = anaPlot(hList, hT)
      if debug: aPlot.Debug=True
      hTot = aPlot.makeSinglePlot(1, normVal)
      del aPlot
      
      hTot.Draw("hist")
      if hT in histRanges:
         ranges = histRanges[hT]
         hTot.GetXaxis().SetRangeUser(ranges[0], ranges[1]) 
      


      if "noCut" not in conf.switches()["HTcuts"]:
         c1.Print("plotDump/bTagEff_%s_%s_%s.png"%(sigSamp, hT, bMulti[0]))
      else:
         c1.Print("plotDump/bTagEff_%s_%s_noCuts.png"%(sigSamp, hT))

   pass


def jetFlavourQuick(debug=False):

   dirs        = conf.inDirs()
   hists       = conf.anaHists()
   sinHists    = conf.sinHists()
   sFile       = conf.sigFile()
   sigSamp     = conf.switches()["signalSample"]
   histRanges  = conf.histRanges()

   if debug: print sFile[sigSamp][0]
  
   normVal = None
   if conf.switches()["norm"]:
      normVal = 1.

   c1 = r.TCanvas()

   
   inFiles=["T2cc_220_195","T2cc_220_170","T2cc_220_145"]
   inFiles=["T2cc_220_195_pt50","T2cc_220_170_pt50","T2cc_220_145_pt50"]
   inFiles=["T2cc_220_145", "T2cc_220_145_pt50"]

   mg = r.TMultiGraph()

   lg = r.TLegend(0.6, 0.17, 0.85, 0.42)

   for iF in inFiles:
      hList=[]
      rFile = r.TFile().Open(sFile[iF][0])
      print "\n>> %s"%iF
      for i in range(4):
         ctr=0
         for d in dirs:
            if debug: print "%s/jetFlavourICF_%d"%(d,i)
            h = rFile.Get("%s/jetFlavourICF_%d"%(d,i))
            if ctr==0: hT = h.Clone()
            else: hT.Add(h)
            ctr+=1
         hList.append(hT)
   
      g = r.TGraph(4)

      ctr1=0
      for hT in hList:   
         charmFrac = hT.GetBinContent(5)/hT.GetEntries()
         g.SetPoint(ctr1, ctr1, charmFrac)

         myDict = {
               0:"first",
               1:"second",
               2:"third",
               3:"fourth",
               }
         
         print "Frac of gen charm %s jets: %f.2"%(myDict[ctr1], charmFrac) 
         ctr1+=1
   
      g.Draw("P")
      #g.SetTitle("Charm Fraction - %s; Jet Rank (pT ordered); genCharm Frac."%iF)
      #g.GetXaxis().SetRangeUser(0.,.4)
      #g.GetXaxis().SetRangeUser(-1, 5)
      #g.GetXaxis().SetTitleOffset(1.4)
      g.SetMarkerStyle(29)
      g.SetMarkerSize(4)

      if "195" in iF: g.SetMarkerColor(r.kRed)
      if "195_pt50" in iF: g.SetMarkerColor(r.kRed-2)
      if "170" in iF: g.SetMarkerColor(r.kBlue)
      if "170_pt50" in iF: g.SetMarkerColor(r.kBlue-2)
      if "145" in iF: g.SetMarkerColor(r.kViolet)
      if "145_pt50" in iF: g.SetMarkerColor(r.kViolet+2)
      if "300" in iF: g.SetMarkerColor(r.kGreen-2)
      if "160" in iF: g.SetMarkerColor(r.kOrange)

      #for i in range(len(hList)):
      #   bin = g.GetXaxis().FindBin(i)
      #   g.GetXaxis().SetBinLabel(bin, myDict[i])

      #g.GetXaxis().LabelsOption("d")
      #g.GetXaxis().SetLabelSize(0.05)

      lg.AddEntry(g, iF, "P")

      #c1.Print("plotDump/%s_charmFrac_%d.png"%(iF,ctr))

      mg.Add(g)

   mg.SetTitle("Charm Fraction; Jet Rank (pT ordered); genCharm Frac.")
   mg.Draw("AP")

   for i in range(len(hList)):
      bin = mg.GetXaxis().FindBin(i)
      mg.GetXaxis().SetBinLabel(bin, myDict[i])
   mg.GetXaxis().LabelsOption("d")
   mg.GetXaxis().SetLabelSize(0.05)
   mg.GetXaxis().SetTitleOffset(1.35)
   mg.GetYaxis().SetRangeUser(0., 0.35)

   lg.SetFillColor(0)
   #lg.SetLineColor(0)
   lg.Draw()
   c1.Print("plotDump/total_charmFrac.png")

