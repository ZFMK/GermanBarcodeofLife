from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.renderers import render
import pymysql
import os
import uuid

from .async_email import send_mail
from .vars import config, messages

import logging
log = logging.getLogger(__name__)


if config['dwb']['use_dwb'] > 0:
	from .odbc_transfer import Transfer_DWB as DWB

sql_select_user_expertise = """SELECT u.uid, u.name, u.vorname, u.nachname,
		u.mail, IFNULL(CONCAT_WS(' ', u.salutation, u.title),'') AS salutation, e.name, e.tid FROM users u
	LEFT JOIN UserExpertiseRequest uer ON uer.uid = u.uid
	LEFT JOIN Expertise e ON e.tid = uer.id_expertise
	LEFT JOIN UserExpertise ue ON ue.id_Expertise = e.tid
	LEFT JOIN users u2 ON u2.uid = ue.uid
	INNER JOIN UserRole ur2 ON ur2.uid=u2.uid
WHERE u.status = '{0}' AND ur2.rid IN (1, 2)
	AND u2.uid = '{uid}'"""

def notify_developers(subject, message):
	log.error(message)
	dev_group = config['dev_group'].split(';')
	send_from = config['smtp']['sender']
	for mail_to in dev_group:
		send_mail(mail_to, send_from, subject, message.replace('\t', '	'))


def set_number_requests(conn, session):
	cur = conn.cursor()
	if 2 in session['role']:
		# -- get number od requests
		sql_select_sum = ["""SELECT
					SUM(IF(u1.status = '0', 1, 0)) AS new_users,
					SUM(IF(u1.status = '1', 1, 0)) AS new_expertises
				FROM users u2
					LEFT JOIN UserExpertise ue ON u2.uid=ue.Uid
					LEFT JOIN UserExpertiseRequest uer ON ue.id_Expertise=uer.id_Expertise
					LEFT JOIN users u1 ON u1.uid=uer.Uid
					INNER JOIN UserRole ur ON ur.uid=u2.uid
				WHERE ur.rid IN (1,2) AND u2.uid = {uid}""",
						  """SELECT COUNT(s.id) FROM Shippings s
					inner join ShippingRequests sr on sr.id = s.ShippingRequestId
				WHERE sr.ContactId = {uid} AND s.status='raw'"""]
		cur.execute(sql_select_sum[0].format(**session))
		row = cur.fetchone()
		session['new_users'] = int(row[0])
		session['new_expertise'] = int(row[1])
		cur.execute(sql_select_sum[1].format(**session))
		row = cur.fetchone()
		session['shipping_requests'] = int(row[0])
	cur.close()


