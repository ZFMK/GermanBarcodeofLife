#!/usr/bin/python
# -*- coding: utf8 -*-
"""
	Synchronize DiversityColelction

	reverse Geocode: https://github.com/geopy/geopy

	Test Species-Names:
([A-Z][a-z]+
  (?:\W+\(?\S+\)?)?
    (?:\W+[a-z0-9\.]+)?)
(?=$|(?:\W+\S+\W+\d{4})|(?:\W+\S+))
"""
import MySQLdb as mdb
import pyodbc
import pprint
import sys, re
import selects  # -- the queries
from collections import defaultdict
import datetime
import ConfigParser
config = ConfigParser.SafeConfigParser()
config.read('../config.ini')

VERBOSE = int(config.get('option', 'verbose'))
ENVIRONMENT = config.get('option', 'environment')
PROJECT = int(config.get('fims_cache', 'dc_project'))

import pudb

COMPARE = False

def sql_clean(s):
	if s==None:
		return ""
	return s.replace("\'","'").replace("'","\\\'").replace(';'',','').replace('"','\\\"').replace('\r\n','').replace('&','and')

class Base(object):
	def __init__(self):
		#pudb.set_trace()
		self.queries = selects.queries(project=PROJECT)

class MySQLBase(object):
	def __init__(self):
		self.con = self.__mysql_connect()
		self.cur = self.con.cursor()
		self.commit = self.__commit

	def insert(self):
		raise NotImplementedError()

	def __mysql_connect(self):
		db_host = config.get('fims_cache', 'mysql_host')
		db_user = config.get('fims_cache', 'mysql_user')
		db_pwd = config.get('fims_cache', 'mysql_passwd')
		db_name = config.get('fims_cache', 'mysql_database')
		try:
			con = mdb.connect(host=db_host, user=db_user, passwd=db_pwd, db=db_name)
		except mdb.Error, e:
			print "Error %d: %s" % (e.args[0],e.args[1])
			sys.exit(1)
		return con

	def __commit(self):
		try:
			self.con.commit()
		except mdb.Error, e:
			if self.con:
				self.con.rollback()
			print "Error %d: %s" % (e.args[0],e.args[1])
			sys.exit(1)

	def final(self):
		if self.con:
			self.con.close()


class GBOL_Fims(Base, MySQLBase):
	def __init__(self, reset=False):
		Base.__init__(self)
		MySQLBase.__init__(self)
		self.cur = self.con.cursor()
		self.entries = {}
		self.columns = []
		try:
			self.cur.execute('TRUNCATE GBOL_FIMS_tmp')
		except Exception, detail:
			print "Error in %s:\n"%q
			print Exception, detail
			exit
		else:
			self.commit()

	def getColumnHeaders(self):
		resU = []
		U = resU.append
		self.cur.execute(self.queries.columns_headers())
		for row in self.cur.fetchall():
			U(row[0])
		self.columns = resU
		return self.columns

	def insertQuery(self):
		if len(self.columns)==0:
			self.getColumnHeaders()
		values = '%s,' * (len(self.columns)-2)
		resA = """INSERT INTO {0} ({1}) VALUES ({2} NOW(), NOW())""".format(self.queries.temp_table, ",".join(self.columns), values)
		return resA

	def getEntries(self):
		resU = {}
		self.cur.execute(self.queries.all_ids())
		for row in self.cur.fetchall():
			resU[int(row[0])] = 1
		self.entries = resU
		return self.entries

	def insert(self, data):
		q = self.insertQuery()
		try:
			self.cur.executemany(q, data)
		except Exception, detail:
			print "Programming error in %s:\n"%q
			print Exception, detail
			exit
		else:
			self.commit()

	def finish(self):
		q = self.queries.finish()
		try:
			self.cur.execute('TRUNCATE GBOL_FIMS')
		except Exception, detail:
			print "Error in %s:\n"%q
			print Exception, detail
			exit
		else:
			self.commit()
		try:
			self.cur.execute(q)
		except Exception, detail:
			print "Error in %s:\n"%q
			print Exception, detail
			exit
		else:
			self.commit()
			try:
				self.cur.execute('TRUNCATE GBOL_FIMS_tmp')
			except Exception, detail:
				print "Error in %s:\n"%q
				print Exception, detail
				exit
			else:
				self.commit()

class DWBBase(object):
	def __init__(self):
		self.con = self.__odbc_connect()

	def __odbc_connect(self):
		MS_SQL_DB = config.get('fims_cache', 'mssql_connection')
		cnxn = pyodbc.connect(MS_SQL_DB)
		return cnxn

class DWB(DWBBase, Base):
	def __init__(self):
		Base.__init__(self)
		DWBBase.__init__(self)
		self.entries = {}
		self.taxon_matcher = re.compile("([A-Z][a-z]+(?:\W+\(?\S+\)?)?(?:\W+[a-z0-9\.]+)?)(?=$|(?:\W+\S+\W+\d{4})|(?:\W+\S+))",re.VERBOSE)

	def fetchEntries(self):
		resU = {}
		odbc_csr = self.con.cursor()
		odbc_csr.execute(self.queries.dwb_all())
		columns = [column[0] for column in odbc_csr.description]
		for row in odbc_csr.fetchall():
			# -- row = {t[0]: value for (t, value) in zip(odbc_csr.description, row)}
			try:
				taxon = self.taxon_matcher.search(row[9])
			except TypeError, e:
				row[9] = ''
			else:
				if taxon and len(taxon.groups())>0:
					row[9] = taxon.groups()[0]
			resU[int(row[0])] = row[0:-2]+(row[-2].strftime('%Y-%m-%d %H:%M:%S'),row[-1].strftime('%Y-%m-%d %H:%M:%S'))
		self.entries = resU

	def getEntries(self):
		for entry in self.entries.items():
			yield entry[1]

# ============ Main =========== #
resA = []
A = resA.append

pp = pprint.PrettyPrinter(indent=2)

fims = GBOL_Fims()
if COMPARE:
	fims.getEntries()
dwb = DWB()
dwb.fetchEntries()

A("No. of entries in DWB: %i" % len(dwb.entries))
A("No. of entries in FIMS: %i" % len(fims.entries))

if COMPARE:
	d = selects.DictDiffer(dwb.entries, fims.entries)
	old =  list(d.added())
	new = list(d.removed())
	both = d.changed()
	unchanged = d.unchanged()

	A("No. Ids in DWB but not in FIMS: %i" % len(old))
	A("No. Ids in FIMS and not in DWB: %i" % len(new))
	A("No. Ids in DWB + FIMS: %i" % len(both))
	A("Unchanged: %i" % len(unchanged))

	print "\n".join(resA)

print 'Inserting %i entries in FIMS' % len(dwb.entries)
i = 0
for entry in dwb.getEntries():
	i+= 1
	s = "\r\t%06i: %s             " % (i, entry[3])
	print >> sys.stdout, s,
	fims.insert([entry]) # -- all entries
print 'Done, inserted %i entries into FIMS'
print 'Copying to final table:'
fims.finish()
print 'Done'

