"""
Changes to DB:
2015-04-23 - Indices for Fundorte search
ALTER TABLE `gbol-python`.`GBOL_Institutes`
	ADD INDEX `idx_project_institute` (`project_institute` ASC),
	ADD INDEX `idx_project_name` (`project_name` ASC),
	ADD INDEX `idx_institute_short` (`institute_short` ASC),
	ADD INDEX `idx_institute_name` (`institute_name` ASC);
ALTER TABLE `gbol-python`.`GBOL_Data_Fields`
	ADD INDEX `idx_lang` (`lang` ASC);
ALTER TABLE `gbol-python`.`GBOL_Specimen`
	DROP INDEX `idx_color` ;

***Reset User Data (except zfmk-tk):***
delete ue from UserExpertise ue left join users u on u.uid=ue.uid where u.uid not in (42);
truncate UserExpertise;
truncate UserExpertiseRequest;
truncate `ShippingRequests`;
delete rui FROM RelUserInstitution rui left join users u on rui.uid=u.uid where u.uid not in (42);
delete from users where uid not in (42);
insert into UserExpertise values (42,26793);
"""
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.renderers import render
import datetime
from passlib.hash import bcrypt_sha256
import subprocess
import os
import uuid
import math
import pudb

import pymysql

from .async_email import send_mail

from .vars import messages, config

from .odbc_transfer import Transfer_DWB as DWB, Transfer_CacheDB as CacheDB  # unsued

from .collection_sheet_write import writeExcelFile
from .collection_sheet_get_id import readTransactionId

import logging

log = logging.getLogger(__name__)


def _user_role(lang, role=[]):
    txt = {'de': {'1': 'Administrator', '2': 'Taxon-Koordinator', '3': 'Experte', '4': 'Redaktion', '5': 'Tester'},
           'en': {'1': 'Administrator', '2': 'Coordinator', '3': 'Expert', '4': 'Editor', '5': 'Tester'}}
    resA = []
    A = resA.append

    if role is None:
        role = ['3']
    for key in ['1', '2', '3', '4', '5']:
        val = txt[lang][key]
        if key in role:
            A('<input type="checkbox" name="role" value="{0}" checked="checked" />{1}<br />'.format(key, val))
        else:
            A('<input type="checkbox" name="role" value="{0}" />{1}<br />'.format(key, val))
    A('<br />')
    return "".join(resA)


def get_user_data(con, uid):
    # get name of user, username if name is None
    user_data = {}
    cur = con.cursor()
    sql = """SELECT CONCAT_WS(';', salutation, title, vorname, nachname) AS `name`,
                `name` AS username, mail, IFNULL(`street`,'') AS street,
                CONCAT_WS(' ', zip, city) AS city, country AS country
            FROM users WHERE uid = {0}""".format(uid)
    cur.execute(sql)
    row = cur.fetchone()
    user_data['name'] = ' '.join([e for e in row[0].split(';') if len(e) > 0])
    if len(user_data['name']) == 0:
        user_data['name'] = row[1]
    user_data['username'] = row[1]
    user_data['email'] = row[2]
    user_data['street'] = row[3]
    user_data['city'] = row[4]
    user_data['country'] = row[5]
    return user_data


def sql_clean(d):
    try:
        r = {}
        for key, value in d.items():
            if value is None:
                r[key] = 'NULL'
            else:
                try:
                    r[key] = '"%s"' % value.replace("\'", "'").replace("'", "\\\'").replace('"', '\\\"').replace('&',
                                                                                                                 'and')
                except AttributeError as e:
                    r[key] = value  # -- int
        return r
    except AttributeError as e:
        if d is None:
            r = 'NULL'
        else:
            try:
                r = '"%s"' % d.replace("\'", "'").replace("'", "\\\'").replace('"', '\\\"').replace('&', 'and')
            except AttributeError as e:
                r = d  # -- int
        return r


def fkt_clean(value):
    if isinstance(value, str) and len(value) == 0:
        return None
    if value is None:
        return None
    else:
        try:  # -- 0xf6 -> ö in iso8859-1
            s = value.strip()
            return '%s' % s
        except AttributeError as e:
            return value  # -- either None or int
        except UnicodeError as e:
            s = unicode(s, "ISO-8859-1")
            return '%s' % s
        else:
            return value


@view_config(route_name='dashboard')
def dashboard_view(request):
    session = request.session
    set_language(request)
    lang = get_language(request)
    if 'role' in session and session['role'] is not None:
        conn = pymysql.connect(host=config['host'], port=config['port'],
                               user=config['user'], passwd=config['pw'], db=config['db'])
        user_data = get_user_data(conn, session['uid'])
        conn.close()
        result = render('templates/%s/sammeln/dashboard.pt' % lang, {"uData": user_data['name']}, request=request)
        response = Response(result)
        return response
    url = request.route_url('login')
    return HTTPFound(location=url)