@view_config(route_name='orderTable')
def orderTable_view(request):
	conn = pymysql.connect(host=config['host'], port=config['port'],
						   user=config['user'], passwd=config['pw'], db=config['db'])
	cur = conn.cursor()
	session = request.session
	table = request.POST.get('table')
	column = request.POST.get('column')
	order = request.POST.get('order')
	sql = ""
	if table == "sammeltabelle":
		sql = "SELECT count, kindof, requestdate, xlsfile FROM ShippingRequests where uid = " + str(session['uid'])
	elif table == "versandanschreiben":
		sql = "SELECT sr.transactionKey, sr.requestDate, s.uploaded FROM ShippingRequests sr INNER JOIN Shippings s " \
			  "ON s.shippingrequestid = sr.id WHERE sr.uid = " + str(session['uid'])
	elif table == "user":
		sql = "SELECT u.uid, u.name, u.vorname, u.nachname , u.mail, concat_ws(u.salutation), ' ', u.title " \
			  "AS salutation, e.name AS expertise FROM users u " \
			  "LEFT JOIN UserExpertiseRequest uer ON uer.uid = u.uid " \
			  "LEFT JOIN Expertise e ON e.tid = uer.id_expertise " \
			  "LEFT JOIN UserExpertise ue ON ue.id_Expertise = e.tid " \
			  "LEFT JOIN users u2 ON u2.uid = ue.uid " \
			  "WHERE u.status = 0 AND u2.role IN (1, 2) AND u2.uid =" + str(session['uid'])
	elif table == "expertise":
		sql = "SELECT u.uid, u.name, u.vorname, u.nachname, e.name AS expertise, e.tid FROM users u " \
			  "LEFT JOIN UserExpertiseRequest uer ON uer.uid = u.uid " \
			  "LEFT JOIN Expertise e ON e.tid = uer.id_expertise " \
			  "LEFT JOIN UserExpertise ue ON ue.id_Expertise = e.tid " \
			  "LEFT JOIN users u2 ON u2.uid = ue.uid " \
			  "WHERE u.status = 1 AND u2.role IN (1, 2) AND u2.uid =" + str(session['uid'])
	elif table == "shippings":
		sql = "SELECT s.id,s.uploaded,s.xlsfile,s.count,s.status FROM gbol_python.Shippings s " \
			  "INNER JOIN ShippingRequests sr ON sr.id = s.shippingrequestid WHERE sr.uid = " + str(session['uid'])
	sql = sql + " ORDER BY " + column + " " + order
	cur.execute(sql)
	dataA = []
	A = dataA.append
	count = 0
	for row in cur:
		if count % 2 == 0:
			style = "even"
		else:
			style = "odd"
		A('<tr class="' + style + '">')
		if table in ("sammeltabelle", "versandanschreiben"):
			A("""<td>{1}</td>
			<td>{2}</td>
			<td>{3}</td>
			<td><a href="/download?fileName={4}&fileOption={0}">Herunterladen</a></td>""".format(table, *row))
		elif table == "user":
			A("""<td><input type="Checkbox" onclick="changeUsers({0})"></td>
				<td>{0}</td>
				<td>{1}</td>
				<td>{5}</td>
				<td>{2}</td>
				<td>{3}</td>
				<td>{4}</td>
				<td>{6}</td>""".format(*row))
		elif table == "expertise":
			A("""<td><input type="Checkbox" onclick="changeUsers({0})"></td>
				<td>{0}</td>
				<td>{1}</td>
				<td>{2}</td>
				<td>{3}</td>
				<td>{4}</td""".format(*row))
		elif table == "shippings":
			A("""<td><input type="Checkbox" onclick="changeUsers('+str(row[0])+')"></td>')
				<td>{0}</td>
				<td>{1}</td>
				<td><a href="/download?fileName={2}&fileOption=upload">Herunterladen</a></td>
				<td>{3}</td>
				<td>{4}</td>""".format(*row))
		A("</tr>")
		count += 1
	cur.close()
	conn.close()
	return Response("".join(dataA))


