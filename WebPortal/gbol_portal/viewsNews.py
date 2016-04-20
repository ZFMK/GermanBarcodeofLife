from pyramid.response import Response
from pyramid.view import view_config
from pyramid.renderers import render
import pymysql
import subprocess
import os

from .vars import config, messages


@view_config(route_name='news')
def news_view(request):
    message = ""
    newscontent = ""
    post_id = 0
    i = 0
    lk = []
    set_language(request)
    lan = get_language(request)
    cancel = messages['news_reset'][lan]
    html = messages['news_reset_html'][lan]
    session = request.session
    create_news = False
    if 'role' in session and session['role'] is not None:
        if 4 in session['role']:  # -- Newsman
            create_news = True
    conn = pymysql.connect(host=config['host'], port=config['port'],
                           user=config['user'], passwd=config['pw'], db=config['db'])
    cur = conn.cursor()
    if create_news and (" Absenden " in request.POST.values() or " Send " in request.POST.values()):
        user_id = session['uid']
        replace = {"Ä": "&Auml;", "Ü": "&Uuml;", "Ö": "&Ouml;", "ß": "&szlig;", "ä": "&auml;",
                   "ü": "&uuml;", "ö": "&ouml;", "'": "\'"}  # Anführungszeichen?
        values = request.POST.get('content')
        for k, v in replace.items():
            values = values.replace(k, v)
        for l in request.POST.keys():
            lk.append(l)
        post_id = int(lk[1][4:])
        if values not in ('<h2><strong>Titel</strong></h2>\r\n\r\n<p>Inhalt</p>\r\n', '',
                          '<h2><strong>Title</strong></h2>\r\n\r\n<p>Content</p>\r\n'):
            if post_id == 0:
                values = (user_id, values, lan)
                try:
                    cur.execute("INSERT INTO News (`user_id`, `text`, `date`, `lang`) "
                                "VALUES ({0}, '{1}', current_date(), '{2}')".format(*values))
                except Exception as e:
                    message = "MySQL error: %r" % e
                else:
                    conn.commit()
                    message = messages['news_message_saved'][lan]
            else:
                values = (values, post_id)
                try:
                    cur.execute("UPDATE News SET `text`=%s WHERE id='%s'", values)
                except Exception as e:
                    message = "MySQL error: %r" % e
                else:
                    conn.commit()
                    message = messages['news_message_updated'][lan]
        else:
            message = messages['news_message_empty'][lan]
    sql = "SELECT id, user_id, `text`, date as date_sort, DATE_FORMAT(date, '%d.%m.%Y') as datum, lang " \
          "FROM News WHERE lang='" + lan + "' ORDER BY date_sort DESC"
    cur.execute(sql)
    news_template_editor = """
		<form method="post"><div id="news{0}" name="news">
			{2} {3}</div>
			<condition tal:condition="python:4 in request.session.get('role')">
				<div id="editbutton">
					<input type="submit" id="edit" name="edit{4}" value="{1}"/>
				</div>
			</condition>
		</form><br />
		<hr />"""
    for row in cur:
        if 'role' in session and session['role'] is not None and 4 in session['role']:
            newscontent += news_template_editor.format(i, messages['news_edit'][lan], row[4], row[2], row[0])
        else:
            newscontent += """<div id="news{0}" name="news">{1} {2}</div><br /><hr />""".format(i, row[4], row[2])
        i += 1
    if " Bearbeiten " in request.POST.values() or " Edit " in request.POST.values():
        for l in request.POST.keys():
            post_id = l[4:]  # edit0 <- 0, edit49 <-- 49 (id des postings in db)
        sql = "SELECT text FROM News WHERE id=" + post_id + ""
        cur.execute(sql)
        for row in cur:
            html = row[0]
        cancel = messages['news_cancel'][lan]
    else:
        post_id = 0
    cur.close()
    conn.close()
    if message == "":
        result = render('templates/' + str(lan) + '/news/news.pt', {'lan': lan, 'html': html,
                                                                    'newscontent': newscontent, 'post_id': post_id,
                                                                    'cancel': cancel}, request=request)
    else:
        result = render('templates/' + str(lan) + '/news/news.pt', {'message': message, 'lan': lan, 'html': html,
                                                                    'newscontent': newscontent, 'post_id': post_id,
                                                                    'cancel': cancel}, request=request)
    response = Response(result)
    return response


