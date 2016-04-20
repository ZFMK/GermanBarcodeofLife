from pyramid.response import Response
from pyramid.view import view_config
from pyramid.renderers import render
import pymysql
import re
import os

from html import unescape

from .vars import taxon_ids, messages, config, states

import logging
log = logging.getLogger(__name__)

grad_rex = re.compile(r'[A-Z°\']+')
dir_rex = re.compile(r'[EWNS]+')


def get_select_taxa(cur, lang, tax_id='None'):
    resC = []
    C = resC.append

    C('<select id="choiceTaxa{0}" name="choiceTaxa{1}" required="required">')
    if tax_id == 'None':
        C("""<option selected="selected" value="None">%s</option>""" % messages['results']['choose_taxa'][lang])

    sql_taxa = """SELECT t1.id, t1.taxon, t1.lft, t1.rgt
		FROM GBOL_Taxa t1
		WHERE t1.id IN ({0})
		ORDER BY t1.taxon""".format(taxon_ids)
    cur.execute(sql_taxa.replace('\n', ' ').replace('\t', ''))
    for row in cur.fetchall():
        if int(row[0]) == tax_id:
            C("""<option value="{0};{2};{3}" selected="selected">{1}</option>""".format(*row))
        else:
            C("""<option value="{0};{2};{3}">{1}</option>""".format(*row))
    C("""</select>""")

    return "".join(resC)


def get_select_states(lang, state_id='None'):
    resC = []
    C = resC.append

    C("""<select id="choiceState{0}" name="choiceState{1}" required="required">""")
    if state_id == 'None':
        C("""<option selected="selected" value="None">%s</option>""" % messages['results']['choose_states'][lang])

    for i in range(0, len(states[lang])):
        C("""<option value="{0}">{1}</option>""".format(i, states[lang][i]))
    C("""</select>""")

    return "".join(resC)


def _send_file_response(self, filepath):
    from paste.fileapp import FileApp
    user_filename = '_'.join(filepath.split('/')[-2:])
    file_size = os.path.getsize(filepath)

    headers = [('Content-Disposition', 'attachment; filename=\"' + user_filename + '\"'),
               ('Content-Type', 'text/plain'),
               ('Content-Length', str(file_size))]

    from paste.fileapp import FileApp
    fapp = FileApp(filepath, headers=headers)

    return fapp(request.environ, self.start_response)


def grad2decimal(value):
    return float(value.replace(',', '.').strip())
    v = value.replace('~', '').replace(',', '.').strip()
    m = grad_rex.search(v)
    if not m:
        return float(v)

    if '-' in v and v[0] != '-':
        v = v.split('-')[0]
    v = v.split('°')

    if len(v) == 1:
        [deg, sign] = v[0].split(' ')
        deg = float(deg)
        m = 0.0
        sec = 0.0
    else:
        deg = float(v[0])
        if dir_rex.search(v[1]):
            m = 0.0
            sec = 0.0
            sign = v[1]
        else:
            m = float(v[1].split("'")[0]) / 60.0
            residue = v[1].split("'")[1:]

            sec = 0.0

            if len(residue) > 2:
                sec = float(residue[0]) / 60 / 60
                sign = residue[2]
            elif len(residue) == 2:
                sec = float(residue[0])
                sign = residue[1]
            elif len(residue) == 1:
                sign = residue[0]
            else:
                sign = 'X'  # -- assume positive direction

    if sign in ('S', 'W'):
        sign = -1.0
    else:
        sign = 1.0

    return round((deg + m + sec) * sign, 5)


