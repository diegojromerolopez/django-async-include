# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import
from io import open
import django
import os
import unittest
from django.template import Context, Template

os.environ['DJANGO_SETTINGS_MODULE'] = 'async_include.tests.settings'
django.setup()

import async_include.templatetags.async_include
async_include.templatetags.async_include.get_unique_template_id = lambda *args, **kwargs: "1"

from async_include.templatetags.async_include import slugify_template_path


class AsyncIncludeRenderTest(unittest.TestCase):
    """
    Tests the async_include template tag.
    """

    def __init__(self, *args, **kwargs):
        super(AsyncIncludeRenderTest, self).__init__(*args, **kwargs)

        self.template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")

    def render_template(self, path, context=None):
        """
        Renders a template in a path.
        :param path: Template path to be rendered. It is relative to this files's directory templates subdirectory.
        :param context: Context dict that will be replaced in that template. By default is empty.
        :return: a rendered template as a string.
        """
        if context is None:
            context = {}
        context = Context(context)

        template_path = os.path.join(self.template_dir, path)

        template_file = open(template_path, "rb")
        template_string = template_file.read()
        return Template(template_string).render(context)

    def test_template_path_slug(self):
        """
        Test if template slug function is working all right.
        """
        self.assertEqual(slugify_template_path("this/is/a%-%template/path-with-different-chars-like-ñáéíóúhtml"), "this_is_a_template_path_with_different_chars_like_naeiouhtml")
        self.assertEqual(slugify_template_path("this.is.another.templatehtml"), "thisisanothertemplatehtml")
