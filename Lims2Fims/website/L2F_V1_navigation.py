#!/usr/bin/python
# -*- coding: utf8 -*-
"""
	Lims2Fims Navigation module
	Version 1
	2015-01-04: new
"""
def navigation(current=''):
	sort_keys = ['start','status','transfer_seqs']
	titles = {
		'start':['Start applications of the GBOL-ZFMK Lab','index.py'],
		'transfer_seqs':['Lims2Fims transfer sequences','L2F_V1_start_pgm.py'],
		'status':['Lims2Fims status overview','L2F_V1_status.py']
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
