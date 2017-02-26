# django-async-include
Asynchronous inclusion of Django templates

# What's this?

This is a project to help the ajax load of chunks of HTML with minimal effort on the developer side,
providing an easy way to improve web-site experience for your users by minimizing perceived loading times.

# Requirements

This application has no extra Python package requirements.

Of course you will need [Django](https://www.djangoproject.com/) version 1.10 or newer. I have no tested in lower versions of Django but it
should work fine with versions from 1.8 to 1.9.

Having said that, this application needs [jQuery](https://jquery.com/) to fetch the templates. So make sure you have jquery loaded in your HEAD HTML section.

The easiest way of inclue jQuery in your project is by [loading it from a CDN](https://code.jquery.com/):

```html
<script
  src="https://code.jquery.com/jquery-3.1.1.min.js"
  integrity="sha256-hVVnYaiADRTO2PzUGmuLJr8BLUSjGIZsDYGmIJLv2b8="
  crossorigin="anonymous"></script>
```

Beware of the version of jQuery if you are using bootstrap or other framework that can't work with jQuery's last version.


# Installation

## Using pip

```sh
pip install django-async-include
```

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

```html
{% async_include "<path of the >" <object1_name>=<object1> <object2_name>=<object2> ... <objectN_name>=<objectN>  %}
```

## Examples

```html
{# Load the template and informs the board object is required for the included template  #}
{% async_include "boards/components/view/current_percentage_of_completion.html" board=board %}
```

# Author
Diego J. Romero López is a Software Engineer at intelligenia and can be contacted by email at diegojREMOVETHISromerolopezREMOVETHIS@gmail.com.

Remove REMOVETHIS to read the real email address.