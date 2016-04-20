import pymysql
from pyramid.response import Response
from pyramid.view import view_config

from .vars import config

import logging
log = logging.getLogger(__name__)


@view_config(route_name='searchUser')
def searchUser_view(request):
    conn = pymysql.connect(host=config['host'], port=config['port'],
                           user=config['user'], passwd=config['pw'], db=config['db'])
    cur = conn.cursor()
    value = request.POST.get('caption')
    column = request.POST.get('column')
    order = request.POST.get('order')
    sql = "SELECT u.uid, u.name, u.vorname, u.nachname, u.mail FROM users u "
    if value != "":
        sql = sql + " WHERE u.name like '%{0}%' or u.vorname LIKE '%{0}%' or u.nachname " \
                    "LIKE '%{0}%' OR u.mail LIKE '%{0}%'".format(value)
    sql = sql + " ORDER BY " + column + " " + order
    cur.execute(sql)
    data = ""
    count = 0
    for row in cur:
        if count % 2 == 0:
            style = "even"
        else:
            style = "odd"
        data += '<tr class="' + style + '">'
        data += "<td>" + str(row[0]) + "</td>"
        data += '<td> <a href="/sammeln/userEdit?uid='+str(row[0])+'">' + str(row[1]) + '</a></td>'
        data += "<td>" + str(row[2]) + "</td>"
        data += "<td>" + str(row[3]) + "</td>"
        data += "<td>" + str(row[4]) + "</td>"
        data += "<td></td>"
        data += "</tr>"
        count += 1
    cur.close()
    conn.close()
    return Response(data)

