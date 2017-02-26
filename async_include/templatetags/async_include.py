# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json

from django import template
from django.contrib.contenttypes.models import ContentType
from django.template import loader, Context
from django.utils.text import slugify
from django.core import serializers
from django.forms.models import model_to_dict

register = template.Library()


@register.simple_tag(takes_context=True)
def async_include(context, template_path, *args, **kwargs):
    t = loader.get_template('async_include/template_tag.html')

    replacements = {"template_path": template_path, "block_id": slugify(template_path), "context": {}}

    for context_object_name, context_object in kwargs.items():
        is_model_object = hasattr(context_object, "id") and hasattr(context_object.__class__, "__name__")
        if is_model_object:
            object_id = context_object.id
            model = context_object.__class__.__name__
            app_name = ContentType.objects.get_for_model(context_object).app_label
            replacements["context"][context_object_name] = {"type": "model", "id": object_id, "app_name": app_name, "model": model}
        else:
            replacements["context"][context_object_name] = {"type": "safe_value", "value": context_object}


    replacements["context"] = json.dumps(replacements["context"])

    return t.render(Context(replacements))
