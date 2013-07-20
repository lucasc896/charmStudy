#!/usr/bin/env python
# encoding: utf-8
"""
qcdTest.py

Created by Chris Lucas on 2013-05-13.
Copyright (c) 2013 University of Bristol. All rights reserved.
"""

import ROOT as r
from sys import exit
from array import *

r.gROOT.SetBatch(False)
r.gStyle.SetOptStat(0)

# script to read in alphaT vs HT plots.
# - needs to be able to read in different jet multiplicities
# - also do rebinning

def switches():

   myDict = {
         "triggers": ["signal", "HT"][1],
         "jMulti": ["inc", "eq2j", "eq3j", "eq4j"],
         "rebin": [False, True],
         "anaBins": [False, True][0], # plot using analysis binning
   }

   return myDict

def getHist(inFile=None, hName="", bMulti=[], dirs=[]):

   hT = None
   for d in dirs:
      for i in bMulti:
         h = inFile.Get("%s/%s_%d" % (d, hName, i))
         # print "%s/%s_%d" % (d, hName, i)
         if hT is None:
            hT = h.Clone()
         else:
            hT.Add(h)

   if switches()["anaBins"]:
      xbins = [175., 225., 275., 325.]+[375.+i*100 for i in range(7)]
      ybins = [0.5+0.01*i for i in range(11)]+[0.7, 0.8, 0.9, 1.0, 1.5, 2.0, 2.5]

      xBins = array('d', xbins)
      yBins = array('d', ybins)

      # print xBins

      hOut = r.TH2F("temp", "temp", len(xBins)-1, xBins, len(yBins)-1, yBins)

      for x in range(hT.GetXaxis().GetNbins()):
         for y in range(hT.GetYaxis().GetNbins()):
            val = hT.GetBinContent(x, y)
            xbin = hT.GetXaxis().GetBinCenter(x)
            ybin = hT.GetYaxis().GetBinCenter(y)
            if val>0.:
               hOut.Fill(xbin, ybin, val)
      
   else:
      hOut = hT.Clone()

   return hOut

def main():

   swt = switches()

   if swt["triggers"]=="signal":
      iF = r.TFile.Open("../../rootfiles/anaPlots_v3/outParkedHT_anaPlots_v2.root")
   elif swt["triggers"]=="HT":
      iF = r.TFile.Open("../../rootfiles/anaPlots_v3/outHT_2012_PSRW_anaPlots_v2.root")

   try:
      tmp = iF
   except NameError:
      print "Could not open file."
      exit()


   HTbins = ["175_275", "275_325", "325_375", "375_475", "475_575", "575_675", "675_775", "775_875", "875"]
   bMulti = [i for i in range(6)]

   # set some axis ranges
   if swt["triggers"] == "signal":
      xlo = 175.
      xhi = 875.
      ylo = 0.5
      yhi = 1.
   elif swt["triggers"] == "HT":
      xlo = 175.
      xhi = 875.
      ylo = 0.5
      yhi = 0.8

   for jM in swt["jMulti"]:

      c1 = r.TCanvas()

      outFileName = "out/qcdTest_%s-triggers_%s%s.pdf" % (swt["triggers"], jM, "_anaBins" if swt["anaBins"] else "")

      befDirs = []
      aftDirs = []

      for ht in HTbins:
         befDirs.append(jM + "_noMhtMet_" + ht)
         aftDirs.append(jM + "_" + ht)

      hBefore = getHist(inFile = iF, hName = "alphaT_vs_HT", bMulti = bMulti, dirs = befDirs)
      hAfter = getHist(inFile = iF, hName = "alphaT_vs_HT", bMulti = bMulti, dirs = aftDirs)

      if swt["anaBins"]:
         dOpt = "colz text"
      else:
         dOpt = "colz"

      hBefore.SetTitle("before MHT/MET cut")
      hBefore.Draw(dOpt)
      hBefore.GetXaxis().SetRangeUser(xlo, xhi)
      hBefore.GetYaxis().SetRangeUser(ylo, yhi)

      c1.Print(outFileName + "(")

      hAfter.SetTitle("after MHT/MET cut")
      hAfter.Draw(dOpt)
      hAfter.GetXaxis().SetRangeUser(xlo, xhi)
      hAfter.GetYaxis().SetRangeUser(ylo, yhi)

      c1.Print(outFileName)

      hSubtract = hBefore.Clone()
      hSubtract.Add(hAfter, -1)
      hSubtract.SetTitle("before - after")
      hSubtract.Draw(dOpt)
      hSubtract.GetXaxis().SetRangeUser(xlo, xhi)
      hSubtract.GetYaxis().SetRangeUser(ylo, yhi)  

      c1.Print(outFileName)

      c1.SetLogz(1)

      c1.Print(outFileName)

      c1.SetLogz(0)

      hDivide = hAfter.Clone()
      hDivide.Divide(hBefore)
      hDivide.SetTitle("after/before")
      hDivide.Draw(dOpt)
      hDivide.GetXaxis().SetRangeUser(xlo, xhi)
      hDivide.GetYaxis().SetRangeUser(ylo, yhi)

      c1.Print(outFileName + ")")

if __name__=="__main__":
   main()
