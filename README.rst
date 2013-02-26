Django Sidebar
==============

Dynamic Sidebar creation for Django. Easily create and manage sidebar from Django Admin with drag and drop sidebar widget ordering.

Requirement
------------
Django 1.3+

Installation
------------
From pypi::

    $ pip install django-sidebar

or::

    $ easy_install django-sidebar

or clone from github::

    $ git clone git://github.com/ekaputra07/django-sidebar.git

or::

    $ cd django-sidebar
    $ sudo python setup.py install

Usage
-----
**1. Add 'sidebar' into project INSTALLED_APPS settings :**
::

    # file: settings.py
    
    INSTALLED_APPS = (
        ...
        ...
        'sidebar',
    )

**2. Synchronize project database :**::

    $ python manage.py syncdb

**3. Create a directory called 'sidebar_widgets' inside the project directory :**

It is in the same directory as *manage.py* file, and **remember** to put an empty **__init__.py** in it so python can access its content.::

    .
    ..
    manage.py
    sidebar_widgets/
    
**4. Add a sidebar settings into 'settings.py' :**

This settings value will determine what **sidebar location** and **sidebar widget** are available.


Each **sidebar location must have unique ID**, this id could be the position of itself on the page.

And each widget is determined by its **filename without the extension**.::

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

**5. Create the sidebar widget**

To create widget, you must register the widget in the *AVAILABLE\_SIDEBAR\_WIDGETS* settings (described in the step #4 above).

**Example :**

If your sidebar widget named **promotional_image**, create a file inside the **sidebar_widgets** directory and name it **promotional_image.py**.
::

    sidebar_widgets/
         __init__.py
         promotional_image.py

The widget *promotional\_image.py* would look like this::

    from sidebar.base import SidebarWidget, sidebar_widget
    from django import forms

    TEMPLATE = """
    {{widget_title}}
    <div class="side_block">
    {{text|safe}}
    </div>
    """
    
    class TextForm(forms.Form):
        text = forms.CharField(widget=forms.Textarea)
    
    class TextSidebarWidget(SidebarWidget):
        admin_form = TextForm
        template_text = TEMPLATE
    
    # register out Widget
    sidebar_widget = TextSidebarWidget('Text Widget','Display custom text or Html')

Now, start the server, go to Django administration page. On the Sidebars page, open (or create the sidebar if no yet created) the available sidebar and our widget will available on the widgets list. 
