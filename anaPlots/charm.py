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

###-------------------------------------------------------------------###
                        ### Main Program ###
###-------------------------------------------------------------------###

runMode     = conf.mode()
switches    = conf.switches()

if runMode=="plotting":
  if switches["plotMode"]=="anaPlots":
    anaP.runAnaPlots()
  if switches["plotMode"]=="standardPlots":
    anaP.runStandPlots()
  if switches["plotMode"]=="comparisonPlots":
    anaP.runComparPlots()
      
elif runMode=="yieldTables":
  print "\n  >>>  Making yield tables\n"

  tabl.printTable()
  