@view_config(route_name='regist')
def regist_view(request):
    session = request.session
    set_language(request)
    lang = get_language(request)
    form = {'pass1': '', 'pass2': '', 'name': '', 'title': '', 'salutation': '',
            'vorname': '', 'nachname': '', 'phone': '', 'mail': '', 'referenzen': '',
            'expertiseAngaben': '', 'expertise': 0, 'termsofuse': '', 'expertisename': ''}

    # -- Spam checkings: current time in microseconds since epoch for spam checkings
    import time
    ticks = time.time()

    msg = []
    success = True
    conn = pymysql.connect(host=config['host'], port=config['port'], user=config['user'], passwd=config['pw'],
                           db=config['db'])
    cur = conn.cursor()
    G = request.POST.get
    if 'op' in request.POST:
        p = request.POST
        if p.get('user-url') is not None and p.get('user-url') != '':  # -- must be empty
            msg.append(messages['robot'][lang])
            success = False
        if p.get('check') is not None and p.get('check') in session:
            form_ticks = session[p.get('check')]
            del session[p.get('check')]
            if ticks - form_ticks < 15.0:  # - form processed in less than 15 seconds -> spam!
                msg.append(messages['robot'][lang])
                success = False
        if success:
            for e in ('pass1', 'pass2', 'name', 'title', 'salutation', 'vorname', 'nachname',
                      'phone', 'mail', 'referenzen', 'expertiseAngaben', 'expertise', 'gbol_termsofuse'):
                form[e] = fkt_clean(p.get(e))
            form['lang'] = lang
            form['user_id'] = None
            if form['pass1'] != form['pass2']:
                msg.append(messages['pwd_unmatch'][lang])
                success = False
        if success and any([form['pass1'] is None, form['pass2'] is None, form['name'] is None,
                            form['vorname'] is None, form['nachname'] is None,
                            form['mail'] is None, form['referenzen'] is None,
                            form['expertise'] is '0', form['termsofuse'] is None]):
            msg.append(messages['required_fields'][lang])
            success = False
        if success:
            cur.execute("SELECT uid FROM users WHERE name = '{name}'".format(**form))
            form['user_id'] = cur.fetchone()
            if form['user_id'] is not None:
                msg.append(messages['username_present'][lang])
                success = False
                form['user_id'] = None
        if success:
            form['newpasswd'] = bcrypt_sha256.encrypt(form['pass1'])
            insert_user_sql = ["""INSERT INTO users (`name`, pass, mail, vorname,
                    nachname, language, passwd_drupal, salutation, `title`,
                    referenzen, expertiseAngaben, `status`, phone, `created`)
                VALUES({sql_name},'{newpasswd}',{sql_mail},{sql_vorname},
                    {sql_nachname},'{lang}', NULL, {sql_salutation},{sql_title},
                    {sql_referenzen}, {sql_expertiseAngaben}, '0', {sql_phone}, NOW())""",
                               """INSERT INTO UserExpertiseRequest(uid, id_expertise, RequestDate)
                    VALUES ({user_id}, '{expertise}', NOW())""",
                               """INSERT INTO UserRole (uid, rid)
                    VALUES ({user_id}, '3')"""]
            for e in ('name', 'title', 'salutation', 'vorname', 'nachname',
                      'phone', 'mail', 'referenzen', 'expertiseAngaben'):
                key = 'sql_%s' % e
                form[key] = sql_clean(form[e])
            try:
                i = 0
                for query in insert_user_sql:
                    q = query.replace('\t', '').replace('\n', ' ')
                    cur.execute(q.format(**form))
                    if i == 0:
                        form['user_id'] = conn.insert_id()
                    i += 1
            except Exception as e:
                msg.append('Error {}'.format(*e))
                conn.rollback()
                success = False
            else:
                conn.commit()
        """ 24.03.2015, PG: Removed sync of users (agents) between DWB and GBOL Webportal
        if success and config['dwb']['use_dwb']>0:  # -- write new user into DiversityWorkbench
            try:
                dwb = DWB()
                result = dwb.addAgentIntoDWB(loginName=form['name'], pw=form['pass1'], \
                    agentTitle=form['title'], givenName=form['vorname'], inheritedName=form['nachname'], \
                    phone=form['phone'], email=form['mail'], userId=form['user_id'])
            except Exception as e:
                msg.append('Could not connect to order processing system. Please try again later (%r)' % e)
                success = False
            else:
                success = result['success']
                if not success:
                    msg.append(result['msg'])
                """
        if success:
            # -- send email to user -- #
            cur.execute("""SELECT name FROM Expertise WHERE tid = {expertise}""".format(**form))
            row = cur.fetchone()
            if row is not None:
                form['expertisename'] = row[0]
                mail_to = form['mail']
                send_from = config['smtp']['sender']
                text = messages['reg_exp_mail_body'][lang].format(
                    **{k: form[k] for k in ('salutation', 'title', 'vorname', 'nachname', 'expertisename') if
                       k in form and k is not None})
                try:
                    if config['dwb']['use_dwb'] > 0:
                        send_mail(mail_to, send_from, messages['reg_exp_mail_subject'][lang], text)
                except Exception as e:
                    msg.append(
                        'Sorry, could not send confirmation mail to you. But your data have been saved. '
                        'Error was: {0}'.format(e))

                # -- send email to taxoncoordinator -- #
                cur.execute("""SELECT CONCAT_WS(' ',
                        salutation,
                        title,
                        u.vorname, u.nachname
                    ) AS `name`, u.mail
                    FROM users u
                        INNER JOIN UserRole ur ON ur.uid=u.uid
                        LEFT JOIN UserExpertise ue ON ue.uid = u.uid
                    WHERE ur.rid = 2 AND ue.id_expertise = {expertise}""".format(**form))
                row = cur.fetchone()
                if row is not None:
                    mail_to = row[1]
                    send_from = config['smtp']['sender']
                    header = "Neue GBoL Registrierung"
                    text = """{0},

                        {salutation} {title} {vorname} {nachname} hat sich für die Expertise {expertisename} angemeldet.
                        Bitte prüfen Sie die Angaben und zertifizieren Ihn anschließend.

                        Viele Grüße,

                        Ihr GBoL Webportal""".format(row[0], **form)
                else:
                    mail_to = "info"
                    send_from = config['smtp']['sender']
                    header = "Neue GBOL Registrierung"
                    text = """Liebes ZFMK TK Team,

                        {salutation} {title} {vorname} {nachname} hat sich für die Expertise {expertisename} angemeldet.

                        Dafür ist jedoch kein Taxonkoordinator eingetragen!

                        Bitte prüfen Sie die Angaben und zertifizieren Ihn anschließend.

                        Viele Grüße,

                        der Programmierer""".format(**form)
                if config['dwb']['use_dwb'] > 0:
                    send_mail(mail_to, send_from, header, text.replace('\t', ''))
            if len(msg) > 0:
                request.session.flash("<br />".join(msg))
            else:
                request.session.flash(messages['user_created'][lang])
            cur.close()
            conn.close()
            return HTTPFound(location=request.route_url('home'))
        if not success and 'user_id' in form and form['user_id'] is not None:
            SQL = ['DELETE FROM users WHERE Uid={user_id}',
                   'DELETE FROM UserExpertise WHERE uid!=={user_id}']
            cur = conn.cursor()
            for sql in SQL:
                cur.execute(sql.format(**form))
            conn.commit()

    form['check'] = bcrypt_sha256.encrypt(str(ticks))
    session[form['check']] = ticks

    cur.execute("SELECT tid, name FROM Expertise")
    expert = []
    if int(form['expertise']) == 0:
        expert.append('<option value="0" selected="selected">{0}</option>'.format(messages['pls_select'][lang]))
    for row in cur:
        if int(row[0]) == int(form['expertise']):
            expert.append('<option value="{0}" selected="selected">{1}</option>'.format(*row))
        else:
            expert.append('<option value="{0}">{1}</option>'.format(*row))
    cur.close()
    conn.close()
    if len(msg) > 0:
        result = render('templates/%s/sammeln/regist.pt' % lang,
                        {'expertises': "".join(expert), 'form': form, 'message': "<br />".join(msg)}, request=request)
    else:
        result = render('templates/%s/sammeln/regist.pt' % lang, {'expertises': "".join(expert), 'form': form},
                        request=request)
    response = Response(result)
    return response


@view_config(route_name='logout')
def logout_view(request):
    ses = request.session
    if ses['mask'] is not None and len(ses['mask']) > 0:
        lang = get_language(request)
        conn = pymysql.connect(host=config['host'], port=config['port'], user=config['user'], passwd=config['pw'],
                               db=config['db'])
        new_uid = ses['mask'].pop()
        loadUser(conn, new_uid, ses, lang, masq=False)
        url = request.route_url('dashboard')
    else:
        ses['vorname'] = None
        ses['nachname'] = None
        ses['role'] = None
        ses['uid'] = None
        ses['mask'] = []
        ses['new_users'] = 0
        ses['new_expertise'] = 0
        ses['shipping_requests'] = 0
        url = request.route_url('home')
    return HTTPFound(location=url)


