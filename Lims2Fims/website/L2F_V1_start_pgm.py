#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess
from datetime import datetime
import cgi, cgitb
#cgitb.enable()
import sys
import os.path, os
import time
# import Navigation as nav
import L2F_V1_navigation as nav

logfilename = '../log/L2F_V1_start_pgm.log'
pidfilename = '../log/L2F_V1_run_pgm.pid'

def run(loghandle):
	print '<h3> Program Lims2Fims started.... </h3><br/>'
	p1 = subprocess.Popen('./L2F_V1_run_pgm.py called_by_L2F_start_pgm', shell=True, universal_newlines=True, stdout=loghandle, stderr=loghandle)
	time.sleep(3)


print "Content-type: text/html"

log = open(logfilename, "a")

print """
<html>
<head><title>L2F_V1_start_pgm</title></head>
<link type="text/css" rel="stylesheet" href="style.css">
<body>
"""
print nav.navigation('transfer_seqs')

print """<h1> L2F_V1_start_pgm Version 1.0 </h1><br/>
"""

form1 = cgi.FieldStorage()
if ('h_start_pgm' in form1) and (form1.getvalue('h_start_pgm')=='1'):
	run(log)

if os.path.isfile(pidfilename):
	print '<h3> Program Lims2Fims L2F is running. Please wait about 2 minutes before checking program progress .... </h3><br/>'
	print """
		<form method="GET" action="L2F_V1_start_pgm.py">
			<input type="submit" value=" Check program progress "/>
		</form>
	"""
else:
	print '<h3> Program Lims2Fims L2F has ended or is not running at the moment.</h3><br/>'
	print """
		<form method="GET" action="L2F_V1_start_pgm.py">
			<input type="submit" value=" Start program Lims2Fims "/>
			<input name="h_start_pgm" type="hidden" size="20" maxlength="20" value="1"/>
		</form>
	"""

print """
  <br/>
	<form method="GET" action="L2F_V1_status.py"/>
		<input type="submit" value=" Back to status overview "/>
	</form>
</body>
</html>
"""

log.flush()
log.close()