@view_config(route_name='nutzer-zertifizieren')
def nutzer_zertifizieren_view(request):
	""" TEST:
	DELETE ue FROM UserExpertise ue
			LEFT JOIN users u ON ue.uid=u.uid
		WHERE u.name='user-porifera';
	DELETE ue FROM UserExpertiseRequest ue
			LEFT JOIN users u ON ue.uid=u.uid
		WHERE u.name='user-porifera';
	INSERT INTO gbol-python.UserExpertiseRequest
		(Uid, id_Expertise, RequestDate)
		VALUES (740,26820,NOW());
	update users set status='0' where name='user-porifera';
	"""
	session = request.session
	conn = pymysql.connect(host=config['host'], port=config['port'],
						   user=config['user'], passwd=config['pw'], db=config['db'])
	set_language(request)
	lang = get_language(request)
	msg = []
	if 'role' in session and session['role'] is not None:
		if 1 not in session['role'] and 2 not in session['role']:
			return HTTPFound(location=request.route_url('dashboard'))
		if 'accept' in request.POST or 'decline' in request.POST:
			sql_get_user = "SELECT name, mail, vorname, nachname, CONCAT_WS(' ', salutation, ' ', title) " \
						   "AS salutation FROM users WHERE uid = '{0}'"
			cur = conn.cursor()

			users = request.POST.get('userIds')
			if users != "":
				users = users.replace("$", "")
				users = users[:len(users) - 1]
				users = users.split(",")
				if 'accept' in request.POST:
					sql_certify_user = ["""UPDATE users
							SET status = '1' WHERE uid = '{0}'""",
										"""INSERT INTO UserExpertise (
							SELECT uid, id_expertise
								FROM UserExpertiseRequest
							WHERE uid = '{0}')""",
										"""DELETE FROM UserExpertiseRequest where uid = '{0}'"""]
					for curr_user in users:
						success = True

						cur.execute(sql_get_user.format(curr_user))
						acc = cur.fetchone()

						""" 24.03.2015, PG: Removed sync of users (agents) between DWB and GBOL Webportal
						if success and config['dwb']['use_dwb']>0:
							cur.execute("select id_expertise from UserExpertiseRequest
							where uid = '{0}'".format(curr_user))
							for row in cur.fetchall():
								expertise = row[0]
								# -- Write new Expertise into DiversityWorkbench via Webservice
								try:
									dwb = DWB()
									result = dwb.addProjectToAgent(loginName=acc[0],
									userId=curr_user, expertiseID=expertise)
								except Exception as e:
									msg.append('{0}'.format(e))
									success = False
								else:
									success = result['success']
						"""

						for sql in sql_certify_user:
							try:
								cur.execute(sql.format(curr_user))
							except Exception as e:
								msg.append(
									'Could not certify user {0}. The following error occured: {}'.format(acc[0], *e))
								conn.rollback()
								success = False
						if success:  # -- Email to user
							conn.commit()
							header = messages['email_reg_subject'][lang].format(*acc)
							send_from = config['smtp']['sender']
							send_to = acc[1]
							text = messages['email_reg_body'][lang].format(*acc)
							try:
								send_mail(send_to, send_from, header, text.replace('\t', ''))
							except Exception as e:
								msg.append('Registration message could not be send to user: %s. Error was: %r\n' % (
									curr_user, e))
				elif 'decline' in request.POST:
					sql_decline_user = ["""DELETE ue FROM UserExpertise ue
								LEFT JOIN users u ON ue.uid=u.uid
							WHERE u.name='{0}'""",
										"""DELETE ue FROM UserExpertiseRequest ue
								LEFT JOIN users u ON ue.uid=u.uid
							WHERE u.name='{0}'""",
										"""DELETE FROM UserRole WHERE uid='{0}'""",
										"""DELETE FROM users WHERE uid='{0}'"""]

					for curr_user in users:
						success = True

						cur.execute(sql_get_user.format(curr_user))
						acc = cur.fetchone()

						""" 24.03.2015, PG: Removed sync of users (agents) between DWB and GBOL Webportal
						if config['dwb']['use_dwb']>0:
							try:
								dwb = DWB()
								result = dwb.removeAgentFromDWB(loginName=acc[0])
							except Exception as e:
								msg.append('{0}'.format(e))
								success = False
							else:
								success = result['success']
								if not success:
									msg.append(result['msg'])
						"""

						for sql in sql_decline_user:
							try:
								cur.execute(sql.format(acc[0]))
							except Exception as e:
								msg.append(
									'Could not remove user {0}. The following error occured: {}'.format(acc[0], *e))
								conn.rollback()
								success = False
						if success:
							conn.commit()
							header = messages['email_reg_subject'][lang].format(*acc)
							send_from = config['smtp']['sender']
							send_to = acc[1]
							text = messages['email_reg_body_decline'][lang].format(*acc)
							try:
								send_mail(send_to, send_from, header, text.replace('\t', ''))
							except Exception as e:
								msg.append(
									'Registration information message could not be send for user: %s. '
									'Error was: %r\n' % (curr_user, e))
			cur.close()
		set_number_requests(conn, session)

		data = []
		D = data.append
		cur = conn.cursor()
		cur.execute(sql_select_user_expertise.format(0, **session))
		count = 0
		for row in cur:
			if count % 2 == 0:
				style = "even"
			else:
				style = "odd"
			D('<tr class="{0}">'.format(style))
			D("""<td><input type="checkbox" name="userId" onclick="changeUsers({0})"></td>
				<td><a href="/sammeln/userEdit?uid={0}">{1}</a></td>
				<td>{5}</td>
				<td>{2}</td>
				<td>{3}</td>
				<td>{4}</td>
				<td>{6}</td>""".format(*row))
			D("</tr>")
			count += 1
		cur.close()
		conn.close()
		if len(msg) > 0:
			result = render('templates/%s/admin/userZertifizieren.pt' % lang,
							{'value': "".join(data), "message": "<br />".join(msg)}, request=request)
		else:
			result = render('templates/%s/admin/userZertifizieren.pt' % lang, {'value': "".join(data)}, request=request)
		response = Response(result)
		return response
	url = request.route_url('login')
	return HTTPFound(location=url)


