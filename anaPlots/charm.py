#!/usr/bin/env python
# encoding: utf-8
"""
tables.py

Created by Chris Lucas on 2012-11-14.
Copyright (c) 2012 University of Bristol. All rights reserved.
"""

import configuration as conf
import tables as tabl
import makeAnaPlots as anaP
import bTagPlots as bTagP

def printLine():
   print "========================================="

###-------------------------------------------------------------------###
                        ### Main Program ###
###-------------------------------------------------------------------###

#runMode     = conf.mode()
switches    = conf.switches()

if conf.mode()=="anaPlots":
   printLine()
   print "  ***// Running anaPlots Analysis \\***"
   printLine()
   if switches["runMode"]=="plotting":
      if switches["plotMode"]=="anaPlots":
         anaP.runAnaPlots()
      if switches["plotMode"]=="standardPlots":
         anaP.runStandPlots()
      if switches["plotMode"]=="comparisonPlots":
         anaP.runComparPlots()
        
   elif switches["runMode"]=="yieldTables":
      print "\n  >>>  Making yield tables\n"
      tabl.printTable()


elif conf.mode()=="bTagEff":
   printLine()
   print "  ***// Running anaPlots Analysis \\***"
   printLine()
   if switches["runMode"]=="plotting":
      if switches["plotMode"]=="standardPlots":
         bTagP.runStandPlots()

