#!/usr/bin/python
# -*- coding: utf8 -*-

# from: https://wiki.python.org/moin/CgiScripts
# und: https://docs.python.org/2/library/cgi.html

import cgi
import cgitb; cgitb.enable()  # for troubleshooting
import MySQLdb as mdb
import TEPN_V1_navigation as nav2
import ConfigParser
config = ConfigParser.SafeConfigParser()
config.read('../config.ini')

DB = {'host': "131.220.75.4",
	'user': "gbol_db_user",
	'passwd': "s1puncula",
	'database': "lims"}

Status_Lex = {'ok': 'OK', 'deleted': 'Deleted', 'ignore': 'Ignore entry, since sampleId is not supported (for example N-Probe)',
	'prepared': 'Prepared for Extraction-Plate-Name transfer into Diversity Collection DB', 'error': 'Error', 'new': 'New datarows (run program TEPN Transfer Extraction-Plate Names)' }

class StatusClass(object):
	def __init__(self):
		self.con = self.mysql_connect()
		self.cur = self.con.cursor()
		self.status_data = {}
		self.maxIdExtraction = '0'
		self.maxIdTransfer = '0'
		self.countExtraction = '0'
		self.countTransfer = '0'

	def mysql_connect(self, db_params):
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
		sql_status = """Select count(t.id) as `count`, t.`status` from Transfer_Extr_Plate_Name as t group by t.status order by count(t.id) desc"""
		self.cur.execute(sql_status)
		for row in self.cur.fetchall():
			r = {t[0]: value for (t, value) in zip(self.cur.description, row)}
			# -- mappen von Spaltenüberschriften (cur.description) auf Werte (row) und Aufbau eines Dictionaries mit key/value-Paaren: key = Spaltenname, value = Wert
			self.status_data[r['status']] = r['count']

		sql_maxIdExtraction = """Select max(id) from extraction"""
		self.cur.execute(sql_maxIdExtraction)
		for mid in self.cur.fetchall():
			self.maxIdExtraction = '%s' % mid[0]

		sql_maxIdTransfer = """Select max(id) from Transfer_Extr_Plate_Name"""
		self.cur.execute(sql_maxIdTransfer)
		for mid in self.cur.fetchall():
			self.maxIdTransfer = '%s' % mid[0]

		sql_countExtraction = """Select count(*) from extraction"""
		self.cur.execute(sql_countExtraction)
		for mid in self.cur.fetchall():
			self.countExtraction = '%s' % mid[0]

		sql_countTransfer = """Select count(*) from Transfer_Extr_Plate_Name"""
		self.cur.execute(sql_countTransfer)
		for mid in self.cur.fetchall():
			self.countTransfer = '%s' % mid[0]

	def reset_status(self, id_list):
		sql_reset = "Update Transfer_Extr_Plate_Name Set status='new' Where status='error' and id in ({0})".format(",".join(id_list))
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
		resA.append('<form action="TEPN_V1_status_detail.py" method="GET">')

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

		if ('error' in self.status_data):
			A('<br/>')
			A('<br/>')
			A('<br/>')
			A('<h3>Error handling</h3>')
			A('<table border="1" width="100%">')
			resA.extend(self.__data_cell(['error']))
			A('</table>')

		A('<br/>')
		A('<br/>')
		A('<br/>')
		A('<h3>Informational</h3>')
		A('<table border="1" width="100%">')
		resA.extend(self.__data_cell(self.status_data.keys(), not_shown=['ok', 'error', 'new']))
		A('</table>')

		A('</form>')

		A('<br/>')
		A('<form method="GET" action="TEPN_V1_start_pgm.py">')
		A('<input type="submit" value="Transfer Extraction-Plate names"/>')
		A('</form>')

		return "".join(resA)  # verknüpft Listenelemente (entfernt die Kommas)

def main():
	print "Content-type: text/html"

	print """
	<html>

	<head><title>TEPN_V1_status</title></head>
	<!-- <link type="text/css" rel="stylesheet" href="style.css"> -->
	<link type="text/css" rel="stylesheet" href="style.css">

	<body>
	"""

	print nav2.navigation('status')

	print """
	<h1> TEPN_V1_status Version 1.0 </h1>
	<p>Overview of Extraction-Plate names transferred to Diversity Collection and errors that are in the Geneious database that blocks data transfer!</p>
	<p>Click on <strong>detail</strong> to get an overview and to reset erroneous data (after correcting the errors).</p>
	"""

	form = cgi.FieldStorage()
	status_class = StatusClass()

	if 'submit_reset' in form and 'reset' in form:
		reset_list = form.getlist('reset')
		if (form.getvalue('submit_reset')=='Goerror'):
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

	if (status_class.maxIdExtraction <> status_class.maxIdTransfer):
		print """<h3> Transfer Extraction-Plate names is necessary, MaxIdExtraction=%s MaxIdTransfer=%s </h3>""" % (status_class.maxIdExtraction, status_class.maxIdTransfer)
	#else:
	#	print """<h3> MaxIdExtraction=%s MaxIdTransfer=%s </h3>""" % (status_class.maxIdExtraction, status_class.maxIdTransfer)

	print status_class.show_data(form1=form)
	print repr(status_class) # die 'rohen' Daten

	print """<p> MaxIdExtraction=%s MaxIdTransfer=%s CountExtraction=%s CountTransfer=%s </p>""" % (status_class.maxIdExtraction, status_class.maxIdTransfer, status_class.countExtraction, status_class.countTransfer)

	status_class.final()

	print """
	</body>

	</html>
	"""

if __name__ == "__main__":
	main()
