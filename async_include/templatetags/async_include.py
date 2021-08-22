# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import jsonpickle
import uuid

from .. import crypto
from .. import checksum

from django.conf import settings
from django import template
from django.contrib.contenttypes.models import ContentType
from django.db.models.query import QuerySet
from django.template import loader, Context
from django.utils.text import slugify
from django.utils.translation import get_language


register = template.Library()


# Unique template id
def get_unique_template_id():
    """
    Get an unique id for a template as a string.
    :return: an unique id for a template.
    """
    return uuid.uuid4().urn[9:].replace('-', '')


def slugify_template_path(template_path):
    """
    Slugify template path.
    Replaces everything that is not an alphanumeric
    character in the template path.
    :param template_path: string with the template path.
    :return: slug of the template path.
    """
    return slugify(template_path.replace('/', '_').replace('-', '_'))


# Async include template tag.
# Prepares data to be sent to the server and
# loads the rendered template by using AJAX
@register.simple_tag(takes_context=True)
def async_include(context, template_path, *args, **kwargs):
    t = loader.get_template('async_include/template_tag.html')

    # Slugified template path. It will be used in the block_id and
    # as a class of this block
    slugified_template_path = slugify_template_path(template_path)

    # Unique block id (uniqueness based on UUID)
    block_id = '{0}__{1}'.format(
        slugified_template_path, get_unique_template_id()
    )

    # Give the possibility to customize the HTML tag
    html__tag = kwargs.pop('html__tag', 'div')

    # HTML tag class
    html__tag__class = kwargs.pop('html__tag__class', slugified_template_path)

    # Shall we show a spinner?
    spinner__visible = kwargs.pop('spinner__visible', True)

    # Spinner template path
    spinner__template_path = kwargs.pop(
        'spinner__template_path', 'async_include/spinner.html'
    )

    # Recurrent requests
    request__frequency = kwargs.pop('request__frequency', 'once')

    replacements = {
        'template_path': template_path,
        'block_id': block_id,
        'html__tag': html__tag,
        'html__tag__class': html__tag__class,
        'spinner__visible': spinner__visible,
        'spinner__template_path': spinner__template_path,
        'request__frequency': request__frequency,
        'context': {}
    }

    for context_object_name, context_object in kwargs.items():
        # For each passed parameter,
        # it can be a model object or a safe value (string or number)
        is_model_object = (
            hasattr(context_object, 'id') and
            hasattr(context_object.__class__, '__name__')
        )

        # We store a reference of the model object based on its model name,
        # app and id. We will send this data to the view
        # to load there this object
        if is_model_object:
            object_id = context_object.id
            model_name = context_object.__class__.__name__
            app_name = (
                ContentType.objects.get_for_model(context_object).app_label
            )
            model_object_as_str = '{0}-{1}-{2}'.format(
                app_name, model_name, object_id
            )
            replacements['context'][context_object_name] = {
                'type': 'model',
                'id': object_id,
                'app_name': app_name,
                'model': model_name,
                '__checksum__': checksum.make(model_object_as_str)
            }

        elif type(context_object) == QuerySet:
            model = context_object.model
            model_name = model.__name__
            app_name = ContentType.objects.get_for_model(model).app_label

            sql_query, params = context_object.query.sql_with_params()

            nonce, encrypted_sql, tag = crypto.encrypt(
                key=settings.SECRET_KEY[:16], data=sql_query
            )

            replacements['context'][context_object_name] = {
                'type': 'QuerySet',
                'query': encrypted_sql.decode('latin-1'),
                'params': params,
                'nonce': nonce.decode('latin-1'),
                'tag': tag.decode('latin-1'),
                'app_name': app_name,
                'model': model_name,
            }

        # Safe values are sent as is to the view
        # that will render the template
        else:
            context_object_as_str = '{0}'.format(context_object)
            replacements['context'][context_object_name] = {
                'type': 'safe_value',
                'value': context_object,
                'value_as_str': context_object_as_str,
                '__checksum__': checksum.make(context_object_as_str)
            }

    # Serialization of context that will be sent
    replacements['context'] = jsonpickle.dumps(replacements['context'])

    # Pass language code
    replacements['language_code'] = get_language()

    # Render the template of this template tag
    try:
        # Django < 1.11
        return t.render(Context(replacements))
    except TypeError:
        # Django >= 1.11
        return t.render(replacements)
