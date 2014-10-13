import ROOT as r
import numpy as np
import math as ma

r.gROOT.SetBatch(r.kTRUE)

"""
To-do:
1. Make inclusive stop pT bin for 800 and above
"""

def white_list(point = [], respect = False):

    white = [[175, 115], [225, 165], [275, 245]]
    # white = [[300, 290]]

    if respect:
        if point in white:
            return True
        else:
            return False
    else:
        return True

def plot_weights(dicto = {}):
    
    c1 = r.TCanvas()
    compare_2d = r.TH2D("weights", "weights; m_{stop} (GeV); m_{LSP} (GeV);", 13, 62.5, 387.5, 78, -2.5, 387.5)
    compare_2d_hi = r.TH2D("weights_hi", "weights_hi; m_{stop} (GeV); m_{LSP} (GeV);", 13, 62.5, 387.5, 78, -2.5, 387.5)

    for mstop in dicto:
        for mlsp in dicto[mstop]:
            n_ents = 0
            vals = []
            avg_weights = []
            for boost in dicto[mstop][mlsp]:
                if boost <200. or boost>600.:
                    continue
                vals.append(dicto[mstop][mlsp][boost][0])
                avg_weights.append(1./ma.pow(dicto[mstop][mlsp][boost][1], 1))

            avg = np.average(vals, weights=avg_weights)
            compare_2d.Fill(mstop, mlsp, avg)

                # compare_2d.Fill(mstop, mlsp, dicto[mstop][mlsp][boost][0])

                # if boost < 700.:
                #     n_ents += 1
                #     compare_2d_hi.Fill(mstop, mlsp, dicto[mstop][mlsp][boost][0])
    
    # compare_2d.Scale(0.1)
    compare_2d.Draw("colztext")
    compare_2d.GetZaxis().SetRangeUser(0.95, 1.2)
    r.gStyle.SetOptStat(0)
    c1.Print("stop_weights/summary.pdf")

    # compare_2d_hi.Scale(float(1./n_ents))
    # compare_2d_hi.Draw("colztext")
    # compare_2d_hi.GetZaxis().SetRangeUser(0.95, 1.3)
    # c1.Print("stop_weights/summary_hi.pdf")

def missing_masses():
    """return list of missing mass points in T2cc"""

    points = []

    # delta mass points (50 and 70)
    for mstop in [100.+25.*i for i in range(11)]:
        points.append([mstop, mstop-50])
        points.append([mstop, mstop-70])

    for mlsp in [375.-10.*i for i in range(1, 9)]:
        points.append([375., mlsp])

    return points

def add_missing_weights(dicto = {}):

    # for point in missing_masses():
    #     # use mstop 350. points for 375.
    #     if point[0] == 375.:
    #         dicto[point[0]][point[1]] = dicto[point[0]-25.][point[1]-25.] #copy weight
            
    #     else:
    #         # only get here if mStop != 375, so is a diagonal point
    #         # take the point above
    #         dicto[point[0]][point[1]] = dicto[point[0]][point[1]+10]
    
    dicto[375] = dicto[350]        



def strip_outlier(data = [], m = 3.):
    """return list with outliers shrunk"""

    new = [np.abs(d - np.median(data)) for d in data]
    mdev = np.median(new)
    meand = np.mean(data)
    snew = []

    for d in new:
        if mdev:
            snew.append(d/mdev)
        else:
            snew.append(0.)
    for n in range(len(snew)):
        # if outside m*mdev then set to m*mdev (above or below)
        if snew[n]>m or snew[n] == 0.:
            if data[n] > meand:
                data[n] = meand + m*mdev
            elif data[n] < meand:
                data[n] = meand - m*mdev

def strip_high_weights(data = [], max_weight = 5.):
    # also remove weights greater than 5
    for n in range(len(data)):
        if data[n] > max_weight:
            data[n] = max_weight


def dict_printer(dicto = {}, indent = 1):

  # print "> Outputting dictionary format.\n"

  print "{ (%d keys)\n" % len(dicto)
  for key in dicto:
    print "\t"*indent, "'%s': " % key,
    if dict == type(dicto[key]):
      dict_printer(dicto[key], indent+1)
    else:
      print dicto[key]
  print "\t"*indent, "}\n"

