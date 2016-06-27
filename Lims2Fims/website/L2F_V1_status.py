#!/usr/bin/python
# -*- coding: utf8 -*-

# from: https://wiki.python.org/moin/CgiScripts
# und: https://docs.python.org/2/library/cgi.html

import cgi
import cgitb; cgitb.enable()  # for troubleshooting
import MySQLdb as mdb
import L2F_V1_navigation as nav
import ConfigParser
config = ConfigParser.SafeConfigParser()
config.read('../config.ini')

Status_Lex = {'ok': 'OK', 'deleted': 'Deleted', 'ignore_already_passed_less': 'Already passed sequences',
	'ignore_failed': 'Failed sequences', 'prepared': 'Prepared (maybe transfer of sequences is necessary)',
	'error': 'Error', 'new': 'New datarows (run program LIMS2FIMS transfer sequences)', 'obsolete': 'Transferred sequence is obsolete' }

class StatusClass(object):
	def __init__(self):
		self.con = self.mysql_connect()
		self.cur = self.con.cursor()
		self.status_data = {}
		self.maxIdAssem = '0'
		self.maxIdExport = '0'
		self.countAssem = '0'
		self.countExport = '0'

	def mysql_connect(self):
		DB = {}
		for option in config.options('lims2fims_mysql'):
			DB[option] = config.get('lims2fims_mysql', option)
		try:
			con = mdb.connect(host=DB['host'], user=DB['user'], passwd=DB['passwd'], db=DB['database'])
		except mdb.Error, e:
			print "Error %d: %s" % (e.args[0],e.args[1])
			sys.exit(1)
		return con

	def final(self):
		## Trenne die Verbindungen zu den Datenbanken'
		self.con.close()

	def get_status(self):
		sql_status = """Select count(ae.id) as `count`, ae.`status` from assembly_export_COI as ae group by status order by count(ae.id) desc"""
		self.cur.execute(sql_status)
		for row in self.cur.fetchall():
			r = {t[0]: value for (t, value) in zip(self.cur.description, row)}
			# -- mappen von Spaltenüberschriften (cur.description) auf Werte (row) und Aufbau eines Dictionaries mit key/value-Paaren: key = Spaltenname, value = Wert
			self.status_data[r['status']] = r['count']

		sql_maxIdAssem = """Select max(id) from assembly"""
		self.cur.execute(sql_maxIdAssem)
		for mid in self.cur.fetchall():
			self.maxIdAssem = '%s' % mid[0]

		sql_maxIdExport = """Select max(id) from assembly_export_COI"""
		self.cur.execute(sql_maxIdExport)
		for mid in self.cur.fetchall():
			self.maxIdExport = '%s' % mid[0]

		sql_countAssem = """Select count(*) from assembly"""
		self.cur.execute(sql_countAssem)
		for mid in self.cur.fetchall():
			self.countAssem = '%s' % mid[0]

		sql_countExport = """Select count(*) from assembly_export_COI"""
		self.cur.execute(sql_countExport)
		for mid in self.cur.fetchall():
			self.countExport = '%s' % mid[0]


	def reset_status(self, id_list):
		sql_reset = "Update assembly_export_COI Set status='new' Where (status='error' or status='prepared') and id in ({0})".format(",".join(id_list))
		print '<h3>Reset:</h3>'
		print '<p>%s</p>' % sql_reset
		try:
			self.cur.execute(sql_reset)
			self.con.commit()
		except mdb.Error, e:
			raise mdb.Error, "Error %d: %s" % (e.args[0],e.args[1])
		else:
			return '<p>%s</p>' % sql_reset

	def __repr__(self):
		return repr(self.status_data)

	def __data_cell(self, keys, not_shown=[]):
		# called by show_data: display table row
		resB = []
		B = resB.append
		for k in keys:
			if k not in not_shown:
				B('<tr>')
				if k in Status_Lex:
					B('<td width="60%">{0}</td><td width="20%">{1}</td><td width="20%"><button name="status_type" value="{2}" type="submit">detail</button></td>'.format(Status_Lex[k], self.status_data[k], k))
				else:
					B('<td width="60%">{0}</td><td width="20%">{1}</td><td width="20%"><button name="status_type" value="{2}" type="submit">detail</button></td>'.format(k, self.status_data[k], k))
				B('</tr>')
		return resB

	#	def __str__(self): ersetzt durch def show_data(self, form1):
	def show_data(self, form1):
		resA = []
		A = resA.append
		resA.append('<form action="L2F_V1_status_detail.py" method="GET">')

		if ('new' in self.status_data):
			A('<h3>OK and New</h3>')
		else:
			A('<h3>OK</h3>')
		A('<table border="1" width="100%">')
		if ('new' in self.status_data):
			resA.extend(self.__data_cell(['ok', 'new']))
		else:
			resA.extend(self.__data_cell(['ok']))
		A('</table>')

		#del self.status_data['ok']  # lösche aus dictionary

		if (('prepared' in self.status_data) or ('error' in self.status_data)):
			A('<br/>')
			A('<br/>')
			A('<br/>')
			A('<h3>Error handling</h3>')
			if (('error' in self.status_data) and ('prepared' not in self.status_data)):
				A('<table border="1" width="100%">')
				resA.extend(self.__data_cell(['error']))
				A('</table>')
			elif (('prepared' in self.status_data) and ('error' not in self.status_data)):
				A('<table border="1" width="100%">')
				resA.extend(self.__data_cell(['prepared']))
				A('</table>')
			else:
				A('<table border="1" width="100%">')
				resA.extend(self.__data_cell(['prepared', 'error']))
				A('</table>')

		A('<br/>')
		A('<br/>')
		A('<br/>')
		A('<h3>Informational</h3>')
		A('<table border="1" width="100%">')
		resA.extend(self.__data_cell(self.status_data.keys(), not_shown=['ok', 'prepared', 'error', 'new']))
		A('</table>')

		A('</form>')

		A('<br/>')
		A('<form method="GET" action="L2F_V1_start_pgm.py">')
		A('<input type="submit" value="Transfer sequences from Geneious DB into Diversity Collection DB"/>')
		A('</form>')

		return "".join(resA)  # verknüpft Listenelemente (entfernt die Kommas)