def dataSelect(uid, lang, field_ids, search_category, search_str, separator=','):
    sqlA = []
    sql = sqlA.append
    sql("SELECT s.id,")
    if uid > 0:
        sql("replace(g.lat, ',', '.') as center_x, replace(g.lon, ',', '.') as center_y, ")
    else:
        sql("replace(g.center_x, ',', '.'), replace(g.center_y, ',', '.'), ")
    sql("""COALESCE(s.taxon, t.taxon) AS taxon,
		p.taxon AS parenttaxon,
		gi.institute_short AS institute,
		(select
			group_concat(concat('"', d.field_id, '":"',
				if(d.field_id = 2, substr(d.term, 1,11), COALESCE(d.term,'')),'"')
				separator '{2}')
			FROM GBOL_Data2Specimen ds
				INNER JOIN GBOL_Data d ON d.id = ds.data_id
				INNER JOIN GBOL_Data_Fields f ON (f.id = d.field_id AND f.lang='{1}')
			 WHERE d.field_id IN ({0}) AND ds.specimen_id = s.id
		) AS data,
		COALESCE(sc.`name`,'') AS vernacular,
		IF(s.barcode>0, 1, 0) AS barcode
		FROM GBOL_Specimen s
			LEFT JOIN GBOL_Taxa t ON t.id = s.taxon_id
			LEFT JOIN GBOL_Taxa p ON p.id = t.parent_id
			LEFT JOIN GBOL_TaxaCommonNames sc ON (s.taxon_id=sc.taxon_id and sc.`code`='{1}')
			LEFT JOIN GBOL_Institutes gi ON gi.institute_id=s.institute_id
			LEFT JOIN GBOL_Geo g ON g.specimen_id = s.id""".format(",".join(field_ids), lang, separator))
    if search_category == "treeview":
        sql(""" WHERE t.id in (select p.id FROM GBOL_Taxa n, GBOL_Taxa p where n.id = {0}
			AND p.`lft` >= n.`lft` AND p.`lft` <= n.`rgt`)""".format(search_str))
    else:  # -- no category selected
        if search_category == '0' or search_category == "":
            if search_str != "":  # -- and search string
                sql("""LEFT JOIN (
					SELECT p.id FROM GBOL_Taxa n, GBOL_Taxa p
					WHERE p.`lft` >= n.`lft` AND p.`lft` <= n.`rgt`
						AND n.id IN (
							SELECT t.id FROM GBOL_Taxa t left join GBOL_TaxaCommonNames sc ON t.id=sc.taxon_id
							WHERE t.taxon LIKE '{1}' OR (sc.`name` LIKE '{1}' AND sc.`code`='{0}'))
					) AS tt ON tt.id = s.taxon_id
				LEFT JOIN (
					SELECT distinct s.id
						FROM GBOL_Data2Specimen ds inner join
							GBOL_Specimen s on ds.specimen_id = s.id inner join
							GBOL_Data d ON d.id = ds.data_id inner join
							GBOL_Data_Fields f ON (f.id=d.field_id AND f.lang='{0}') inner join
							GBOL_Institutes gi on s.institute_id=s.institute_id
						WHERE (d.term LIKE '%{1}%'
							OR gi.project_institute like '%{1}%'
							OR gi.project_name like '%{1}%'
							OR gi.institute_short like '%{1}%'
							OR gi.institute_name like '%{1}%')""".format(lang, search_str))
                if uid == 0:
                    sql(" AND f.restricted<1")
                sql(""") ss ON ss.id=s.id
				WHERE tt.id IS NOT NULL OR ss.id IS NOT NULL""")
        else:  # -- category selected
            if search_str == "":  # -- and no search string
                pass
            else:  # -- and search string
                if search_category == "19":
                    sql(""" LEFT JOIN (
						SELECT p.id FROM GBOL_Taxa n, GBOL_Taxa p
						WHERE p.`lft` >= n.`lft` AND p.`lft` <= n.`rgt`
							AND n.id IN (
								SELECT t.id FROM GBOL_Taxa t left join GBOL_TaxaCommonNames sc ON t.id=sc.taxon_id
								WHERE t.taxon LIKE '%{0}%' OR (sc.`name` LIKE '%{0}%' AND sc.`code`='{1}'))
					) ts ON ts.id=t.id WHERE ts.id IS NOT NULL""".format(search_str, lang))
                elif search_category == "22":
                    sql(""" WHERE gi.project_institute like '%{0}%'
						OR gi.project_name like '%{0}%'
						OR gi.institute_short like '%{0}%'
						OR gi.institute_name like '%{0}%'""".format(search_str, lang))
                else:
                    sql(""" LEFT JOIN (
						SELECT s.id
						FROM GBOL_Data2Specimen ds INNER JOIN
							GBOL_Specimen s ON ds.specimen_id = s.id INNER JOIN
							GBOL_Data d ON d.id = ds.data_id INNER JOIN
							GBOL_Data_Fields f ON (f.id=d.field_id AND f.lang='{0}')
						WHERE f.id = '{1}' AND d.term LIKE '%{2}%'
						""".format(lang, search_category, search_str))
                    if uid == 0:
                        sql(""" AND f.restricted<1""")
                    sql(""") ss ON ss.id=s.id WHERE ss.id IS NOT NULL""")
    sql(""" ORDER BY `taxon`""")
    return "".join(sqlA).replace('\t', ' ').replace('\n', '')


