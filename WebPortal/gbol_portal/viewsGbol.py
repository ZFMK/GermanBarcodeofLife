from pyramid.response import Response
from pyramid.view import view_config
from pyramid.renderers import render

@view_config(route_name='was-ist-gbol')
def was_ist_gbol_view(request):
    set_language(request)
    lan = get_language(request)
    result = render('templates/' + str(lan) + '/projekt/was-ist-gbol.pt', {}, request=request)
    response = Response(result)
    return response

@view_config(route_name='vision')
def vision_view(request):
    set_language(request)
    lan = get_language(request)
    result = render('templates/' + str(lan) + '/projekt/vision.pt', {}, request=request)
    response = Response(result)
    return response

@view_config(route_name='ziele')
def ziele_view(request):
    set_language(request)
    lan = get_language(request)
    result = render('templates/' + str(lan) + '/projekt/ziele.pt', {}, request=request)
    response = Response(result)
    return response

@view_config(route_name='anwendungsgebiete')
def anwendungsgebiete_view(request):
    set_language(request)
    lan = get_language(request)
    result = render('templates/' + str(lan) + '/projekt/anwendungsgebiete.pt', {}, request=request)
    response = Response(result)
    return response

@view_config(route_name='warum-dna-barcoding')
def warum_dna_barcoding_view(request):
    set_language(request)
    lan = get_language(request)
    result = render('templates/' + str(lan) + '/barcoding/warum-dna-barcoding.pt', {}, request=request)
    response = Response(result)
    return response

@view_config(route_name='was-ist-dna-barcoding')
def was_ist_dna_barcoding_view(request):
    set_language(request)
    lan = get_language(request)
    result = render('templates/' + str(lan) + '/barcoding/was-ist-dna-barcoding.pt', {}, request=request)
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
            #deutschen teil laden
            return 'de'
        elif session['languange'] == 'en':
            #englischen teil laden
            return 'en'
    return 'de'
