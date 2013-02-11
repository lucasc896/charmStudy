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
print len(argv)
if len(argv)>4:
   upSYield = argv[1]
   upYield = argv[2]
   baseYield = argv[3]
   downYield = argv[4]
   downSYield = argv[5]
else:
   upSYield = "T2cc 220 145 down5 & 169.0 $^{\pm 13.0 }$ & 75.0 $^{\pm 8.7 }$ & 44.0 $^{\pm 6.6 }$ & 17.0 $^{\pm 4.1 }$ & 0.0 $^{\pm 0.0 }$ & 2.0 $^{\pm 1.4 }$ & 0.0 $^{\pm 0.0 }$ & 0.0 $^{\pm 0.0 }$  \\"
   upYield = argv[1]
   baseYield = argv[2]
   downYield = argv[3]
   downSYield = "T2cc 220 145 down5 & 169.0 $^{\pm 13.0 }$ & 75.0 $^{\pm 8.7 }$ & 44.0 $^{\pm 6.6 }$ & 17.0 $^{\pm 4.1 }$ & 0.0 $^{\pm 0.0 }$ & 2.0 $^{\pm 1.4 }$ & 0.0 $^{\pm 0.0 }$ & 0.0 $^{\pm 0.0 }$  \\"
#if len(argv)>3: downYield = argv[3]
#else: downYield = "T2cc 220 145 down5 & 169.0 $^{\pm 13.0 }$ & 75.0 $^{\pm 8.7 }$ & 44.0 $^{\pm 6.6 }$ & 17.0 $^{\pm 4.1 }$ & 0.0 $^{\pm 0.0 }$ & 2.0 $^{\pm 1.4 }$ & 0.0 $^{\pm 0.0 }$ & 0.0 $^{\pm 0.0 }$  \\"

splBase = baseYield.split(" & ")
splUp = upYield.split(" & ")
splSUp = upSYield.split(" & ")
splDown = downYield.split(" & ")
splSDown = downSYield.split(" & ")

upFrac = []
upSFrac = []
downFrac = []
downSFrac = []

for stringBase, stringUp, stringSUp, stringDown, stringSDown in zip(splBase[1:], splUp[1:], splSUp[1:], splDown[1:], splSDown[1:]):
   valBase = stringBase.split(" ")[0]
   valUp = stringUp.split(" ")[0]
   valSUp = stringSUp.split(" ")[0]
   valDown = stringDown.split(" ")[0]
   valSDown = stringSDown.split(" ")[0]
   
   if float(valBase)==0:
      upFrac.append(0)
      upSFrac.append(0)
      downFrac.append(0)
      downSFrac.append(0)
   else:
      upFrac.append( float(valUp)/float(valBase) )
      upSFrac.append( float(valSUp)/float(valBase) )
      downFrac.append( float(valDown)/float(valBase) )
      downSFrac.append( float(valSDown)/float(valBase) )

upLine = splBase[0]+" Up5 Frac & "
upSLine = splBase[0]+" Up10 Frac & "
downLine = splBase[0]+" Down5 Frac & "
downSLine = splBase[0]+" Down10 Frac & "

for up, sup, down, sdown in zip(upFrac, upSFrac, downFrac, downSFrac):
   upLine += "%.5s & "%str(up)
   upSLine += "%.5s & "%str(sup)
   downLine += "%.5s & "%str(down)
   downSLine += "%.5s & "%str(sdown)

#if len(argv)>3: print "\n"+downLine[:-2]+" \\\\"

if len(argv)>4: print upSLine[:-2]+" \\\\"+"\n"
print upLine[:-2]+" \\\\"+"\n"
if len(argv)>4: print downSLine[:-2]+" \\\\"+"\n"
print downLine[:-2]+" \\\\"+"\n"
