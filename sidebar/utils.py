from django.utils.importlib import import_module
from django.utils import simplejson
from django.http import HttpResponse
from django.conf import settings

from sidebar.models import Sidebar, SidebarWidget
from sidebar.forms import WidgetTitleForm, DefaultAdminForm

def form_to_json(form):
    """
    Convert form data (field name and value) to json format,
    in this format we store the data in the database.
    """

    form_data = {}
    for field in form:

        #if form data is an object (eg. ModelChoiceField), we take different
        #way to save
        if isinstance(form.cleaned_data[field.name], object) and getattr(form.cleaned_data[field.name],'id',''):
            obj = form.cleaned_data[field.name]
            form_data[field.name] = obj.id
        else:
            form_data[field.name] = form.cleaned_data[field.name]
    return simplejson.dumps(form_data)

def json_to_dict(json_data):
    """Convert json formated data to its original format"""
    return simplejson.loads(json_data)

def get_sidebar_widgets():
    """Get all available widgets."""

    widgets = []
    for widget_id in settings.AVAILABLE_SIDEBAR_WIDGETS:
        try:
            wgt = import_module('sidebar_widgets.%s' % widget_id)
            reload(wgt)
        except:
            pass
        else:
            widgets.append(wgt.sidebar_widget)
    return widgets


def get_widget_name(widget_id):
    """Get widget name from widget ID"""

    name = ''

    widgets = get_sidebar_widgets()
    for widget in widgets:
        if widget.id == widget_id:
            name = widget.name
            break

    return name


def add_widget(widget_id, sidebar_id):
    """Add widget to sidebar"""

    sidebar = None
    try:
        sidebar = Sidebar.objects.get(pk=sidebar_id)
    except Sidebar.DoesNotExist:
        return
    else:
        name = get_widget_name(widget_id)
        widget = SidebarWidget()
        widget.title = name
        widget.sidebar = sidebar
        widget.widget = widget_id
        widget.save()
        return True


def render_single_widget(widgets, widget_item):
    """Render a single widget and return the output"""

    widget = None

    for w in widgets:
        if w.id == widget_item.widget:
            widget = w
            break
    # If widget found, render it
    if widget:
        widget_data = widget_item.content
        try:
            widget_params = json_to_dict(widget_data)
        except:
            output = widget.render(widget_item.title, None)
        else:
            output = widget.render(widget_item.title, widget_params)
        return output

    return False


def render_widgets(widget_list):
    """
    Loop through widget_list and render each of them.
    and return all result at once.
    """

    widgets = get_sidebar_widgets()
    output = []

    for widget in widget_list:
        single_widget = render_single_widget(widgets, widget)
        if single_widget:
            output.append(single_widget)

    return u''.join(output)


def get_full_widget_data(widgets, widget_item):
    """Get full widget data"""

    widget = None
    for w in widgets:
        if w.id == widget_item.widget:
            widget = w
            break

    if widget:
        data = {}
        data['id'] = widget_item.id
        data['title'] = widget_item.title
        data['type'] = widget_item.widget

        data['title_form'] = WidgetTitleForm(
                                            initial={'widget_title': data['title']}
                                            )
        if widget.admin_form:
            try:
                initial=json_to_dict(widget_item.content)
            except:
                data['admin_form'] = widget.admin_form()
            else:
                data['admin_form'] = widget.admin_form(
                                            initial=initial
                                            )
        return data

    return False


def get_used_widgets(sidebar_id):
    """get full widgets data for current sidebar, to show in admin page."""

    widgets = get_sidebar_widgets()
    sidebar = None
    all_used_widget = []

    try:
        sidebar = Sidebar.objects.get(pk=sidebar_id)
    except Sidebar.DoesNotExist:
        pass
    else:
        widget_list = sidebar.sidebarwidget_set.all()
        widget_list = list(widget_list)

        for widget in widget_list:
            used_widget_data = get_full_widget_data(widgets, widget)
            if used_widget_data:
                all_used_widget.append(used_widget_data)

    return all_used_widget


def update_widget(request):
    """ Update single Widget """

    result = {}
    widgets = get_sidebar_widgets()
    widget_id = request.POST.get('widget_id', 0)

    try:
        widget_item = SidebarWidget.objects.get(pk=widget_id)
    except SidebarWidget.DoesNotExist:
        return result
    else:
        widget = None
        for w in widgets:
            if w.id == widget_item.widget:
                widget = w
                break
        if not widget:
            return result
        else:
            title_form = WidgetTitleForm(request.POST)
            #prepare widget admin form for validation
            if widget.admin_form:
                admin_form = widget.admin_form(request.POST)
            else:
                admin_form = DefaultAdminForm(request.POST)

            if title_form.is_valid() and admin_form.is_valid():
                widget_item.title = title_form.cleaned_data['widget_title']
                widget_item.content = form_to_json(admin_form)
                widget_item.save()
                result['status'] = 'success'
                result['title'] = title_form.cleaned_data['widget_title']
            else:
                error_fields = {}
                error_fields.update(title_form.errors)
                error_fields.update(admin_form.errors)
                result['error_fields'] = [field for field in error_fields]

    return result

def reorder_widgets(widgets):
    """Reorder widget positions"""

    widget_ids = widgets.split(',')
    count = 1
    #main loop to re-set menu order value
    for w_id in widget_ids:
        try:
            widget = SidebarWidget.objects.get(pk=w_id)
        except:
            pass
        else:
            widget.order = count
            widget.save()
            count += 1
    return

def delete_widget(widget_id):
    """Delete widget from"""

    try:
        widget = SidebarWidget.objects.get(pk=widget_id)
    except:
        return
    else:
        widget.delete()
        return

