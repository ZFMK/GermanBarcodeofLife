#!/usr/bin/python
# -*- coding: utf8 -*-
"""
    Synchronize GBOL Data in DC with MySQL cache
"""
import MySQLdb as mdb
import pyodbc
import pprint
import sys, re
import selects  # -- the queries
from collections import defaultdict
import datetime

VERBOSE = 1
PROJECT = 1  #: 1: All from GBOL, 2: only one Dataset

config = {
	'cache_db' = {'gbol_fims': {'host': "localhost",
		'user': "some_user",
		'passwd': "some_password",
		'database': db}
	},
	'dwb' = {'coll_zfmk': 'DSN=dwb_prod2;UID=<ms sql username here>;PWD=<ms sql password here>',
		'tnt': 'DSN=TNT;UID=<ms sql username here>;PWD=<ms sql password here>'
	}
}

def sql_clean(s):
	if s==None:
		return ""
	return s.replace("\'","'").replace("'","\\\'").replace(';'',','').replace('"','\\\"').replace('\r\n','').replace('&','and')

class Base(object):
	def __init__(self):
		self.queries = selects.queries(project=PROJECT)

class MySQLBase(object):
	def __init__(self):
		self.con = self.__mysql_connect(db='gbol_fims')
		self.cur = self.con.cursor()
		self.commit = self.__commit

	def insert(self):
		raise NotImplementedError()

	def __mysql_connect(self, db):
		dbs = config['cache_db']
		try:
			con = mdb.connect(host=dbs[db]['host'], user=dbs[db]['user'], passwd=dbs[db]['passwd'], db=db)
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
		if reset:
			self.cur.execute("truncate `GBOL_Fims`")
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
	def __init__(self, db_name):
		self.con = self.__odbc_connect(db_name)

	def __odbc_connect(self, db):
		cnxn = pyodbc.connect(config['dwb'][db])
		return cnxn

class DWB(DWBBase, Base):
	def __init__(self):
		Base.__init__(self)
		DWBBase.__init__(self, 'coll_zfmk')
		self.entries = {}

	def getEntries(self):
		resU = {}
		odbc_csr = self.con.cursor()
		odbc_csr.execute(self.queries.dwb_all())
		columns = [column[0] for column in odbc_csr.description]
		for row in odbc_csr.fetchall():
			resU[int(row[0])] = row[0:-2]+(row[-2].strftime('%Y-%m-%d %H:%M:%S'),row[-1].strftime('%Y-%m-%d %H:%M:%S'))
		self.entries = resU
		return self.entries

# ============ Main =========== #
resA = []
A = resA.append

pp = pprint.PrettyPrinter(indent=2)

fims = GBOL_Fims()
fims.getEntries()
dwb = DWB()
dwb.getEntries()

A("No. of entries in DWB: %i" % len(dwb.entries))
A("No. of entries in FIMS: %i" % len(fims.entries))

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

if 1: #if len(old)>0:
	fims.insert([dwb.entries[i] for i in dwb.entries]) # -- all entries
	print 'Done, Copying to final table:'
	fims.finish()
	print 'Done'

