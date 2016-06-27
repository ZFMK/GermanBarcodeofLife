#!/usr/bin/python
# -*- coding: utf8 -*-
"""
	TEPN Navigation module
	Version 1
	2015-01-05: new
"""
def navigation(current=''):
	sort_keys = ['start','status','transfer_epn']
	titles = {
		'start':['Start applications of the GBOL-ZFMK Lab','index.py'],
		'transfer_epn':['TEPN Transfer Extraction-Plate Names','TEPN_V1_start_pgm.py'],
		'status':['TEPN status overview','TEPN_V1_status.py']
	}
	resA = []
	A = resA.append
	A('<div id="navi_head">')
	A('<ul>')
	for key in sort_keys:
		if key=='start' and current=='start':
			continue
		item = titles[key]
		if current==key:
			A('<li><a href="%s" class="active">%s</a></li>' % (item[1], item[0]))
		else:
			A('<li><a href="%s">%s</a></li>' % (item[1], item[0]))
	A('</ul>')
	A('</div>')
	return "".join(resA)
