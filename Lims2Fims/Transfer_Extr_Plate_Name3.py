#!/usr/bin/python
"""
Transfer_Extr_Plate_Name
    Logik
	1) Suche neue Eintraege in der LIMS Tabelle extraction und speichere diese in die LIMS Tabelle Transfer_Extr_Plate_Name.
	2) Fuelle die LIMS Tabelle Transfer_Extr_Plate_Name mit Informationen aus der Tabelle extraction und plate.
	3) Suche in der LIMS Tabelle Transfer_Extr_Plate_Name nach vorbereiteten Eintraegen (Status=prepared). Fuer jeden vorbereiteten Eintrag:
	  a) Suche den zugehoerigen Eintrag in der FIMS Tabelle CollectionSpecimen.
	  b) Schreibe den Extractionsplattenname (oder die Extractionsplattenname) in das feld AdditionalNotes.
	  c) Setze fuer den aktuellen vorbereiteten Eintrag den Status=ok.

	Aenderungen:
		V2 Neuer MySQL Server geneious01 -> geneiousdb01
		V2 Aktiviere Call von stored Procedures
		V3 Setze Status von ignore auf error

"""
import MySQLdb as mdb
import pyodbc
import pprint
import sys
import os
import base64
import md5
import time
import ConfigParser
config = ConfigParser.SafeConfigParser()
config.read('./config.ini')

ENVIRONMENT = config.get('option', 'environment')
MS_SQL_DB = config.get(ENVIRONMENT, 'mssql_database')


def mysql_connect():
	DB = {}
	for option in config.options('lims2fims_mysql'):
		DB[option] = config.get('lims2fims_mysql', option)
	try:
		con = mdb.connect(host=DB['host'], user=DB['user'], passwd=DB['passwd'], db=DB['database'])
	except mdb.Error, e:
		print "Error %d: %s" % (e.args[0],e.args[1])
		sys.exit(1)
	return con

def final():
	## Trenne die Verbindungen zu den Datenbanken'
	db.close()
	cnxn.close()

# ============ Main =========== #
param_max_anzahl = int(config.get('option', 'param_max_anzahl'))

if ENVIRONMENT == 'test':
	param_debug_mode = 1
else:
	param_debug_mode = 0

# maximale Anzahl von ExtractionPlateNames eines CollectionSpecimen Eintrages
param_maxCountExtractPlates = int(config.get('option', 'param_maxCountExtractPlates'))

print 'Start Transfer_Extr_Plate_Name V3'

db = mysql_connect()
cur1 = db.cursor()  #suche prepared Eintraege
cur2 = db.cursor()  #suche Eintraege zur SampleId
cur3 = db.cursor()  #setze Status Eintraege in LIMS Tabelle assembly_export_COI
cur4 = db.cursor()  #call procedure
print 'Verbindung zu MySql-Server hergestellt'

# DWB Connection
cnxn=pyodbc.connect(config.get(ENVIRONMENT, 'mssql_connection'))
odbc_cursor1 = cnxn.cursor()
print 'Verbindung zu MS SQL-Server hergestellt'

## Erzeuge neue Eintraege in der LIMS Tabelle Transfer_Extr_Plate_Name
#GRANT EXECUTE ON PROCEDURE InsertIntoTransferTable TO 'gbol_admin'@'localhost'
# V2
cur4.execute("call InsertIntoTransferTable()")
cur4.close()
db.commit()
cur4 = db.cursor()  #call procedure
print 'Nach Call InsertIntoTransferTable'

## Fuelle Tabelle Transfer_Extr_Plate_Name
# V2
cur4.execute("call FillTransferTable()")
cur4.close()
db.commit()
# cur4 = db.cursor()
print 'Nach Call FillTransferTable'

