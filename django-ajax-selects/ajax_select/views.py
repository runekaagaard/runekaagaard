
from ajax_select import get_lookup
from django.contrib.admin import site
from django.db import models
from django.http import HttpResponse


def ajax_lookup(request,channel):
    """ this view supplies results for both foreign keys and many to many fields """
    
    def empty_response(): return HttpResponse('') # suspicious
    def format_item(lookup_channel, item):
        itemf = lookup_channel.format_item(item)
        itemf = itemf.replace("\n","").replace("|","&brvbar;")
        return itemf
    
    # Get and check the request.
    if request.method == "GET":
        request_by_method = request.GET
    elif request.method == "POST":
        request_by_method = request.POST
    else: return empty_response()    
    if 'q' not in request_by_method and 'id' not in request_by_method:
        return empty_response()
    
    lookup_channel = get_lookup(channel)
    
    if 'q' in request_by_method:
        instances = lookup_channel.get_query(request_by_method['q'],request)
        results = []
        for item in instances:
            itemf = format_item(lookup_channel, item)
            resultf = lookup_channel.format_result(item)
            resultf = resultf.replace("\n","").replace("|","&brvbar;")
            results.append( "|".join((unicode(item.pk),itemf,resultf)) )
        return HttpResponse("\n".join(results))
    elif 'id' in request_by_method:
        instance = lookup_channel.get_query_by_id(request_by_method['id'],request)
        return HttpResponse(format_item(lookup_channel, instance))
    else:
        return empty_response()

def add_popup(request,app_label,model):
    """ present an admin site add view, hijacking the result if its the dismissAddAnotherPopup js and returning didAddPopup """ 
    themodel = models.get_model(app_label, model) 
    admin = site._registry[themodel]

    admin.admin_site.root_path = "/ajax_select/" # warning: your URL should be configured here. 
    # as in your root urls.py includes :
    #    (r'^ajax_select/', include('ajax_select.urls')),
    # I should be able to auto-figure this out but ...

    response = admin.add_view(request,request.path)
    if request.method == 'POST':
        if response.content.startswith('<script type="text/javascript">opener.dismissAddAnotherPopup'):
            return HttpResponse( response.content.replace('dismissAddAnotherPopup','didAddPopup' ) )
    return response

