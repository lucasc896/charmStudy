#!/usr/bin/env python
# encoding: utf-8
"""
qcdTest.py

Created by Chris Lucas on 2013-05-13.
Copyright (c) 2013 University of Bristol. All rights reserved.
"""

import ROOT as r
from sys import exit

r.gROOT.SetBatch(False)

# script to read in alphaT vs HT plots.
# - needs to be able to read in different jet multiplicities
# - also do rebinning

def switches():

   myDict = {
         "triggers": ["signal", "HT"][1],
         "jMulti": ["inc", "eq2j", "eq3j", "eq4j"],
         "rebin": [False, True],
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

   return hT

def main():

   swt = switches()

   if swt["triggers"]=="signal":
      iF = r.TFile.Open("../../rootfiles/anaPlots_v3/outParkedHT_anaPlots.root")
   elif swt["triggers"]=="HT":
      iF = r.TFile.Open("../../rootfiles/anaPlots_v3/outHT_2012_PSRW_anaPlots.root")

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
      yhi = 3.
   elif swt["triggers"] == "HT":
      xlo = 175.
      xhi = 875.
      ylo = 0.5
      yhi = 0.8

   for jM in swt["jMulti"]:

      c1 = r.TCanvas()

      outFileName = "out/qcdTest_%s-triggers_%s.pdf" % (swt["triggers"], jM)

      befDirs = []
      aftDirs = []

      for ht in HTbins:
         befDirs.append(jM + "_noMhtMet_" + ht)
         if jM!="inc":
            pre = jM+"_inc"
         else:
            pre = jM
         aftDirs.append(pre + "_" + ht)

      hBefore = getHist(inFile = iF, hName = "alphaT_vs_HT", bMulti = bMulti, dirs = befDirs)
      hAfter = getHist(inFile = iF, hName = "alphaT_vs_HT", bMulti = bMulti, dirs = aftDirs)

      # print hBefore, hAfter

      hBefore.SetTitle("before MHT/MET cut")
      hBefore.Draw("colz")
      hBefore.GetXaxis().SetRangeUser(xlo, xhi)
      hBefore.GetYaxis().SetRangeUser(ylo, yhi)

      c1.Print(outFileName + "(")

      hAfter.SetTitle("after MHT/MET cut")
      hAfter.Draw("colz")
      hAfter.GetXaxis().SetRangeUser(xlo, xhi)
      hAfter.GetYaxis().SetRangeUser(ylo, yhi)

      c1.Print(outFileName)

      hSubtract = hBefore.Clone()
      hSubtract.Add(hAfter, -1)
      hSubtract.SetTitle("before - after")
      hSubtract.Draw("colz")
      hSubtract.GetXaxis().SetRangeUser(xlo, xhi)
      hSubtract.GetYaxis().SetRangeUser(ylo, yhi)      

      c1.Print(outFileName)

      hDivide = hAfter.Clone()
      hDivide.Divide(hBefore)
      hDivide.SetTitle("after/before")
      hDivide.Draw("colz")
      hDivide.GetXaxis().SetRangeUser(xlo, xhi)
      hDivide.GetYaxis().SetRangeUser(ylo, yhi)

      c1.Print(outFileName + ")")

if __name__=="__main__":
   main()
