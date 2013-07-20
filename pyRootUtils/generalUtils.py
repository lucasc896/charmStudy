#!/usr/bin/env python
# encoding: utf-8
"""
generalUtils.py

Created by Chris Lucas on 2012-10-28.
Copyright (c) 2012 University of Bristol. All rights reserved.
"""

import sys
import os
import ROOT as r
import math
import re
import configuration as conf
import xSec as xS
from Log import *
from sys import exit


###-------------------------------------------------------------------###
###-------------------------------------------------------------------###

class multiPlot(object):
  """Rate plot producer"""
  def __init__(self, hists = None):
    super(multiPlot, self).__init__()
    self.hists = hists
    self.listColors = [r.kBlack, r.kBlue+1, r.kAzure+10, r.kViolet-1]
    self.Debug = False
    self.DoGrid = True
    self.SetLogy = False
    self.xRange = []
    self.yRange = []
    self.xRebin = 1
    self.yRebin = 1
    self.hTitles = []
    self.sigTitle = ""
    self.canvTitle = ""
    self.oFileName = ""
    self.lg = r.TLegend()
    self.ln1 = r.TLine()
    self.ln2 = r.TLine()
    self.ln3 = r.TLine()
    self.SetStyle()
  
  def makeMultiPlot(self):
    """docstring for MakeRatePlot"""
    c1 = r.TCanvas()
    if self.SetLogy: c1.SetLogy()

    self.MakeLegend()

    if not self.hTitles:
      for i in range( len(self.hists) ):
        self.hTitles.append( "hist_%d"%i )

    ctr=0

    for h, kCol, ttl in zip(self.hists, self.listColors, self.hTitles):
      if self.Debug: print "*** Hist: ", h
      if ctr==0:
        h.SetTitle( self.canvTitle )
        h.Draw("hist")
        h.GetYaxis().SetLabelSize(0.04)
        h.GetXaxis().SetTitleSize(0.04)
        if self.xRange:
          h.GetXaxis().SetRangeUser(self.xRange[0], self.xRange[1])
        if self.yRange:
          h.GetYaxis().SetRangeUser(self.yRange[0], self.yRange[1])
          pass

      h.SetLineWidth(2)
      h.SetLineColor(kCol)
      h.SetFillColor(0)
      h.Draw("histsame")
      self.lg.AddEntry(h, ttl, "L")
      ctr+=1

    if not self.SetLogy: self.ln1.Draw()
    if not self.SetLogy: self.ln2.Draw()
    if not self.SetLogy: self.ln3.Draw()
    self.lg.Draw()

    return c1

  def SetStyle(self):
    """docstring for SetStyle"""
    r.gStyle.SetOptStat(0)
    r.gStyle.SetOptTitle(0)
    r.gStyle.SetMarkerSize(2)

  def MakeLegend(self):
    """docstring for MakeLegend"""
    self.lg = r.TLegend(0.6, 0.68, 0.74, 0.87)

    self.lg.SetFillColor(0)
    self.lg.SetLineColor(0)
    self.lg.SetLineStyle(0)

  def DrawLine(self, xval=[]):
    """docstring for DrawLine"""
    print "in DrawLine: ", self.yRange
    if len(xval)>0:
      self.ln1 = r.TLine(xval[0], self.yRange[0], xval[0], self.yRange[1])
      self.ln1.SetLineColor(16)
      self.ln1.SetLineStyle(2)
    if len(xval)>1:  
      self.ln2 = r.TLine(xval[1], self.yRange[0], xval[1], self.yRange[1])
      self.ln2.SetLineColor(16)
      self.ln2.SetLineStyle(2)
    if len(xval)>2:
      self.ln3 = r.TLine(xval[2], self.yRange[0], xval[2], self.yRange[1])
      self.ln3.SetLineColor(16)
      self.ln3.SetLineStyle(2)

###-------------------------------------------------------------------###
###-------------------------------------------------------------------###