def dict_output(dicto = {}, out_file_name = "out.txt"):
    
    print "dict_output is deprecated."
    return

    out = ""

    out += "from icf.core import PSet\n\n"
    out += "stop_vect_weights = PSet(\n"

    for mstop in dicto:
        out += "\t%.0f = PSet(\n" % mstop
        for mlsp in dicto[mstop]:
            out += "\t\t%.0f = PSet(\n" % mlsp
            for boost, weight in dicto[mstop][mlsp].items():
                out += "\t\t\t\t%.0f = %.3f,\n" % (boost, weight)
            out += "\t\t),\n"
        out += "\t),\n"
    out += ")\n"

    f0 = open(out_file_name, 'w')
    f0.write(out)
    f0.close()

def lut_output(dicto = {}, out_file_name = "lut_out.txt"):

    out = ""
    for mstop in dicto:
        for boost, weight in dicto[mstop].items():
            out += "%.1f\t%.1f\t%.3f\n" % (mstop, boost, weight[0])

    out += "\n"

    f0 = open(out_file_name, 'w')
    f0.write(out)
    f0.close()

def process_hists(h0=None, h1=None):

    weights = {}

    for xbin in range(1, h_t2cc.GetNbinsX()+1):
        mstop = h_t2cc.GetXaxis().GetBinCenter(xbin)

        data = {
            "boost"         :[],
            "t2cc"          :[],
            "t2_4body"      :[],
            "weight"        :[],
            "weight_err"    :[],
            "t2cc_norm"     :0.,
            "t2_4body_norm" :0.,
        }

        # if h_t2cc.GetBinContent(xbin, ybin, 1) <= 0: continue
        # if mstop < mlsp: continue

        if mstop > 360.: continue
        if mstop < 100.: continue

        weights[mstop] = {}

        # loop through all boost values in spectrum
        for ybin in range(1, 11):
            t2cc_val = h_t2cc.GetBinContent(xbin, ybin)
            t2_4body_val = h_t2_4body.GetBinContent(xbin, ybin)

            if ma.isnan(t2cc_val):
                t2cc_val = 0.
            if ma.isnan(t2_4body_val):
                t2_4body_val = 0.

            data['t2cc_norm'] += t2cc_val
            data['t2_4body_norm'] += t2_4body_val

            if ybin < 12:
                data['boost'].append(h_t2cc.GetYaxis().GetBinLowEdge(ybin))
                data['t2cc'].append(t2cc_val)
                data['t2_4body'].append(t2_4body_val)


        get_weights(data)

        # remove strong outliers
        strip_outlier(data['weight'])
        strip_high_weights(data['weight'], 2.5)

        plot_weight_distro(data, "%.1f" % mstop)

        for i in range(len(data['boost'])):
            weights[mstop][data['boost'][i]] = [data['weight'][i], data['weight_err'][i]]
        
    add_missing_weights(weights)        

    dict_printer(weights)
    # dict_output(weights)
    lut_output(weights)
    # plot_weights(weights)


def get_weights(dict = {}):

    if dict['t2cc_norm'] > 0.:
        t2cc_norm = 1./dict['t2cc_norm']
    else:
        t2cc_norm = 1.

    if dict['t2_4body_norm'] > 0.:
        t2_4body_norm = 1./dict['t2_4body_norm']
    else:
        t2_4body_norm = 1.

    for i in range(len(dict['t2cc'])):
        dict['t2cc'][i]     = dict['t2cc'][i]*t2cc_norm
        dict['t2_4body'][i] = dict['t2_4body'][i]*t2_4body_norm

    for i in range(len(dict['boost'])):
        if dict['t2_4body'][i] > 0. and dict['t2cc'][i] > 0.:
            this_weight = float(dict['t2cc'][i]/dict['t2_4body'][i])
            this_weight_err = this_weight * ma.pow(ma.pow(dict['t2cc'][i]/t2cc_norm,-3.)+ma.pow(dict['t2_4body'][i]/t2_4body_norm,-3.),.5)
        else:
            this_weight = 1.
            this_weight_err = 1.


        if ma.isnan(this_weight):
            this_weight = 1.
            this_weight_err = 1.
        dict['weight'].append(this_weight)
        dict['weight_err'].append(this_weight_err)

