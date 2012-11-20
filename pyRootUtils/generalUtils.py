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
import configuration as conf

## r.gROOT.SetStyle("Plain") #To set plain bkgds for slides
#r.gStyle.SetTitleBorderSize(0)
#r.gStyle.SetCanvasBorderMode(0)
#r.gStyle.SetCanvasColor(0)#Sets canvas colour white
#r.gStyle.SetOptStat(2210)#set no title on Stat box
#r.gStyle.SetLabelOffset(0.001)
#r.gStyle.SetLabelSize(0.003)
#r.gStyle.SetLabelSize(0.005,"Y")#Y axis
#r.gStyle.SetLabelSize(0.1,"X")#Y axis
#r.gStyle.SetTitleSize(0.06)
#r.gStyle.SetTitleW(0.7)
#r.gStyle.SetTitleH(0.07)
#r.gStyle.SetOptTitle(1)
##r.gStyle.SetOptStat(0)
#r.gStyle.SetOptFit(1)
#r.gStyle.SetAxisColor(1, "XYZ");
#r.gStyle.SetStripDecimals(r.kTRUE);
#r.gStyle.SetTickLength(0.03, "XYZ");
#r.gStyle.SetNdivisions(510, "XYZ");
#r.gStyle.SetPadTickX(1);
#r.gStyle.SetPadTickY(1);
#r.gStyle.SetLabelColor(1, "XYZ");
#r.gStyle.SetLabelFont(42, "XYZ");
#r.gStyle.SetLabelOffset(0.01, "XYZ");
#r.gStyle.SetLabelSize(0.05, "XYZ");
#r.gStyle.SetHatchesLineWidth(2)
#r.gStyle.SetPalette(1)
#

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
    self.hTitles = []
    self.canvTitle = ""
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
    #self.lg.SetFillStyle(0)
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




class anaPlot(object):
  """making specific analysis plots"""
  def __init__(self, hists = None, label=""):
    super(anaPlot, self).__init__()
    self.hists = hists
    self.listColors = [r.kBlack, r.kBlue+1, r.kAzure+10, r.kViolet-1]
    self.Debug = False
    self.DoGrid = False
    self.SetLogy = False
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
    
          self.lg.AddEntry(h1, samp, "L")
    
          st1.Add(h)

          ctr+=1

        st1.Draw("hist")

        oFileName = "Stack_%s_%s.png"%(hT, b)

        c1.Print(oFileName)


  def makeSinglePlot(self, rebin=None, norm=None):
    """docstring for makeSinglePlot"""
    c1 = r.TCanvas()

    if self.SetLogy: c1.SetLogy()

    for i in range( len(self.hists) ):
      if i==0: h=self.hists[i].Clone()
      elif i>0: h.Add(self.hists[i])
    
    #if "Charm" in h.GetName():
    #  self.canvTitle = self.canvTitle.replace("Charm","Bottom")
    #  xTitle = h.GetXaxis().GetTitle()
    #  xTitle = xTitle.replace("charm", "bottom")
    #  h.SetXTitle(xTitle)
    #if "Stop" in h.GetName():
    #  self.canvTitle = self.canvTitle.replace("Stop", "Sbottom")
    #  xTitle = h.GetXaxis().GetTitle()
    #  xTitle = xTitle.replace("stop", "sbottom")
    #  h.SetXTitle(xTitle)      

    h.SetLineColor(r.kMagenta+1)
    h.SetLineWidth(2)

    if "TH1D" in str( type(h) ):
      #h.Draw("hist")
      if rebin: h.Rebin(rebin)

    if "TH2D" in str( type(h) ):
      h.SetLabelSize(0.02, "Z")
      #h.SetLabelOffset(-2, "Z")
      #h.Draw("colz")
      if rebin: h.RebinX(rebin)

    if norm and "n_Event" not in self.canvTitle: self.normHist(h, norm)
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
    #self.lg.SetFillStyle(0)
    self.lg.SetLineColor(0)
    self.lg.SetLineStyle(0)

  def normHist(self, h, normVal=1.):
    """docstring for normHist"""
    if float(h.GetEntries())==0: return 0
    h.Scale( normVal/float(h.GetEntries()) )




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