class anaPlot(object):
  """making specific analysis plots"""
  def __init__(self, hists = None, label=""):
    super(anaPlot, self).__init__()
    self.hists = hists
    self.listColors = [r.kBlack, r.kBlue+1, r.kAzure+10, r.kViolet-1]
    self.Debug = False
    self.DoGrid = False
    self.SetLogy = False
    self.xSecNorm = False
    self.xRange = []
    self.yRange = []
    self.hTitles = []
    self.label = label
    self.canvTitle = label
    self.lg = r.TLegend()
    self.SetStyle()

  def makeAnaPlot(self, inFiles=None, sigFile=None, bMulti=None, dirs=None):
    """docstring for makeAnaPlot"""

    c1=r.TCanvas()
    st1 = r.THStack("hs", "test stack 1")
    if self.SetLogy: c1.SetLogy()
    self.MakeLegend()

    sFile = r.TFile.Open(sigFile)

    for hT, rVal in self.hists.iteritems():
      for b in bMulti:
        ctr=0
        for iF in inFiles:
          rFile = r.TFile.Open(iF)
          ctr1=0

          tmp = iF.split("/")
          tmp2 = tmp[len(tmp)-1].split("_")[0]
          samp = tmp2[3:]

          for d in dirs:
            for suf in getbMultis(b):
              h = rFile.Get("%s/%s%s"%(d, hT, suf))
              if ctr1==0: h1 = h.Clone()
              else: h1.Add(h)
              ctr1+=1

          if ctr==0:
            h1.GetXaxis().SetTitle(self.xTitle)
            h1.GetYaxis().SetTitle(self.yTitle)
            h1.SetTitle(self.canvTitle)

          h1.SetLineColor(self.listColors[ctr])
          h1.Rebin(rebin)
          h1.SetLineWidth(2)
          h1.GetYaxis().SetTitleOffset(1.4)
    
          self.lg.AddEntry(h1, samp, "L")
    
          st1.Add(h)

          ctr+=1

        st1.Draw("hist")

        oFileName = "plotDump/Stack_%s_%s.png"%(hT, b)
        c1.Print(oFileName)


  def makeSinglePlot(self, rebinX=None, rebinY=None, norm=None):
    """docstring for makeSinglePlot"""
    c1 = r.TCanvas()

    for i in range( len(self.hists) ):
      if i == 0: h=self.hists[i].Clone()
      else: h.Add(self.hists[i])   

    h.SetLineColor(r.kMagenta+1)
    h.SetLineWidth(2)
    h.GetYaxis().SetTitleOffset(1.4)

    if "TH1D" in str( type(h) ):
      if rebinX: h.Rebin(rebinX)
      if self.SetLogy:
        h.SetMinimum(0.001)
      else:
        h.SetMinimum(0.)

    if "TH2D" in str( type(h) ):
      h.SetLabelSize(0.02, "Z")
      if rebinX: h.RebinX(rebinX)
      if rebinY: h.RebinY(rebinY)

    if norm and "n_Event" not in self.canvTitle: 
      self.normHist(h, norm)
    if "n_Event" in self.canvTitle: r.gStyle.SetOptStat("i")

    return h

  def SetStyle(self):
    """docstring for SetStyle"""
    #r.gStyle.SetOptStat(0)
    r.gStyle.SetOptTitle(0)
    r.gStyle.SetMarkerSize(2)

  def MakeLegend(self):
    """docstring for MakeLegend"""
    self.lg = r.TLegend(0.6, 0.68, 0.74, 0.87)

    self.lg.SetFillColor(0)
    self.lg.SetFillStyle(0)
    self.lg.SetLineColor(0)
    self.lg.SetLineStyle(0)

  def normHist(self, h, normVal=1.):
    """docstring for normHist"""
    if float(h.GetEntries())==0: return 0
  
    if self.xSecNorm:
      scaleF = normVal
    else:
      ## unit normalisation here ##
      ent = 0
      for i in range(h.GetNbinsX()):
        # if h.GetBinLowEdge(i)>275: # hack line to normalise above certain bin value
          ent += h.GetBinContent(i)
      try:
        scaleF = float(normVal/ent)
      except ZeroDivisionError:
        Log.error("Zero entries found in plot when attempting to normalise.")
        sys.exit()

    h.Scale( scaleF )

    
###-------------------------------------------------------------------###
###-------------------------------------------------------------------###

