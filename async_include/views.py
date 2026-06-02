import json
from typing import Dict, Any

from . import checksum
from . import crypto
from django.apps import apps
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils import translation
from django.views.decorators.csrf import csrf_exempt


# Return the template with the remote context replaced
@csrf_exempt
def get_template(request: HttpRequest) -> HttpResponse:

    # POST request is mandatory
    if request.method != 'POST':
        return HttpResponse(status=400)

    json_body: Dict[str, Any] = json.loads(request.body.decode('utf-8'))
    path: Any = json_body.get('path')
    path_checksum: Any = json_body.get('path_checksum')

    # Verify template path signature to prevent arbitrary template loading (Defense in Depth)
    if not isinstance(path, str) or not isinstance(path_checksum, str):
        return HttpResponse(status=400, content='Invalid template path parameters', content_type='text/plain')

    if '..' in path or path.startswith('/'):
        return HttpResponse(status=400, content='Invalid template path traversal detected', content_type='text/plain')

    if path_checksum != checksum.make(path):
        return HttpResponse(
            status=403, content='JSON tampering detected when loading template path', content_type='text/plain'
        )

    # Remote context
    # The caller has sent the model objects and
    # safe values (strings, numbers, etc.) as a dict with
    # the app_labels, model and id
    context: Dict[str, Any] = json_body.get('context', {})

    # language
    language_code: Any = json_body.get('language_code')

    replacements: Dict[str, Any] = {}

    # For each remote context value, we load it again
    for context_object_name, context_object_load_params in context.items():
        # Type of the value
        object_type: str = context_object_load_params['type']

        # If the value is a model, we load the model object and
        # include it in the template replacements
        if object_type == 'model':
            app_name: str = context_object_load_params['app_name']
            model_name: str = context_object_load_params['model']
            object_id: Any = context_object_load_params['id']
            # Checking if JSON has been tampered
            model_object_as_str = '{0}-{1}-{2}'.format(app_name, model_name, object_id)
            if context_object_load_params['__checksum__'] != checksum.make(model_object_as_str):
                return HttpResponse(
                    status=403, content='JSON tampering detected when loading object', content_type='text/plain'
                )

            # Loading the model
            model = apps.get_model(app_name, model_name)
            # Loading the object and including it as a replacement
            try:
                model_object = model.objects.get(pk=object_id)
            except model.DoesNotExist:
                model_object = None

            replacements[context_object_name] = model_object

        # If the value is a QuerySet we include it in the template replacements
        elif object_type == 'QuerySet':
            # Loading the model
            app_name = context_object_load_params['app_name']
            model_name = context_object_load_params['model']
            model = apps.get_model(app_name, model_name)
            params = tuple(context_object_load_params['params'])
            nonce: str = context_object_load_params['nonce']
            tag: str = context_object_load_params['tag']

            try:
                # Decryption of the data
                raw_query = crypto.decrypt(
                    key=settings.SECRET_KEY,
                    nonce=nonce,
                    encrypted_data=context_object_load_params['query'],
                    tag=tag,
                )
            except ValueError:
                return HttpResponse(
                    status=403,
                    content='JSON tampering detected when decrypting QuerySet',
                    content_type='text/plain',
                )

            # Loading the object and including it as a replacement
            replacements[context_object_name] = model.objects.raw(raw_query, params)

        # If the value is a safe value,
        # we include it in the template replacements
        elif object_type == 'safe_value':
            value = context_object_load_params['value']
            value_as_str: str = context_object_load_params['value_as_str']
            # Checking if JSON has been tampered
            if context_object_load_params['__checksum__'] != checksum.make(value_as_str):
                return HttpResponse(
                    status=403,
                    content='JSON tampering detected when loading safe value '
                    'for attribute \'{0}\'. Value: \'{1}\''.format(context_object_name, value_as_str),
                    content_type='text/plain',
                )

            # Including the safe value as a replacement
            replacements[context_object_name] = value

    # Activate the language
    if isinstance(language_code, str):
        translation.activate(language_code)

    # Render the template
    return render(request, path, replacements)
