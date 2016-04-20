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
    def leave(self, odbc_conn, msg):
        if odbc_conn:
            odbc_conn.final()
        log.debug(msg)
        ret = {"success": False, "msg": msg, "data": []}
        return ret

    def removeAgentFromDWB(self, loginName):
        """Method to remove a GBOL User from DiversityWorkbench """
        resA = []
        A = resA.append

        try:
            odbc_conn = ODBC_DB('DiversityAgents_%s' % config['dwb']['name_suffix'])
        except Exception as e:
            return self.leave(odbc_conn, msg="Fatal error: could not odbc_connect to administration: %r" % e)

        sql = """DECLARE    @return_value int
            EXEC @return_value = procRemoveAgent_GBOL
                    @LoginName = N'{0}';
            SELECT    'Return Value' = @return_value
        """.format(loginName)

        log.info('Remove user: %s', loginName)
        log.debug('Remove user SQL: %r', sql.replace('\t', '').replace('\n', ''))
        try:
            odbc_conn.cur.execute(sql.replace('\t', '').replace('\n', ''))
            odbc_conn.commit()
        except Exception as e:
            return self.leave(odbc_conn, msg="Fatal error: could not remove %s: %r" % (loginName, e))
        else:
            result = odbc_conn.cur.fetchone()[0]
            if result != '2':
                return self.leave(odbc_conn, msg="Fatal error: could not remove %s: %r" % (loginName, e))
        odbc_conn.final()
        return {"success": True, "data": []}

    def addAgentIntoDWB(self, loginName, pw, agentTitle, givenName, inheritedName, phone, email, userId):
        """Method to add a GBOL User into DiversityWorkbench """
        resA = []
        A = resA.append

        try:
            odbc_conn = ODBC_DB('DiversityAgents_%s' % config['dwb']['name_suffix'])
        except Exception as e:
            return self.leave(odbc_conn, msg="Fatal error: could not odbc_connect to administration: %r" % e)

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
            odbc_conn.cur.execute(sql.replace('\t', '').replace('\n', ''))
            odbc_conn.commit()
        except Exception as e:
            return self.leave(odbc_conn, msg="Fatal error: could not save %s: %r" % (loginName, e))
        odbc_conn.final()
        return {"success": True, "data": []}

    def addProjectToAgent(self, loginName, userId, expertiseID):
        """ Method to add a new gbol expertise/user relation into DWB project/agent """
        try:
            odbc_conn = ODBC_DB('DiversityCollection_%s' % config['dwb']['name_suffix'])
        except Exception as e:
            return self.leave(odbc_conn, msg="Fatal error: could not odbc_connect to administration: %r" % e)

        sql = """exec procInsertAgentProject_GBOL @LoginName = '{0}',
            @GBoL_UserID = {1},
            @ProjectID = {2}""".format(loginName, userId, expertiseID)
        log.info('Certify Agent/ New Expertise: %s', loginName)
        log.debug('Certify Agent/ New Expertise SQL: %s', sql)
        try:
            odbc_conn.cur.execute(sql.replace('\t', '').encode("utf-8").decode('utf-8'))
        except Exception as e:
            return self.leave(odbc_conn, msg="Fatal error: could not save expertise for %s: %r" % (loginName, e))
        else:
            odbc_conn.commit()
        odbc_conn.final()
        return {"success": True, "data": []}

    def getSpecimenId(self, conn, sizeOfSample, numberOfSample, collectorName, instituteID, expertiseID):
        """ Insert specimen data from GBOL into DiversityWorkbench
            Return list of CollectionSpecimenIDs from inserted specimen data
        """
        log.debug("Insert specimen data")
        if instituteID == 12:
            try:
                odbc_conn = ODBC_DB(db='DiversityCollection_SGND')
            except Exception as e:
                return self.leave(odbc_conn, msg="Fatal error: could not connect to shipment center: %r" % e)
        else:
            try:
                odbc_conn = ODBC_DB()
            except Exception as e:
                return self.leave(odbc_conn, msg="Fatal error: could not connect to shipment center: %r" % e)
        cmd = []
        C = cmd.append
        C("exec gbol_AddSpecimen @sizeOfSample = ")
        C(str(sizeOfSample))
        C(", @numberOfSample = ")
        C(str(numberOfSample))
        C(", @collectorName = '")
        C(collectorName)
        C("', @instituteID = '")
        C(str(instituteID))
        C("', @expertise = ")
        C(str(expertiseID))

        log.info('Insert material: for %r', expertiseID)
        log.debug('Insert material SQL: %s', "".join(cmd))
        try:
            odbc_conn.cur.execute("".join(cmd))
        except Exception as e:
            return self.leave(odbc_conn, msg="Fatal error: could not save material order data: %r" % e)
        else:
            odbc_conn.commit()

        # -- sql to get the CollectionSpecimenID block which was inserted with the procedure above
        sql = []
        S = sql.append
        S("BEGIN")
        S("""SET NOCOUNT ON;""")
        S("DECLARE @id int;")
        S("SELECT @id = MAX(CollectionSpecimenID) FROM CollectionSpecimen WHERE DepositorsName = '%s' AND" % collectorName)
        if instituteID == 3:  # -- ZFMK
            if sizeOfSample == 2:
                if config['dwb']['name_suffix'] == 'Test':
                    S(" CollectionSpecimenID >= 3500000;")
                else:
                    S(" CollectionSpecimenID >= 2500000;")
            elif sizeOfSample == 5:
                if config['dwb']['name_suffix'] == 'Test':
                    S(" CollectionSpecimenID < 3500000 AND CollectionSpecimenID >= 3000000;")
                else:
                    S(" CollectionSpecimenID < 2500000 AND CollectionSpecimenID >= 2000000;")
            else:
                odbc_conn.final()
                return {"success": True, "data": []}
        elif instituteID == 12:  # -- SGND
            S(" CollectionSpecimenID >= 1000000;")
        else:
            odbc_conn.final()
            return {"success": True, "data": []}
        S("SELECT MIN(CollectionSpecimenID) as [first], MAX(CollectionSpecimenID) as [last] FROM CollectionSpecimen WHERE CollectionSpecimenID <= @id AND CollectionSpecimenID > @id - %i" % numberOfSample)
        S("END")
        try:
            odbc_conn.cur.execute("\n".join(sql))
            rows = odbc_conn.cur.fetchall()
        except Exception as e:
            return self.leave(odbc_conn, msg="Fatal error: could not save material order data: %r" % e)
        else:
            resA = []
            for row in rows:
                resA.append(int(row[0]))
                resA.append(int(row[1]))
        odbc_conn.final()
        return {"success": True, "data": resA}