def main():
	print "Content-type: text/html"

	print """
	<html>

	<head><title>L2F_V1_status</title></head>
	<link type="text/css" rel="stylesheet" href="style.css">

	<body>"""
	print nav.navigation('status')
	print """<h1> L2F_V1_status Version 1.0 </h1>
	<!-- <p>MySQL DB connection and status query</p> -->
	<p>Overview of data sucessfully transferred into Diversity Collection DB and errors that are in the Geneious database that blocks data transfer!</p>
	<p>Click on <strong>detail</strong> to get an overview and to reset erroneous data (after correcting the errors).</p>
	"""

	form = cgi.FieldStorage()
	status_class = StatusClass()

	if 'submit_reset' in form and 'reset' in form:
		reset_list = form.getlist('reset')
		if (form.getvalue('submit_reset')=='Goprepared') or (form.getvalue('submit_reset')=='Goerror'):
			try:
				ret = status_class.reset_status(reset_list)
			except Exception, e:
				print '<h3>Error:</h3>'
				print '<p>No data reset!<br/>Error detail:<br/><pre>'
				print e #  error message
				print '</pre></p>'
			else:  #  reset succesfull
				print '<p>Reset of data successfull!</p>'

	status_class.get_status()

	if (status_class.maxIdAssem <> status_class.maxIdExport):
		print """<h3> Transfer sequences from Geneious DB into Diversity Collection DB is necessary, MaxIdAssem=%s MaxIdExport=%s </h3>""" % (status_class.maxIdAssem, status_class.maxIdExport)
	#else:
	#	print """<h3> MaxIdAssem=%s MaxIdExport=%s </h3>""" % (status_class.maxIdAssem, status_class.maxIdExport)

	print status_class.show_data(form1=form)
	print repr(status_class) # die 'rohen' Daten

	print """<p> MaxIdAssem=%s MaxIdExport=%s CountAssem=%s CountExport=%s </p>""" % (status_class.maxIdAssem, status_class.maxIdExport, status_class.countAssem, status_class.countExport)

	status_class.final()

	print """
	<!-- <a href="zweite.html">Zur&uuml;ck zur zweiten HTML Seite</a> -->
	</body>

	</html>
	"""

if __name__ == "__main__":
	main()