@view_config(route_name='ergebnisse')
def ergebnisse_view(request):
    session = request.session
    set_language(request)
    lang = get_language(request)
    uid = 0
    last_updated = ''
    if 'uid' in session:
        if session['uid'] is not None:
            uid = session['uid']

    conn = pymysql.connect(host=config['host'], port=config['port'],
                           user=config['user'], passwd=config['pw'], db=config['db'])
    cur = conn.cursor()
    resT = get_select_taxa(cur, lang)
    sql_last_update = """SELECT DATE_FORMAT(`date`, '%d.%m.%Y %H:%i:%s') FROM Sync_Transfer_Log"""
    cur.execute(sql_last_update)
    for row in cur.fetchall():
        last_updated = row[0]
    cur.close()
    conn.close()
    resS = get_select_states(lang)

    message = request.session.pop_flash()
    if len(message) < 1:
        result = render('templates/%s/ergebnisse/ergebnisse.pt' % lang, {'uid': uid, 'lan': lang, 'select_taxa': resT,
                                                                         'select_states': resS,
                                                                         'last_updated': last_updated}, request=request)
    else:
        message = message[0]
        result = render('templates/%s/ergebnisse/ergebnisse.pt' % lang, {'uid': uid, 'lan': lang, 'select_taxa': resT,
                                                                         'select_states': resS,
                                                                         'last_updated': last_updated,
                                                                         'message': message},
                        request=request)
    response = Response(result)
    return response


@view_config(route_name='fillOptions')
def fillOptions_view(request):
    resO = []
    O = resO.append
    conn = pymysql.connect(host=config['host'], port=config['port'],
                           user=config['user'], passwd=config['pw'], db=config['db'])
    cur = conn.cursor()

    uid = int(request.POST.get('user_id'))
    lan = request.POST.get('lan')
    sql = "SELECT id, field_name FROM GBOL_Data_Fields WHERE lang='{0}' AND " \
          "id NOT IN (2, 3, 11, 12, 15, 16, 17, 19, 20, 26, 27, 28)".format(lan)
    if uid == 0:
        sql += " and restricted != 1"
    cur.execute(sql)

    for row in cur:
        O("""<option value="{0}">{1}</option>""".format(row[0], row[1]))
    cur.close()
    conn.close()
    return Response("".join(resO))


@view_config(route_name='loadTreeView')
def loadTreeView_view(request):
    conn = pymysql.connect(host=config['host'], port=config['port'],
                           user=config['user'], passwd=config['pw'], db=config['db'])
    cur = conn.cursor()
    resA = []
    A = resA.append
    nodeid = request.POST.get('nodeid')
    lan = request.POST.get('lan')
    query = """SELECT t.taxon,
				t.id, t.parent_id,
				t.known,
				t.collected,
				t.barcode,
				t.collected_individuals,
				t.barcode_individuals, t.rgt - t.lft AS rank,
				if(sc.taxon_id IS NULL, '', sc.`name`) AS vernacular
			FROM GBOL_Taxa t
				LEFT JOIN GBOL_TaxaCommonNames sc ON (t.id=sc.taxon_id AND sc.`code`='{1}')
			WHERE lft IS NOT NULL AND parent_id = {0} ORDER BY t.taxon""".format(nodeid, lan)
    # log.debug('%s SQL Treeview:\n%s', __name__, query)
    try:
        cur.execute(query)
    except Exception as e:
        cur.close()
        conn.close()
        return Response(
            '{{"success": false, "text": "Error {1}", "node": {0}, "entries": []}}'.format(nodeid, e.args[0]))
    for row in cur:
        A('["{0}",{1},{2},{3},{4},{5},{6},{7},{8}, "{9}"]'.format(*row))

    cur.close()
    conn.close()
    return Response('{{"success": true, "node": {0}, "entries": [{1}]}}'.format(nodeid, ",".join(resA)))


