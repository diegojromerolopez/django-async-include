# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import hashlib
import uuid

from .. import crypto
from .. import checksum

from django.conf import settings
from django import template
import jsonpickle
from django.contrib.contenttypes.models import ContentType
from django.db.models.query import QuerySet
from django.template import loader, Context
from django.utils.text import slugify
from django.core import serializers
from django.forms.models import model_to_dict


register = template.Library()


# Async include template tag. Prepares data to be sent to the server and loads the
# rendered template by using AJAX
@register.simple_tag(takes_context=True)
def async_include(context, template_path, *args, **kwargs):
    t = loader.get_template('async_include/template_tag.html')

    # Unique block id (uniqueness based on UUID)
    block_id = "{0}-{1}".format(slugify(template_path.replace("/", "-")), uuid.uuid4().urn[9:])

    replacements = {"template_path": template_path, "block_id": block_id, "context": {}}

    for context_object_name, context_object in kwargs.items():
        # For each passed parameter, it can be a model object or a safe value (string or number)
        is_model_object = hasattr(context_object, "id") and hasattr(context_object.__class__, "__name__")

        # We store a reference of the model object based on its model name, app and id
        # We will send this data to the view to load there this object
        if is_model_object:
            object_id = context_object.id
            model_name = context_object.__class__.__name__
            app_name = ContentType.objects.get_for_model(context_object).app_label
            model_object_as_str = "{0}-{1}-{2}".format(app_name, model_name, object_id)
            replacements["context"][context_object_name] = {
                "type": "model",
                "id": object_id,
                "app_name": app_name,
                "model": model_name,
                "__checksum__": checksum.make(model_object_as_str)
            }

        elif type(context_object) == QuerySet:
            model = context_object.model
            model_name = model.__name__
            app_name = ContentType.objects.get_for_model(model).app_label

            sql_query, params = context_object.query.sql_with_params()

            nonce, encrypted_sql, tag = crypto.encrypt(key=settings.SECRET_KEY[:16], data=sql_query)

            replacements["context"][context_object_name] = {
                "type": "QuerySet",
                "query": encrypted_sql.decode("latin-1"),
                "params": params,
                "nonce": nonce.decode("latin-1"),
                "tag": tag.decode("latin-1"),
                "app_name": app_name,
                "model": model_name,
            }

        # Safe values are sent "as is" to the view that will render the template
        else:
            context_object_as_str = "{0}".format(context_object)
            replacements["context"][context_object_name] = {
                "type": "safe_value",
                "value": context_object,
                "value_as_str": context_object_as_str,
                "__checksum__": checksum.make(context_object_as_str)
            }

    # Serialization of context that will be sent
    replacements["context"] = jsonpickle.dumps(replacements["context"])

    # Render the template of this template tag
    return t.render(Context(replacements))
