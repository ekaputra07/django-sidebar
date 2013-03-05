Usage
=====

1. **Add 'sidebar' into project INSTALLED_APPS settings**::

    #file: settings.py
        
    INSTALLED_APPS = (
        ...
        ...
        'sidebar',
    )

2. **Add sidebar urls into project urls**::

        #file urls.py
        urlpatterns = patterns('',
        ...
        ...
        url(r'sidebar/', include('sidebar.urls')),
        )
            
3. **Synchronize project database**::

    $ python manage.py syncdb

4. **Create a directory called 'sidebar_widgets' inside the project directory** 

   It is in the same directory as *manage.py* file, and **remember** to put an **\_\_init\_\_.py** in it so python can access its content.::

    .
    ..
    manage.py
    sidebar_widgets/
    
5. **Add a sidebar settings into 'settings.py'**

   This settings value will determine what *sidebar location* and *sidebar widget* are available.

   Each **sidebar location must have unique ID**, this id could be the position of itself on the page.

   And each widget is determined by its **filename without the extension**.
   ::

        # Specify the available sidebar location, example:
        # 'left' and 'right' is the location ID.
        
        AVAILABLE_SIDEBARS = (
            ('left', 'Left Sidebar'),
            ('right', 'Right Sidebar'),
        )
        
        # Specify the available sidebar widget, example:
        # 'promotional_image' is the ID of the widget, taken from its file name without the file extension.
        # the filename of 'promotional_image' widget is 'promotional_image.py'
        
        AVAILABLE_SIDEBAR_WIDGETS = (
            'promotional_image',
        )

6. **Create the widget**

   To create the widget, you must register the widget in the *AVAILABLE\_SIDEBAR\_WIDGETS* settings (described in the step #5 above). **Example :**

  If your sidebar widget named **promotional_image**, create a file inside the **sidebar_widgets** directory and name it **promotional_image.py**.
  ::

   sidebar_widgets/
   __init__.py
   promotional_image.py

   
  The widget *promotional_image.py* would look like this:
  ::

   from sidebar.base import SidebarWidget, sidebar_widget
   from django import forms
    
   TEMPLATE = """
   {{widget_title}}
   <div class="side_block">
   <img src="{{image}}"/>
   {{text|safe}}
   </div>
   """
        
   class TextForm(forms.Form):
       text = forms.CharField(widget=forms.Textarea)
       image = forms.CharField()
        
   class PromotionalImage(SidebarWidget):
       admin_form = TextForm
       template_text = TEMPLATE
        
   # register the Widget
   sidebar_widget = PromotionalImage('Promotional Image','Display a promotional image with text')

7. **Add a place for our sidebar in template**

   Open your template file where the sidebar will be rendered, and make a simple call to the sidebar tag:
   ::

        <!-- this is your template file. eg. index.html -->
        
        <div class="sidebar">

        {% load sidebar_tags %}
        {% get_sidebar 'left' %} or {% get_sidebar 'right' %}

        </div>

Now, start the server, go to Django administration page. On the Sidebars page, open (or create the sidebar if no yet created) the available sidebar and our widget will be available on the widgets list.