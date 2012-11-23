#!/usr/bin/env python
# encoding: utf-8

import ROOT as r

inFile = "ISRWeights_TopologyT2bb.root"
pointName = "h_ISRWeight_lastPt_150_100"

rFile = r.TFile().Open(inFile)

h = rFile.Get(pointName)

f = open("%s.txt"%(pointName), "w")

for i in range(h.GetXaxis().GetNbins()):
    line = "ISRReweight_%d_%d %s\n"%(h.GetBinLowEdge(i), h.GetBinLowEdge(i)+10, h.GetBinContent(i))
    f.write(line)
