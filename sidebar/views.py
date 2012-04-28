from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils import simplejson
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from sidebar.utils import add_widget, update_widget, reorder_widgets
from sidebar.utils import delete_widget, get_used_widgets

@login_required
def ajax_load_widgets(request):
    """load sidebar ajax"""

    if request.is_ajax():
        if request.method == 'POST':
            sidebar_id = request.POST.get('sidebar_id', 0)
            widgets = get_used_widgets(sidebar_id)

            return render_to_response(
                                'admin/sidebar/sidebar/widgets.html',
                                {'used_widgets': widgets},
                                context_instance = RequestContext(request)
                                )

@login_required
def ajax_add_to_sidebar(request):
    """ Add widget to sidebar """

    if request.is_ajax():
        if request.method == 'POST':
            widget = request.POST.get('widget','')
            sidebar = request.POST.get('sidebar', 0)
            result = add_widget(widget, int(sidebar))
            if result:
                return HttpResponse(
                                simplejson.dumps({'status':'1'}),
                                content_type='application/javascript; charset=utf-8;')
            else:
                return HttpResponse(
                                simplejson.dumps({'status':'0'}),
                                content_type='application/javascript; charset=utf-8;')
                                
@login_required
def ajax_update_widget(request):
    """ Update single widget """

    if request.is_ajax():
        if request.method == 'POST':
            result = update_widget(request)
            return HttpResponse(
                            simplejson.dumps(result),
                            content_type='application/javascript; charset=utf-8;')
                            
@login_required
def ajax_reorder_widget(request):
    """ Reorder widget position """

    if request.is_ajax():
        if request.method == 'POST':
            widgets = request.POST.get('order','')
            if widgets:
                reorder_widgets(widgets)
            return HttpResponse(simplejson.dumps({'status':'success'}),
                                content_type='application/javascript; charset=utf-8;')
                                
@login_required
def ajax_delete_widget(request):
    """ Delete single widget """

    if request.is_ajax():
        if request.method == 'POST':
            widget_id = request.POST.get('widget_id', 0)
            if widget_id:
                delete_widget(widget_id)
            return HttpResponse(simplejson.dumps({'status':'success'}),
                                content_type='application/javascript; charset=utf-8;')