def passwd_drupal(passwd):
    cmd = os.path.join(config['homepath'], 'password-hash.sh "' + passwd + '"')
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    tmp = p.communicate()[0]
    tmp = tmp[25:].replace(b'\n', b'')
    return tmp


def passwd_drupal_test(passwd, storedHash):
    cmd = os.path.join(config['homepath'], 'password-test.sh')
    p = subprocess.call([cmd, passwd, storedHash])
    return p == 1


def loadUser(conn, user_id, ses, lang, masq=False):
    cur = conn.cursor()
    sql = """SELECT u.`name`, u.vorname, u.nachname,
            GROUP_CONCAT(ur.rid) AS role, u.uid, IF(login IS NULL, 0, 1) AS login
        FROM users u
            LEFT JOIN UserRole ur ON ur.uid=u.uid
        WHERE u.`uid` = '{0}'""".format(user_id)
    cur.execute(sql)
    row = cur.fetchone()
    if row is not None:
        ses['username'] = row[0]
        ses['vorname'] = row[1]
        ses['nachname'] = row[2]
        if row[3] is not None:
            ses['role'] = [int(r) for r in row[3].split(',')]
        else:
            ses['role'] = None
        ses['uid'] = int(row[4])
        ses['new_users'] = 0
        ses['new_expertise'] = 0
        ses['shipping_requests'] = 0
        if 'mask' not in ses:
            ses['mask'] = []
    else:
        return {'message': messages['wrong_credentials'][lang]}
    if int(row[5]) == 0 and not masq:  # -- first login
        cur.execute("UPDATE users SET `login`=NOW() WHERE uid = '{0}'".format(user_id))
    conn.commit()
    cur.close()


def set_number_requests(conn, session):
    cur = conn.cursor()
    if 2 in session['role']:
        # -- get number od requests
        sql_select_user_expertise = ["""SELECT
                    SUM(IF(u1.`status` = '0', 1, 0)) AS new_users,
                    SUM(IF(u1.`status` = '1', 1, 0)) AS new_expertises
                FROM users u2
                    LEFT JOIN UserExpertise ue ON u2.uid=ue.Uid
                    LEFT JOIN UserExpertiseRequest uer ON ue.id_Expertise=uer.id_Expertise
                    LEFT JOIN users u1 ON u1.uid=uer.Uid
                    INNER JOIN UserRole ur ON ur.uid=u2.uid
                WHERE ur.rid IN (1,2) AND u2.uid = {uid}""",
                                     """SELECT COUNT(s.id) FROM Shippings s
                    INNER JOIN ShippingRequests sr ON sr.id = s.ShippingRequestId
                WHERE sr.ContactId = {uid} AND s.`status`='raw'"""]
        cur.execute(sql_select_user_expertise[0].format(**session))
        row = cur.fetchone()
        session['new_users'] = int(row[0])
        session['new_expertise'] = int(row[1])
        cur.execute(sql_select_user_expertise[1].format(**session))
        row = cur.fetchone()
        session['shipping_requests'] = int(row[0])
    cur.close()


@view_config(route_name='login')
def login_view(request):
    # -- auf status prüfen wenn status 1 dann weiter wenn status 0 nicht einloggen + meldung warten auf zertifizierung
    set_language(request)
    lang = get_language(request)
    message = ''
    session = request.session
    conn = pymysql.connect(host=config['host'], port=config['port'],
                           user=config['user'], passwd=config['pw'], db=config['db'])
    cur = conn.cursor()
    if 'op' in request.POST:
        userName = request.POST.get('name')
        passwd = request.POST.get('pass')
        cur.execute("SELECT passwd_drupal, pass, status, uid FROM users WHERE name = %s", [userName])
        row = cur.fetchone()
        if row is not None and row[0] is not None:
            if not passwd_drupal_test(passwd, row[0]):
                result = render('templates/%s/sammeln/login.pt' % lang,
                                {'message': messages['wrong_credentials'][lang]}, request=request)
                response = Response(result)
                return response
            newpasswd = bcrypt_sha256.encrypt(passwd)
            try:
                cur.execute("UPDATE users SET passwd_drupal = NULL, pass = %s WHERE name = %s", [newpasswd, userName])
            except Exception as e:
                message = 'An error occured while updating the user account: %r' % e
                request.session.flash(message)
            else:
                conn.commit()
        else:
            if row is not None and row[1] is not None:
                if not bcrypt_sha256.verify(passwd, row[1]):
                    result = render('templates/%s/sammeln/login.pt' % lang,
                                    {'message': messages['wrong_credentials'][lang]}, request=request)
                    response = Response(result)
                    return response
            else:
                result = render('templates/%s/sammeln/login.pt' % lang,
                                {'message': messages['wrong_credentials'][lang]}, request=request)
                response = Response(result)
                return response
        if int(row[2]) != 1:
            result = render('templates/%s/sammeln/login.pt' % lang, {'message': messages['still_locked'][lang]},
                            request=request)
            response = Response(result)
            return response
        loadUser(conn, row[3], session, lang)
    cur.close()
    if 'role' in session and session['role'] is not None:
        set_number_requests(conn, session)
        url = request.route_url('dashboard')
        return HTTPFound(location=url)

    conn.close()
    if len(message) > 0:
        result = render('templates/%s/sammeln/login.pt' % lang, {'message': message}, request=request)
    else:
        result = render('templates/%s/sammeln/login.pt' % lang, {}, request=request)
    response = Response(result)
    return response


@view_config(route_name='masqUser')
def masqUser_view(request):
    ses = request.session
    set_language(request)
    lang = get_language(request)
    if 'role' in ses and ses['role'] is not None:
        if 1 not in ses['role'] and 2 not in ses['role']:
            return {}
    if 'masq_uid' in request.POST:
        conn = pymysql.connect(host=config['host'], port=config['port'],
                               user=config['user'], passwd=config['pw'], db=config['db'])
        masq_uid = request.POST.get('masq_uid')
        if 'mask' not in ses:
            ses['mask'] = []
        ses['mask'].append(ses['uid'])
        loadUser(conn, masq_uid, ses, lang, masq=True)
    url = request.route_url('dashboard')
    return HTTPFound(location=url)


