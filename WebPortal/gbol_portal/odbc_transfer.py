from .vars import config
import logging
log = logging.getLogger(__name__)

try:
	import pyodbc
except ImportError as e:
	log.error(e)


class ODBC_DB(object):
	def __init__(self, db=''):
		if db == '':
			self.db_name = 'DiversityCollection_%s' % config['dwb']['name_suffix']
		else:
			self.db_name = db
		self.con = self.__connect()
		self.cur = self.con.cursor()
		self.commit = self.__commit

	def __connect(self):
		con = pyodbc.connect("{0};Database={1}".format(config['dwb']['connection_string'], self.db_name))
		log.debug("Connected to %s" % self.db_name)
		return con

	def __commit(self):
		try:
			self.con.commit()
		except Exception as e:
			if self.con:
				self.con.rollback()
			raise Exception(e)

	def final(self):
		if self.con:
			self.con.close()


class Transfer_DWB():
	def __init__(self):
		self.cxn = None

	def leave(self, msg):
		self.finish()
		log.debug(msg)
		ret = {"success": False, "msg": msg, "data": []}
		return ret

	def finish(self):
		"""
		Close odbc connection
		"""
		if self.cxn:
			self.cxn.final()
		self.cxn = None

	def __generate_specimen_id_sql(self, instituteID, sizeOfSample, numberOfSample, userName):
		res_s = []
		s = res_s.append
		s("BEGIN")
		s("""SET NOCOUNT ON;""")
		s("DECLARE @id int;")
		s("SELECT @id = MAX(CollectionSpecimenID) FROM CollectionSpecimen\
			WHERE DepositorsName = '%s' AND" % userName)
		if instituteID == 3:  # -- ZFMK
			if sizeOfSample == 2:
				if config['dwb']['name_suffix'] == 'Test':
					s(" CollectionSpecimenID >= 3500000 AND CollectionSpecimenID < 5000000;")
				else:
					s(" CollectionSpecimenID >= 2500000 AND CollectionSpecimenID < 5000000;")
			elif sizeOfSample == 5:
				if config['dwb']['name_suffix'] == 'Test':
					s(" CollectionSpecimenID < 3500000 AND CollectionSpecimenID >= 3000000;")
				else:
					s(" CollectionSpecimenID < 2500000 AND CollectionSpecimenID >= 2000000;")
		elif instituteID == 12:  # -- SGND
			s(" CollectionSpecimenID >= 1000000 AND CollectionSpecimenID < 10000000;")
		else:  # -- all other institutes
			if sizeOfSample in (2,5):
				s(" CollectionSpecimenID < 10000000 AND CollectionSpecimenID >= 5000000;")

		s("SELECT MIN(CollectionSpecimenID) as [first], MAX(CollectionSpecimenID) as [last] \
			FROM CollectionSpecimen \
			WHERE CollectionSpecimenID <= @id AND CollectionSpecimenID > @id - %i" % numberOfSample)
		s("END")
		return res_s

	def removeAgentFromDWB(self, loginName):
		"""Method to remove a GBOL User from DiversityWorkbench """
		resA = []
		A = resA.append

		try:
			self.cxn = ODBC_DB('DiversityAgents_%s' % config['dwb']['name_suffix'])
		except Exception as e:
			return self.leave(msg="Fatal error: could not odbc_connect to administration: %r" % e)

		sql = """DECLARE	@return_value int
			EXEC @return_value = procRemoveAgent_GBOL
					@LoginName = N'{0}';
			SELECT	'Return Value' = @return_value
		""".format(loginName)

		log.info('Remove user: %s', loginName)
		log.debug('Remove user SQL: %r', sql.replace('\t', '').replace('\n', ''))
		try:
			self.cxn.cur.execute(sql.replace('\t', '').replace('\n', ''))
			self.cxn.commit()
		except Exception as e:
			return self.leave(msg="Fatal error: could not remove %s: %r" % (loginName, e))
		else:
			result = self.cxn.cur.fetchone()[0]
			if result != '2':
				return self.leave(msg="Fatal error: could not remove %s: %r" % (loginName, e))
		self.finish()
		return {"success": True, "data": []}

	def addAgentIntoDWB(self, loginName, pw, agentTitle, givenName, inheritedName, phone, email, userId):
		"""Method to add a GBOL User into DiversityWorkbench """
		resA = []
		A = resA.append

		try:
			self.cxn = ODBC_DB('DiversityAgents_%s' % config['dwb']['name_suffix'])
		except Exception as e:
			return self.leave(msg="Fatal error: could not odbc_connect to administration: %r" % e)

		if agentTitle not in ('Prof. Dr.', 'Prof.', 'Dr.'):
			agentTitle = None
		if inheritedName is not None:
			A(inheritedName)
		else:
			inheritedName = ''
		if givenName is not None:
			A(", %s" % givenName)
		else:
			givenName = ''
		if agentTitle is not None:
			A(" %s" % agentTitle)
		else:
			agentTitle = ''
		agentName = "".join(resA)
		if phone is None:
			phone = ''

		# -- Stored procedure to insert a new user into DiversityWorkbench
		sql = """exec procInsertAgentNew_GBOL @LoginName = N'{0}',
			@Passwd = N'{1}',
			@AgentName = N'{2}',
			@AgentTitle = N'{3}',
			@GivenName = N'{4}',
			@InheritedName = N'{5}',
			@Telephone = N'{6}',
			@Email = N'{7}',
			@GBOL_user_id = {8}""".format(loginName, pw, agentName, agentTitle, givenName,
										  inheritedName, phone, email, userId)
		log.info('Insert user: %s', loginName)
		log.debug('Insert user SQL: %r', sql.replace('\t', '').replace('\n', ''))
		try:
			self.cxn.cur.execute(sql.replace('\t', '').replace('\n', ''))
			self.cxn.commit()
		except Exception as e:
			return self.leave(msg="Fatal error: could not save %s: %r" % (loginName, e))
		self.finish()
		return {"success": True, "data": []}

	def addProjectToAgent(self, loginName, userId, expertiseID):
		""" Method to add a new gbol expertise/user relation into DWB project/agent """
		try:
			self.cxn = ODBC_DB('DiversityCollection_%s' % config['dwb']['name_suffix'])
		except Exception as e:
			return self.leave(msg="Fatal error: could not odbc_connect to administration: %r" % e)

		sql = """exec procInsertAgentProject_GBOL @LoginName = '{0}',
			@GBoL_UserID = {1},
			@ProjectID = {2}""".format(loginName, userId, expertiseID)
		log.info('Certify Agent/ New Expertise: %s', loginName)
		log.debug('Certify Agent/ New Expertise SQL: %s', sql)
		try:
			self.cxn.cur.execute(sql.replace('\t', '').encode("utf-8").decode('utf-8'))
		except Exception as e:
			return self.leave(msg="Fatal error: could not save expertise for %s: %r" % (loginName, e))
		else:
			self.cxn.commit()
		self.finish()
		return {"success": True, "data": []}

	def getSpecimenId(self, mysql_conn, sizeOfSample, numberOfSample, userName, instituteID, expertiseID, userID):
		""" Insert specimen data from GBOL into DiversityWorkbench
			Return list of CollectionSpecimenIDs from inserted specimen data
		"""
		log.debug("Insert specimen data")
		if instituteID == 12:
			try:
				self.cxn = ODBC_DB(db='DiversityCollection_SGND')
			except Exception as e:
				return self.leave(msg="Fatal error: could not connect to shipment center: %r" % e)
		else:
			try:
				self.cxn = ODBC_DB()
			except Exception as e:
				return self.leave(msg="Fatal error: could not connect to shipment center: %r" % e)
		sql = """exec gbol_AddSpecimen @sizeOfSample = {0},
			@numberOfSample = {1},
			@agentName = N'{2}',
			@instituteID = {3},
			@expertiseID = {4},
			@GBOL_UserID = {5}""".format(sizeOfSample, numberOfSample, userName, instituteID, expertiseID, userID)

		log.info('Insert material: for %r', expertiseID)
		log.debug('Insert material SQL: ---%s---', sql)
		try:
			self.cxn.cur.execute(sql)
		except Exception as e:
			return self.leave(msg="Fatal error: could not save material order data: %r" % e)
		else:
			self.cxn.commit()

		sql = self.__generate_specimen_id_sql(instituteID, sizeOfSample, numberOfSample, userName)
		if len(sql)==0:
			return {"success": False, "data": []}
		try:
			self.cxn.cur.execute("\n".join(sql))
			rows = self.cxn.cur.fetchall()
		except Exception as e:
			return self.leave(msg="Fatal error: could not save material order data: %r" % e)
		else:
			resA = []
			for row in rows:
				resA.append(int(row[0]))
				resA.append(int(row[1]))
		self.finish()
		return {"success": True, "data": resA}