#Suche in der LIMS Tabelle Transfer_Extr_Plate_Name vorbereitete Eintraege (Status=prepared).
p_loop_anzahl = 0
cur1.execute("Select id, sampleId, collSpecId From Transfer_Extr_Plate_Name Where status='prepared' Order By id")
P = cur1.fetchall()
for p in P:
	if (p_loop_anzahl == param_max_anzahl):
		if (param_debug_mode == 1):
			print '  Maximale Anzahl der Prepared-Loop Durchlaeufe erreicht'
		break
	p_loop_anzahl = p_loop_anzahl + 1
	p_id = '%s' % (p[0])
	p_sampleId = '%s' % (p[1])
	p_collSpecId = '%s' % (p[2])
	#if (param_debug_mode == 1):
	print '  ********************** Verarbeite p_id=' + p_id + ' p_sampleId=' + p_sampleId + ' p_collSpecId=' + p_collSpecId + ' **************************'
	if (param_debug_mode == 1):
		print '  Suche den CollectionSpecimen Eintrag'

	# Suche Eintrag in DWB DiversityCollection_DB.dbo.CollectionSpecimen
	odbc_cursor1.execute("Select Count(*) from %s.dbo.CollectionSpecimen Where CollectionSpecimenId=%s" % (MS_SQL_DB, p_collSpecId) )
	s1_count=''
	S1 = odbc_cursor1.fetchall()
	for s1 in S1:
		s1_count = '%s' % (s1[0])
		if (param_debug_mode == 1):
			print '  CollectionSpecimen Anzahl s1_count=' + s1_count
	if (s1_count=='1'):
		# CollectionSpecimen Eintrag gefunden, ermittle concatPlatenames
		if (param_debug_mode == 1):
			print '  CollectionSpecimen Eintrag Id=%s gefunden, ermittle concatPlatenames' % p_collSpecId
		p_print = "group_concat(concat(t.platename,' ',t.plateLocation,'/',t.plateSize) SEPARATOR '; ') as concatPlatenames,"
		p_print = p_print + " count(t.collSpecId) as collSpecAnzahl, t.collSpecId from Transfer_Extr_Plate_Name as t"
		p_print = p_print + (" Where t.collSpecId=%s And (t.status='ok' Or t.status='prepared') Group by t.collSpecId;" % p_collSpecId)
		if (param_debug_mode == 1):
			print ("    Select %s" % p_print)
		cur2.execute("Select %s" % p_print)
		E = cur2.fetchall()
		for e in E:
			e_concatPlatenames = '%s' % (e[0])
			if (param_debug_mode == 1):
				print '    e_concatPlatenames=' + e_concatPlatenames
			e_collSpecAnzahl = '%s' % (e[1])
			if (param_debug_mode == 1):
				print '    e_collSpecAnzahl=' + e_collSpecAnzahl
			e_collSpecId = '%s' % (e[2])
			if (param_debug_mode == 1):
				print '    e_collSpecId=' + e_collSpecId

			# Maximale Anzahl von ExtractionPlates erreicht
			e_collSpecAnzahl_int=int(e_collSpecAnzahl)
			if (e_collSpecAnzahl_int > param_maxCountExtractPlates):
				p_print = ("Transfer_Extr_Plate_Name Set status='error', note='Ignore_transfer_MaxAnzahlExtrPlateNamesErreicht, Max=%s'" % e_collSpecAnzahl)
				p_print = p_print + (" Where id=%s" % p_id)
				if (param_debug_mode == 1):
					print ("    Update %s" % p_print)
				cur3.execute("Update %s" % p_print)
				db.commit()
				continue

			# Schreibe die concatPlatenames in AdditionalNotes Feld
			p_print = ("%s.dbo.CollectionSpecimen Set AdditionalNotes='%s' Where CollectionSpecimenID=%s" % (MS_SQL_DB, e_concatPlatenames, p_collSpecId))
			if (param_debug_mode == 1):
				print ("    Update %s" % p_print)
			odbc_cursor1.execute("Update %s" % p_print)
			cnxn.commit()

			# Setze den Status auf ok
			p_print = ("Transfer_Extr_Plate_Name Set status='ok', note='Transfer_ExtrPlateName ok', concatPlateNames='%s' Where id=%s" % (e_concatPlatenames, p_id))
			if (param_debug_mode == 1):
				print ("    Update %s" % p_print)
			cur3.execute("Update %s" % p_print)
			db.commit()

		# Ende E-Loop
		if (param_debug_mode == 1):
			print '  Ende CollectionSpecimen Eintrag Id=%s gefunden' % p_collSpecId
	else:
		# CollectionSpecimen Eintrag nicht gefunden
		if (param_debug_mode == 1):
			print ("  Update Transfer_Extr_Plate_Name Set status='error', note='Ignore_transfer_CollSpecEintragNichtgefunden, CollSpecId=%s' Where id=%s" % (p_collSpecId, p_id))
		cur3.execute("Update Transfer_Extr_Plate_Name Set status='error', note='Ignore_transfer_CollSpecEintragNichtgefunden, CollSpecId=%s' Where id=%s" % (p_collSpecId, p_id))
		db.commit()
		continue
	if (param_debug_mode == 1):
		print '  Nach der Suche des CollectionSpecimen Eintrags'
	# time.sleep(0.5)

print ("Nach P-Loop, %i mal durchlaufen" % p_loop_anzahl)

#  Close DB connections & trigger=ON
final()

print 'Nach dem Trennen der Datenbankverbindungen, Programmende'
