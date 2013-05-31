#!/usr/bin/env python
# encoding: utf-8

from sys import argv
from sys import exit
from Log import *

# Code is very reliant on input file format!!
# 
# List "beforeCut" yields, followed by "afterCut" yields

###-------------------------------------------------------------------###


def getYieldsFromLatex(texLine = ""):
   
   yields = []

   for i in texLine.split("&"):
      tmp = i.split("$")[0]
      try:
         val = float(tmp)
      except ValueError:
         pass
      else:
         yields.append(val)

   return yields

###-------------------------------------------------------------------###

def formatLabel(label=""):

  label = label.replace("TauEle", r"$\tau \to e \nu$")
  label = label.replace("TauMu", r"$\tau \to \mu \nu$")
  label = label.replace("TauHad", r"$\tau \to had$")
  label = label.replace("VEle", r"$W/Z \to e \nu$")
  label = label.replace("VMu", r"$W/Z \to \mu \nu$")

  return label

###-------------------------------------------------------------------###

def printEffs(d = {}):

   outTxt = ""
   for i in d:
      outTxt += formatLabel(i) + " Efficiency "
      for bef, aft in zip(d[i][0], d[i][1]):
         outTxt += "& %.3f " % float(aft/bef)
      outTxt += "\\\\\n"

   print outTxt

###-------------------------------------------------------------------###

def printPurs(d = {}):

   # get list of total vetoes made in HT
   totVetoes =  [i-j for i, j in zip(d["All"][0], d["All"][1])]

   outTxt = ""
   for i in d:
      if "All" in i:
         continue
      outTxt += formatLabel(i) + " Purity "
      for bef, aft, tot in zip(d[i][0], d[i][1], totVetoes):
         outTxt += "& %.3f " % float((bef-aft)/tot)
      outTxt += "\\\\\n"
   print outTxt

###-------------------------------------------------------------------###

def printTotals(d = {}):

   for i in d:
      print ">>>", i
      print "Before:", d[i][0]
      print "After:", d[i][1]
      print "B-A:", [j-k for j, k in zip(d[i][0], d[i][1])]

###-------------------------------------------------------------------###

if len(argv) < 2:
   print "Please enter a trailing option."
   print "\t'p' for purity calculation"
   print "\t'e' for efficiency"
   exit()

inFile = open('in.txt', 'r')

inStuff = {
      "All":[],
      "TauEle":[],
      "TauMu":[],
      "TauHad":[],
      "VEle":[],
      "VMu":[],
}

for line in inFile:
   tmp = line.split("\n")[0]
   if "tau" in tmp and "mu" in tmp:
      inStuff["TauMu"].append(tmp)
   elif "tau" in tmp and " e " in tmp:
      inStuff["TauEle"].append(tmp)
   elif "tau" in tmp and "had" in tmp:
      inStuff["TauHad"].append(tmp)
   elif "W" in tmp and "mu" in tmp:
      inStuff["VMu"].append(tmp)
   elif "W" in tmp and " e " in tmp:
      inStuff["VEle"].append(tmp)
   else:
      inStuff["All"].append(tmp)

# replace raw latex in "inStuff" dict with yields
for i in inStuff:
   befYields = getYieldsFromLatex( inStuff[i][0] )
   aftYields = getYieldsFromLatex( inStuff[i][1] )

   inStuff[i] = [befYields, aftYields]

# entry format: "<process>": [[before yeilds in HT], [after yields in HT]] 

if "e" in argv[1]:
   printEffs(inStuff)

elif "p" in argv[1]:
   printPurs(inStuff)

elif "t" in argv[1]:
   printTotals(inStuff)