def plot_weight_distro(dicto = {}, name_string = ""):

    h0 = r.TH1D("h0_%s" % name_string, "h0_%s" % name_string, 10, 0., 1000.)
    h1 = r.TH1D("h1_%s" % name_string, "h1_%s" % name_string, 10, 0., 1000.)
    hw = r.TH1D("hw_%s" % name_string, "hw_%s" % name_string, 10, 0., 1000.)
    h_line_hack = r.TH1D("hline", "hline", 10, 0., 1000.)
    for i in range(1, 11):
        h_line_hack.SetBinContent(i, 1.)

    for i in range(len(dicto['t2cc'])):
        h0.Fill(dicto['boost'][i], dicto['t2cc'][i])
        h1.Fill(dicto['boost'][i], dicto['t2_4body'][i])
        # hw.Fill(dicto['boost'][i], dicto['weight'][i])
        bin = hw.FindBin(dicto['boost'][i])
        hw.SetBinContent(bin, dicto['weight'][i])
        hw.SetBinError(bin, dicto['weight_err'][i])

    hr = h0.Clone()
    hr.Divide(h1)

    c1 = r.TCanvas()

    h0.Draw("hist")
    h0.SetLineColor(r.kBlue)
    unity_norm(h0)
    h1.Draw("histsame")
    h1.SetLineColor(r.kRed)
    unity_norm(h1)
    c1.SetLogy(1)
    c1.Print("stop_weights/%s_h0h1.pdf" % name_string)
    hr.Draw("hist")
    h_line_hack.Draw("same")
    h_line_hack.SetLineStyle(2)
    # c1.Print("stop_weights/%s_hr.pdf" % name_string)
    c1.SetLogy(0)
    hw.Draw("hist")
    hw.SetMinimum(0.)
    h_line_hack.Draw("same")
    h_line_hack.SetLineStyle(2)
    c1.Print("stop_weights/%s_hw.pdf" % name_string)

def unity_norm(h = None):
    
    for i in range(1, h.GetNbinsX()+1):
        val = h.GetBinContent(i)
        try:
            norm = 1./h.Integral()
        except ZeroDivisionError:
            norm = 1.

        h.SetBinContent(i, val*norm)

if __name__ == "__main__":


    f_t2cc = r.TFile.Open("../../rootfiles/stopVectReweight_v0/outT2cc_2d_stopVectReweight.root")
    f_t2_4body = r.TFile.Open("../../rootfiles/stopVectReweight_v0/outT2_4body_2d_stopVectReweight.root")

    h_t2cc      = f_t2cc.Get("noCuts_0_10000/mStop_mLSP_stopVectPt")
    h_t2_4body  = f_t2_4body.Get("noCuts_0_10000/mStop_mLSP_stopVectPt")

    c1 = r.TCanvas()
    h_t2cc.Draw("colztext")
    c1.Print("t2cc_xy.pdf")

    h_t2_4body.Draw("colztext")
    c1.Print("t2_4body_xy.pdf")
    
    stop_weights = process_hists(h_t2cc, h_t2_4body)

    exit()

    h_stop_t2cc = f_t2cc.Get("noCuts_0_10000/stopGenPtVect")
    h_stop_t2_4body = f_t2_4body.Get("noCuts_0_10000/stopGenPtVect")
    print h_stop_t2cc, h_stop_t2_4body

    c2 = r.TCanvas()

    h_stop_t2cc.Draw("hist")
    h_stop_t2cc.SetLineColor(r.kBlue)
    unity_norm(h_stop_t2cc)



    h_stop_t2_4body.Draw("histsame")
    h_stop_t2_4body.SetLineColor(r.kRed)
    print h_stop_t2_4body.GetBinContent(1)
    unity_norm(h_stop_t2_4body)



    c2.Print("stop_weights/h_stopVect_compare.pdf")

    h_rat = h_stop_t2cc.Clone()
    h_rat.Divide(h_stop_t2_4body)
    h_rat.Draw("hist")


    c2.Print("stop_weights/h_stopVect_ratio.pdf")
