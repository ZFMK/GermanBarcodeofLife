#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess
from datetime import datetime
import sys
import os.path, os
import TEPN_V1_navigation as nav2


logfilename = '../log/TEPN_V1_run_pgm.log'
pidfilename = '../log/TEPN_V1_run_pgm.pid'
# cmd = "ping -c5 www.google.de"
cmd = "../Transfer_Extr_Plate_Name3.py"

def show_error(msg):
	print "Content-type: text/html"  # unterdrueckt Fenster 'Oeffnen von script'
	print """
	<html>
	<head><title>TEPN_V1_run_pgm</title></head>
	<link type="text/css" rel="stylesheet" href="style.css">
	<body>"""

	print nav2.navigation('run_pgm')

	print """<h1> TEPN_V1_run_pgm Version 1.0 </h1><br/>
	"""

	print '<h3> %s </h3><br/>' % msg

	print """
	<br/>
	<form method="GET" action="TEPN_V1_status.py"/>
	<input type="submit" value=" Back to status overview "/>
	</form>
	</body>
	</html>
	"""

def run(cmd, loghandle):
	pidfile = open(pidfilename, 'w')
	p = subprocess.Popen(cmd, shell=True, universal_newlines=True, stdout=loghandle, stderr=loghandle)
	pidfile.write(str(p.pid))
	pidfile.close()
	p.wait()
	os.remove(pidfilename)


# = main =========
#print "Content-type: text/html"  # unterdrueckt Fenster 'Oeffnen von script'
if len(sys.argv) <> 2:
	show_error('Program call not supported, number of parameter.')
	sys.exit(1)

if (sys.argv[1] <> 'called_by_TEPN_start_pgm'):
	show_error('Program call not supported, input variable.')
	sys.exit(1)

if os.path.isfile(pidfilename):
	show_error('Program Transfer-Extraction-Platten-Names TEPN is already running.')
	sys.exit(1)

try:
	log = open(logfilename, "a")
except IOError, e:
	msg1 = 'Error creating logfile %s: %s' % (logfilename,e.args[1])  # -- (13, "Permission denied")
	show_error(msg1)
	sys.exit(1)

today1 = datetime.today()
print >> log, "\nTEPN started: %s" % today1.strftime('%d-%m-%Y %H:%M:%S')
log.flush()

try:
	run(cmd, log)
except IOError, e:
	msg2 = 'Error creating pidfile %s: %s' % (pidfilename,e.args[1])
	print >> log, msg2
	show_error(msg2)
	log.flush()
	log.close()
	sys.exit(1)

today2 = datetime.today()
print >> log, "\nTEPN ended: %s" % today2.strftime('%d-%m-%Y %H:%M:%S')

log.flush()
log.close()
