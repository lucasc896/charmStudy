#!/usr/bin/env python
# encoding: utf-8
"""
charm.py

Created by Chris Lucas on 2012-11-14.
Copyright (c) 2012 University of Bristol. All rights reserved.
"""
import sys
import configuration as conf
import tables as tabl
import makeAnaPlots as anaP
import bTagPlots as bTagP
from optparse import OptionParser
from Log import *

sys.path.append("/path/to/tools/LogTools/")

parser = OptionParser()

parser.add_option("-d", "--debug",
                  action="store_true", dest="doDebug", default=False,
                  help="run code in Debug mode")

(options, args) = parser.parse_args()

def line():
   return "="*40

###-------------------------------------------------------------------###
                        ### Main Program ###
###-------------------------------------------------------------------###

if options.doDebug:
   print "\n"
   Log.debug("\t>>> RUNNING IN DEBUG MODE\n")

if conf.mode()=="anaPlots":
   
   print "\n%s"%line()
   print "  ***// Running anaPlots Analysis \\***"
   print line()+"\n"
   
   if conf.switches()["runMode"]=="plotting":
      if conf.switches()["plotMode"]=="anaPlots":
         anaP.runAnaPlots(debug=options.doDebug)
      if conf.switches()["plotMode"]=="standardPlots":
         anaP.runStandPlots(debug=options.doDebug)
      if conf.switches()["plotMode"]=="comparisonPlots":
         anaP.runComparPlots(debug=options.doDebug, doLogy=False)
         if conf.switches()["printLogy"]:
            anaP.runComparPlots(debug=options.doDebug, doLogy=True)         
        
   elif conf.switches()["runMode"]=="yieldTables":

      if len( conf.bMulti() )>1:
         print "\n"
         Log.error("*** ERROR: Too many b-tag multiplicities for yield mode. ***")
         Log.error("\tChange 'bMulti()' in configurtion.py\n")
         sys.exit()
      
      print "\n  >>>  Making yield tables\n"
      tabl.printTable(debug=options.doDebug)


elif conf.mode()=="bTagEff":
   
   print "\n%s"%line()
   print "  ***// Running anaPlots Analysis \\***"
   print line()+"\n"
   
   if conf.switches()["runModeBTag"]=="charmFrac":
      bTagP.jetCharmFrac(debug=options.doDebug)
   elif conf.switches()["runModeBTag"]=="standardPlots":
      bTagP.runStandPlots(debug=options.doDebug)
   elif conf.switches()["runModeBTag"]=="charmPhi":
      bTagP.doCharmPhiStudy(debug=options.doDebug)


elif conf.mode()=="dev":
   pass