class Print(object):
  """docstring for printPDF"""
  def __init__(self, Fname):
    super(Print, self).__init__()
    self.canvas = r.TCanvas()
    self.DoPageNum = True
    self.fname = Fname
    # self.rfile = r.TFile(self.fname[:-4]+".root",'RECREATE')
    self.pageCounter = 1
    self.open()


  def toFile(self,ob,title):
    """docstring for toFile"""
    # self.rfile.cd()
    # ob.SetName(title)
    # ob.SetTitle(title)
    # ob.Write()
    # ob = None
    pass

  def cd(self):
    """docstring for cd"""
    self.canvas.cd()
    pass


  def open(self, frontText = "<none>"):
    """docstring for open"""
    tpt1 = r.TText(0.07, 0.26, frontText)
    tpt2 = r.TText(0.07, 0.2, "Chris Lucas")
    tpt1.Draw()
    tpt2.Draw()
    self.canvas.Print(self.fname+"[")
    r.gPad.SetRightMargin(0.15)
    r.gPad.SetLeftMargin(0.15)
    r.gPad.SetTopMargin(0.1)
    r.gPad.SetBottomMargin(0.2)   

    pass


  def close(self):
    """docstring for close"""
    # self.rfile.Write()
    # self.rfile.Close()
    self.canvas.Print(self.fname+"]")
    pass


  def Clear(self):
    """docstring for Clear"""
    self.canvas.Clear()
    pass

  def SetLog(self,axis,BOOL):
    """docstring for SetLog"""
    if 'x' in axis:
      if BOOL:
        self.canvas.SetLogx()
      else:
        self.canvas.SetLogx(r.kFALSE)
    if 'y' in axis:
      if BOOL:
        self.canvas.SetLogy()
      else:
        self.canvas.SetLogy(r.kFALSE)
    pass

  def SetGrid(self,BOOL):
    """docstring for SetGrid"""
    if BOOL:
      self.canvas.SetGrid()
    else:
      self.canvas.SetGrid(r.kFALSE)
    pass


  def Print(self):
    """docstring for Print"""
    num = r.TLatex(0.95,0.01,"%d"%(self.pageCounter))
    num.SetNDC()
    if self.DoPageNum: num.Draw("same")
    # self.canvas.SetGridx()
    # self.canvas.SetGridy()
    self.canvas.Print(self.fname)
    self.pageCounter += 1
    pass

  def PrintCanvas(self, c1):
    """docstring for PrintCanvas"""
    num = r.TLatex(0.95,0.01,"%d"%(self.pageCounter))
    num.SetNDC()
    if self.DoPageNum: num.Draw("same")
    c1.Print(self.fname)
    self.pageCounter += 1
    pass

###-------------------------------------------------------------------###
###-------------------------------------------------------------------###

class stackPlots(object):
  """docstring for stackPlots"""
  def __init__(self, bgHists=None, bgTitles=None, sigHist=None, dataHist=None):
    super(stackPlots, self).__init__()
    self.bgHists = bgHists
    self.bgTitles = bgTitles
    self.Debug = False
    self.PrintLogy = False
    self.xRange = []
    self.yRange = []
    self.xRebin = 1
    self.yRebin = 1
    self.hTitles = []
    self.sigTitle = ""
    self.canvTitle = ""
    self.oFileName = ""
    self.listColors = [r.kBlue+1, r.kRed-3, r.kYellow+2, r.kGreen+1, r.kViolet]
    self.nSignal = 0
    self.targLumi = conf.switches()["lumiNorm"] # units: fb-1
    if sigHist:
      self.sigHist = sigHist
    else:
      self.sigHist=None
    if dataHist:
      self.dataHist = dataHist
    else:
      self.dataHist = None

  def drawStack(self):

    if conf.switches()["hiRes"]:
      c1 = r.TCanvas("myStack", "myStack", 1600, 1200)
    else: 
      c1 = r.TCanvas()

    stTitle = "%s;%s;%s"%(self.canvTitle, self.bgHists[0].GetXaxis().GetTitle(), self.bgHists[0].GetYaxis().GetTitle())
    st1 = r.THStack("hs", stTitle)
    lg = r.TLegend(0.62, 0.65, 0.9, 0.88)
    lg.SetFillColor(0)
    lg.SetLineColor(0)

    ctr=0

    for h, hT in zip(self.bgHists, self.bgTitles):
      h.SetLineWidth(2)
      h.SetLineColor(self.listColors[ctr])
      h.SetFillColor(self.listColors[ctr])
      h.Rebin(self.xRebin)
      st1.Add(h)
      lg.AddEntry(h, hT, "L")
      ctr+=1

    st1.Draw("hist")

    if "TH2" in str( type(h) ):
      if self.xRange:
        ranges = self.xRange
        st1.GetXaxis().SetRangeUser(ranges[0], ranges[1])
      if self.yRange:
        ranges = self.yRange
        st1.GetYaxis().SetRangeUser(ranges[0], ranges[1])

    elif "TH1" in str( type(h) ):
      if self.xRange:
        ranges = self.xRange
        st1.GetXaxis().SetRangeUser(ranges[0], ranges[1])

    if self.sigHist: 
      self.sigHist.SetLineStyle(2)
      self.sigHist.SetLineWidth(2)
      self.sigHist.SetLineColor(r.kRed)
      self.sigHist.Rebin(self.xRebin)
      lg.AddEntry(self.sigHist, self.sigTitle, "L")
      self.sigHist.Draw("samehist")
      self.sigHist.Scale(self.getSigNorm())
    if self.dataHist: 
      self.dataHist.SetLineStyle(2)
      self.dataHist.SetLineWidth(2)
      self.dataHist.SetLineColor(r.kBlack)
      self.dataHist.Rebin(self.xRebin)
      self.dataHist.Draw("same")    

    lg.Draw()

    c1.Print(self.oFileName)

    if self.PrintLogy:
      c1.SetLogy(1)
      c1.Print(oFileName)

  def getSigNorm(self):

    # do regex matching for particle masses
    pattern = r"._mSt(\d*)_."

    regex = re.compile(pattern)
    result = regex.findall(self.sigTitle)

    if len(result) > 0:
      mass = eval(result[0])
    else:
      Log.error("No regex match for stop mass found")
      sys.exit()

    # here assuming mass is of a stop particle
    Log.info("Normalising for mStop = %d\n" % mass)

    xsec = xS.stopXSec[mass]

    factor = (self.targLumi*xsec)/float(self.nSignal)

    return factor