@view_config(route_name='expertise-zertifizieren')
def expertise_zertifizieren_view(request):
	session = request.session
	conn = pymysql.connect(host=config['host'], port=config['port'],
						   user=config['user'], passwd=config['pw'], db=config['db'])
	set_language(request)
	lang = get_language(request)
	success = True
	msg = []
	if 'role' in session and session['role'] is not None:
		if 1 not in session['role'] and 2 not in session['role']:
			url = request.route_url('dashboard')
			return HTTPFound(location=url)
		if 'accept' in request.POST or 'decline' in request.POST:
			cur = conn.cursor()
			users = request.POST.get('userIds')
			if users != "":
				users = users.replace("$", "")
				users = users[:len(users) - 1]
				users = users.split(",")
				i = 0
				if 'accept' in request.POST:
					while i < len(users):
						data = users[i].split(" ")
						# -- update user, insert userexpertise, delete expertiserequest
						try:
							cur.execute("""INSERT INTO UserExpertise
								(Uid,id_Expertise)
								SELECT uid, id_expertise
									FROM UserExpertiseRequest
								WHERE uid = '{0}'
									AND id_expertise ='{1}'""".format(*data))
						except Exception as e:
							msg.append('Fatal error: could not certify user! {}'.format(*e))
							conn.rollback()
							success = False
						else:
							conn.commit()
						""" 24.03.2015, PG: Removed sync of users (agents) between DWB and GBOL Webportal
						if success and config['dwb']['use_dwb']>0:
							cur.execute("select name from users where uid = '{0}'".format(*data))
							acc = cur.fetchone()
							try:
								dwb = DWB()
								result = dwb.addProjectToAgent(loginName=acc[0],userId=data[0], expertiseID=data[1])
							except Exception as e:
								msg.append('{0}'.format(e))
								success = False
							else:
								success = result['success']
						"""
						if success:
							cur.execute("""DELETE FROM UserExpertiseRequest
								WHERE uid = '{0}'
									AND id_expertise = '{1}'""".format(*data))
							conn.commit()
							cur.execute("""SELECT name, mail, vorname, nachname, CONCAT_WS(' ', salutation, title)
										AS salutation FROM users WHERE uid = '{0}'""".format(data[0]))
							acc = cur.fetchone()
							cur.execute("""SELECT name FROM Expertise WHERE tid = '{0}'""".format(data[1]))
							exp_name = cur.fetchone()[0]
							mail_addr = acc[1]
							header = messages['reg_exp_mail_subject'][lang]
							send_from = config['smtp']['sender']
							send_to = mail_addr
							text = messages['reg_exp_accept'][lang].format(exp_name, acc[2], acc[3], acc[4])
							try:
								send_mail(send_to, send_from, header, text.replace('\t', ''))
							except Exception as e:
								msg.append('Message could not be send to user: %s. Error was: %r\n' % (data, e))
						else:
							msg.append(result['msg'])
						i += 1
				elif 'decline' in request.POST:
					cur = conn.cursor()
					while i < len(users):
						data = users[i].split(" ")
						# -- delete userexpertiserequest
						cur.execute("""delete from UserExpertiseRequest
							where uid = '{0}'
								and id_expertise = '{1}'""".format(*data))
						conn.commit()
						cur.execute("""SELECT name, mail, vorname, nachname, CONCAT_WS(' ', salutation, title)
										AS salutation FROM users WHERE uid = '{0}'""".format(data[0]))
						acc = cur.fetchone()
						cur.execute("""SELECT name FROM Expertise WHERE tid = '{0}'""".format(data[1]))
						exp_name = cur.fetchone()
						mail_addr = acc[1]
						header = messages['reg_exp_mail_subject'][lang]
						send_from = config['smtp']['sender']
						send_to = mail_addr
						text = messages['reg_exp_decline'][lang].format(exp_name, acc[2], acc[3], acc[4])
						try:
							send_mail(send_to, send_from, header, text.replace('\t', ''))
						except Exception as e:
							msg.append('Message could not be send to user: %s. Error was: %r\n' % (data, e))
						i += + 1
			cur.close()
			set_number_requests(conn, session)

		data = []
		D = data.append
		cur = conn.cursor()
		cur.execute(sql_select_user_expertise.format(1, **session))
		count = 0
		for row in cur:
			if count % 2 == 0:
				style = "even"
			else:
				style = "odd"
			D('<tr class="{0}">'.format(style))
			D("""<td><input type="Checkbox" onclick="changeUsersExpertise({0}, {7})"></td>
				<td>{1}</td>
				<td>{2}</td>
				<td>{3}</td>
				<td>{6}</td>
			</tr>""".format(*row))
			count += 1
		cur.close()
		conn.close()
		if len(msg) > 0:
			result = render('templates/%s/admin/expertiseZertifizieren.pt' % lang,
							{'value': "".join(data), "message": "<br />".join(msg)}, request=request)
		else:
			result = render('templates/%s/admin/expertiseZertifizieren.pt' % lang, {'value': "".join(data)},
							request=request)
		response = Response(result)
		return response
	url = request.route_url('login')
	return HTTPFound(location=url)