@view_config(route_name='masqUserList')
def masqUserList_view(request):
    ses = request.session
    conn = pymysql.connect(host=config['host'], port=config['port'],
                           user=config['user'], passwd=config['pw'], db=config['db'])
    cur = conn.cursor()
    if 'role' in ses and ses['role'] is not None:
        if 1 not in ses['role'] and 2 not in ses['role']:
            return {}
    q = request.GET.get('q')
    if 2 in ses['role'] and 1 not in ses['role']:  # -- TK
        cur.execute("""SELECT
                ue2.uid,
                CONCAT_WS(', ', u.nachname, CONCAT(LEFT(u.vorname, 1), '.'),
                CONCAT_WS(' ', u.salutation, u.title)) AS `name`
            FROM UserExpertise ue1
                LEFT JOIN UserExpertise ue2 ON ue2.id_expertise=ue1.id_expertise
                LEFT JOIN Expertise e ON e.tid=ue2.id_expertise
                LEFT JOIN users u ON u.uid=ue2.uid
                LEFT JOIN UserRole ur ON ur.uid=ue2.uid
            WHERE ue1.uid={uid} AND ue2.uid!={uid}
                AND ur.rid=3
                AND u.`status`>0
                AND (u.name LIKE '{0}%' OR u.vorname LIKE '{0}%' OR u.nachname LIKE '{0}%')
            GROUP BY ue2.uid
            ORDER BY u.nachname""".format(q, **ses))
    else:  # -- Admin
        cur.execute("""SELECT
                u.uid,
                CONCAT_WS(', ', u.nachname, CONCAT(LEFT(u.vorname, 1), '.'),
                CONCAT_WS(' ', u.salutation, u.title)) AS `name`
            FROM users u
                LEFT JOIN UserExpertise ue2 ON ue2.uid=u.uid
            WHERE u.`status`>0
                AND (u.name LIKE '{0}%' OR u.vorname LIKE '{0}%' OR u.nachname LIKE '{0}%')
            GROUP BY u.uid
            ORDER BY u.nachname""".format(q))
    resA = []
    D = resA.append
    for row in cur:  # -- [ { label: "Choice1", value: "value1" }, ... ]
        D('{{"value":{0}, "label":"{1}"}}'.format(*row))
    cur.close()
    conn.close()
    return Response('[{0}]'.format(",".join(resA)))


@view_config(route_name='versenden')
def versenden_view(request):
    session = request.session
    if 'role' in session and session['role'] is not None:
        set_language(request)
        lang = get_language(request)
        result = render('templates/%s/sammeln/sammeln-versenden.pt' % lang, {}, request=request)
        response = Response(result)
        return response
    url = request.route_url('login')
    return HTTPFound(location=url)


@view_config(route_name='sammeltabelle')
def sammeltabelle_view(request):
    """ called by '/sammeln/sammeltabelle-herunterladen' """
    session = request.session
    set_language(request)
    lang = get_language(request)
    if 'role' in session and session['role'] is not None:
        if lang == 'en':
            material_verbose = {'2': '2ml', '5': '5ml', 'x': 'Other'}
        else:
            material_verbose = {'2': '2ml', '5': '5ml', 'x': 'Sonstiges'}
        data = []
        D = data.append
        conn = pymysql.connect(host=config['host'], port=config['port'], user=config['user'], passwd=config['pw'],
                               db=config['db'])
        cur = conn.cursor()
        cur.execute("""SELECT sr.id, sr.count, sr.kindof,
                DATE_FORMAT(sr.requestdate, '%Y-%m-%d %T') AS requestdate,
                sr.xlsfile , e.`name` AS expertise
            FROM ShippingRequests sr
                LEFT JOIN Expertise e ON e.tid=sr.expertiseid
            WHERE sr.uid = {uid} ORDER BY sr.requestdate DESC""".format(**session))
        style = "even"
        for row in cur:
            if row[2] is None or row[2] == 'None':
                continue
            if style == "even":
                style = "odd"
            else:
                style = "even"
            D("""<tr class="{0}" data-id="{3}">
                <td>{8}</td><td>{4}</td><td>{2}</td><td>{6}</td>
                <td><a href="/download?fileOption=collectionsheet&fileName={7}" class="download-coll-sheet">{7}</a></td>
                </tr>""".format(style, messages['download'][lang], material_verbose[row[2]], *row))
        message = request.session.pop_flash()
        if len(message) < 1:
            result = render('templates/%s/sammeln/sammeltabelle-herunterladen.pt' % lang,
                            {"data": "".join(data).replace('\t', '')}, request=request)
        else:
            message = message[0]
            result = render('templates/%s/sammeln/sammeltabelle-herunterladen.pt' % lang,
                            {"data": "".join(data).replace('\t', ''), 'message': message}, request=request)
        response = Response(result)
        return response
    url = request.route_url('login')
    return HTTPFound(location=url)


def create_CollectionSheet(request, lang, params):
    #cmd = os.path.join(config['homepath'], 'collection_sheet_write.php')
    template_collection_sheet = config['collection_table']['template']


#    try:
#        templateFileName = os.path.join(config['homepath'], 'documents/download', template_collection_sheet)
#        targetFileName = os.path.join(config['homepath'], config['collection_table']['ordered'],
#                                      params['XlsFile'])
#        ret = subprocess.check_output([cmd,
#                                       templateFileName,
#                                       targetFileName,
#                                       str(params['FirstTubeId']),
#                                       str(params['LastTubeId']),
#                                       str(params['transactionKey']),
#                                       lang], universal_newlines=True)

    try:
        templateFileName = os.path.join(config['homepath'], 'documents/download', template_collection_sheet)
        targetFileName = os.path.join(config['homepath'], config['collection_table']['ordered'],
                                      params['XlsFile'])
        ret = writeExcelFile([templateFileName,
                              targetFileName,
                              str(params['FirstTubeId']),
                              str(params['LastTubeId']),
                              str(params['transactionKey']),
                              lang])

    except Exception as e:
        return {'success': False, 'msg': 'An error occured while writing the excel sheet: %r' % e}
    # url = request.route_url('sammeltabelle')
    # return HTTPFound(location=failed_url)
    if ret in (0, 255):
        return {'success': False, 'msg': 'An error occured while writing the excel sheet.'}
    # os.remove(targetFileName)
    # url = request.route_url('sammeltabelle')
    # return HTTPFound(location=failed_url)
    return {'success': True, 'msg': ''}