###-------------------------------------------------------------------###

def comparPlots(hList=None, debug=None, doLogy=False):

  jM = conf.switches()["jetMulti"]
  sSamp = conf.comparFiles()
  bM = conf.bMulti()

  if debug:
    Log.debug("comparPlots: %s"%hList[0].GetName())

  for h in hList:
    if "TH2" in str( type(h) ): return

  #defult colors
  colors = [r.kRed, r.kBlue, r.kGreen, r.kCyan, r.kMagenta, r.kYellow-1]

  colorDict = {
        "T2cc_160":r.kRed,
        "T2cc_300":r.kGreen-2,
        "T2cc_220_145":4,
        "T2cc_220_170":r.kOrange-3,
        "T2cc_220_195":6,
  }

  # swap in sample specific colors
  for key, val in colorDict.iteritems():
    for i in range( len(sSamp) ):
      if key in sSamp[i]:
        colors[i]=colorDict[key]

  if conf.switches()["hiRes"]:
    c1 = r.TCanvas("c1", "c1", 1600, 1200)
  else: 
    c1 = r.TCanvas()

  r.gStyle.SetOptStat(0)

  if len(hList)==2:
    lg = r.TLegend(0.57, 0.70, 0.895, 0.89)
  elif len(hList)==3:
    lg = r.TLegend(0.68, 0.72, 0.94, 0.89)
  elif len(hList)==4:
    lg = r.TLegend(0.64, 0.64, 0.895, 0.89)
  elif len(hList)==5:
    lg = r.TLegend(0.55, 0.6, 0.945, 0.94)
  elif len(hList)==6:
    lg = r.TLegend(0.65, 0.57, 0.895, 0.89)
  hOrder = getHistOrder(hList)

  if len(hList)==2:
    pd1 = r.TPad("pd1", "pd1", 0., 0.3, 1., 1.)
    pd1.SetBottomMargin(0.005)
    pd1.SetRightMargin(0.05)
    pd1.Draw()
    if conf.switches()["printLogy"]: pd1.SetLogy(r.kTRUE)


    pd2 = r.TPad("pd2", "pd2", 0., 0.02, 1., 0.3)
    pd2.SetTopMargin(0.05)
    pd2.SetBottomMargin(0.26)
    pd2.SetRightMargin(0.05)
    pd2.SetGridx(1)
    pd2.SetGridy(1)
    pd2.Draw()

    pd1.cd()

  ctr=0
  for i in hOrder:
    hList[i].SetLineColor(colors[i])
    entTitle = sSamp[i]

    if entTitle == "T2cc_200": entTitle="Pythia"
    elif entTitle == "T2cc_NF_200_120_cut": entTitle="Madgraph"
    elif "_delta" in entTitle: entTitle = entTitle.split("_")[0]+"_"+entTitle.split("_")[-1]
    elif "_175_" in entTitle: entTitle = "mStop=%s, mLSP=%s"%(entTitle.split("_")[-2], entTitle.split("_")[-1])

    entTitle = entTitle.split("_")
    entTitle = " ".join(entTitle)

    lg.AddEntry(hList[i], entTitle, "L")

    if ctr==0:
      hList[i].Draw("hist")
    else:
      hList[i].Draw("histsame")

    if conf.switches()["printLogy"]:
      c1.SetLogy(r.kTRUE)

    ctr+=1

  hList[hOrder[0]].SetLabelSize(0.04,"Y")
  hList[hOrder[0]].SetTitleOffset(1.2, "Y")
  hList[hOrder[0]].SetTitleSize(0.04, "Y")

  if len(hList)>2:
    hList[hOrder[0]].SetTitleSize(0.06, "X")
    hList[hOrder[0]].SetTitleOffset(0.8, "X")
    r.gPad.SetLeftMargin(0.12)
    r.gPad.SetRightMargin(0.05)
    r.gPad.SetTopMargin(0.05)
    r.gPad.SetBottomMargin(0.12)

  lg.SetFillColor(0)
  lg.SetFillStyle(0)
  lg.SetLineColor(0)
  lg.SetLineStyle(0)
  lg.Draw()

  if len(hList)==2:
    pd2.cd()

    hRatio = hList[0].Clone()
    hRatio.Divide( hList[1] )
    hRatio.SetMarkerStyle(4)
    hRatio.SetMarkerSize(.7)
    hRatio.SetLineWidth(1)
    hRatio.SetLineColor(r.kBlack)
    hRatio.GetYaxis().SetTitle("Ratio")

    # sort ratio ranges
    ranges = getRatioRanges(hRatio)
    hRatio.GetYaxis().SetRangeUser(ranges[0],ranges[1])
    
    hRatio.SetLabelSize(0.12, "X")
    hRatio.SetLabelSize(0.07, "Y")
    hRatio.SetTitleSize(0.13, "X")
    hRatio.SetTitleSize(0.11, "Y")
    hRatio.SetTitleOffset(0.25, "Y")
    hRatio.SetTitleOffset(.9, "X")
    hRatio.Draw("pe1")

    fit = r.TF1("fit","pol0", hRatio.GetXaxis().GetBinLowEdge(1), hRatio.GetXaxis().GetBinUpEdge(hRatio.GetNbinsX()))
    r.gStyle.SetOptFit(1)
    hRatio.Fit(fit)

  if not doLogy:
    c1.Print("plotDump/compare_%s_%s_%s_%s%s.%s"%(hList[0].GetName(),bM[0], jM, sSamp[0].split("_")[0], 
      "_noCuts" if "noCut" in conf.switches()["HTcuts"] else "", conf.switches()["outFormat"]))
  else:
    c1.SetLogy(1)
    c1.Print("plotDump/compar_%s_%s_%s_%s_%slog.%s"%(hList[0].GetName(),bM[0], jM, sSamp[0].split("_")[0], 
      "noCuts_" if "noCut" in conf.switches()["HTcuts"] else "", conf.switches()["outFormat"]))