@view_config(route_name='publikationen')
def publikations_view(request):
    message = ""
    pubcontent = ""
    user_id = 0
    post_id = 0
    i = 0
    lk = []
    set_language(request)
    lan = get_language(request)
    if lan == 'en':
        cancel = "Reset"
        html = '<h3><strong>Titel</strong></h3><p>Inhalt <a class="ext" href="Insert link to article here">PDF</a></p>'
    else:
        cancel = "Zur&uuml;cksetzen"
        html = '<h3><strong>Title</strong></h3><p>Content ' \
               '<a class="ext" href="Link zum Artikel hier einsetzen">PDF</a></p>'
    session = request.session
    create_news = False
    if 'role' in session and session['role'] is not None:
        if 4 in session['role']:  # -- Newsman
            create_news = True
    if create_news and (" Absenden " in request.POST.values() or " Send " in request.POST.values()):
        replace = {"Ä": "&Auml;", "Ü": "&Uuml;", "Ö": "&Ouml;", "ß": "&szlig;", "ä": "&auml;", "ü": "&uuml;",
                   "ö": "&ouml;", "?": "&#063;", '"ext" href': ' "ext" target="_blank" href'}  # Anführungszeichen?
        values = request.POST.get('content')
        for k, v in replace.items():
            values = values.replace(k, v)
        for l in request.POST.keys():
            lk.append(l)
        post_id = int(lk[1][4:])
        if values not in ('<h3><strong>Titel</strong></h3>\r\n\r\n<p>Inhalt '
                          '<a class= "ext" target="_blank" href="Link zum Paper hier einsetzen">PDF</a></p>\r\n', '',
                          '<h2><strong>Titel</strong></h2><p>Inhalt '
                          '<a class="ext" href="Link zum Paper hier einfügen">PDF</a></p>'):
            conn = pymysql.connect(host=config['host'], port=config['port'],
                                   user=config['user'], passwd=config['pw'], db=config['db'])
            cur = conn.cursor()
            if 'username' in session:
                name = request.session.get('username')
            cur.execute("SELECT uid FROM users WHERE name = '" + name + "'")
            for row in cur:
                user_id = row[0]
            if post_id == 0:
                values = (user_id, values, lan)
                try:
                    cur.execute("INSERT INTO Publikationen (user_id, text, date, lang) "
                                "VALUES (%s, %s, current_date(), %s)", values)
                    conn.commit()
                    message = messages['pub_updated'][lan]
                except Exception as e:
                    message = "MySQL Fehler: %r" % e
            else:
                values = (values, post_id)
                try:
                    cur.execute("UPDATE Publikationen SET text=%s WHERE id='%s'", values)
                    conn.commit()
                    message = messages['pub_saved'][lan]
                except Exception as e:
                    message = "MySQL Fehler: %r" % e
            cur.close()
            conn.close()
        else:
            message = messages['pub_error'][lan]
    conn = pymysql.connect(host=config['host'], port=config['port'],
                           user=config['user'], passwd=config['pw'], db=config['db'])
    cur = conn.cursor()
    sql = "SELECT id, user_id, text, date as date_sort, DATE_FORMAT(date, '%d.%m.%Y') as datum, lang " \
          "FROM Publikationen WHERE lang='" + lan + "' ORDER BY date_sort DESC"
    cur.execute(sql)
    for row in cur:
        if 'role' in session and session['role'] is not None and 4 in session['role']:
            div1 = '<form method="post"><div id="pub'
            div2 = '" name="pub">{0} {1}</div><condition tal:condition="python: request.session.get(\'role\') ' \
                   'and request.session.role in [1,2]"><div tal:condition="python: request.session.get(\'role\') ' \
                   'and request.session.role in [1,2]" id="editbutton"><input type="submit" id="edit" ' \
                   'name="edit'.format(row[4], row[2])
            div3 = '" value=" Bearbeiten "></div></condition></form><br><hr>'
            pubcontent += div1 + str(i) + div2 + str(row[0]) + div3
        else:
            div1 = '<div id="pub'
            div2 = '" name="pub">{0} {1}</div><br><hr>'.format(row[4], row[2])
            pubcontent += div1 + str(i) + div2
        i += 1
    if " Bearbeiten " in request.POST.values() or " Edit " in request.POST.values():
        for l in request.POST.keys():
            post_id = l[4:]  # edit0 <- 0, edit49 <-- 49 (id des postings in db)
        sql = "SELECT text FROM Publikationen WHERE id=" + post_id + ""
        cur.execute(sql)
        for row in cur:
            html = row[0]
        if lan == 'en':
            cancel = "Cancel"
        else:
            cancel = "Abbrechen"
    cur.close()
    conn.close()
    if message == "":
        result = render('templates/' + str(lan) + '/news/publikationen.pt',
                        {'lan': lan, 'html': html, 'pubcontent': pubcontent, 'post_id': post_id,
                         'cancel': cancel}, request=request)
    else:
        result = render('templates/' + str(lan) + '/news/publikationen.pt',
                        {'message': message, 'lan': lan, 'html': html, 'pubcontent': pubcontent, 'post_id': post_id,
                         'cancel': cancel}, request=request)
    response = Response(result)
    return response