@view_config(route_name='sammelliste')
def sammelliste_view(request):
	session = request.session
	conn = pymysql.connect(host=config['host'], port=config['port'],
						   user=config['user'], passwd=config['pw'], db=config['db'])
	set_language(request)
	lang = get_language(request)
	if 'role' in session:
		if session['role'] is not None:
			if 2 not in session['role']:
				url = request.route_url('dashboard')
				return HTTPFound(location=url)
			cur = conn.cursor()
			P = request.POST
			if 'new_state' in P:
				sql_update = """UPDATE Shippings SET status = '{0}' WHERE id = '{1}'"""
				shipping_id = P.get('shipping_id')
				new_state = P.get('new_state')
				cur.execute(sql_update.format(new_state, shipping_id))
				conn.commit()
			cur.execute("""SELECT s.id,
					s.uploaded,
					s.xlsfile,
					s.count,
					s.status,
					CONCAT_WS(', ', u.nachname, u.vorname) AS username
				FROM Shippings s
					INNER JOIN ShippingRequests sr ON sr.id = s.shippingrequestid
					LEFT JOIN users u ON sr.uid=u.uid
				WHERE sr.ContactId = {uid} ORDER BY s.uploaded ASC""".format(**session))
			data = []
			D = data.append
			style = "even"
			for row in cur:
				if style == "even":
					style = "odd"
				else:
					style = "even"
				resC = []
				C = resC.append
				C("""<select class="state-select" name="state" shipping_id="{0}">""".format(row[0]))
				for state in ['raw', 'cooking', 'done']:
					s = messages['states'][lang][state]
					if row[4] == state:
						C("""<option value="{0}" selected="selected">{1}</option>""".format(state, s))
					else:
						C("""<option value="{0}">{1}</option>""".format(state, s))
				C("""</select>""")
				D('<tr class="{0} {1}">'.format(style, row[4]))
				D("""<td><a href="/download?fileName={2}&fileOption=tk_ct">{5}</a></td>
					<td><a href="/download?fileName={2}&fileOption=tk_ct">{2}</a></td>
					<td>{1}</td>
					<td>{3}</td>""".format(*row))
				D("""<td>{0}</td></tr>""".format("".join(resC)))
			cur.close()
			conn.close()
			result = render('templates/%s/admin/hochgeladeneSammellisten.pt' % lang, {'value': "".join(data)},
							request=request)
			# log.info('%s Result Hochgeladene Sammeltabellen:\n%r', __name__, result)
			response = Response(result)
			return response
	url = request.route_url('login')
	return HTTPFound(location=url)


