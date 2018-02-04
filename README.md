# django-async-include
Asynchronous inclusion of Django templates

# What's this?

This is a project to help the ajax load of chunks of HTML with minimal effort on the developer side,
providing an easy way to improve web-site experience for your users by minimizing perceived loading times.

[This is the development repository](https://github.com/diegojromerolopez/django-async-include).

# How does it work?

The async_include template tag sends the context to the server using an AJAX request.

In the case of model objects, it sends the model, application and id. In the case of QuerySets,
it sends the encrypted parametriced SQL. Of course, in the case of safe values like strings, booleans or numbers
this data are send "as is".

The receiver is a basic view of this application that renders the template with the received context and
returns it in the AJAX call.

# Requirements

This application only depends on [pycryptodome](https://github.com/Legrandin/pycryptodome) and [jsonpickle](https://jsonpickle.github.io/).

Of course you will need [Django](https://www.djangoproject.com/) version 1.10 or newer. I have no tested in lower versions of Django but it
should work fine with versions from 1.8 to 1.9.

## jQuery
Having said that, this application needs [jQuery](https://jquery.com/) to fetch the templates. So make sure you have jquery loaded in your HEAD HTML section.

The easiest way of inclue jQuery in your project is by [loading it from a CDN](https://code.jquery.com/):

```html
<script
  src="https://code.jquery.com/jquery-3.1.1.min.js"
  integrity="sha256-hVVnYaiADRTO2PzUGmuLJr8BLUSjGIZsDYGmIJLv2b8="
  crossorigin="anonymous"></script>
```

Beware of the version of jQuery if you are using bootstrap or other framework that can't work with jQuery's last version.

## Fontawesome (optional)

[Fontawesome](http://fontawesome.io/) is the the-facto standard of font icons of our time. Include it in your project to see the spinner moving when loading the remote templates.

The easiest way to include it by using a CDN. For example, [bootstrap CDN](https://www.bootstrapcdn.com/fontawesome/) (not afiliated nor they endorse this project) is one of the most known.

Default waiting spinner uses fontawesome. You can overwrite **async_include/spinner.html** template if don't want to use
the default fontawesome style.

# Installation

## Using pip

[This package is in pypi](https://pypi.python.org/pypi/django-async-include) so you only have to write:

```sh
pip install django-async-include
```

to install it.

## Install master version

Include this code in your requirements.txt file:

```sh
-e git://github.com/diegojromerolopez/django-async-include.git#egg=django_async_include
```


## Installation in your Django project

Include the application in your project's **settings.py**:

```sh

INSTALLED_APPS = [
    ## ...
    'async_include',
]

```

## Include django-async-include URLs

Include the URLs of Django-Async-Include in your **urls.py** project in the namespace **async_include**:

```python
urlpatterns = [
    # ...
    url(r'^async_include/', include('async_include.urls', namespace="async_include")),
]
```

# Use

Load the **async_include** template tags at the top of your file and use the **async_include**
template tag as a replacement of the django include template tag.

You have to pass the local context explicitily to the async included templates, so you can pass all variables you
need in your included template as named parameters of the **async_include** template tag.

```html

{# Load the async_include template tag at the top of your template file #}
{% load async_include %}

{# Call the async_include template tag indicating what objects needs to replace it #}
{% async_include "<path of the >" <object1_name>=<object1> <object2_name>=<object2> ... <objectN_name>=<objectN>  %}
```

## Warning and limitations

### Object dynamic attributes

No dynamic attribute will be passed to the templates given that only a reference to it is passed from the caller to the
included template callee. **Don't use dynamic attributes inside an async_included template**.

Howewer, the full object will be passed to the async_included template, so you could call its methods and properties
without any problem.

### QuerySets

Each QuerySet is passed as encrypted SQL and converted on the receiver to a RawQuerySet.

RawQuerySet has no __len__ method so length filter returns allways 0.

To fix this we have implemented a new version of the length filter that will be loaded in your template if you overwrite

```html
{% load async_included %}
```

Note that this templatetag file is **async_included**, ending in **ed**.

## Examples

### Pasing an object 

```html
{% load async_include %}

{# .. #}

{# Load the template and informs the board object is required for the included template  #}
{% async_include "boards/components/view/current_percentage_of_completion.html" board=board %}
```

### Pasing a QuerySet

```html
{% load async_include %}

{# .. #}

{% async_include "boards/components/view/summary.html" board=board member=member next_due_date_cards=next_due_date_cards %}
```


# Customization

## Spinner

Overwrite **async_include/spinner.html** template if you want to change the spinner from fontawesome one (default) by a
background image or a image. Otherwise, make sure you are loading fontawesome fonts.

Note that the spinner must have class **async_included-spinner**. Otherwise spinner behavior is going to be impredictable.

### Show/Hide spinner

Including the optional parameter **spinner__visible=False** when calling the async_include template tag will not show the spinner block.

```html
{% load async_include %}

{# .. #}

{# Will not show the spinner #}
{% async_include "boards/components/view/last_comments.html" board=board spinner__visible=False %}
```

### Customize spinner template per async_include template tag call

Use the optional parameter **spinner__template_path** to set a diferrent template path for an specific async_include call in your templates.

```html
{% load async_include %}

{# .. #}

{# Will not show the spinner #}
{% async_include "boards/components/view/last_comments.html" board=board spinner__template_path="templates/comments/last_comments_spinner.html" %}
```

Remember the spinner tag should contain the **async_included-spinner** class.

## Block wrapper html tag

Wrapper tag is **div** and maybe you don't want that. Set **html__tag** optional  parameter to the name of the tag you need in that particular context.

Example:

```html
{% load async_include %}

{# .. #}

{# Will be replaced by <li></li> block insted of <div></div> #}
{% async_include "boards/components/view/last_comments.html" board=board html__tag='li' %}
```

## Block wrapper html tag class

Customize the wrapper class by passing **html__tag__class** optional parameter to the template tag.

```html
{% load async_include %}

{# .. #}

{# Will be replaced by <li></li> block insted of <div></div> #}
{# Class last_comments will be added to wrapper class #}
{% async_include "boards/components/view/last_comments.html" board=board html__tag='li' html__tag__class='last_comments' %}
```

## Request frequency

If do you want to make frequent requests, set request__frequency to the number of seconds you want
to make the requests.

Example:

```html
{% load async_include %}

{# .. #}

{# Upate the last comments each 60 seconds #}
{% async_include "boards/components/view/last_comments.html" board=board request__frequency=60 %}
```

# Main author
Diego J. Romero-López is a Software Engineer at [Drivies](https://www.driviesapp.com/).

This project is in no way endorsed or related in any way to my past or current employers.

Contact me by email at diegojREMOVETHISromerolopezREMOVETHIS@gmail.com.

# Contributors

- [Erik Telepovský](https://github.com/eriktelepovsky):
  - Bug fixes.
  - Modern mobile browser support.
  - PyPy configuration fixes.
  - Python3 support.
  - Multi language support.
