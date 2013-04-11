import os

print os.environ

import ROOT as r

r.gROOT.SetBatch(r.kTRUE)
r.gStyle.SetOptFit(0001)


def getHist(fileName=None, hName="", bMulti=[], dirs=[]):

   iF = r.TFile.Open(fileName)

   hT = None
   for d in dirs:
      for i in bMulti:
         h = iF.Get("%s/%s_%d" % (d, hName, i))
         #h = iF.Get("%s/%s" % (d, hName))
         if hT is None:
            hT = h.Clone()
         else:
            hT.Add(h)

   return hT


HTdirs_template = ["275_325", "325_375", "375_475", "475_575", "575_675", "675_775", "775_875", "875"]
noCutdirs = ["noCuts_0_10000"]
inFiles = {
      "200,120": "../../rootfiles/anaPlots_225/outT2cc_200_120_anaPlots.root",
      "200,190": "../../rootfiles/anaPlots_225/outT2cc_200_190_anaPlots.root"
      }
jetMulti = ["le3j", "ge4j", "inc"][2]
bMulti = ["0b", "1b", "inc"][2]


c1 = r.TCanvas()

if bMulti == "0b":
   bM = [0]
elif bMulti == "1b":
   bM = [1]
elif bMulti == "inc":
   bM = [i for i in range(5)]


for point, inFile in inFiles.iteritems():

   HTdirs = []
   for ht in HTdirs_template:
      HTdirs.append(jetMulti+"_"+ht)

   nocuts = getHist(fileName=inFile, hName="n_Jets", bMulti=bM, dirs=noCutdirs)
   sele = getHist(fileName=inFile, hName="n_Jets", bMulti=bM, dirs=HTdirs)

   eff = sele.Clone()
   eff.Divide(nocuts)

   eff.GetXaxis().SetTitle("N_{vtx}")
   eff.GetYaxis().SetTitle("Selection Efficiency")
   eff.GetYaxis().SetTitleOffset(1.25)

   eff.Draw()

   eff.SetTitle("T2cc - %s" % point)

   fit =r.TF1("linear","x*[0]+[1]",0.,40.)
   fit.SetParNames("m", "c")
   eff.Fit("linear")
   fit.Draw("lsame")

   c1.Print("nJets_%s_%s_%s.pdf" % (jetMulti, bMulti, point.replace(",", "_")))