@view_config(route_name='filemanager')
def filemanager_view(request):
    cmd = os.path.join(config['homepath'], 'static/js/ckeditor/filemanager/connectors/php/filemanager.php')
    if 'mode' in request.GET:
        mode = request.GET.get('mode')
    if 'name' in request.GET:
        name = request.GET.get('name')
    if 'path' in request.GET:
        path = os.path.join(config['homepath'], request.GET.get('path'))
    if 'old' in request.GET:
        old = request.GET.get('old')
    if 'new' in request.GET:
        new = request.GET.get('new')
    if 'mode' in request.POST:
        mode = request.POST.get('mode')
    if 'currentpath' in request.POST:
        currentpath = request.POST.get('currentpath')
    if mode == 'addfolder':
        p = subprocess.Popen("php " + cmd + " " + mode + " " + name + " " + path, shell=True, stdout=subprocess.PIPE)
        json_result = p.communicate()[0]
    elif mode in ('getinfo', 'getfolder', 'delete', 'download', 'preview'):
        p = subprocess.Popen("php " + cmd + " " + mode + " " + path, shell=True, stdout=subprocess.PIPE)
        json_result = p.communicate()[0]
    elif mode == 'rename':
        p = subprocess.Popen("php " + cmd + " " + mode + " " + old + " " + new, shell=True, stdout=subprocess.PIPE)
        json_result = p.communicate()[0]
    elif mode == 'add':
        filename = request.POST['newfile'].filename
        inputFile = request.POST['newfile'].file
        filePath = os.path.join(config['homepath'], config['news']['media_directory'], filename)
        newFile = open(filePath, 'wb')
        inputFile.seek(0)
        while True:
            data = inputFile.read(2 << 16)
            if not data:
                break
            newFile.write(data)
        newFile.close()
        json_result = '<textarea>{{"Path":"{0}", "Name": "{1}", "Error": "", ' \
                      '"Code": 0}}</textarea>'.format(currentpath, filename)  # <-- from filemanager.class.php
    return Response(json_result)


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
