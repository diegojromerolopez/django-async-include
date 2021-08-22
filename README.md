# django-async-include

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/diegojromerolopez/django-async-include/graphs/commit-activity)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/django-async-include.svg)](https://pypi.python.org/pypi/django-async-include/)
[![PyPI version gelidum](https://badge.fury.io/py/django-async-include.svg)](https://pypi.python.org/pypi/django-async-include/)
[![PyPI status](https://img.shields.io/pypi/status/django-async-include.svg)](https://pypi.python.org/pypi/django-async-include/)
[![PyPI download month](https://img.shields.io/pypi/dm/django-async-include.svg)](https://pypi.python.org/pypi/django-async-include/)
[![Maintainability](https://api.codeclimate.com/v1/badges/a795d65d98ec8e261709/maintainability)](https://codeclimate.com/github/diegojromerolopez/django-async-include/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/a795d65d98ec8e261709/test_coverage)](https://codeclimate.com/github/diegojromerolopez/django-async-include/test_coverage)

Asynchronous inclusion of Django templates

# What's this?

This is a project to help the ajax load of chunks of HTML with minimal effort on the developer side,
providing an easy way to improve web-site experience for your users by minimizing perceived loading times.

[This is the development repository](https://github.com/diegojromerolopez/django-async-include).

# How does it work?

The async_include template tag sends the context to the server using an AJAX request.

In the case of model objects, it sends the model, application and id. In the case of QuerySets,
it sends the encrypted parametrized SQL. Of course, in the case of safe values like strings, booleans or numbers
this data are sent "as is".

The receiver is a basic view of this application that renders the template with the received context and
returns it in the AJAX call.

# Requirements

This application only depends on [pycryptodome](https://github.com/Legrandin/pycryptodome) and [jsonpickle](https://jsonpickle.github.io/).

Of course, you will need [Django](https://www.djangoproject.com/) version 1.10 or newer.

## jQuery
No jQuery is required as of version 0.6.6.

## Fontawesome (optional)
[Fontawesome](http://fontawesome.io/) is the the-facto standard of font icons of our time. Include it in your project to see the spinner moving when loading the remote templates.

The easiest way to include it by using a CDN. For example, [bootstrap CDN](https://www.bootstrapcdn.com/fontawesome/)
(not affiliated, nor they endorse this project) is one of the most known.

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
from django.urls import path, include

urlpatterns = [
    # ...
    path(r'async_include/', include('async_include.urls', namespace="async_include")),
]
```

# Use

Load the **async_include** template tags at the top of your file and use the **async_include**
template tag as a replacement of the django include template tag.

You have to pass the local context explicitly to the async included templates, so you can pass all variables you
need in your included template as named parameters of the **async_include** template tag.

```html

{# Load the async_include template tag at the top of your template file #}
{% load async_include %}

{# Call the async_include template tag indicating what objects needs to replace it #}
{% async_include "<path of the >" <object1_name>=<object1> <object2_name>=<object2> ... <objectN_name>=<objectN>  %}
```

There is also a repository with a full example:
[django-async-include-example](https://github.com/diegojromerolopez/django-async-include-example).

## Warning and limitations

### Object dynamic attributes

No dynamic attribute will be passed to the templates given that only a reference to it is passed from the caller to the
included template callee. **Don't use dynamic attributes inside an async_included template**.

However, the full object will be passed to the async_included template, so you could call its methods and properties
without any problem.

### QuerySets

Each QuerySet is passed as encrypted SQL and converted on the receiver to a RawQuerySet.

Note that RawQuerySets have no __len__ method so length filter returns always 0.

To fix this we have implemented a new version of the length filter
that will be loaded in your template if you overwrite it.

```html
{% load async_included %}
```

Note that this templatetag file is **async_included**, ending in **ed**.

## Examples

### Passing an object 

```html
{% load async_include %}

{# .. #}

{# Load the template and informs the board object is required for the included template  #}
{% async_include "boards/components/view/current_percentage_of_completion.html" board=board %}
```

### Passing a QuerySet

```html
{% load async_include %}

{# .. #}

{% async_include "boards/components/view/summary.html" board=board member=member next_due_date_cards=next_due_date_cards %}
```


# Customization

## Spinner

Overwrite **async_include/spinner.html** template if you want to change the spinner from fontawesome one (default) by a
background image or an image. Otherwise, make sure you are loading fontawesome fonts.

Note that the spinner must have class **async_included-spinner**. Otherwise, the spinner behavior is going to be unpredictable.

### Show/Hide spinner

Including the optional parameter **spinner__visible=False** when calling the async_include template tag will not show the spinner block.

```html
{% load async_include %}

{# .. #}

{# Will not show the spinner #}
{% async_include "boards/components/view/last_comments.html" board=board spinner__visible=False %}
```

### Customize spinner template per async_include template tag call

Use the optional parameter **spinner__template_path** to set a different template path for a specific async_include 
call in your templates.

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

{# Will be replaced by <li></li> block instead of <div></div> #}
{% async_include "boards/components/view/last_comments.html" board=board html__tag='li' %}
```

## Block wrapper html tag class

Customize the wrapper class by passing **html__tag__class** optional parameter to the template tag.

```html
{% load async_include %}

{# .. #}

{# Will be replaced by <li></li> block instead of <div></div> #}
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

{# Update the last comments each 60 seconds #}
{% async_include "boards/components/view/last_comments.html" board=board request__frequency=60 %}
```

# Main author
Diego J. Romero-López is a Software Engineer based on Madrid (Spain).

This project is in no way endorsed or related in any way to my past or current employers.

Contact me by email at diegojREMOVETHISromerolopezREMOVETHIS@gmail.com.

# Contributors

- [Erik Telepovský](https://github.com/eriktelepovsky):
  - Bug fixes.
  - Modern mobile browser support.
  - PyPy configuration fixes.
  - Python3 support.
  - Multi-language support.
