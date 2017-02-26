# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json

from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader, Context

from django.apps import apps


# Return the template with the remote context replaced
def get_template(request):

    json_body = json.loads(request.body)

    path = json_body.get("path")

    # Remote context
    # The caller has sent the model objects and safe values (strings, numbers, etc.) as a dict with
    # the app_labels, model and id
    context = json_body.get("context")
    replacements = {}

    # For each remote context value, we load it again
    for context_object_name, context_object_load_params in context.items():
        # Type of the value
        object_type = context_object_load_params["type"]

        # If the value is a model, we load the model object and include it in the template replacements
        if object_type == "model":
            # Loading the model
            model = apps.get_model(context_object_load_params["app_name"], context_object_load_params["model"])
            # Loading the object and including it as a replacement
            replacements[context_object_name] = model.objects.get(id=context_object_load_params["id"])

        # If the value is a safe value we include it in the template replacements
        elif object_type == "safe_value":
            # Including the safe value as a replacement
            replacements[context_object_name] = context_object_load_params["value"]

    # Render the template
    return render(request, path, replacements)
