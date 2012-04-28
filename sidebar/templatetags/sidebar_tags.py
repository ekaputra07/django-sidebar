from django import template
register = template.Library()

from sidebar.utils import get_sidebar_widgets, render_widgets, get_used_widgets
from sidebar.models import Sidebar, SidebarWidget

@register.inclusion_tag('admin/sidebar/sidebar/sidebar_builder.html')
def sidebar_builder(object_id):
    """
    Sidebar Builder tags to use in django admin Sidebar manager.
    """

    data = {
        'sidebar_id': object_id,
        'available_widgets' : get_sidebar_widgets(),
        }

    return data

@register.simple_tag
def get_sidebar(position_id):
    """
    Tags to pull sidebar content(widgets) into the location where this tag
    was called.
    """
    sidebar = None
    try:
        sidebar = Sidebar.objects.get(position=position_id)
    finally:

        if sidebar:
            widgets = sidebar.sidebarwidget_set.all()
            widgets = list(widgets)
            return render_widgets(widgets)

        else:
            return ''