@view_config(route_name='nutzer-verwaltung')
def nutzer_verwaltung_view(request):
	session = request.session
	conn = pymysql.connect(host=config['host'], port=config['port'],
						   user=config['user'], passwd=config['pw'], db=config['db'])
	if 'role' in session:
		if session['role'] is not None:
			if not 1 in session['role'] and not 2 in session['role']:
				url = request.route_url('dashboard')
				return HTTPFound(location=url)
			set_language(request)
			lang = get_language(request)
			cur = conn.cursor()
			if 2 in session['role'] and 1 not in session['role']:  # -- TK
				cur.execute("""SELECT
						ue2.uid,
						CONCAT_WS(', ', u.nachname, CONCAT(LEFT(u.vorname, 1), '.'),
						CONCAT_WS(' ', u.salutation, u.title)) AS name,
						u.mail,
						GROUP_CONCAT(DISTINCT e.name) AS expertise,
						GROUP_CONCAT(DISTINCT r.role),
						IF(u.status>0,'certified','pending') AS status,
						DATE_FORMAT(u.created, '%Y-%m-%d %T') AS created,
						IF(u.login IS NULL,'Never',DATE_FORMAT(u.login, '%Y-%m-%d %T')) AS login_date,
						IF(u.access IS NULL,'Never',DATE_FORMAT(u.access, '%Y-%m-%d %T')) AS access_date
					FROM UserExpertise ue1
						LEFT JOIN UserExpertise ue2 ON ue2.id_expertise=ue1.id_expertise
						LEFT JOIN Expertise e ON e.tid=ue2.id_expertise
						LEFT JOIN users u ON u.uid=ue2.uid
						LEFT JOIN UserRole ur ON ur.uid=ue2.uid
						LEFT JOIN Role r ON r.id = ur.rid
					WHERE ue1.uid={uid} AND ue2.uid!={uid}
						AND ur.rid=3
					GROUP BY ue2.uid
					ORDER BY u.nachname""".format(**session))
			else:  # -- Admin
				cur.execute("""SELECT
						u.uid,
						CONCAT_WS(', ', u.nachname, CONCAT(LEFT(u.vorname, 1), '.'),
						CONCAT_WS(' ', u.salutation, u.title)) AS name,
						u.mail,
						GROUP_CONCAT(DISTINCT e.name) AS expertise,
						GROUP_CONCAT(DISTINCT r.role),
						IF(u.status>0,'certified','pending') AS status,
						DATE_FORMAT(u.created, '%Y-%m-%d %T') AS created,
						IF(u.login IS NULL,'Never',DATE_FORMAT(u.login, '%Y-%m-%d %T')) AS login_date,
						IF(u.access IS NULL,'Never',DATE_FORMAT(u.access, '%Y-%m-%d %T')) AS access_date
					FROM users u
						LEFT JOIN UserExpertise ue2 ON ue2.uid=u.uid
						LEFT JOIN Expertise e ON e.tid=ue2.id_expertise
						LEFT JOIN UserRole ur ON ur.uid=u.uid
						LEFT JOIN Role r ON r.id = ur.rid
					GROUP BY u.uid
					ORDER BY u.nachname""")
			resA = []
			D = resA.append
			count = 0
			for row in cur:
				if count % 2 == 0:
					style = "even"
				else:
					style = "odd"
				D('<tr class="{0}">'.format(style))
				D("""<td><a href="/sammeln/userEdit?uid={0}">{1}</a></td>
					<td>{2}</td>
					<td>{3}</td>
					<td>{4}</td>
					<td>{5}</td>
					<td>{6}</td>
					<td>{7}</td>
					<td>{8}</td>
					</tr>""".format(*row))
				count += 1
			cur.close()
			conn.close()
			result = render('templates/%s/admin/userManagment.pt' % lang, {'data': "".join(resA)}, request=request)
			response = Response(result)
			return response
	url = request.route_url('login')
	return HTTPFound(location=url)


@view_config(route_name='upload_media')
def upload_media_view(request):
	session = request.session
	if 'role' in session and session['role'] is not None:
		if 4 not in session['role']:  # -- Newsman
			url = request.route_url('dashboard')
			return HTTPFound(location=url)
		if "uploadedfile" in request.POST and "uploadedfile" in request.POST:
			file_request = request.POST['uploadedfile']
			filename = file_request.filename.split('/')[-1].replace(' ', '_')
			inputFile = file_request.file
			file_to_save = "{0}.{1}".format(uuid.uuid4(), filename.split('.')[-1])
			filePath = os.path.join(config['homepath'], config['news']['media_directory'], file_to_save)
			outputFile = open(filePath, 'wb')
			inputFile.seek(0)
			while True:
				data = inputFile.read(2 << 16)
				if not data:
					break
				outputFile.write(data)
			outputFile.close()
			ret = """{{
				"original_filename": "{1}",
				"downloadUrl": "/{0}/{2}",
				"thumbUrl": "/{0}/{2}",
			}}""".format(config['news']['media_directory'], filename, file_to_save)
			return Response(ret.replace('\t', '').replace('\n', ' '))


def set_language(request):
	session = request.session
	if 'btnGerman' in request.POST:
		session['languange'] = 'de'
	elif 'btnEnglish' in request.POST:
		session['languange'] = 'en'


def get_language(request):
	session = request.session
	if 'languange' in session:
		if session['languange'] == 'de':
			return 'de'
		elif session['languange'] == 'en':
			return 'en'
	return 'de'
