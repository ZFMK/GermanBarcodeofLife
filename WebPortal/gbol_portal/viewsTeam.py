from pyramid.response import Response
from pyramid.view import view_config
from pyramid.renderers import render
import pymysql

from .vars import config


@view_config(route_name='institute')
def institute_view(request):
    set_language(request)
    lan = get_language(request)
    result = render('templates/' + str(lan) + '/team/institute.pt', {}, request=request)
    response = Response(result)
    return response


@view_config(route_name='organisation')
def organisation_view(request):
    set_language(request)
    lan = get_language(request)
    result = render('templates/' + str(lan) + '/team/organisation.pt', {}, request=request)
    response = Response(result)
    return response


@view_config(route_name='projekte')
def projekte_view(request):
    set_language(request)
    lan = get_language(request)
    result = render('templates/' + str(lan) + '/team/projekte.pt', {}, request=request)
    response = Response(result)
    return response


@view_config(route_name='experten')
def experten_view(request):
    set_language(request)
    lan = get_language(request)
    conn = pymysql.connect(host=config['host'], port=config['port'], 
                           user=config['user'], passwd=config['pw'], db=config['db'])
    cur = conn.cursor()
    cur.execute("""select distinct e.name,
        COUNT(ue.uid),
        GROUP_CONCAT(u.vorname ,' ' , u.Nachname SEPARATOR '<br>')
    from Expertise e left join UserExpertise ue on e.tid = ue.id_expertise inner join
        (
        select uid, vorname, nachname from users where role=3 and public=1
            union
        select uid, NULL, NULL from users where role=3 and public=0
        ) u on u.uid=ue.uid
    group by e.name
    order by e.name""")
    data = ""
    for row in cur:
        data += "<h3>" + row[0]
        data += "<small> " + str(row[1])
        if row[1] == 1:
            if lan == "de":
                data += " Experte"
            elif lan == "en":
                data += " expert"
        else:
            if lan == "de":
                data += " Experten"
            elif lan == "en":
                data += " experts"
        if str(row[2]) == 'None':
            data += "</small></h3><p>  </p>"
        else:
            data += "</small></h3><p> " + str(row[2]) + " </p>"
    result = render('templates/' + str(lan) + '/team/experten.pt', {'experten': data}, request=request)
    response = Response(result)
    return response


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
