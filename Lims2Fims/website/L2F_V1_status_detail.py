#!/usr/bin/python
# -*- coding: utf8 -*-

# from: https://wiki.python.org/moin/CgiScripts
# und: https://docs.python.org/2/library/cgi.html

import cgi
import cgitb; cgitb.enable()  # for troubleshooting
import MySQLdb as mdb

import L2F_V1_status as sdb
import L2F_V1_navigation as nav

class StatusClassDetail(sdb.StatusClass):
	def __init__(self):
		sdb.StatusClass.__init__(self)
		self.status_data_detail_fieldnames = []
		self.status_data_detail = []

	def get_detail(self,form1):
		sql = "SELECT id,workflowId as workflow,extractionId,dwb_CollectionSpecimenId as CollSpecId,sampleId,status,note,assemProgress as assProgress,assemNotes as assNotes,assemPlateSuffix as assPlateSuffix,assemContam as assContam"
		sql = sql + ",pcrAnzahl as Pcrs,cycleSeqForwAnzahl as SeqForws,cycleSeqForwTraceAnzahl as SeqFTraces,cycleSeqRevAnzahl as SeqRevs,cycleSeqRevTraceAnzahl as SeqRTraces"
		sql = sql + " FROM assembly_export_COI"
		sql = sql + " WHERE id>0"
		if 'status_type' in form1:
			sql = sql + (" and status='%s'" % form1.getvalue('status_type'))
		elif 'h_status_type' in form1:
			sql = sql + (" and status='%s'" % form1.getvalue('h_status_type'))
		else:
			sql = sql + " and status='ok'"
		if 'id_gleich' in form1:
			try:
				vari = int(form1.getvalue('id_gleich'))     #throw exception if not an integer
			except TypeError as e:
				print ("<br/>id_gleich:%s<br/>" % e)
				vari = 0
			except ValueError as e:
				print ("<br/>id_gleich:%s<br/>" % e)
				vari = 0
			if vari > 0:
				sql = sql + (" and id=%i" % vari)
		if 'id_groesser_gleich' in form1:
			try:
				vari = int(form1.getvalue('id_groesser_gleich'))     #throw exception if not an integer
			except TypeError as e:
				print ("<br/>id_groesser_gleich:%s<br/>" % e)
				vari = 0
			except ValueError as e:
				print ("<br/>id_groesser_gleich:%s<br/>" % e)
				vari = 0
			if vari > 0:
				sql = sql + (" and id>=%i" % vari)
		if 'id_kleiner_gleich' in form1:
			try:
				vari = int(form1.getvalue('id_kleiner_gleich'))     #throw exception if not an integer
			except TypeError as e:
				print ("<br/>id_kleiner_gleich:%s<br/>" % e)
				vari = 0
			except ValueError as e:
				print ("<br/>id_kleiner_gleich:%s<br/>" % e)
				vari = 0
			if vari > 0:
				sql = sql + (" and id<=%i" % vari)
		if ('note_like' in form1) and (form1.getvalue('note_like')<>'Null'):
				sql = sql + (" and note like '%s'" % form1.getvalue('note_like'))
		if ('plate_like' in form1) and (form1.getvalue('plate_like')<>'Null'):
				sql = sql + (" and assemPlateSuffix like '%s'" % form1.getvalue('plate_like'))
		sql = sql + " Order by id"
		sql = sql + " Limit 100"
		print ("""<br/><p class="status-msg">%s</p>""" % sql)  # Debug
		for k in form1.keys():
			print "<br/>%s: %s" % (k, form1.getvalue(k)) # Debug
		print "<br/><br/>"
		self.cur.execute(sql)
		self.status_data_detail_fieldnames = self.cur.description
		self.status_data_detail = self.cur.fetchall()

	def __repr__(self):
		return repr(self.status_data_detail)

	def set_filter(self, form2):
		maxIdExport = '0'
		sql_maxIdExport = """Select max(id) from assembly_export_COI"""
		self.cur.execute(sql_maxIdExport)
		for mid in self.cur.fetchall():
			maxIdExport = '%s' % mid[0]

		resB = []
		B = resB.append
		resB.append('<form action="L2F_V1_status_detail.py" method="GET">')

		if ('status_type' in form2):
			B('<h3> Status-Typ=%s, MaxId=%s</h3>' % (form2.getvalue('status_type'), maxIdExport))
			B('<input name="h_status_type" type="hidden" size="100" maxlength="100" value="%s"/>' % form2.getvalue('status_type'))
		elif ('h_status_type' in form2):
			B('<h3> Status-Typ=%s, MaxId=%s</h3>' % (form2.getvalue('h_status_type'), maxIdExport))
			B('<input name="h_status_type" type="hidden" size="100" maxlength="100" value="%s"/>' % form2.getvalue('h_status_type'))
		else:
			B('<h3> Status-Typ=ok, MaxId=%s</h3>' % maxIdExport)
			B('<input name="h_status_type" type="hidden" size="100" maxlength="100" value="ok"/>')

		B('<br/>')
		B('Filter:<br/>')
		if ('id_gleich' in form2) and (form2.getvalue('id_gleich')<>'0'):
			B('Id=:<input name="id_gleich" type="text" size="20" maxlength="20" value="%s"/>(0=Filter off)<br/>' % form2.getvalue('id_gleich'))
		else:
			B('Id=:<input name="id_gleich" type="text" size="20" maxlength="20" value="0"/>(0=Filter off)<br/>')
		if ('id_kleiner_gleich' in form2) and (form2.getvalue('id_kleiner_gleich')<>'0'):
			B('Id<=:<input name="id_kleiner_gleich" type="text" size="20" maxlength="20" value="%s"/>(0=Filter off)<br/>' % form2.getvalue('id_kleiner_gleich'))
		else:
			B('Id<=:<input name="id_kleiner_gleich" type="text" size="20" maxlength="20" value="0"/>(0=Filter off)<br/>')
		if ('id_groesser_gleich' in form2) and (form2.getvalue('id_groesser_gleich')<>'0'):
			B('Id>=:<input name="id_groesser_gleich" type="text" size="20" maxlength="20" value="%s"/>(0=Filter off)<br/>' % form2.getvalue('id_groesser_gleich'))
		else:
			B('Id>=:<input name="id_groesser_gleich" type="text" size="20" maxlength="20" value="0"/>(0=Filter off)<br/>')
		if ('note_like' in form2) and (form2.getvalue('note_like')<>'Null'):
			B('Note like:<input name="note_like" type="text" size="150" maxlength="150" value="%s"/>(Null=Filter off)<br/>' % form2.getvalue('note_like'))
		else:
			B('Note like:<input name="note_like" type="text" size="150" maxlength="150" value="Null"/>(Null=Filter off)<br/>')
		if ('plate_like' in form2) and (form2.getvalue('plate_like')<>'Null'):
			B('Plate_Suffix like:<input name="plate_like" type="text" size="100" maxlength="100" value="%s"/>(Null=Filter off)<br/>' % form2.getvalue('plate_like'))
		else:
			B('Plate_Suffix like:<input name="plate_like" type="text" size="100" maxlength="100" value="Null"/>(Null=Filter off)<br/>')
		B('<br/>')
		B('<button name="filter_refresh" value="DoFilterRefresh" type="submit"> Refresh filter </button>')

		B('</form>')
		return "".join(resB)  # verknüpft Listenelemente (entfernt die Kommas)

	def show_data(self, form1):
		resA = []
		A = resA.append
		resA.append('<form action="L2F_V1_status.py" method="post">')
		resA.append('<table border="1">')

		A('<br/>')

		A('<tr>') # Spaltennamen
		if ('status_type' in form1) and ((form1.getvalue('status_type')=='prepared') or (form1.getvalue('status_type')=='error')):
			A('<th>Reset</th>')
		if ('h_status_type' in form1) and ((form1.getvalue('h_status_type')=='prepared') or (form1.getvalue('h_status_type')=='error')):
			A('<th>Reset</th>')
		for fieldname in self.status_data_detail_fieldnames:  # -- Spaltennamen
			A('<th>{0}</th>'.format(fieldname[0]))
		A('</tr>')

		for row in self.status_data_detail:  # -- laufe durch alle Einträge
			A('<tr>')
			if ('status_type' in form1) and ((form1.getvalue('status_type')=='prepared') or (form1.getvalue('status_type')=='error')):
				A('<td><input type="checkbox" name="reset" value="{0}"/></td>'.format(row[0]))
			if ('h_status_type' in form1) and ((form1.getvalue('h_status_type')=='prepared') or (form1.getvalue('h_status_type')=='error')):
				A('<td><input type="checkbox" name="reset" value="{0}"/></td>'.format(row[0]))
			for value in row:  # -- jeder Wert in item
				A('<td>{0}</td>'.format(value))
			A('</tr>')

		A('</table>')

		vari = 0
		if ('status_type' in form1) and (form1.getvalue('status_type')=='prepared'):
			A('<input type="checkbox" onClick="select_all(this)" /><span id="toggle_select_text">Select All</span><br/><br/>')
			A('<button name="submit_reset" value="Goprepared" type="submit"> Do Reset </button>')
			vari=1
		if ('h_status_type' in form1) and (form1.getvalue('h_status_type')=='prepared'):
			A('<input type="checkbox" onClick="select_all(this)" /><span id="toggle_select_text">Select All</span><br/><br/>')
			A('<button name="submit_reset" value="Goprepared" type="submit"> Do Reset </button>')
			vari=1
		if ('status_type' in form1) and (form1.getvalue('status_type')=='error'):
			A('<input type="checkbox" onClick="select_all(this)" /><span id="toggle_select_text">Select All</span><br/><br/>')
			A('<button name="submit_reset" value="Goerror" type="submit"> Do Reset </button>')
			vari=1
		if ('h_status_type' in form1) and (form1.getvalue('h_status_type')=='error'):
			A('<input type="checkbox" onClick="select_all(this)" /><span id="toggle_select_text">Select All</span><br/><br/>')
			A('<button name="submit_reset" value="Goerror" type="submit"> Do Reset </button>')
			vari=1
		A('<button name="Back_to_Status_Overview" value="BackToStatusOverview" type="submit"> Back to status overview </button>')

		A('</form>')

		return "".join(resA)  # verknüpft Listenelemente (entfernt die Kommas)

def main():
	form = cgi.FieldStorage()

	# print "Content-type: text/html\x0D\x0A"
	print "Content-type: text/html"

	print """
	<html>

	<head><title>L2F_V1_status_detail</title></head>
	<link type="text/css" rel="stylesheet" href="style.css">

	<script language="JavaScript">
		function select_all(source) {
			var checkboxes = document.getElementsByName('reset');
			var n=checkboxes.length;
			var i = 0;
			var text = document.getElementById('toggle_select_text');
			for(var i; i<n; i++) {
				checkboxes[i].checked = source.checked;
			}
			if (source.checked) {
				text.innerHTML='Unselect All';
			} else {
				text.innerHTML='Select All';
			}
		}
	</script>

	<body>"""

	print nav.navigation('status_detail')

	print """<h1> L2F_V1_status_detail Version 1.0 </h1><br/>
	"""

	status_class_detail = StatusClassDetail()
	print status_class_detail.set_filter(form2=form)
	status_class_detail.get_detail(form)

	print status_class_detail.show_data(form1=form)
	status_class_detail.final()

	print """
	</body>

	</html>
	"""

if __name__ == "__main__":
	main()
