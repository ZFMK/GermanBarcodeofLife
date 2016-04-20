from pyramid.response import Response
from pyramid.view import view_config
from pyramid.renderers import render


@view_config(route_name='wer-kann-mitmachen')
def wer_kann_mitmachen_view(request):
    set_language(request)
    lan = get_language(request)
    result = render('templates/' + str(lan) + '/mitmachen/wer-kann-mitmachen.pt', {}, request=request)
    response = Response(result)
    return response


@view_config(route_name='teilnahmeinfos')
def teilnahmeinfos_view(request):
    set_language(request)
    lan = get_language(request)
    result = render('templates/' + str(lan) + '/mitmachen/teilnahmeinfos.pt', {}, request=request)
    response = Response(result)
    return response


@view_config(route_name='vorteile')
def vorteile_view(request):
    set_language(request)
    lan = get_language(request)
    result = render('templates/' + str(lan) + '/mitmachen/vorteile.pt', {}, request=request)
    response = Response(result)
    return response


@view_config(route_name='verantwortung-der-sammler')
def verantwortung_der_sammler_view(request):
    set_language(request)
    lan = get_language(request)
    result = render('templates/' + str(lan) + '/mitmachen/verantwortung-der-sammler.pt', {}, request=request)
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