# @view_config(route_name='getSpecimenGeoInfo', renderer='json')
@view_config(route_name='getSpecimenGeoInfo')
def getSpecimenGeoInfo_view(request):
    """Species			27
	Common Name			28
	Country				 7
	Bundesland			26
	Institute			22
	Catalogue-No.		 1
	Family
	"""
    conn = pymysql.connect(host=config['host'], port=config['port'],
                           user=config['user'], passwd=config['pw'], db=config['db'])
    cur = conn.cursor()
    search_str = request.POST.get('id')
    search_category = request.POST.get('category')
    uid = request.POST.get('user_id')
    lang = request.POST.get('lan')

    field_ids = ['7', '26', '1']
    no_results = {'de': "Es tut uns Leid, für das gesuchte Taxon haben wir noch kein Material in GBOL erhalten oder "
                        "das Taxon wird nicht für Deutschland geführt. Bitte wenden Sie sich bei Fragen gerne per Mail "
                        "an info@bol-germany.de.",
                  'en': "We are sorry, no entries for this taxon have been found. Either we did not get any specimens "
                        "for this taxon so far, or it is not listed on the target list for Germany. Please contact us "
                        "via info@bol-germany.de for any further inquiries."}
    geo_min_max = ['-180', '-90', '180', '90']
    geo_coords = []

    C = geo_coords.append
    resA = []
    A = resA.append
    resB = []
    B = resB.append

    sql = dataSelect(int(uid), lang, field_ids, search_category, search_str)
    cur.execute(sql)

    for row in cur:
        if row[1] is None or row[2] is None:
            A('{{"id": {0}, "coord":["", ""], "species": "{3}", "taxon":"{4}", "institute":"{5}", "data":{{{6}}}, '
              '"vernacular": "{7}", "barcode": "{8}"}}'.format(*row))
        else:
            try:
                a = grad2decimal(row[1])
                b = grad2decimal(row[2])
            except ValueError:
                A('{{"id": {0}, "coord":["", ""], "species": "{3}", "taxon":"{4}", "institute":"{5}", "data":{{{6}}}, '
                  '"vernacular": "{7}", "barcode": "{8}"}}'.format(*row))
            else:
                A('{{"id": {2}, "coord":["{0}", "{1}"], "species": "{5}", "taxon":"{6}", "institute":"{7}", '
                  '"data":{{{8}}}, "vernacular": "{9}", "barcode": "{10}"}}'.format(a, b, *row))
                C([a, b])

    if len(geo_coords) > 0:
        geo_min_max[0] = min(geo_coords, key=lambda item: (item[0]))[0]
        geo_min_max[1] = min(geo_coords, key=lambda item: (item[1]))[1]
        geo_min_max[2] = max(geo_coords, key=lambda item: (item[0]))[0]
        geo_min_max[3] = max(geo_coords, key=lambda item: (item[1]))[1]
    try:
        if geo_min_max[2] - geo_min_max[0] < 10:  # Is substraction of strings possible?
            geo_min_max[0] -= 3
            geo_min_max[2] += 3
        if geo_min_max[3] - geo_min_max[1] < 10:
            geo_min_max[1] -= 3
            geo_min_max[3] += 3
    except TypeError as e:
        log.warn('viewsAjax, getSpecimenGeoInfo, calculation of bounding box "geo_min_max": '
                 '%r\nError was: %r' % (geo_min_max, e))
    field_query = """SELECT id, field_name FROM GBOL_Data_Fields WHERE lang='{1}' AND
					 id IN (27, 20, 28, {0}, 22, 19) ORDER BY `order`""".format(",".join(field_ids), lang)
    cur.execute(field_query)
    for row in cur:
        B('[{0}, "{1}"]'.format(*row))

    cur.close()
    conn.close()

    if len(resA) == 0:
        text = '{{"success": false, "text": "{0}", "lang":"{1}", "entries": [], "bounds":[{3}], ' \
               '"fields": [{2}]}}'.format(no_results[lang], lang, ",".join(resB), ",".join(geo_min_max))
    else:
        text = '{{"success": true, "lang":"{0}", "entries": [{1}], "bounds":[{3}], ' \
               '"fields": [{2}]}}'.format(lang, ",".join(resA), ",".join(resB), ",".join([str(c) for c in geo_min_max]))

    return Response(text)


