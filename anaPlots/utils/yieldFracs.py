#!/usr/bin/env python
# encoding: utf-8
"""
yieldFracs.py

Created by Chris Lucas on 2012-11-14.
Copyright (c) 2012 University of Bristol. All rights reserved.
"""

from sys import argv

#baseYield = "T2cc 220 145 & 158.0 $^{\pm 12.6 }$ & 69.0 $^{\pm 8.3 }$ & 44.0 $^{\pm 6.6 }$ & 18.0 $^{\pm 4.2 }$ & 0.0 $^{\pm 0.0 }$ & 2.0 $^{\pm 1.4 }$ & 0.0 $^{\pm 0.0 }$ & 0.0 $^{\pm 0.0 }$  \\"
#upYield = "T2cc 220 145 up5 & 162.0 $^{\pm 12.7 }$ & 60.0 $^{\pm 7.7 }$ & 49.0 $^{\pm 7.0 }$ & 17.0 $^{\pm 4.1 }$ & 0.0 $^{\pm 0.0 }$ & 2.0 $^{\pm 1.4 }$ & 0.0 $^{\pm 0.0 }$ & 0.0 $^{\pm 0.0 }$  \\"
#downYield = "T2cc 220 145 down5 & 169.0 $^{\pm 13.0 }$ & 75.0 $^{\pm 8.7 }$ & 44.0 $^{\pm 6.6 }$ & 17.0 $^{\pm 4.1 }$ & 0.0 $^{\pm 0.0 }$ & 2.0 $^{\pm 1.4 }$ & 0.0 $^{\pm 0.0 }$ & 0.0 $^{\pm 0.0 }$  \\"

baseYield = argv[1]
upYield = argv[2]
if len(argv)>3: downYield = argv[3]
else: downYield=downYield = "T2cc 220 145 down5 & 169.0 $^{\pm 13.0 }$ & 75.0 $^{\pm 8.7 }$ & 44.0 $^{\pm 6.6 }$ & 17.0 $^{\pm 4.1 }$ & 0.0 $^{\pm 0.0 }$ & 2.0 $^{\pm 1.4 }$ & 0.0 $^{\pm 0.0 }$ & 0.0 $^{\pm 0.0 }$  \\"

splBase = baseYield.split(" & ")
splUp = upYield.split(" & ")
splDown = downYield.split(" & ")


upFrac = []
downFrac = []

for stringBase, stringUp, stringDown in zip(splBase[1:], splUp[1:], splDown[1:]):
   valBase = stringBase.split(" ")[0]
   valUp = stringUp.split(" ")[0]
   valDown = stringDown.split(" ")[0]

   if float(valBase)==0:
      upFrac.append(0)
      downFrac.append(0)
   else:
      upFrac.append( float(valUp)/float(valBase) )
      downFrac.append( float(valDown)/float(valBase) )

upLine = splBase[0]+" UpFrac & "
downLine = splBase[0]+" DownFrac & "

for up, down in zip(upFrac, downFrac):
   upLine += "%.5s & "%str(up)
   downLine += "%.5s & "%str(down)

if len(argv)>3: print "\n"+downLine[:-2]+" \\\\"
print upLine[:-2]+" \\\\"+"\n"