@view_config(route_name='material-anfordern')
def material_anfordern_view(request):
    session = request.session
    set_language(request)
    lang = get_language(request)
    if 'role' in session and session['role'] is not None:
        conn = pymysql.connect(host=config['host'], port=config['port'], user=config['user'], passwd=config['pw'],
                               db=config['db'])
        cur = conn.cursor()
        msg = []
        success = False
        user_id = (session['uid'])
        requestuser = get_user_data(conn, user_id)
        if lang == 'en':
            material_verbose = {'2': '2ml tubes', '5': '5ml tubes', 'x': 'Other (no tubes)'}
        else:
            material_verbose = {'2': '2ml Röhrchen', '5': '5ml Röhrchen', 'x': 'Sonstiges (keine Röhrchen)'}
        if 'op' in request.POST:
            form_material = request.POST.get("material")
            if request.POST.get("amount") != "":
                form_amount = int(request.POST.get("amount"))
            else:
                form_amount = ""
            form_group = request.POST.get("taxgroup")
            if form_material is None or form_amount == "" or form_group == "":
                msg.append(messages['order_info_missing'][lang])
                success = False
            else:
                size = 0
                number = 0
                if form_material == "2":
                    size = 2
                    number = 95 * form_amount
                elif form_material == "5":
                    size = 5
                    number = 36 * form_amount
                elif form_material == "x":
                    number = int(form_amount)
                start_tube_no = 1
                end_tube_no = 1
                now = datetime.datetime.now()
                trancKey = "{0}_{1}".format(user_id, str(now))
                trancKey = trancKey[:-7].replace(':', '').replace(' ', '_')
                form_group = form_group.split("_")
                if size == 2 or size == 5:
                    cur.execute("SELECT name FROM users WHERE uid = {0}".format(user_id))
                    row = cur.fetchone()
                    cur.execute("""SELECT i.`name`, i.Id AS id FROM users u
                        INNER JOIN RelUserInstitution ui ON ui.uid = u.uid
                        INNER JOIN Institution i ON i.id = ui.institutionId
                        INNER JOIN UserExpertise ue ON ue.uid = u.uid
                        INNER JOIN Expertise e ON e.tid = ue.id_Expertise
                    WHERE u.uid = {0} AND e.tid = {1}""".format(*form_group))
                    institut = cur.fetchone()
                    result = {}
                    try:  # - get bunch of GBOL-IDs from FIMS
                        cache = DWB()
                        result = cache.getSpecimenId(conn=conn, sizeOfSample=size, numberOfSample=number,
                                                     collectorName=str(row[0]), instituteID=institut[1],
                                                     expertiseID=form_group[1])
                    except Exception as e:
                        result['msg'] = 'Could not connect to order processing system. Please try again later (%r)' % e
                        success = False
                    else:
                        success = result['success']
                    if success:
                        data = result['data']
                        start_tube_no = int(data[0])
                        end_tube_no = int(data[1])
                    else:
                        msg.append(result['msg'])
                else:
                    end_tube_no = int(start_tube_no) + number - 1
                    success = True
                if end_tube_no < start_tube_no:
                    t = start_tube_no
                    start_tube_no = end_tube_no
                    end_tube_no = t
            if success:
                try:
                    params = {'transactionKey': trancKey,
                              'uid': user_id,
                              'KindOf': str(form_material),
                              'Count': str(number),
                              'ExpertiseId': str(form_group[1]),
                              'ContactId': str(form_group[0]),
                              'RequestDate': str(now).replace(" ", "/"),
                              'XlsFile': trancKey + ".xlsx",
                              'FirstTubeId': str(start_tube_no),
                              'LastTubeId': str(end_tube_no)}
                    keys = params.keys()
                    cols = ", ".join(k for k in keys)
                    values = ", ".join('"%s"' % params[k] for k in keys)
                    cur.execute("""INSERT INTO ShippingRequests ({0}) VALUES ({1})""".format(cols, values))
                    conn.commit()
                except Exception as e:
                    msg.append(
                        'An error occured during order processing: %r. '
                        'Order could not be saved into database!' % e.args)
                    success = False
                else:
                    success = True
            if success:  # -- create sheet
                result = create_CollectionSheet(request, lang, params)
                success = result['success']
                if not success:
                    msg.append(result['msg'])
            if success:  # -- send email
                msg.append(messages['order_success'][lang])
                cur.execute("""SELECT CONCAT_WS(' ',
                        salutation,
                        title,
                        vorname,
                        nachname) AS name, mail
                    FROM users WHERE uid = {0}""".format(form_group[0]))
                koordinator = cur.fetchone()
                cur.execute("SELECT name FROM Expertise WHERE tid = {1}".format(*form_group))
                expertisename = cur.fetchone()
                mail_to = koordinator[1]
                send_from = config['smtp']['sender']
                mail_subject = "GBOL - Bestellung von Versandmaterial"
                mail_body = messages['mail_req_body'].format(koordinator[0], now.strftime('%d %b. %Y - %T'),
                                                             material_verbose[form_material], number,
                                                             expertisename[0], start_tube_no, end_tube_no,
                                                             **requestuser)
                try:
                    if config['dwb']['use_dwb'] > 0:
                        send_mail(mail_to, send_from, mail_subject, mail_body.replace('\t', ''))
                except Exception as e:
                    msg.append(
                        'An error occured during order processing: %r. '
                        'Order could not be send to Taxon Coordinator!' % e.args)
                    success = False
                else:
                    success = True
        if not success:  # -- either order processing error or first call of this page
            addrTag = 0
            resO = []
            O = resO.append
            if requestuser['street'] == '' or requestuser['city'] == '' or requestuser['country'] == '':
                addrTag = 1
            addr = "{name}<br />{street}<br />{city}<br />{country}".format(**requestuser)
            cur.execute("""SELECT u.vorname, u.nachname, u.uid, e.tid, e.name, i.name, i.shortname
                FROM users u INNER JOIN RelUserInstitution ui ON ui.uid = u.uid
                    INNER JOIN Institution i ON i.id = ui.institutionId
                    INNER JOIN UserExpertise ue ON ue.uid = u.uid
                    INNER JOIN Expertise e ON e.tid = ue.id_Expertise
                WHERE e.tid IN (SELECT id_Expertise FROM UserExpertise WHERE uid = {0})""".format(user_id))
            rows = cur.fetchall()
            if len(rows) == 1:
                O("""<option selected="selected" value="{2}_{3}">{4}, {6} ({0} {1})</option>""".format(*rows[0]))
            else:
                resO.append(
                    """<option selected="selected" value="">- {0} -</option>""".format(messages['select'][lang]))
                for row in rows:
                    if len(row[4]) > 20:
                        taxon = str(row[4])[0:17] + '...'
                    else:
                        taxon = str(row[4])
                    O("""<option value="{3}_{4}">{0}, {7} ({1} {2})</option>""".format(taxon, *row))
        if len(msg) > 0:
            if not success:
                result = render('templates/%s/sammeln/versandmaterial-anfordern.pt' % lang,
                                {"addrTag": addrTag, "address": addr, "options": "".join(resO),
                                 "message": "<br/>".join(msg)}, request=request)
            else:
                request.session.flash("<br/>".join(msg))
                url = request.route_url('sammeltabelle')
                return HTTPFound(location=url)
        else:
            result = render('templates/%s/sammeln/versandmaterial-anfordern.pt' % lang,
                            {"addrTag": addrTag, "address": addr, "options": "".join(resO)}, request=request)
        response = Response(result)
        return response
    url = request.route_url('login')
    return HTTPFound(location=url)