@view_config(route_name='csvExport')
def csvExport_view(request):
    import codecs
    conn = pymysql.connect(host=config['host'], port=config['port'],
                           user=config['user'], passwd=config['pw'], db=config['db'])
    cur = conn.cursor()
    search_str = request.POST.get('caption')
    search_category = request.POST.get('category')
    uid = int(request.POST.get('user_id'))
    lang = request.POST.get('lan')
    success = True

    # -- Get fields and names
    if uid > 0:  # logged in
        sqlDataFields = """SELECT id, field_name, category, `order` FROM `GBOL_Data_Fields`
                           WHERE lang="{0}" ORDER BY `order`""".format(lang)
    else:
        sqlDataFields = """SELECT id, field_name, category, `order` FROM `GBOL_Data_Fields`
                           WHERE lang="{0}" AND restricted<1 ORDER BY `order`""".format(lang)
    cur.execute(sqlDataFields)
    field_ids = []
    field_names = []
    for row in cur:
        field_names.append(row[1])
        field_ids.append(str(row[0]))

    f = []
    F = f.append
    if search_str != "":
        F(search_str.replace(' ', ''))
    if search_category == '0' or search_category == "":
        search_category = ""
    else:
        F(search_category.replace(' ', ''))

    filename = lang + "_".join(f) + ".txt"
    myFile = config['homepath'] + "/documents/download/" + filename

    fh = open(myFile, 'w')
    fd = fh.fileno()
    os.write(fd, codecs.BOM_UTF8)  # -- write utf8 byte order mark

    # -- Get the Data
    if uid > 0:  # barcode present if logged in
        sql = dataSelect(int(uid), lang, field_ids, search_category, search_str, '§')
    else:
        cleaned_field_ids = [i for i in field_ids if i != '20']
        sql = dataSelect(int(uid), lang, cleaned_field_ids, search_category, search_str, '§')

    cur.execute(sql)

    # -- Header
    headerRow = []
    H = headerRow.append
    for i in range(0, len(field_ids)):
        if field_ids[i] == '15':  # -- insert Coordinates before no. indivuals
            H("{0}".format(messages['coord'][lang]))
        H("{0}".format(field_names[i]))
    os.write(fd, bytes("\t".join(headerRow) + '\n', 'utf-8'))

    barcode_present = [unescape('&#x02717;'), unescape('&#x02714;')]  # -- 0 = not present, 1 = present
    # -- Body
    for row in cur:
        bodyRow = []
        B = bodyRow.append
        data = {}
        if row[6] is not None:
            # try:
            data = {e[0]: e[1] for e in [d.split(':', 1) for d in row[6].replace('"', '').split("§")]}
        # except IndexError as e:
        for i in xrange(0, len(field_ids)):
            if field_ids[i] == '15':  # -- insert Coordinates before no. indivuals
                if row[1] and row[2]:
                    B("{1};{2}".format(*row))
                else:
                    B("")
            try:  # -- value present?
                B("{0}".format(data[field_ids[i]]))
            except KeyError:
                if field_ids[i] == '19':  # -- insert parent Taxon
                    B("{4}".format(*row))
                elif field_ids[i] == '20':  # -- Barcode present?
                    B(barcode_present[row[8]])
                elif field_ids[i] == '27':  # -- Species
                    B("{3}".format(*row))
                elif field_ids[i] == '22' and row[5]:  # -- Institute
                    B("{5}".format(*row))
                else:
                    B("")
        if len(bodyRow) > 0:
            os.write(fd, bytes("\t".join(bodyRow) + '\n', 'utf-8'))
            success = True
    fh.flush()
    fh.close()

    if success:
        return Response('{{"success": true, "filename": "{}"}}'.format(filename))

    return Response('{{"success": false, "text": "{0}"}}'.format(messages['error'][lang]))


