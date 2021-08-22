# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import jsonpickle

from . import checksum
from . import crypto
from django.apps import apps
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import translation
from django.views.decorators.csrf import csrf_exempt


# Return the template with the remote context replaced
@csrf_exempt
def get_template(request):

    # POST request is mandatory
    if request.method != 'POST':
        return HttpResponse(status=400)

    json_body = jsonpickle.loads(request.body.decode('utf-8'))
    path = json_body.get('path')

    # Remote context
    # The caller has sent the model objects and
    # safe values (strings, numbers, etc.) as a dict with
    # the app_labels, model and id
    context = json_body.get('context')

    # language
    language_code = json_body.get('language_code')

    replacements = {}

    # For each remote context value, we load it again
    for context_object_name, context_object_load_params in context.items():
        # Type of the value
        object_type = context_object_load_params['type']

        # If the value is a model, we load the model object and
        # include it in the template replacements
        if object_type == 'model':
            app_name = context_object_load_params['app_name']
            model_name = context_object_load_params['model']
            object_id = context_object_load_params['id']
            # Loading the model
            model = apps.get_model(app_name, model_name)
            # Loading the object and including it as a replacement
            model_object = model.objects.get(id=object_id)
            # Checking if JSON has been tampered
            model_object_as_str = '{0}-{1}-{2}'.format(
                app_name, model_name, object_id
            )
            if (
                context_object_load_params['__checksum__'] !=
                checksum.make(model_object_as_str)
            ):
                return HttpResponse(
                    status=403,
                    content='JSON tampering detected when loading object',
                    content_type='text/plain'
                )

            replacements[context_object_name] = model_object

        # If the value is a QuerySet we include it in the template replacements
        elif object_type == 'QuerySet':
            # Loading the model
            app_name = context_object_load_params['app_name']
            model_name = context_object_load_params['model']
            model = apps.get_model(app_name, model_name)
            params = context_object_load_params['params']
            nonce = context_object_load_params['nonce']
            tag = context_object_load_params['tag']

            try:
                # Decryption of the data
                raw_query = crypto.decrypt(
                    key=settings.SECRET_KEY[:16],
                    nonce=nonce,
                    encrypted_data=context_object_load_params['query'],
                    tag=tag
                )

                # Loading the object and including it as a replacement
                replacements[context_object_name] = model.objects.raw(
                    raw_query, params
                )
            except ValueError:
                pass

        # If the value is a safe value,
        # we include it in the template replacements
        elif object_type == 'safe_value':
            value = context_object_load_params['value']
            value_as_str = context_object_load_params['value_as_str']
            # Checking if JSON has been tampered
            if (
                context_object_load_params['__checksum__'] !=
                    checksum.make(value_as_str)
            ):
                return HttpResponse(
                    status=403,
                    content='JSON tampering detected when loading safe value '
                            'for attribute \'{0}\'. Value: \'{1}\''.format(
                                context_object_name, value_as_str
                            ),
                    content_type='text/plain'
                )

            # Including the safe value as a replacement
            replacements[context_object_name] = value

    # Activate the language
    translation.activate(language_code)

    # Render the template
    return render(request, path, replacements)