@view_config(route_name='versandanschreiben')
def versandtanschreiben_view(request):
    """ upload collection sheet """
    session = request.session
    set_language(request)
    lang = get_language(request)
    msg = []
    if 'role' in session and session['role'] is not None:
        if 'op' in request.POST and len(str(request.POST['uploadedDoc'])) > 3:
            filename = request.POST['uploadedDoc'].filename
            inputFile = request.POST['uploadedDoc'].file
            count = request.POST['Number']
            conn = pymysql.connect(host=config['host'], port=config['port'], user=config['user'], passwd=config['pw'],
                                   db=config['db'])
            cur = conn.cursor()
            filePath = os.path.join(config['homepath'], config['collection_table']['filled'], filename)
            outputFile = open(filePath, 'wb')
            inputFile.seek(0)
            while True:
                data = inputFile.read(2 << 16)
                if not data:
                    break
                outputFile.write(data)
            outputFile.close()

            #cmd = os.path.join(config['homepath'], 'collection_sheet_get_id.php')
            try:
                trancKey = readTransactionId([filePath])
                #trancKey = subprocess.check_output([cmd, filePath], universal_newlines=True)
            except Exception as e:
                msg.append(
                    'An error occured: Please send your collection sheet to the taxon coordinator via email. (%r)' % e)
                os.remove(filePath)
                result = render('templates/%s/sammeln/versandanschreiben.pt' % lang, {"message": "<br />".join(msg)},
                                request=request)
                response = Response(result)
                return response
            try:
                transaction_id = int(trancKey)
            except ValueError as e:
                transaction_id = trancKey
            if transaction_id in (0, 255):
                msg.append(
                    'An error occured when reading excel sheet. Please send your '
                    'collection sheet to the taxon coordinator via email.')
                os.remove(filePath)
                result = render('templates/%s/sammeln/versandanschreiben.pt' % lang, {"message": "<br />".join(msg)},
                                request=request)
                response = Response(result)
                return response
            else:
                cur.execute(
                    "SELECT id, uid, expertiseid, contactid FROM ShippingRequests "
                    "WHERE transactionKey = '{0}'".format(transaction_id))
                row = cur.fetchone()
                if row is not None:
                    requestid = row[0]
                    cur.execute("""SELECT concat_ws(' ',
                            salutation, title, vorname, nachname) AS name
                        FROM users WHERE uid = '{1}'""".format(*row))
                    requestuser = cur.fetchone()
                    cur.execute("""SELECT concat_ws(' ',
                            salutation, title, vorname, nachname) AS name,
                            mail
                        FROM users WHERE uid = '{3}'""".format(*row))
                    coordinator = cur.fetchone()
                    cur.execute("SELECT name FROM Expertise WHERE tid = " + str(row[2]))
                    expertisename = cur.fetchone()
                    cur.execute("Select * from Shippings where ShippingRequestId = %s", requestid)
                    row = cur.fetchone()
                    if row is not None:
                        cur.execute("""Update Shippings set uploaded = %s,
                            xlsfile = %s, count = %s, Status = 'raw'
                            where shippingrequestid = %s""",
                                    [str(datetime.datetime.now()).replace(" ", "/"), filename, count, requestid])
                    else:
                        cur.execute("""INSERT INTO Shippings (ShippingRequestId,
                            Uploaded, XlsFile, Count, Status)
                            VALUES (%s,%s,%s,%s,'raw')""",
                                    [requestid, str(datetime.datetime.now()).replace(" ", "/"), filename, count])
                    conn.commit()
                    msg.append(messages['succ_upload'][lang])
                    mail_to = coordinator[1]
                    send_from = config['smtp']['sender']
                    header = "Hochgeladene Sammeltabelle"
                    text = """Hallo {0},

                        {1} hat eine Sammeltabelle für das\n
                        Taxon {2} hochgeladen.

                        Viele Grüße,

                        Ihr GBoL Team
                    """.format(coordinator[0], requestuser[0], expertisename[0])
                    if config['dwb']['use_dwb'] > 0:
                        send_mail(mail_to, send_from, header, text.replace('\t', ''))
                else:
                    msg.append(messages['err_upload'][lang])
                    os.remove(filePath)
            cur.close
            conn.close
        if len(msg) < 1:
            result = render('templates/%s/sammeln/versandanschreiben.pt' % lang, {}, request=request)
        else:
            result = render('templates/%s/sammeln/versandanschreiben.pt' % lang, {"message": "<br />".join(msg)},
                            request=request)
        response = Response(result)
        return response
    url = request.route_url('login')
    return HTTPFound(location=url)


@view_config(route_name='image_upload')
def image_upload_view(request):
    session = request.session
    set_language(request)
    if 'role' in session and session['role'] is not None:
        if 'op' in request.POST and len(str(request.POST['uploadedfile'])) > 3:
            filename = request.POST['uploadedfile'].filename
            inputFile = request.POST['uploadedfile'].file
            filePath = os.path.join(config['homepath'], config['news']['media_directory'], filename)
            outputFile = open(filePath, 'wb')
            inputFile.seek(0)
            while True:
                data = inputFile.read(2 << 16)
                if not data:
                    break
                outputFile.write(data)
            outputFile.close()
            inputFile.close()
            ret = '{{original_filename:"{0}", downloadUrl: "{1}", thumbUrl: ""}}'.format(filename, filePath)
            return Response(ret)
    url = request.route_url('login')
    return HTTPFound(location=url)


@view_config(route_name='webeditor')
def webeditor_view(request):
    session = request.session
    if 'role' in session and session['role'] is not None:
        set_language(request)
        lang = get_language(request)
        result = render('templates/%s/sammeln/webeditor.pt' % lang, {}, request=request)
        response = Response(result)
        return response
    url = request.route_url('login')
    return HTTPFound(location=url)


@view_config(route_name='versandanschreiben-anzeigen')
def versandtanschreiben_anzeigen_view(request):
    # called by versandanschreiben-anzeigen
    session = request.session
    set_language(request)
    lang = get_language(request)
    if 'role' in session and session['role'] is not None:
        data = []
        D = data.append
        count = 0
        conn = pymysql.connect(host=config['host'], port=config['port'], user=config['user'], passwd=config['pw'],
                               db=config['db'])
        cur = conn.cursor()
        cur.execute("""SELECT sr.transactionKey, sr.requestDate, s.uploaded, e.`name` AS expertise
            FROM ShippingRequests sr
                INNER JOIN Shippings s ON s.shippingrequestid = sr.id
                LEFT JOIN Expertise e ON e.tid=sr.expertiseid
            WHERE sr.uid = {uid} ORDER BY uploaded DESC""".format(**session))
        for row in cur.fetchall():
            if count % 2 == 0:
                style = "even"
            else:
                style = "odd"
            D('<tr class="{0}">'.format(style))
            D("""<td>{0}</td>
                <td>{3}</td>
                <td>{1}</td>
                <td>{2}</td>
                <td> <a href="/download?fileName={0}&fileOption=versandanschreiben">""".format(*row))
            D(messages['download'][lang])
            D("""</a></td></tr>""")
            count += 1
        cur.close()
        conn.close()
        result = render('templates/%s/sammeln/versandanschreiben-anzeigen.pt' % lang, {"data": "".join(data)},
                        request=request)
        response = Response(result)
        return response
    url = request.route_url('login')
    return HTTPFound(location=url)