@view_config(route_name='autocomplete_statistics')
def autocomplete_statistics_view(request):
    conn = pymysql.connect(host=config['host'], port=config['port'],
                           user=config['user'], passwd=config['pw'], db=config['db'])
    cur = conn.cursor()
    taxa = []
    T = taxa.append
    sql_taxa = """SELECT t1.id, t1.taxon, t1.lft, t1.rgt
                  FROM GBOL_Taxa t1
                  WHERE t1.rank IN ('cl.', 'ord.','fam.')
                  ORDER BY t1.taxon"""
    cur.execute(sql_taxa)
    for row in cur.fetchall():
        T('{{"id": "{0}", "taxon": "{1}", "lft": "{2}", "rgt":"{3}"}}'.format(*row))
    ret = '[{0}]'.format(",".join(taxa))
    cur.close()
    conn.close()
    return Response(ret)


@view_config(route_name='get_statisticsDE')
def get_statisticsDE_view(request):
    conn = pymysql.connect(host=config['host'], port=config['port'],
                           user=config['user'], passwd=config['pw'], db=config['db'])
    cur = conn.cursor()
    data = []
    D = data.append
    data2 = []
    D2 = data2.append
    lang = request.POST.get('lang')
    if lang is None:
        lang = "de"
    if request.POST.get('choiceTaxaDE') != "not_chosen_ta":
        choice_taxa = request.POST.get('choiceTaxaDE')
        (choice_taxa, tax_lft, tax_rgt) = choice_taxa.split(';')

        sql = "SELECT taxon, known, collected, barcode FROM GBOL_Taxa WHERE id={0}".format(choice_taxa)
        sql2 = """SELECT t.id, (SELECT r.taxon FROM GBOL_Taxa r WHERE r.id = t.parent_id) AS family, t.taxon,
                  GROUP_CONCAT(DISTINCT d.term ORDER BY d.term) AS states
                  FROM GBOL_Taxa t
                      INNER JOIN GBOL_Specimen s ON s.taxon_id=t.id
                      INNER JOIN GBOL_Data2Specimen ds ON s.id=ds.specimen_id
                      INNER JOIN GBOL_Data d ON ds.data_id=d.id
                  WHERE t.rank='sp.' AND d.term IN ('Europa','Baden-Württemberg','Bayern','Berlin','Brandenburg',
                      'Bremen','Hamburg','Hessen','Mecklenburg-Vorpommern','Niedersachsen','Nordrhein-Westfalen',
                      'Rheinland-Pfalz','Saarland','Sachsen','Sachsen-Anhalt','Schleswig-Holstein','Thüringen')
                  AND t.lft>'{0}' AND t.rgt<'{1}'
                  GROUP BY t.id ORDER BY family""".format(tax_lft, tax_rgt)
        cur.execute(sql)
        for row in cur:
            total = row[1] - row[2]
            coll = row[2] - row[3]
            barc = row[3]
            D('"{0}": [["{4}", {1}], ["{5}", {2}], ["{6}", {3}]]'
              .format(row[0], total, coll, barc,
                      messages['ncoll'][lang], messages['nbar'][lang], messages['barc'][lang]))

        # pivottabelle
        if sql2 != "":
            cur.execute(sql2)
            for row in cur:
                D2('["{0}","{1}","{2}","{3}"]'.format(row[0], row[1], row[2], row[3]))
    ret = '{{"data":{{{0}}}, "data2":[{1}]}}'.format(",".join(data), ",".join(data2))
    cur.close()
    conn.close()
    return Response(ret)


