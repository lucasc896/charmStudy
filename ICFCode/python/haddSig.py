#!/usr/bin/env python

import os, sys
import commands
import subprocess

sigs = ["300", "160", "195", "170", "145"][0:5]
anaMode = ["anaPlots", "noCuts_bTagEff"][0]

for s in sigs:
   if s=="195" or s=="170" or s=="145":
      print "hadd outT2cc_220_%s_%s.root */*%s*.root"%(s, anaMode,s)
   else:
      print "hadd outT2cc_%s_%s.root */*%s*.root"%(s, anaMode, s)
print ""