class Transfer_CacheDB(Transfer_DWB):

    def leave(self, conn, msg):
        if conn:
            conn.final()
        log.debug(msg)
        ret = {"success": False, "msg": msg, "data": []}
        return ret

    def getSpecimenId(self, conn, sizeOfSample, numberOfSample, collectorName, instituteName, expertiseID):
        """ Insert specimen data from GBOL into DiversityWorkbench
            Return list of CollectionSpecimenIDs from inserted specimen data
        """
        log.debug("Insert specimen data")

        cmd = []
        C = cmd.append
        C("CALL gbol_AddSpiceman (sizeOfSample = ")
        C(str(sizeOfSample))
        C(", numberOfSample = ")
        C(str(numberOfSample))
        C(", collectorName = '")
        C(collectorName)
        C("', instituteName = '")
        C(instituteName)
        C("', expertise = ")
        C(str(expertiseID))

        cur = conn.cursor()
        log.info('Insert material: for %r', expertiseID)
        log.debug('Insert material SQL: %s', "".join(cmd))
        try:
            cur.execute("".join(cmd))
        except Exception as e:
            return self.leave(conn, msg="Fatal error: could not save material order data: %r" % e, data=[])
        else:
            conn.commit()

        # sql to get the CollectionSpecimenID block which was inserted with the procedure above
        sql = []
        S = sql.append
        S("SELECT MAX(CollectionSpecimenID) FROM CollectionSpecimen WHERE DepositorsName = '%s' AND" % collectorName)
        sql.append(name)
        if sizeOfSample == 2:
            if config['dwb']['name_suffix'] == 'Test':
                S(" CollectionSpecimenID >= 3500000;")
            else:
                S(" CollectionSpecimenID >= 2500000;")
        elif sizeOfSample == 5:
            if config['dwb']['name_suffix'] == 'Test':
                S(" CollectionSpecimenID < 3500000 AND CollectionSpecimenID >= 3000000;")
            else:
                S(" CollectionSpecimenID < 2500000 AND CollectionSpecimenID >= 2000000;")
        else:
            return {"success": true, "data": []}

        cur.execute("".join(sql).encode("utf-8"))
        row = cur.fetchone()
        max_id = row[0]
        sql = "SELECT MIN(CollectionSpecimenID), MAX(CollectionSpecimenID) FROM CollectionSpecimen " \
              "WHERE CollectionSpecimenID <= %i AND CollectionSpecimenID > %i - %i" % (max_id, max_id, number)  # number
        cur.execute(sql)
        resA = []
        resA.append(int(row[0]))
        resA.append(int(row[1]))
        conn.final()
        return {"success": True, "data": resA}
