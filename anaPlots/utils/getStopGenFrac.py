import ROOT as r

inFiles = ["Stop100", "Stop175", "Stop250"]
c1 = r.TCanvas()

for ins in inFiles:
   iF = r.TFile.Open("../../rootfiles/anaPlots_225/outT2cc_ISRRW13_%s_anaPlots.root"%ins)

   for i in range(5):
      h = iF.Get("noCuts_0_10000/stopGenPtVect_%d"%(i))
      if i==0: hT = h.Clone()
      else: hT.Add(h)

   hT.Draw()
   c1.Print("before_weighting.png")

   #remove the ISR reweighting!
   for bin in range( hT.GetNbinsX() ):
      center = hT.GetBinCenter(bin)
      weight=1.
      if center<=120.:
         weight = 1.
      elif center > 120 and center <= 150:
         weight = 1.05
      elif center > 150 and center <= 250:
         weight = 1.1
      elif center > 250:
         weight = 1.2   
      hT.SetBinContent( bin, hT.GetBinContent(bin)*weight )

   hT.Draw()
   c1.Print("after_weighting.png")

   bin250 = hT.FindBin(250.)

   total = 0.
   total250 = 0.
   for bin in range( hT.GetNbinsX() ):
      total += hT.GetBinContent(bin)
      if bin>=bin250:
         total250 += hT.GetBinContent(bin)

   print "%s\t%.4s%%"%(ins, float(total250/total)*100.)

