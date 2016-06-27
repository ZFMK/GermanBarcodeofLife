#!/usr/bin/python
# -*- coding: utf-8 -*-
import cgi, cgitb
#cgitb.enable()
import sys
import os.path, os

# import Navigation as nav
import L2F_V1_navigation as nav1
import TEPN_V1_navigation as nav2


print "Content-type: text/html"  # unterdrueckt Fenster 'Oeffnen von script'

print """
<html>
<head><title>Web_Pgms_GBOL_ZFMK</title></head>
<link type="text/css" rel="stylesheet" href="style.css">
<body>
"""

print """
	<img src="img/gen2dc.png" alt="Transfer Geneious data to Diversity Collection">
	<br/>
	<br/>
	<h1>GBOL Webserver Programs</h1><br/>
	<br/>
	<h2 class="pane-title">LIMS2FIMS Transfer Data</h2>
	<div class="pane-content">
	<p>Transfer passed/failed sequences from the Lab-DB (Geneious) into the collection-DB (Diversity Collection)</p>
"""

print nav1.navigation('start')

print """
	</div>

	<h2 class="pane-title">TEPN Transfer Extraction Plate names</h2>
	<div class="pane-content">
	<p>Plate names from the Lab-DB (Geneious) into the collection-DB (Diversity Collection)</p>
"""

print nav2.navigation('start')

print "</div>"

#	<form method="GET" action="TEPN_V1_status.py"/>
#		<input type="submit" value=" Uebertrage Extraction-Plate Namen aus der Lims DB (geneious) in die Fims DB (DWB) "/>
#	</form>

print """
<div class="copyright"><a href="http://www.zfmk.de">(c) ZFMK</a>
</body>
</html>
"""
