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
#   debug       = conf.switches()["debug"]

   if debug: print sFile[sigSamp][0]
  
   normVal = None
   if conf.switches()["unitNorm"]:
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
         c1.Print("plotDump/bTagEff_%s_%s_%s.png"%(sigSamp, hT, hMulti))
      else:
         c1.Print("plotDump/bTagEff_%s_%s_noCuts.png"%(sigSamp, hT))

   pass