@view_config(route_name='get_statisticsBL')
def get_statisticsBL_view(request):
    lang = get_language(request)
    conn = pymysql.connect(host=config['host'], port=config['port'],
                           user=config['user'], passwd=config['pw'], db=config['db'])
    cur = conn.cursor()
    data = []
    D = data.append
    data2 = []
    D2 = data2.append
    if lang is None:
        lang = "de"

    choosen_taxon = request.POST.get('choiceTaxaBL')
    if choosen_taxon != "None":
        (taxon_id, tax_lft, tax_rgt) = choosen_taxon.split(';')
        choosen_state_id = int(request.POST.get('choiceStateBL'))
        choosen_state = states['de'][choosen_state_id]

        sql = """SELECT x.taxon, count(x.c), SUM(x.barcode) FROM (
                    SELECT t1.id, t1.taxon, 1 AS c, s.barcode AS barcode
                    FROM GBOL_Taxa t2
                        INNER JOIN GBOL_Taxa t1 ON (t1.lft<t2.lft AND t1.rgt>t2.rgt)
                        INNER JOIN GBOL_Specimen s ON s.taxon_id=t2.id
                        INNER JOIN GBOL_Data2Specimen ds ON s.id=ds.specimen_id
                        INNER JOIN GBOL_Data d ON ds.data_id=d.id
                    WHERE t2.lft=t2.rgt-1 AND t1.id='{0}' AND d.term='{1}'
                    GROUP BY t2.id, t1.id) AS x""".format(taxon_id, choosen_state)
        sql2 = """SELECT x.id, x.family, x.taxon, count(x.c) AS count, SUM(x.barcode) AS barcodes FROM (
                    SELECT t.id, (SELECT r.taxon FROM GBOL_Taxa r WHERE r.id = t.parent_id) AS family,
                    t.taxon, 1 AS c, s.barcode AS barcode
                    FROM GBOL_Taxa t
                        INNER JOIN GBOL_Specimen s ON s.taxon_id=t.id
                        INNER JOIN GBOL_Data2Specimen ds ON s.id=ds.specimen_id
                        INNER JOIN GBOL_Data d ON (ds.data_id=d.id AND d.field_id=26)
                    WHERE t.rank='sp.' AND d.term='{0}' AND t.lft>'{1}' AND t.rgt<'{2}')
                    AS x GROUP BY x.id""".format(choosen_state, tax_lft, tax_rgt)
        sql3 = """SELECT t.id, (SELECT r.taxon FROM GBOL_Taxa r WHERE r.id = t.parent_id) AS family, t.taxon
                  FROM GBOL_Taxa t
                  WHERE t.collected='0' AND t.rank='sp.' AND t.lft>'{0}' AND t.rgt<'{1}'""".format(tax_lft, tax_rgt)
        cur.execute(sql)
        for row in cur:
            if row[1] == 0:
                D('')
            else:
                coll = row[1] - row[2]
                barc = row[2]
                D('"{0}": [["Collected", 0], ["{3}", {1}], ["{4}", {2}]]'
                  .format(row[0], coll, barc, messages['nbar'][lang], messages['barc'][lang]))
        # collected
        if sql2 != "":
            cur.execute(sql2)
            for row in cur:
                D2('["{0}","{1}","{2}","{3}","{4}"]'.format(row[0], row[1], row[2], row[3], row[4]))
        # not collected
        if sql3 != "":
            cur.execute(sql3)
            for row in cur:
                D2('["{0}","{1}","{2}","{3}","{4}"]'.format(row[0], row[1], row[2], '0', '0'))

    if data2 != "":
        ret = '{{"data":{{{0}}}, "data2":[{1}]}}'.format(",".join(data), ",".join(data2))
    else:
        ret = '{{"data":{{{0}}}}}'.format(",".join(data))
    cur.close()
    conn.close()
    return Response(ret)


@view_config(route_name='get_statisticsMI')
def get_statisticsMI_view(request):
    conn = pymysql.connect(host=config['host'], port=config['port'],
                           user=config['user'], passwd=config['pw'], db=config['db'])
    cur = conn.cursor()
    data = []
    D = data.append
    if request.POST.get('choiceTaxaMI') != "not_chosen_ta":
        choice_taxa = request.POST.get('choiceTaxaMI')
        (taxon_id, tax_lft, tax_rgt) = choice_taxa.split(';')

        sql = """SELECT t.id, (SELECT r.taxon FROM GBOL_Taxa r WHERE r.id = t.parent_id) AS family, t.taxon
                 FROM GBOL_Taxa t
                 WHERE t.collected='0' AND t.rank='sp.' AND t.lft>'{0}' AND t.rgt<'{1}'""".format(tax_lft, tax_rgt)
        cur.execute(sql)
        for row in cur:
            D('["{0}","{1}","{2}"]'.format(row[0], row[1], row[2]))
    ret = '{{"data":[{0}]}}'.format(",".join(data))
    cur.close()
    conn.close()
    return Response(ret)


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
