# -*- coding: utf-8 -*-
import unittest.mock

from django.template.loader import render_to_string
from django.test import TestCase


class TestViews(TestCase):
    @classmethod
    def setUpClass(cls):
        import os
        os.environ.setdefault(
            'DJANGO_SETTINGS_MODULE', 'async_include.tests.settings'
        )
        import django
        django.setup()
        super(TestViews, cls).setUpClass()

    @unittest.mock.patch(
        'async_include.templatetags.async_include.get_unique_template_id'
    )
    @unittest.mock.patch(
        'async_include.templatetags.async_include.slugify_template_path'
    )
    def test_async_include(
            self, mock_slugify_template_path, mock_get_unique_template_id
    ):
        mock_slugify_template_path.return_value = 'test_template_path'
        mock_get_unique_template_id.return_value = 'test_uuid'

        test_async_include_html = render_to_string('test_async_include.html')

        self.assertIn(
            '<script id="script_test_template_path__test_uuid" '
            'type="text/javascript">',
            test_async_include_html
        )
        self.assertIn(
            'make_request__test_template_path__test_uuid',
            test_async_include_html
        )
        self.assertIn(
            'const block_id = "test_template_path__test_uuid";',
            test_async_include_html
        )
