# -*- coding: utf-8 -*-
import jsonpickle
from django.template.loader import render_to_string
from django.test import TestCase
from django.urls import reverse


class TestViews(TestCase):
    @classmethod
    def setUpClass(cls):
        import os
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'async_include.tests.settings')
        import django
        django.setup()
        super(TestViews, cls).setUpClass()

    def test_get_template_ok(self):
        url = reverse('async_include:get_template')
        post_data = jsonpickle.dumps({
            'path': 'async_include/spinner.html',
            'context': {
                'str_var1': {
                    'type': 'safe_value',
                    'value': 'str_var1_value',
                    'value_as_str': 'str_var1_value',
                    '__checksum__': '9ca5473a2e627df34e0c0a3651e7607a'
                }
            },
            'language_code': 'en-us'
        })
        resp = self.client.post(url, data=post_data, content_type='application/json')

        self.assertEqual(200, resp.status_code)
        self.assertEqual({'Content-Type': 'text/html; charset=utf-8'}, resp.headers)
        self.assertEqual(
            render_to_string('async_include/spinner.html').encode('utf-8'),
            resp.content
        )

    def test_get_template_with_json_tampering_in_str_variable(self):
        url = reverse('async_include:get_template')
        post_data = jsonpickle.dumps({
            'path': 'async/template/path.html',
            'context': {
                'str_var1': {
                    'type': 'safe_value',
                    'value': 'str_var1_value',
                    'value_as_str': 'str_var1_value',
                    '__checksum__': 'bad-checksum'
                }
            },
            'language_code': 'en-us'
        })
        resp = self.client.post(url, data=post_data, content_type='application/json')

        self.assertEqual(403, resp.status_code)
        self.assertEqual({'Content-Type': 'text/plain'}, resp.headers)
        self.assertEqual(
            b'JSON tampering detected when loading safe value for attribute \'str_var1\'. '
            b'Value: \'str_var1_value\'',
            resp.content
        )

    def test_get_template_error_404(self):
        url = reverse('async_include:get_template')
        resp = self.client.get(url)

        self.assertEqual(400, resp.status_code)