class stackPlots(object):
  """docstring for stackPlots"""
  def __init__(self, bgHists=None, bgTitles=None, sigHist=None, dataHist=None):
    super(stackPlots, self).__init__()
    self.bgHists = bgHists
    self.bgTitles = bgTitles
    self.Debug = False
    self.PrintLogy = False
    self.listColors = [r.kBlue+1, r.kRed-3, r.kYellow+2, r.kGreen+1, r.kViolet]
    if sigHist:
      self.sigHist = sigHist
    else:
      self.sigHist=None
    if dataHist:
      self.dataHist = dataHist
    else:
      self.dataHist = None

  def drawStack(self, canvTitle="", rebin=1, oFileName="", sigTitle=""):

    c1=r.TCanvas()
    st1 = r.THStack("hs", canvTitle)
    lg = r.TLegend(0.62, 0.72, 0.82, 0.85)
    lg.SetFillColor(0)
    lg.SetLineColor(0)

    ctr=0

    for h, hT in zip(self.bgHists, self.bgTitles):
      h.SetLineWidth(2)
      h.SetLineColor(self.listColors[ctr])
      h.Rebin(rebin)
      st1.Add(h)
      lg.AddEntry(h, hT, "L")
      ctr+=1

    st1.Draw("hist")

    if canvTitle in conf.histRanges():
      ranges = conf.histRanges()[canvTitle]
      st1.GetXaxis().SetRangeUser(ranges[0], ranges[1])

    if self.sigHist: 
      self.sigHist.SetLineStyle(2)
      self.sigHist.SetLineWidth(2)
      self.sigHist.SetLineColor(r.kRed)
      self.sigHist.Rebin(rebin)
      lg.AddEntry(self.sigHist, sigTitle, "L")
      self.sigHist.Draw("samehist")
    if self.dataHist: 
      self.dataHist.SetLineStyle(2)
      self.dataHist.SetLineWidth(2)
      self.dataHist.SetLineColor(r.kBlack)
      self.dataHist.Rebin(rebin)
      self.dataHist.Draw("same")    

    lg.Draw()

    c1.Print(oFileName)

    if self.PrintLogy:
      oFileName = oFileName[:len(oFileName)-4]+"_log.png"
      c1.SetLogy(1)
      c1.Print(oFileName)


  def MakeLegend(self):
    lg = r.TLegend(0.62, 0.72, 0.9, 0.85)
    lg.SetFillColor(0)
    lg.SetLineColor(0)




def comparPlot(h1=None, h2=None):
  
  jM = conf.switches()["jetMulti"]

  # surpress the drawing of 2D hists
  if "TH2" in str( type(h1) ): return
  if "TH2" in str( type(h2) ): return

  c1 = r.TCanvas()
  r.gStyle.SetOptStat(0)

  lg = r.TLegend(0.62, 0.72, 0.82, 0.85)
  lg.SetFillColor(0)
  lg.SetLineColor(0)

  h1.SetLineColor(r.kBlue)
  h2.SetLineColor(r.kRed)

  if findMaxHist(h1, h2):
    h1.Draw("hist")
    h2.Draw("histsame")
  else:
    h2.Draw("hist")
    h1.Draw("histsame")

  lg.AddEntry(h1, "T2cc (160, 110)", "L")
  lg.AddEntry(h2, "T2cc (300, 250)", "L")

  lg.Draw()

  c1.Print("compare_%s_%s.png"%(h1.GetName(),jM))

  pass


def getPlotsFromFile(histName="", dirs=None, bSufs=None, inFile=None, scale=1.):

  ctr=0

  for d in dirs:
    for suf in bSufs:
      h = inFile.Get("%s/%s%s"%(d, histName, suf))
      if ctr==0: h1 = h.Clone()
      else: h1.Add(h)
      ctr+=1
    h1.Scale(scale)
    
  return h1    

def findMaxHist(h1, h2):
  max1, max2 = 0, 0
  for i in range( h1.GetXaxis().GetNbins() ):
    val = h1.GetBinContent(i)
    if val>max1: max1=val

  for i in range( h2.GetXaxis().GetNbins() ):
    val = h2.GetBinContent(i)
    if val>max2: max2=val

  if max1>max2: return True
  else: return False






