@view_config(route_name='nutzer-editieren')
def nutzer_editieren_view(request):
    session = request.session
    set_language(request)
    lang = get_language(request)
    msg = []
    success = True
    admin = False
    conn = pymysql.connect(host=config['host'], port=config['port'],
                           user=config['user'], passwd=config['pw'], db=config['db'])
    cur = conn.cursor()

    if 'role' in session and session['role'] is not None:
        uid = session['uid']
        if 1 in session['role'] or 2 in session['role']:
            # user selected by admin
            if 'uid' in request.params:
                uid = int(request.params['uid'])
            admin = True

        # -- prefill `form` with the actual user data
        userDetails = []
        UD = userDetails.append
        cur.execute("""SELECT
                u.uid,
                IF(LENGTH(u.salutation)=0,NULL,u.salutation) AS salutation,
                IF(LENGTH(u.title)=0,NULL,u.title) AS title,
                GROUP_CONCAT(ur.rid) as role,
                u.`name`,
                u.pass,
                u.vorname,
                u.nachname,
                u.mail,
                IF(LENGTH(u.phone)=0,NULL,phone) AS phone,
                IF(LENGTH(u.street)=0,NULL,street) AS street,
                IF(LENGTH(u.zip)=0,NULL,zip) AS zip,
                IF(LENGTH(u.city)=0,NULL,city) AS city,
                IF(LENGTH(u.country)=0,NULL,country) AS country,
                u.referenzen, u.expertiseAngaben, u.public, u.termsofuse
            FROM users u
                INNER JOIN UserRole ur ON ur.uid=u.uid
            WHERE u.uid = {0}""".format(uid))
        columns = cur.description
        row = cur.fetchone()
        form = {columns[index][0]: value for index, value in enumerate(row)}
        for n in ('oldPw', 'pass1', 'pass2', 'expertise'):
            form[n] = None

        if 'op' in request.POST:
            G = request.POST.get
            R = request.POST.getall
            roles = []
            for e in ('oldPw', 'pass1', 'pass2', 'name', 'title', 'salutation', 'vorname', 'nachname',
                      'phone', 'mail', 'street', 'zip', 'city', 'country',
                      'referenzen', 'expertiseAngaben', 'expertise'):
                form[e] = fkt_clean(G(e))

            form['lang'] = lang
            if admin:
                roles = R('role')
            else:
                roles = form['role'].split(',')
            form['public'] = G('public')
            if form['public'] is None:
                form['public'] = 0

            if admin:
                # we have an admin here, don't need a passwd
                pass
            else:
                if form['oldPw'] is None:
                    msg.append(messages['edt_no_passwd'][lang])
                    success = False
                else:
                    if not bcrypt_sha256.verify(form['oldPw'], form['pass']):
                        msg.append(messages['edt_passwd_wrong'][lang])
                        success = False
            if success and form['pass1'] is not None and form['pass2'] is not None:
                if form['pass1'] == form['pass2']:
                    form['newpasswd'] = bcrypt_sha256.encrypt(form['pass1'])

                    """ 24.03.2015, PG: Removed sync of users (agents) between DWB and GBOL Webportal
                    if config['dwb']['use_dwb']>0:  # -- add user to DiversityWorkbench
                        try:
                            dwb = DWB()
                            result = dwb.addAgentIntoDWB(loginName=form['name'],pw=form['pass1'], \
                                agentTitle=form['titel'], givenName=form['vorname'], \
                                inheritedName=form['nachname'], phone=form['phone'],\
                                email=form['mail'], userId=uid)
                        except Exception as e:
                            msg.append('Could not connect to order processing system. Please try again later (%r)' % e)
                            success = False
                        else:
                            success = result['success']
                    """
                    if success:  # -- change password
                        try:
                            cur.execute("UPDATE users SET pass='{newpasswd}' WHERE uid='{0}'".format(uid, **form))
                        except Exception as e:
                            msg.append('Error {0}: {1}'.format(*e))
                            conn.rollback()
                            cur.close()
                            success = False
                        else:
                            conn.commit()
                    else:
                        msg.append(result['msg'])
                else:
                    msg.append(messages['edt_passwd_mismatch'][lang])
                    success = False
            if success:
                cur = conn.cursor()
                cur.execute("""UPDATE users SET
                    salutation = {salutation},
                    title = {title},
                    vorname = {vorname},
                    nachname = {nachname},
                    phone = {phone},
                    mail = {mail},
                    street = {street},
                    zip = {zip},
                    city = {city},
                    country = {country},
                    referenzen = {referenzen},
                    expertiseAngaben = {expertiseAngaben},
                    public = {public}
                    WHERE uid = {0}""".format(uid, **sql_clean(form)))
                conn.commit()

                if admin:
                    sql_role_delete = """DELETE FROM `UserRole` WHERE uid='{0}'"""
                    sql_role_insert = """INSERT INTO `UserRole` (`uid`,`rid`) VALUES {0}"""
                    s = []
                    for r in roles:
                        s.append('({uid}, {0})'.format(r, **form))
                    cur.execute(sql_role_delete.format(s[0][1:4]))
                    cur.execute(sql_role_insert.format(",".join(s)))
                    conn.commit()
                    msg.append(messages['edt_success'][lang])

                if form['expertise'] is not None:
                    exp_list = {}
                    cur.execute(
                        """INSERT INTO UserExpertiseRequest VALUES({0}, "{expertise}", now())""".format(uid, **form))
                    conn.commit()

                    cur.execute("""SELECT
                        CONCAT_WS(' ', salutation, title, vorname, nachname) AS req_user
                        FROM users WHERE uid = {0}""".format(uid))
                    exp_list['req_user'] = cur.fetchone()[0]

                    cur.execute("SELECT name FROM Expertise WHERE tid = {expertise}".format(**form))
                    exp_list['expertisename'] = cur.fetchone()[0]

                    cur.execute("""SELECT
                        CONCAT_WS(' ', u.salutation, u.title, u.vorname, u.nachname) AS tk_user, u.mail
                        FROM users u
                            INNER JOIN UserRole ur ON ur.uid=u.uid
                            LEFT JOIN UserExpertise ue ON ue.uid = u.uid
                        WHERE ur.rid = 2 AND ue.id_expertise = {expertise}""".format(**form))
                    for row in cur.fetchall():
                        exp_list['tk_user'] = row[0]
                        mail_to = row[1]
                        send_from = config['smtp']['sender']
                        header = messages['reg_exp_mail_subject'][lang]
                        text = messages['reg_exp_chg_mail_body'][lang].format(**exp_list)
                        try:
                            send_mail(mail_to, send_from, header, text)
                        except Exception as e:
                            msg.append('Message could not be send to user: %s. Error was: %r\n' % (form['name'], e))

        # -- All expertises the current user does not have or does not have applied for
        expertise = []
        E = expertise.append
        cur.execute("""SELECT DISTINCT tid, name
            FROM Expertise LEFT JOIN (
                    SELECT uid, id_expertise FROM UserExpertise WHERE uid = {0}
                ) ue ON ue.id_expertise = tid
                    LEFT JOIN (
                        SELECT uid, id_expertise FROM UserExpertiseRequest WHERE uid = {0}
                    ) uer ON uer.id_expertise = tid
                WHERE ue.uid IS NULL AND uer.uid IS NULL""".format(uid))
        for row in cur.fetchall():
            E('<option value="{0}">{1}</option>'.format(*row))

        # -- All expertises of current user
        userExpertise = []
        UE = userExpertise.append
        cur.execute(
            "SELECT name FROM Expertise LEFT JOIN UserExpertise ON tid = id_Expertise WHERE uid = {0}".format(uid))
        for row in cur.fetchall():
            UE("<li>{0} | ".format(*row))
            UE(messages['cert'][lang])
            UE("</li>")

        # -- All expertises the current user has applied for
        userExpertiseRequests = []
        UER = userExpertiseRequests.append
        cur.execute(
            "SELECT name FROM Expertise LEFT JOIN UserExpertiseRequest ON tid = id_Expertise WHERE uid = {0}".format(
                uid))
        for row in cur.fetchall():
            UER("<li>{0} | ".format(*row))
            UER(messages['subm'][lang])
            UER("</li>")

        cur.close()
        conn.close()
        if admin:
            form['role_html'] = _user_role(lang, form['role'])
        else:
            form['role_html'] = ""

        if len(msg) > 0:
            result = render('templates/%s/sammeln/userEdit.pt' % lang, {
                'user': form['name'],
                'expertisen': "".join(expertise),
                'expertisenRequest': "".join(userExpertiseRequests),
                'userExpertisen': "".join(userExpertise),
                'form': form,
                'message': "<br />".join(msg)
            }, request=request)
        else:
            result = render('templates/%s/sammeln/userEdit.pt' % lang, {
                'user': form['name'],
                'expertisen': "".join(expertise),
                'expertisenRequest': "".join(userExpertiseRequests),
                'userExpertisen': "".join(userExpertise),
                'form': form,
            }, request=request)
        response = Response(result)
        return response
    url = request.route_url('login')
    return HTTPFound(location=url)


