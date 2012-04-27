from django.template import Context, Template
from django.template.loader import render_to_string
from django.utils.encoding import force_unicode

"""
IMPORTANT:
Sidebar Widget itself is not a django form widget, but a term of small block/pieces of
information that lives on various part of web page, could be display some
information or have specific functionality. Easily configured and re-ordered
with other widgets.

Yes, its maybe little bit confusing between Django form widget and sidebar widget.
but i have no other words to name or describes it :)

2012 - Eka Putra
"""

class SidebarWidget(object):
    """
    Base class for sidebar widget.
    Each sidebar widget must be subclass of this class.
    """
    admin_form = None
    template_text = ''
    template_file = ''

    def __init__(self, name, description):
        self.id = self.__class__.__name__
        self.name = force_unicode(name)
        self.description = force_unicode(description)

    def render(self, title, params=None):
        """
        Widget render method, rendering method based on template type
        template_text --> template that specified in the code itself.
        template_file --> template is a file.
        """
        params.update({'widget_title': title})
        
        output = ''
        # We need to anticipate if both template_text and template_file defined
        # So, return result of template_text as priority
        if self.template_text:
            template = Template(self.template_text)
            try:
                output = template.render(Context(params))
            except:
                pass
            else:
                return output

        if self.template_file:
            try:
                output = render_to_string(self.template_file, params)
            except:
                pass
            else:
                return output

        return output

sidebar_widget = None
"""
@variable : sidebar_widget

this variable must be used to declaring a new sidebar widget subclass.
without it, new sidebar widget will not be visible in Sidebar Admin page.
"""