###-------------------------------------------------------------------###

def getPlotsFromFile(histName="", dirs=None, bSufs=None, inFile=None, scale=None):

  h1=None
  for d in dirs:
    for suf in bSufs:
      h = inFile.Get("%s/%s%s"%(d, histName, suf))
      if not h1:
        h1 = h.Clone()
      else:
        h1.Add(h)
  if scale: h1.Scale(scale)
    
  return h1    

###-------------------------------------------------------------------###

def getHistOrder(hList=None):
  """returns a list of the reverse order of hList"""

  maxVals = []
  myOrder = []

  for h in hList:
    maxVals.append(h.GetMaximum())
  tmpMax = sorted(maxVals, reverse=True)

  for i in range(len(tmpMax)):
    for k in range(len(maxVals)):
      if tmpMax[i] == maxVals[k]:
        print maxVals[k]
        if k in myOrder:
          Log.error("Repeat in order list. Check plots are non-identical.")
          Log.error("Plot: %s"%hList[0].GetName())
          #exit()
        myOrder.append(k)
  return myOrder[0:len(hList)]

###-------------------------------------------------------------------###

def doRanges(h=None, hD=None):

  if "TH1" in str( type(h) ):
    if hD["xRange"]:
      ranges=hD["xRange"]
      h.GetXaxis().SetRangeUser(ranges[0], ranges[1])
  elif "TH2" in str( type(h) ):
    if hD["xRange"]:
      ranges=hD["xRange"]
      h.GetXaxis().SetRangeUser(ranges[0], ranges[1])
    if hD["yRange"]:
      ranges=hD["yRange"]
      h.GetYaxis().SetRangeUser(ranges[0], ranges[1])      

  pass

###-------------------------------------------------------------------###

def getRatioRanges(h=None):

  min = h.GetMinimum()
  max = h.GetMaximum()

  # calculate a 10% whitespace for about and below
  swing = (max-min)*0.1

  return [min-swing, max+swing]

###-------------------------------------------------------------------###

def normalise(h=None, normVal=1.):

  h = h.Scale(normVal/h.GetEntries())
  print "SCALE: ", normVal
  return h

###-------------------------------------------------------------------###

def setChrisStyle(style="g"):

  if style=="g":
    r.gPad.SetRightMargin(0.3)
  elif style=="m":
    pass
  elif style=="a":
    pass
  pass