@view_config(route_name='pw-forgot')
def pw_forgot_view(request):
    session = request.session
    set_language(request)
    lang = get_language(request)
    msg = []
    success = True
    if 'role' in session and session['role'] is not None:
        url = request.route_url('dashboard')
        return HTTPFound(location=url)
    if 'op' in request.POST:
        acc = request.POST.get('account')
        conn = pymysql.connect(host=config['host'], port=config['port'],
                               user=config['user'], passwd=config['pw'], db=config['db'])
        cur = conn.cursor()
        cur.execute("SELECT uid FROM users WHERE name = '{0}' OR mail = '{0}'".format(acc))
        uid = cur.fetchone()
        if uid is None:
            msg.append(messages['pwd_forgot_not_found'][lang])
            success = False
        else:
            u_uid = str(uuid.uuid3(uuid.NAMESPACE_DNS, str(uid[0])))
            try:
                cur.execute(
                    "INSERT INTO ForgotPw (uid, requestDate, requestLink, notUsed) "
                    "VALUES ('{0}', now(), '{1}', 1)".format(uid[0], u_uid))
            except Exception as e:
                msg.append('Error {0}: {1}'.format(*e))
                conn.rollback()
                success = False
            else:
                conn.commit()
        if success:
            user_data = get_user_data(conn, uid[0])
            cur.close()
            conn.close()
            send_from = config['smtp']['sender']
            mail_subject = messages['pwd_forgot_email_subject'][lang].format(user_data['name'])
            mail_body = messages['pwd_forgot_email_body'][lang].format(user_data['name'], config['hosturl'],
                                                                       u_uid, user_data['username'])
            send_mail(user_data['email'], send_from, mail_subject, mail_body)
            request.session.flash(messages['pwd_forgot_sent'][lang])
            return HTTPFound(location=request.route_url('home'))
        else:
            cur.close()
            conn.close()
    if len(msg) > 0:
        result = render('templates/%s/sammeln/passwort-vergessen.pt' % lang, {'message': "<br />".join(msg)},
                        request=request)
    else:
        result = render('templates/%s/sammeln/passwort-vergessen.pt' % lang, {}, request=request)
    response = Response(result)
    return response


@view_config(route_name='pw-change')
def pw_change_view(request):
    session = request.session
    set_language(request)
    lang = get_language(request)
    msg = []
    if 'op' in request.POST:
        pw1 = request.POST.get('pass1')
        pw2 = request.POST.get('pass2')
        if pw1 != pw2 or pw1 == "" or pw2 == "":
            result = render('templates/%s/sammeln/change-password.pt' % lang,
                            {'message': messages['pwd_unmatch'][lang]}, request=request)
            response = Response(result)
            return response
        else:
            conn = pymysql.connect(host=config['host'], port=config['port'], user=config['user'], passwd=config['pw'],
                                   db=config['db'])
            cur = conn.cursor()
            try:
                cur.execute(
                    "UPDATE users SET pass='{0}' WHERE uid='{1}'".format(bcrypt_sha256.encrypt(pw1), session['uid']))
                cur.execute("UPDATE ForgotPw SET notUsed = 0 WHERE uid = {uid}".format(**session))
            except Exception as e:
                msg.append('Error {0}: {1}'.format(*e))
                conn.rollback()
                cur.close()
            else:
                conn.commit()
                cur.close()
                request.session.flash(messages['pwd_saved'][lang])
                url = request.route_url('home')
                return HTTPFound(location=url)
    if 'role' in session and session['role'] is not None:
        if len(msg) > 0:
            request.session.flash("<br />".join(msg))
        return HTTPFound(location=request.route_url('dashboard'))
    if 'link' in request.params:
        conn = pymysql.connect(host=config['host'], port=config['port'], user=config['user'], passwd=config['pw'],
                               db=config['db'])
        cur = conn.cursor()
        cur.execute("""SELECT uid, requestDate, notUsed FROM ForgotPw
			WHERE requestLink = '{link}' ORDER BY requestDate DESC""".format(**request.params))
        row = cur.fetchone()
        if row is not None:
            if row[2] == 0:
                msg.append(messages['pwd__link_used'][lang])
                request.session.flash("<br />".join(msg))
                return HTTPFound(location=request.route_url('home'))
            if (math.floor(((datetime.datetime.now() - row[1]).total_seconds()) / 3600)) >= 24:
                msg.append(messages['pwd__link_timeout'][lang])
                request.session.flash("<br />".join(msg))
                return HTTPFound(location=request.route_url('home'))
            session['uid'] = str(row[0])
            if len(msg) > 0:
                result = render('templates/%s/sammeln/change-password.pt' % lang, {'message': "<br />".join(msg)},
                                request=request)
            else:
                result = render('templates/%s/sammeln/change-password.pt' % lang, {}, request=request)
            response = Response(result)
            return response
    request.session.flash(messages['pwd__link_invalid'])
    url = request.route_url('home')
    return HTTPFound(location=url)


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