class Transfer_CacheDB(Transfer_DWB):
	def __init__(self):
		Transfer_DWB.__init()

	def leave(self, msg):
		log.debug(msg)
		ret = {"success": False, "msg": msg, "data": []}
		return ret

	def __generate_specimen_id_sql(self, instituteID, sizeOfSample, numberOfSample, userName):
		res_s = []
		s = res_s.append
		s("SELECT MAX(CollectionSpecimenID) FROM CollectionSpecimen WHERE DepositorsName = '%s' AND" % userName)
		if instituteID == 3:  # -- ZFMK
			if sizeOfSample == 2:
				if config['dwb']['name_suffix'] == 'Test':
					s(" CollectionSpecimenID >= 3500000 AND CollectionSpecimenID < 5000000;")
				else:
					s(" CollectionSpecimenID >= 2500000 AND CollectionSpecimenID < 5000000;")
			elif sizeOfSample == 5:
				if config['dwb']['name_suffix'] == 'Test':
					s(" CollectionSpecimenID < 3500000 AND CollectionSpecimenID >= 3000000;")
				else:
					s(" CollectionSpecimenID < 2500000 AND CollectionSpecimenID >= 2000000;")
		elif instituteID == 12:  # -- SGND
			s(" CollectionSpecimenID >= 1000000 AND CollectionSpecimenID < 10000000;")
		elif sizeOfSample in (2,5):  # -- all other institutes
			if sizeOfSample in (2,5):
				s(" CollectionSpecimenID < 10000000 AND CollectionSpecimenID >= 5000000;")
		return res_s

	def getSpecimenId(self, mysql_conn, sizeOfSample, numberOfSample, userName, instituteID, expertiseID, userID):
		""" Insert specimen data from GBOL into DiversityWorkbench
			Return list of CollectionSpecimenIDs from inserted specimen data
		"""
		log.debug("Insert specimen data")

		sql = """exec gbol_AddSpecimen @sizeOfSample = {0},
		  @numberOfSample = {1},
		  @agentName = N'{2}',
		  @instituteID = {3},
		  @expertiseID = {4},
		  @GBOL_UserID = {5}""".format(sizeOfSample, numberOfSample, userName, instituteID, expertiseID, userID)

		cur = conn.cursor()
		log.info('Insert material: for %r', expertiseID)
		log.debug('Insert material SQL: %s', sql)
		try:
			cur.execute(sql)
		except Exception as e:
			return self.leave(msg="Fatal error: could not save material order data: %r" % e, data=[])
		else:
			conn.commit()

		sql = self.__generate_specimen_id_sql(instituteID, sizeOfSample, numberOfSample, userName)
		if len(sql)==0:
			return {"success": False, "data": []}
		cur.execute("".join(sql).encode("utf-8"))
		row = cur.fetchone()
		max_id = row[0]
		sql = "SELECT MIN(CollectionSpecimenID), MAX(CollectionSpecimenID) FROM CollectionSpecimen " \
			  "WHERE CollectionSpecimenID <= %i AND CollectionSpecimenID > %i - %i" % (max_id, max_id, number)  # number
		cur.execute(sql)
		rows = cur.fetchall()
		resA = []
		for row in rows:
			resA.append(int(row[0]))
			resA.append(int(row[1]))
		return {"success": True, "data": resA}
