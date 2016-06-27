#!/usr/bin/python
"""
LIMS to DWB
    Logik (ab Version 19)
	1) Suche neue Eintraege in LIMS Tabelle assembly und speichere diese in LIMS Tabelle assembly_export_COI.
	2) Fuelle die LIMS Tabelle assembly_export_COI. Setze fuer failed-Eintraege den Status auf 'ignore_failed'.
	   'ignore_failed' Eintraege werden nicht weiterverarbeitet, d.h. es werden nur passed-Eintraege weiterverarbeitet.
	3) Ueberpruefe neue passed-Eintraege darauf, ob sie noch nicht in die DWB Datenbank uebertragen worden sind.
	   Eintraege die bereits uebertragen worden sind, werden ausgefiltert, d.h. werden nicht weiterverarbeitet.
	   Eintraege die bereits uebertragen worden sind erhalten den Status 'ignore_already_passed_less' or 'ignore_already_passed_greater'.
	   Eintraege erhalten den Status 'ignore_already_passed_less' falls sie vor dem aktuellen Eintrag in der Tabelle assembly_export_COI liegen.
	   Sie erhalten den Status 'ignore_already_passed_greater' falls sie hinter dem aktuellen Eintrag liegen.
	   Beide 'ignore_already_passed' Eintraege werden nicht weiterverarbeitet.
	4) Suche in der LIMS Tabelle assembly_export_COI nach vorbereiteten Eintraegen (Status=prepared). Fuer jeden vorbereiteten Eintrag:
	  a) Loesche (falls vorhanden) den zur SampleId (dwb_CollectionSpecimenId) zugehoerigen Eintrag in der DWB Tabelle IdentificationUnitAnalysis.
		 Loesche (falls aktiviert, d.h. param_create_trace_file = 1) den zugehoerigen TraceFile.
	  b) Fuege den aktuellen Eintrag der DWB Tabelle IdentificationUnitAnalysis hinzu.
		Speichere (falls aktiviert, d.h. param_create_trace_file = 1) den zugehoerigen Tracefile als Datei ab
	  c) Setze fuer den aktuellen Eintrag den Status=ok.
    Alte Logik (vor Version 19)
	1) Suche neue Eintraege in LIMS Tabelle assembly und speichere diese in LIMS Tabelle assembly_export_COI.
	2) Fuelle die LIMS Tabelle assembly_export_COI.
	3) Suche in LIMS Tabelle assembly_export_COI vorbereitete Eintraege (Status=prepared). Fuer jeden vorbereiteten Eintrag:
	  a) Loesche alle (falls vorhanden) zur SampleId zugehoerigen Eintraege in der DWB Tabelle IdentificationUnitAnalysis.
		 Loesche (falls aktiviert, d.h. param_create_trace_file = 1) die TraceFiles.
	  b) Ermittle in der LIMS Tabelle assembly_export_COI alle zur SampleId zugehoerigen Eintraege mit status=ok oder status=prepared und
	    fuege fuer jeden gefundenen Eintrag den entsprechenden Eintrag in der DWB Tabelle IdentificationUnitAnalysis hinzu.
		Speichere (falls aktiviert, d.h. param_create_trace_file = 1) die zugehoerigen Tracefiles als Datei ab
	  c) Setze fuer den aktuellen Eintrag den Status=ok.

	Aenderungen:
		Setze das aktuelle Datum im IdentificationUnitAnalysis Eintrag.
		Speichere Tracefiles als separate binaere Dateien ab.
		Passe Tracefile Angaben in ToolUsage Feld an.
		Speichere Tracefile in ToolUsage Feld ab.
		V5 Speichere Tracefiles als separate binaere Dateien ab, falls aktiviert d.h. param_create_trace_file = 1.
		V5 Debug-Mode.
		V6 MD5 Info in neues ToolUsage Feld trace_file_org_md5 eintragen
		V6 Weitere neue ToolUsage Felder trace_file_org_length, trace_file_enc_length
		V6 Namensaenderungen trace_file -> trace_file_encoded, tracefile_encoding -> trace_file_encoding
		V7 ToolUsage Namensaenderungen sequence_primer -> sequencing_primer_name, sequence -> sequencing_primer_sequence
		V7   sequence_timestamp -> sequencing_timestamp
		V7 Feldinhalte fuer sequencing_timestamp, sequencing_lab und format werden gefuellt aus assembly_export_COI Feldern
		V7 Parameter fuer Barcoding ToolId und Trace ToolId
		V8 Neues Feld assemNotes
		V8 Loesche auch IdentificationUnitAnalysis_log Eintraege
		V8 Tracelength > param_min_tracelength
		V9 Uebertrage nur eindeutige prepared-Eintraege
		V9 Neue Extract Felder e_assemPlateSuffix und e_assemContam
		V9 Schreibe e_assemContam in ToolUsage Contamination Feld
		V10 Neue Extract Felder e_assem_failure_reason_id, e_assem_failure_reason, e_assem_failure_detail
		V10 Fuelle ToolUsage Felder failure und failure_detail anstelle von contamination Feld
		V11 Ueberpruefe ob der TraceFile mit ABI beginnt
		V12 Neue Felder workflowDate, extractionDate, pcrDate
		V13 Es koennen mehrere passed-Eintraege und mehrere failed-Eintraege fuer eine SampleId angelegt werden
		V14 30.10.2013 Fuelle ResponsibleName in Tabelle IdentificationUnitAnalysis mit assemTechnician Wert
		V15 Feldnamenaenderung date -> exportDate, Fehler MaxCountSpecimenId, Fehler tracefileNotFound
		V16 Verarbeite nur eindeutige prepared Eintraege
		V17 Trigger aus und ein schalten fuer Tabelle IdentificationUnitAnalysis
		V18 Time sleep 1 second
		V18 Trigger eingeschaltet, Sleep ausgeschaltet
		V19 Neue Logic. Verarbeite nur den aktuellen Eintrag und nicht alle zur dwb_CollectionSpecimenId zugehoerigen Eintraege
		V19 Neue MySQL Datenbank lims (gbol_lims -> Lims)
		V20 27.03.2014 Anzahl in 'IdentificationUnit nicht gefunden Meldung', Insert mit neuem Datumsformat
		V21 Neuer MySQL Server localhost -> geneiousdb01
		V21 Aktiviere Call syncAssemblyTables, prepUpdateDWB, checkAlreadyPassed

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

import pudb

VERBOSE = int(config.get('option', 'verbose'))
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
	# Triggers ON
	#odbc_cursor1.execute("ENABLE TRIGGER trgDelIdentificationUnitAnalysis ON IdentificationUnitAnalysis")
	#cnxn.commit()
	#odbc_cursor1.execute("ENABLE TRIGGER trgInsIdentificationUnitAnalysis ON IdentificationUnitAnalysis")
	#cnxn.commit()

	## Trenne die Verbindungen zu den Datenbanken'
	db.close()
	cnxn.close()

# ============ Main =========== #
param_max_anzahl = int(config.get('option', 'param_max_anzahl'))

param_analysisId = int(config.get(ENVIRONMENT, 'param_analysisId'))

param_create_trace_file = int(config.get('option', 'param_create_trace_file'))
param_trace_verzeichnis = config.get('option', 'param_trace_verzeichnis')

if ENVIRONMENT == 'test':
	param_debug_mode = 1
else:
	param_debug_mode = 0

param_barcodingToolid = int(config.get(ENVIRONMENT, 'param_barcodingToolid'))
param_traceToolid = int(config.get(ENVIRONMENT, 'param_traceToolid'))
param_min_tracelength = int(config.get('option', 'param_min_tracelength'))
param_maxCountSpecimenId = int(config.get('option', 'param_maxCountSpecimenId'))

print 'Start L2F_prod21 01.12.2015'

db = mysql_connect()
cur1 = db.cursor()  #prepared Eintraege
cur2 = db.cursor()  #suche Eintraege zur SampleId
cur3 = db.cursor()  #setze Status Eintraege in LIMS Tabelle assembly_export_COI
cur4 = db.cursor()  #call Procedures
print 'Verbindung zu MySql-Server hergestellt'

# DWB Connection
cnxn=pyodbc.connect(config.get(ENVIRONMENT, 'mssql_connection'))
odbc_cursor1 = cnxn.cursor()
print 'Verbindung zu MS SQL-Server hergestellt'

## Erzeuge neue Eintraege in der LIMS Tabelle assembly_export_COI
cur4.execute("call syncAssemblyTables()")
cur4.close()
db.commit()
cur4 = db.cursor()  #call Procedures
print 'Nach Call syncAssemblyTables'

## Fuelle Tabelle assembly_export_COI
cur4.execute("call prepUpdateDWB()")
cur4.close()
db.commit()
cur4 = db.cursor()  #call Procedures
print 'Nach Call prepUpdateDWB'

## Filtere bereits in die DWB uebertragene Eintraege heraus
cur4.execute("call checkAlreadyPassed()")
cur4.close()
db.commit()
# cur4 = db.cursor()  #call Procedures
print 'Nach Call checkAlreadyPassed'

# Triggers OFF
#odbc_cursor1.execute("DISABLE TRIGGER trgDelIdentificationUnitAnalysis ON IdentificationUnitAnalysis")
#cnxn.commit()
#odbc_cursor1.execute("DISABLE TRIGGER trgInsIdentificationUnitAnalysis ON IdentificationUnitAnalysis")
#cnxn.commit()
if (param_debug_mode == 1):
	print 'Nach Triggers off'

#Suche in LIMS Tabelle assembly_export_COI vorbereitete eindeutige Eintraege (Status=prepared).
p_loop_anzahl = 0
cur1.execute(("Select id, dwb_CollectionSpecimenId From assembly_export_COI Where status='prepared'") +
(" AND pcrAnzahl=1 AND cycleSeqForwAnzahl=1 AND cycleSeqForwTraceAnzahl=1 AND cycleSeqRevAnzahl=1 AND cycleSeqRevTraceAnzahl=1 Order By id"))
P = cur1.fetchall()
for p in P:
	if (p_loop_anzahl == param_max_anzahl):
		if (param_debug_mode == 1):
			print '  Maximale Anzahl der Prepared-Loop Durchlaeufe erreicht'
		break
	p_loop_anzahl = p_loop_anzahl + 1
	p_id = '%s' % (p[0])
	p_collSpecimenId = '%s' % (p[1])
	#if (param_debug_mode == 1):
	print '  ** Verarbeite p_id=' + p_id + ' p_collSpecimenId=' + p_collSpecimenId + ' **'

	# Suche Eintrag in DWB DiversityCollection_Workshop.dbo.IdentificationUnit und loesche alten Eintrag in IdentificationUnitAnalysis, falls vorhanden
	odbc_cursor1.execute("Select Count(*) from %s.dbo.IdentificationUnit Where CollectionSpecimenId=%s" % (MS_SQL_DB, p_collSpecimenId))
	S1 = odbc_cursor1.fetchall()
	for s1 in S1:
		s1_count = '%s' % (s1[0])
		if (param_debug_mode == 1):
			print '  IdentificationUnit Eintraege, s1_count=' + s1_count
	identUnitId=''
	if (s1_count=='1'):
		odbc_cursor1.execute("Select IdentificationUnitId from %s.dbo.IdentificationUnit Where CollectionSpecimenId=%s" % (MS_SQL_DB, p_collSpecimenId))
		S2 = odbc_cursor1.fetchall()
		for s2 in S2:
			identUnitId= '%s' % (s2[0])
			if (param_debug_mode == 1):
				print '  IdentificationUnitId=' + identUnitId
		s3_count=''
		s3_count_int=0
		#vor V19 odbc_cursor1.execute("Select Count(*) from DiversityCollection_ZFMK.dbo.IdentificationUnitAnalysis Where CollectionSpecimenId=%s AND IdentificationUnitId=%s AND AnalysisID=%s"
		#% (p_collSpecimenId, identUnitId, param_analysisId) )
		odbc_cursor1.execute("Select Count(*) from %s.dbo.IdentificationUnitAnalysis Where CollectionSpecimenId=%s AND IdentificationUnitId=%s AND AnalysisID=%s AND AnalysisNumber=%s"
		% (MS_SQL_DB, p_collSpecimenId, identUnitId, param_analysisId, p_id) )

		S3 = odbc_cursor1.fetchall()
		for s3 in S3:
			s3_count= '%s' % (s3[0])
			if (param_debug_mode == 1):
				print '  IdentificationUnitAnalysis Eintraege, s3_count=' + s3_count
		s3_count_int=int(s3_count)
		if (s3_count_int > 0):
			# Loesche Eintraege in IdentificationUnitAnalysis
			if (param_debug_mode == 1):
				print ("  Delete From %s.dbo.IdentificationUnitAnalysis Where CollectionSpecimenId=%s AND IdentificationUnitId=%s AND AnalysisID=%s AND AnalysisNumber=%s"
				% (MS_SQL_DB, p_collSpecimenId, identUnitId, param_analysisId, p_id) )
			try:
				odbc_cursor1.execute("Delete From %s.dbo.IdentificationUnitAnalysis Where CollectionSpecimenId=%s AND IdentificationUnitId=%s AND AnalysisID=%s AND AnalysisNumber=%s"
				% (MS_SQL_DB, p_collSpecimenId, identUnitId, param_analysisId, p_id) )
				cnxn.commit()
			except Exception, detail:
				print "An Error occured during Delete 1: %r" % detail
				final()
				sys.exit(1)

				# Loesche Eintraege in IdentificationUnitAnalysis_log
			if (param_debug_mode == 1):
				print ("  Delete From %s.dbo.IdentificationUnitAnalysis_log Where CollectionSpecimenId=%s AND IdentificationUnitId=%s AND AnalysisID=%s AND AnalysisNumber=%s"
				% (MS_SQL_DB, p_collSpecimenId, identUnitId, param_analysisId, p_id) )
			try:
				odbc_cursor1.execute("Delete From %s.dbo.IdentificationUnitAnalysis_log Where CollectionSpecimenId=%s AND IdentificationUnitId=%s AND AnalysisID=%s AND AnalysisNumber=%s"
				% (MS_SQL_DB, p_collSpecimenId, identUnitId, param_analysisId, p_id) )
				cnxn.commit()
			except Exception, detail:
				print "An Error occured during Delete 2: %r" % detail
				final()
				sys.exit(1)
			if (param_create_trace_file==1):
				# vor V19 os.system("rm %sTraceForw.%s.*" % (param_trace_verzeichnis, p_collSpecimenId))
				os.system("rm %sTraceForw.%s.%s" % (param_trace_verzeichnis, p_collSpecimenId, p_id))
				if (param_debug_mode == 1):
					print "  Nach rm %sTraceForw.%s.%s" % (param_trace_verzeichnis, p_collSpecimenId, p_id)
				os.system("rm %sTraceRev.%s.%s" % (param_trace_verzeichnis, p_collSpecimenId, p_id))
				if (param_debug_mode == 1):
					print "  Nach rm %sTraceRev.%s.%s" % (param_trace_verzeichnis, p_collSpecimenId, p_id)
	else:
		if (param_debug_mode == 1):
			print ("  Update assembly_export_COI Set status='error', note='Fehler_L2F_IdentificationUnitEintragIstNichtVorhandenOderNichtEindeutig, Anzahl=%s' Where id=%s" % (s1_count, p_id))
		cur3.execute("Update assembly_export_COI Set status='error', note='Fehler_L2F_IdentificationUnitEintragIstNichtVorhandenOderNichtEindeutig, Anzahl=%s' Where id=%s" % (s1_count, p_id))
		db.commit()
		continue
	if (param_debug_mode == 1):
		print '  Nach der Suche des IdentificationUnit Eintrages und dem Loeschen von IdentificationUnitAnalysis Eintraegen und Trace Dateien '

	#Fuege den aktuellen Eintrag der DWB Tabelle IdentificationUnitAnalysis hinzu.
	#vor V19 Ermittle in der LIMS Tabelle assembly_export_COI alle zur SampleId zugehoerigen Eintraege mit status=ok oder status=prepared und
	#     fuege fuer jeden gefundenen Eintrag den entsprechenden Eintrag in der DWB Tabelle IdentificationUnitAnalysis hinzu.
	#
	passed_eintrag_gefunden = 0
	tracelength_zu_klein = 0
	trace_begin_not_ABI = 0
	maxCountSpecimenReached = 0
	tracefileNotFound = 0
	e_loop_anzahl = 0
	p_print = "id, exportDate, workflowId, workflowDate, extractionTblId, extractionId, extractionDate, dwb_CollectionSpecimenId, sampleId, status, note, "
	p_print = p_print +	"assemDate, assemProgress, assemTechnician, assemNotes, assemConsensus, assemPlateSuffix, assemContam, "
	p_print = p_print +	"assem_failure_reason_id, assem_failure_reason, assem_failure_detail, "
	p_print = p_print + "locus, pcrAnzahl, pcrId, pcrDate, pcrPrName, pcrPrSequence, pcrRevPrName, pcrRevPrSequence, "
	p_print = p_print + "cycleSeqForwAnzahl, cycleSeqForwId, cycleSeqForwPrimerName, cycleSeqForwPrimerSequence, cycleSeqForwTraceAnzahl, cycleSeqForwTraceId, cycleSeqForwTraceName, "
	p_print = p_print + "cycleSeqForwTechnician, cycleSeqForwDate, cycleSeqForwTraceFormat, "
	p_print = p_print + "cycleSeqRevAnzahl, cycleSeqRevId, cycleSeqRevPrimerName, cycleSeqRevPrimerSequence, cycleSeqRevTraceAnzahl, cycleSeqRevTraceId, cycleSeqRevTraceName, "
	p_print = p_print + "cycleSeqRevTechnician, cycleSeqRevDate, cycleSeqRevTraceFormat "
	#vor V19 p_print = p_print + ("From assembly_export_COI Where dwb_CollectionSpecimenId=%s AND (status='prepared' OR status='ok')" % p_collSpecimenId)
	#p_print = p_print + (" AND pcrAnzahl=1 AND cycleSeqForwAnzahl=1 AND cycleSeqForwTraceAnzahl=1 AND cycleSeqRevAnzahl=1 AND cycleSeqRevTraceAnzahl=1 Order By id")
	p_print = p_print + ("From assembly_export_COI Where id=%s" % p_id)
	#print p_print
	#pudb.set_trace()

	cur2.execute("Select %s" % p_print)
	E = cur2.fetchall()
	for e in E:
		e_loop_anzahl = e_loop_anzahl + 1
		if (param_debug_mode == 1):
			print '    Anfang Export-Loop'
		e_id = '%s' % (e[0])
		if (param_debug_mode == 1):
			print '    e_id=' + e_id
		e_exportDate = '%s' % (e[1])
		if (param_debug_mode == 1):
			print '    e_exportDate=' + e_exportDate
		e_workflowId = '%s' % (e[2])
		if (param_debug_mode == 1):
			print '    e_workflowId=' + e_workflowId
		e_workflowDate = '%s' % (e[3])
		if (param_debug_mode == 1):
			print '    e_workflowDate=' + e_workflowDate
		e_extractionTblId = '%s' % (e[4])
		if (param_debug_mode == 1):
			print '    e_extractionTblId=' + e_extractionTblId
		e_extractionId = '%s' % (e[5])
		if (param_debug_mode == 1):
			print '    e_extractionId=' + e_extractionId
		e_extractionDate = '%s' % (e[6])
		if (param_debug_mode == 1):
			print '    e_extractionDate=' + e_extractionDate
		e_dwb_CollectionSpecimenId = '%s' % (e[7])
		if (param_debug_mode == 1):
			print '    e_dwb_CollectionSpecimenId=' + e_dwb_CollectionSpecimenId
		e_sampleId = '%s' % (e[8])
		if (param_debug_mode == 1):
			print '    e_sampleId=' + e_sampleId
		e_status = '%s' % (e[9])
		if (param_debug_mode == 1):
			print '    e_status=' + e_status
		e_note = '%s' % (e[10])
		if (param_debug_mode == 1):
			print '    e_note=' + e_note
		e_assemDate = '%s' % (e[11])
		if (param_debug_mode == 1):
			print '    e_assemDate=' + e_assemDate
		e_assemProgress = '%s' % (e[12])
		if (param_debug_mode == 1):
			print '    e_assemProgress=' + e_assemProgress
		e_assemTechnician = '%s' % (e[13])
		if (param_debug_mode == 1):
			print '    e_assemTechnician=' + e_assemTechnician
		e_assemNotes = '%s' % (e[14])
		if (param_debug_mode == 1):
			print '    e_assemNotes=' + e_assemNotes
		e_assemConsensus = '%s' % (e[15])
		if (param_debug_mode == 1):
			print '    e_assemConsensus[:100]=' + e_assemConsensus[:100]
		e_assemPlateSuffix = '%s' % (e[16])
		if (param_debug_mode == 1):
			print '    e_assemPlateSuffix=' + e_assemPlateSuffix
		e_assemContam = '%s' % (e[17])
		if (param_debug_mode == 1):
			print '    e_assemContam=' + e_assemContam
		e_assem_failure_reason_id = '%s' % (e[18])
		if (param_debug_mode == 1):
			print '    e_assem_failure_reason_id=' + e_assem_failure_reason_id
		e_assem_failure_reason = '%s' % (e[19])
		if (param_debug_mode == 1):
			print '    e_assem_failure_reason=' + e_assem_failure_reason
		e_assem_failure_detail = '%s' % (e[20])
		if (param_debug_mode == 1):
			print '    e_assem_failure_detail=' + e_assem_failure_detail
		e_locus = '%s' % (e[21])
		if (param_debug_mode == 1):
			print '    e_locus=' + e_locus
		e_pcrAnzahl = '%s' % (e[22])
		if (param_debug_mode == 1):
			print '    e_pcrAnzahl=' + e_pcrAnzahl
		e_pcrId = '%s' % (e[23])
		if (param_debug_mode == 1):
			print '    e_pcrId=' + e_pcrId
		e_pcrDate = '%s' % (e[24])
		if (param_debug_mode == 1):
			print '    e_pcrDate=' + e_pcrDate
		e_pcrPrName = '%s' % (e[25])
		if (param_debug_mode == 1):
			print '    e_pcrPrName=' + e_pcrPrName
		e_pcrPrSequence = '%s' % (e[26])
		if (param_debug_mode == 1):
			print '    e_pcrPrSequence=' + e_pcrPrSequence
		e_pcrRevPrName = '%s' % (e[27])
		if (param_debug_mode == 1):
			print '    e_pcrRevPrName=' + e_pcrRevPrName
		e_pcrRevPrSequence = '%s' % (e[28])
		if (param_debug_mode == 1):
			print '    e_pcrRevPrSequence=' + e_pcrRevPrSequence
		e_cycleSeqForwAnzahl = '%s' % (e[29])
		if (param_debug_mode == 1):
			print '    e_cycleSeqForwAnzahl=' + e_cycleSeqForwAnzahl
		e_cycleSeqForwId = '%s' % (e[30])
		if (param_debug_mode == 1):
			print '    e_cycleSeqForwId=' + e_cycleSeqForwId
		e_cycleSeqForwPrimerName = '%s' % (e[31])
		if (param_debug_mode == 1):
			print '    e_cycleSeqForwPrimerName=' + e_cycleSeqForwPrimerName
		e_cycleSeqForwPrimerSequence = '%s' % (e[32])
		if (param_debug_mode == 1):
			print '    e_cycleSeqForwPrimerSequence=' + e_cycleSeqForwPrimerSequence
		e_cycleSeqForwTraceAnzahl = '%s' % (e[33])
		if (param_debug_mode == 1):
			print '    e_cycleSeqForwTraceAnzahl=' + e_cycleSeqForwTraceAnzahl
		e_cycleSeqForwTraceId = '%s' % (e[34])
		if (param_debug_mode == 1):
			print '    e_cycleSeqForwTraceId=' + e_cycleSeqForwTraceId
		e_cycleSeqForwTraceName = '%s' % (e[35])
		if (param_debug_mode == 1):
			print '    e_cycleSeqForwTraceName=' + e_cycleSeqForwTraceName
		e_cycleSeqForwTechnician = '%s' % (e[36])
		if (param_debug_mode == 1):
			print '    e_cycleSeqForwTechnician=' + e_cycleSeqForwTechnician
		e_cycleSeqForwDate = '%s' % (e[37])
		if (param_debug_mode == 1):
			print '    e_cycleSeqForwDate=' + e_cycleSeqForwDate
		e_cycleSeqForwTraceFormat = '%s' % (e[38])
		if (param_debug_mode == 1):
			print '    e_cycleSeqForwTraceFormat=' + e_cycleSeqForwTraceFormat
		e_cycleSeqRevAnzahl = '%s' % (e[39])
		if (param_debug_mode == 1):
			print '    e_cycleSeqRevAnzahl=' + e_cycleSeqRevAnzahl
		e_cycleSeqRevId = '%s' % (e[40])
		if (param_debug_mode == 1):
			print '    e_cycleSeqRevId=' + e_cycleSeqRevId
		e_cycleSeqRevPrimerName = '%s' % (e[41])
		if (param_debug_mode == 1):
			print '    e_cycleSeqRevPrimerName=' + e_cycleSeqRevPrimerName
		e_cycleSeqRevPrimerSequence = '%s' % (e[42])
		if (param_debug_mode == 1):
			print '    e_cycleSeqRevPrimerSequence=' + e_cycleSeqRevPrimerSequence
		e_cycleSeqRevTraceAnzahl = '%s' % (e[43])
		if (param_debug_mode == 1):
			print '    e_cycleSeqRevTraceAnzahl=' + e_cycleSeqRevTraceAnzahl
		e_cycleSeqRevTraceId = '%s' % (e[44])
		if (param_debug_mode == 1):
			print '    e_cycleSeqRevTraceId=' + e_cycleSeqRevTraceId
		e_cycleSeqRevTraceName = '%s' % (e[45])
		if (param_debug_mode == 1):
			print '    e_cycleSeqRevTraceName=' + e_cycleSeqRevTraceName
		e_cycleSeqRevTechnician = '%s' % (e[46])
		if (param_debug_mode == 1):
			print '    e_cycleSeqRevTechnician=' + e_cycleSeqRevTechnician
		e_cycleSeqRevDate = '%s' % (e[47])
		if (param_debug_mode == 1):
			print '    e_cycleSeqRevDate=' + e_cycleSeqRevDate
		e_cycleSeqRevTraceFormat = '%s' % (e[48])
		if (param_debug_mode == 1):
			print '    e_cycleSeqRevTraceFormat=' + e_cycleSeqRevTraceFormat

		# Erzeuge Eintrag in DWB Table IdentificationUnitAnalysis. Stelle sicher, dass nur ein passed Eintrag erstellt wird
		#if ((e_assemProgress=='passed') and (passed_eintrag_gefunden==1)):
		#	if (param_debug_mode == 1):
		#		print '    Erstelle keinen IdentificationUnitAnalysis passed Eintrag, weil schon vorhanden'
		#	continue
		if (e_assemProgress=='passed'):
		 	passed_eintrag_gefunden=1
		if (e_loop_anzahl > param_maxCountSpecimenId):
			maxCountSpecimenReached = 1
			print '    Erstelle keinen IdentificationUnitAnalysis Eintrag, weil maxCountSpecimen=%s erreicht' % (param_maxCountSpecimenId)
			continue
		if (tracelength_zu_klein == 1):
			print '    Erstelle keinen IdentificationUnitAnalysis Eintrag, weil Tracelength zu klein'
			continue
		if (trace_begin_not_ABI == 1):
			print '    Erstelle keinen IdentificationUnitAnalysis Eintrag, weil TraceBegin not ABI'
			continue
		if (tracefileNotFound == 1):
			print '    Erstelle keinen IdentificationUnitAnalysis Eintrag, weil TraceDatei nicht vorhanden'
			continue

		traceForwFile = "%sTraceForw.%s.%s" % (param_trace_verzeichnis, p_collSpecimenId, e_id)
		tu_traceForwFile_encoded = "empty"  # encoded TraceForwFile
		tu_traceForwFile_org_length = 0
		tu_traceForwFile_enc_length = 0
		tu_traceForwFile_org_md5 = "empty"
		traceRevFile  = "%sTraceRev.%s.%s" % (param_trace_verzeichnis, p_collSpecimenId, e_id)
		tu_traceRevFile_encoded = "empty"   # encoded TraceRevFile
		tu_traceRevFile_org_length = 0
		tu_traceRevFile_enc_length = 0
		tu_traceRevFile_org_md5 = "empty"

		# Erzeuge die TraceForw Datei und den zugehoerigen encoded Tracefile
		traceDa = 0
		cur3.execute("Select name, data From traces Where id=%s" % (e_cycleSeqForwTraceId) )
		T1 = cur3.fetchall()
		for t1 in T1:
			traceDa = 1
			if (param_create_trace_file==1):
				tout1 = open(traceForwFile, "wb")
				tout1.write(t1[1])
				tout1.close
				if (param_debug_mode == 1):
					print "    T1-loop Datei=%s erstellt" % (traceForwFile)
			tu_traceForwFile_encoded = base64.b64encode(t1[1])
			tu_traceForwFile_org_length = len(t1[1])
			if (tu_traceForwFile_org_length < param_min_tracelength):
				tracelength_zu_klein = 1
				print ("    T1-loop Tracefile=%s TracefileLength=%s ist kleiner als=%s"
				% (traceForwFile, tu_traceForwFile_org_length, param_min_tracelength) )
			if ((e_cycleSeqForwTraceFormat=='ABI') and (t1[1][:3] != 'ABI')):
				trace_begin_not_ABI = 1
				print ("    T1-loop Tracefile=%s beginnt nicht mit ABI sondern mit %s"
				% (traceForwFile, t1[1][:3]) )
			tu_traceForwFile_enc_length = len(tu_traceForwFile_encoded)
			tu_traceForwFile_org_md5 = md5.new(t1[1]).hexdigest()
			if (param_debug_mode == 1):
				print ("    T1-loop Tracefile=%s TracefileLength=%s EncodedTracefileLength=%s TracefileMD5=%s"
				% (traceForwFile, tu_traceForwFile_org_length, tu_traceForwFile_enc_length, tu_traceForwFile_org_md5) )
		#print 'Nach Schreibe TraceForw Datei'
		if (traceDa == 0):
			tracefileNotFound = 1
			print ("    Keine TraceForw Datei gefunden fuer Id=%s" % (e_cycleSeqForwTraceId))

		# Erzeuge die TraceRev Datei und den zugehoerigen encoded Tracefile
		traceDa = 0
		cur3.execute("Select name, data From traces Where id=%s" % (e_cycleSeqRevTraceId) )
		T2 = cur3.fetchall()
		for t2 in T2:
			traceDa = 1
			if (param_create_trace_file==1):
				tout2 = open(traceRevFile, "wb")
				tout2.write(t2[1])
				tout2.close
				if (param_debug_mode == 1):
					print "    T2-loop Datei=%s erstellt" % (traceRevFile)
			tu_traceRevFile_encoded = base64.b64encode(t2[1])
			tu_traceRevFile_org_length = len(t2[1])
			if (tu_traceRevFile_org_length < param_min_tracelength):
				tracelength_zu_klein = 1
				print ("    T2-loop Tracefile=%s TracefileLength=%s ist kleiner als=%s"
				% (traceRevFile, tu_traceRev_org_length, param_min_tracelength) )
			if ((e_cycleSeqRevTraceFormat=='ABI') and (t2[1][:3] != 'ABI')):
				trace_begin_not_ABI = 1
				print ("    T2-loop Tracefile=%s beginnt nicht mit ABI sondern mit %s"
				% (traceRevFile, t2[1][:3]) )
			tu_traceRevFile_enc_length = len(tu_traceRevFile_encoded)
			tu_traceRevFile_org_md5 = md5.new(t2[1]).hexdigest()
			if (param_debug_mode == 1):
				print ("    T2-loop Tracefile=%s TracefileLength=%s EncodedTracefileLength=%s TracefileMD5=%s"
				% (traceRevFile, tu_traceRevFile_org_length, tu_traceRevFile_enc_length, tu_traceRevFile_org_md5) )
		#print 'Nach Schreibe TraceRev Datei'
		if (traceDa == 0):
			tracefileNotFound = 1
			print ("    Keine TraceRev Datei gefunden fuer Id=%s" % (e_cycleSeqRevTraceId))

		if (tracelength_zu_klein == 1):
			print '    Erstelle keinen IdentificationUnitAnalysis Eintrag, weil Tracelength zu klein'
			continue
		if (trace_begin_not_ABI == 1):
			print '    Erstelle keinen IdentificationUnitAnalysis Eintrag, weil TraceBegin nicht ABI'
			continue
		if (tracefileNotFound == 1):
			print '    Erstelle keinen IdentificationUnitAnalysis Eintrag, weil TraceDatei nicht vorhanden'
			continue

		# Erzeuge ToolUsage Eintrag
		tu = '<Tools xmlns="http://diversityworkbench.net/Schema/tools">'
		#Tool Barcoding
		tu = tu + ('<Tool Name="Barcoding" ToolID="%i">' % param_barcodingToolid)
		tu = tu + ('<Usage Name="locus" Value="%s" />' % e_locus)
		tu = tu + '<Usage Name="project" Value="GBOL" />'
		if (e_assemProgress=='failed'):
			if (e_assem_failure_reason == 'leer'):
				tu = tu + '<Usage Name="failure" Value="" />'
			else:
				tu = tu + ('<Usage Name="failure" Value="%s" />' % e_assem_failure_reason)

			if (e_assem_failure_detail == 'leer'):
				if (e_assemContam == 'leer'):
					tu = tu + '<Usage Name="failure_detail" Value="contaminated" />'
				else:
					tu = tu + ('<Usage Name="failure_detail" Value="%s" />' % e_assemContam)
			else:
				tu = tu + ('<Usage Name="failure_detail" Value="%s" />' % e_assem_failure_detail)
		else:
			tu = tu + '<Usage Name="failure" Value="" />'
			tu = tu + '<Usage Name="failure_detail" Value="" />'
		tu = tu + '</Tool>'
		#Tool Trace Forward
		tu = tu + ('<Tool Name="Trace" ToolID="%i">' % param_traceToolid)
		tu = tu + ('<Usage Name="format" Value="%s">' % e_cycleSeqForwTraceFormat)
		tu = tu + '<ValueEnum>ABI</ValueEnum>'
		tu = tu + '<ValueEnum>SCF</ValueEnum>'
		tu = tu + '</Usage>'
		tu = tu + '<Usage Name="direction" Value="forward">'
		tu = tu + '<ValueEnum>forward</ValueEnum>'
		tu = tu + '<ValueEnum>reverse</ValueEnum>'
		tu = tu + '</Usage>'
		tu = tu + ('<Usage Name="pcr_primer_forward" Value="%s" />' % e_pcrPrName)
		tu = tu + ('<Usage Name="pcr_primer_reverse" Value="%s" />' % e_pcrRevPrName)
		tu = tu + ('<Usage Name="sequencing_primer_name" Value="%s" />' % e_cycleSeqForwPrimerName)
		tu = tu + ('<Usage Name="sequencing_primer_sequence" Value="%s" />' % e_cycleSeqForwPrimerSequence)
		tu = tu + ('<Usage Name="sequencing_timestamp" Value="%s" />' % e_cycleSeqForwDate)
		tu = tu + ('<Usage Name="sequencing_lab" Value="%s" />' % e_cycleSeqForwTechnician)
		if (param_create_trace_file==1):
			tu = tu + ('<Usage Name="trace_filename" Value="%s" />' % traceForwFile)
		else:
			tu = tu + ('<Usage Name="trace_filename" Value="%s" />' % e_cycleSeqForwTraceName)
		tu = tu + ('<Usage Name="trace_file_org_length" Value="%s" />' % tu_traceForwFile_org_length)
		tu = tu + ('<Usage Name="trace_file_org_md5" Value="%s" />' % tu_traceForwFile_org_md5)
		tu = tu + ('<Usage Name="trace_file_encoded" Value="%s" />' % tu_traceForwFile_encoded)
		tu = tu + '<Usage Name="trace_file_encoding" Value="base64" >'
		tu = tu + '<ValueEnum>base64</ValueEnum>'
		tu = tu + '<ValueEnum>hex</ValueEnum>'
		tu = tu + '<ValueEnum>not_encoded</ValueEnum>'
		tu = tu + '</Usage>'
		tu = tu + ('<Usage Name="trace_file_enc_length" Value="%s" />' % tu_traceForwFile_enc_length)
		tu = tu + '</Tool>'
		#Tool Trace Reverse
		tu = tu + ('<Tool Name="Trace" ToolID="%i">' % param_traceToolid)
		tu = tu + ('<Usage Name="format" Value="%s">' % e_cycleSeqRevTraceFormat)
		tu = tu + '<ValueEnum>ABI</ValueEnum>'
		tu = tu + '<ValueEnum>SCF</ValueEnum>'
		tu = tu + '</Usage>'
		tu = tu + '<Usage Name="direction" Value="reverse">'
		tu = tu + '<ValueEnum>forward</ValueEnum>'
		tu = tu + '<ValueEnum>reverse</ValueEnum>'
		tu = tu + '</Usage>'
		tu = tu + ('<Usage Name="pcr_primer_forward" Value="%s" />' % e_pcrPrName)
		tu = tu + ('<Usage Name="pcr_primer_reverse" Value="%s" />' % e_pcrRevPrName)
		tu = tu + ('<Usage Name="sequencing_primer_name" Value="%s" />' % e_cycleSeqRevPrimerName)
		tu = tu + ('<Usage Name="sequencing_primer_sequence" Value="%s" />' % e_cycleSeqRevPrimerSequence)
		tu = tu + ('<Usage Name="sequencing_timestamp" Value="%s" />' % e_cycleSeqRevDate)
		tu = tu + ('<Usage Name="sequencing_lab" Value="%s" />' % e_cycleSeqRevTechnician)
		if (param_create_trace_file==1):
			tu = tu + ('<Usage Name="trace_filename" Value="%s" />' % traceRevFile)
		else:
			tu = tu + ('<Usage Name="trace_filename" Value="%s" />' % e_cycleSeqRevTraceName)
		tu = tu + ('<Usage Name="trace_file_org_length" Value="%s" />' % tu_traceRevFile_org_length)
		tu = tu + ('<Usage Name="trace_file_org_md5" Value="%s" />' % tu_traceRevFile_org_md5)
		tu = tu + ('<Usage Name="trace_file_encoded" Value="%s" />' % tu_traceRevFile_encoded)
		tu = tu + '<Usage Name="trace_file_encoding" Value="base64" >'
		tu = tu + '<ValueEnum>base64</ValueEnum>'
		tu = tu + '<ValueEnum>hex</ValueEnum>'
		tu = tu + '<ValueEnum>not_encoded</ValueEnum>'
		tu = tu + '</Usage>'
		tu = tu + ('<Usage Name="trace_file_enc_length" Value="%s" />' % tu_traceRevFile_enc_length)
		tu = tu + '</Tool>'
		#Ende Tools
		tu = tu + '</Tools>'
		#print tu
		if (param_debug_mode == 1):
			print '    Length_tu=%s, Length_consensus=%s' % (len(tu), len(e_assemConsensus) )

		# Erzeuge Eintrag in DWB Table IdentificationUnitAnalysis.
		p_print = "(CollectionSpecimenID, IdentificationUnitID, AnalysisID, AnalysisNumber, AnalysisDate, Notes, AnalysisResult, ResponsibleName, ToolUsage)"
		p_print = p_print +	(" Values(%s, %s, %s, '%s', CONVERT(VARCHAR(19), GETDATE(), 120), 'L2F insert', '%s', '%s', '%s')" %
		(e_dwb_CollectionSpecimenId, identUnitId, param_analysisId, e_id, e_assemConsensus, e_assemTechnician, tu) )
		sql_to_exec = "Insert Into %s.dbo.IdentificationUnitAnalysis %s" % (MS_SQL_DB, p_print)
		# print sql_to_exec
		try:
			odbc_cursor1.execute(sql_to_exec)
			cnxn.commit()
		except Exception, detail:
			print "An Error occured during Insert: %r" % detail
			final()
			sys.exit(1)

		if (param_debug_mode == 1):
			#print ("Insert Into %s.dbo.IdentificationUnitAnalysis %s" % (MS_SQL_DB, p_print))
			print ("    Insert Into IdentificationUnitAnalysis CollSpecimenId=%s, IdentUnitId=%s, AnalysisId=%s, AnalysisNum='%s'" %
			(e_dwb_CollectionSpecimenId, identUnitId, param_analysisId, e_id) )

	if (param_debug_mode == 1):
		print ('  Nach E-Loop, %i mal durchlaufen' % e_loop_anzahl)

	if ((tracelength_zu_klein == 0) and (trace_begin_not_ABI == 0) and (maxCountSpecimenReached == 0) and (tracefileNotFound == 0)
		and (e_loop_anzahl == 1) and (passed_eintrag_gefunden == 1) ):
		if (param_debug_mode == 1):
			print ("  Update assembly_export_COI Set status='ok', note='L2F_Alles_ok' Where id=%s" % p_id)
		cur3.execute("Update assembly_export_COI Set status='ok', note='L2F_Alles_ok' Where id=%s" % p_id)
		db.commit()
	else:
		if (tracelength_zu_klein == 1):
			print ("  Update assembly_export_COI Set status='error', note='Fehler_L2F_TracelengthZuKlein' Where id=%s" % p_id)
			cur3.execute("Update assembly_export_COI Set status='error', note='Fehler_L2F_TracelengthZuKlein' Where id=%s" % p_id)
			db.commit()
			continue
		if (trace_begin_not_ABI == 1):
			print ("  Update assembly_export_COI Set status='error', note='Fehler_L2F_TracebeginNotABI' Where id=%s" % p_id)
			cur3.execute("Update assembly_export_COI Set status='error', note='Fehler_L2F_TracebeginNotABI' Where id=%s" % p_id)
			db.commit()
			continue
		if (maxCountSpecimenReached == 1):
			print ("  Update assembly_export_COI Set status='error', note='Fehler_L2F_maxCountSpecimenReached' Where id=%s" % p_id)
			cur3.execute("Update assembly_export_COI Set status='error', note='Fehler_L2F_maxCountSpecimenReached' Where id=%s" % p_id)
			db.commit()
			continue
		if (tracefileNotFound == 1):
			print ("  Update assembly_export_COI Set status='error', note='Fehler_L2F_TracefileNotFound' Where id=%s" % p_id)
			cur3.execute("Update assembly_export_COI Set status='error', note='Fehler_L2F_TracefileNotFound' Where id=%s" % p_id)
			db.commit()
			continue
	# time.sleep(0.5)

#if (param_debug_mode == 1):
print ("Nach P-Loop, %i mal durchlaufen" % p_loop_anzahl)

#  Close DB connections & trigger=ON
final()

#if (param_debug_mode == 1):
print 'Nach dem Trennen der Datenbankverbindungen, Programmende'
