#!/usr/bin/env python
# encoding: utf-8

from sys import argv
from sys import exit
from Log import *

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


if len(argv) < 3:
   Log.error("Enter two latex table strings to divide.")
   Log.info("Format: ./yieldDivide.py '<NUMERATOR_STR>' '<DENOM_STR>' ")
   exit()

numRaw = argv[1]
denRaw = argv[2]

numYields = getYieldsFromLatex(numRaw)
denYields = getYieldsFromLatex(denRaw)

if len(numYields) != len(denYields):
   Log.error("Latex strings contain different number of yields.")
   exit()

eff = ["Efficiency"]
for num, den in zip(numYields, denYields):
   val = float(num/den)
   eff.append("%.3f" % val)

print ""
Log.info(" & ".join(eff) + r" \\")
print ""
