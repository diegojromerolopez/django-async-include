import unittest.mock
import json

from django.template.loader import render_to_string
from django.test import TestCase
from django.urls import reverse
from async_include import checksum


class TestViews(TestCase):
    @classmethod
    def setUpClass(cls):
        import os

        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "async_include.tests.settings")
        import django

        django.setup()
        super(TestViews, cls).setUpClass()

    @unittest.mock.patch("django.apps.registry.Apps.get_model")
    @unittest.mock.patch("async_include.checksum.make")
    @unittest.mock.patch("async_include.crypto.decrypt")
    @unittest.mock.patch("django.db.models.query.QuerySet.raw")
    def test_get_template_ok(self, mock_raw, mock_decrypt, mock_make_checksum, mock_get_model):
        mock_make_checksum.return_value = "checksum"
        mock_decrypt.return_value = "decrypt result"
        mock_raw.return_value = "raw return value"

        url = reverse("async_include:get_template")
        post_data = json.dumps(
            {
                "path": "async_include/spinner.html",
                "path_checksum": "checksum",
                "context": {
                    "mock_model": {
                        "type": "model",
                        "id": 3774,
                        "app_name": "mock_app",
                        "model": "MockModel",
                        "__checksum__": "checksum",
                    },
                    "mock_queryset": {
                        "type": "QuerySet",
                        "query": "test_encrypted_sql_query",
                        "app_name": "mock_app",
                        "model": "MockModelForQuerySet",
                        "params": [],
                        "nonce": "test_nonce",
                        "tag": "test_tag",
                    },
                    "str_var1": {
                        "type": "safe_value",
                        "value": "str_var1_value",
                        "value_as_str": "str_var1_value",
                        "__checksum__": "checksum",
                    },
                },
                "language_code": "en-us",
            }
        )
        resp = self.client.post(url, data=post_data, content_type="application/json")

        self.assertEqual(200, resp.status_code)
        self.assertEqual("text/html; charset=utf-8", resp.headers.get("Content-Type"))
        self.assertEqual(render_to_string("async_include/spinner.html").encode("utf-8"), resp.content)
        self.assertEqual(
            [unittest.mock.call("mock_app", "MockModel"), unittest.mock.call("mock_app", "MockModelForQuerySet")],
            mock_get_model.call_args_list,
        )
        self.assertEqual(
            [
                unittest.mock.call("async_include/spinner.html"),
                unittest.mock.call("mock_app-MockModel-3774"),
                unittest.mock.call("str_var1_value"),
            ],
            mock_make_checksum.call_args_list,
        )
        self.assertEqual(
            [
                unittest.mock.call(
                    key="secret-key", nonce="test_nonce", encrypted_data="test_encrypted_sql_query", tag="test_tag"
                )
            ],
            mock_decrypt.call_args_list,
        )

    @unittest.mock.patch("async_include.checksum.make")
    def test_get_template_ok_str_variable(self, mock_make_checksum):
        mock_make_checksum.return_value = "checksum"

        url = reverse("async_include:get_template")
        post_data = json.dumps(
            {
                "path": "async_include/spinner.html",
                "path_checksum": "checksum",
                "context": {
                    "str_var1": {
                        "type": "safe_value",
                        "value": "str_var1_value",
                        "value_as_str": "str_var1_value",
                        "__checksum__": "checksum",
                    }
                },
                "language_code": "en-us",
            }
        )
        resp = self.client.post(url, data=post_data, content_type="application/json")

        self.assertEqual(200, resp.status_code)
        self.assertEqual("text/html; charset=utf-8", resp.headers.get("Content-Type"))
        self.assertEqual(render_to_string("async_include/spinner.html").encode("utf-8"), resp.content)

    @unittest.mock.patch("django.apps.registry.Apps.get_model")
    @unittest.mock.patch("async_include.checksum.make")
    def test_get_template_with_json_tampering_in_model_object_variable(self, mock_make_checksum, mock_get_model):
        mock_make_checksum.return_value = "checksum"

        url = reverse("async_include:get_template")
        post_data = json.dumps(
            {
                "path": "async_include/spinner.html",
                "path_checksum": "checksum",
                "context": {
                    "mock_model": {
                        "type": "model",
                        "id": 3774,
                        "app_name": "mock_app",
                        "model": "MockModel",
                        "__checksum__": "invalid-hecksum",
                    }
                },
                "language_code": "en-us",
            }
        )
        resp = self.client.post(url, data=post_data, content_type="application/json")

        self.assertEqual(403, resp.status_code)
        self.assertEqual("text/plain", resp.headers.get("Content-Type"))
        self.assertEqual(b"JSON tampering detected when loading object", resp.content)
        self.assertEqual([], mock_get_model.call_args_list)
        self.assertEqual(
            [unittest.mock.call("async_include/spinner.html"), unittest.mock.call("mock_app-MockModel-3774")],
            mock_make_checksum.call_args_list,
        )

    def test_get_template_with_json_tampering_in_str_variable(self):
        url = reverse("async_include:get_template")
        path = "async/template/path.html"
        post_data = json.dumps(
            {
                "path": path,
                "path_checksum": checksum.make(path),
                "context": {
                    "str_var1": {
                        "type": "safe_value",
                        "value": "str_var1_value",
                        "value_as_str": "str_var1_value",
                        "__checksum__": "bad-checksum",
                    }
                },
                "language_code": "en-us",
            }
        )
        resp = self.client.post(url, data=post_data, content_type="application/json")

        self.assertEqual(403, resp.status_code)
        self.assertEqual("text/plain", resp.headers.get("Content-Type"))
        self.assertEqual(
            b"JSON tampering detected when loading safe value for attribute 'str_var1'. Value: 'str_var1_value'",
            resp.content,
        )

    def test_get_template_error_400_invalid_method(self):
        url = reverse("async_include:get_template")
        resp = self.client.get(url)
        self.assertEqual(400, resp.status_code)

    def test_get_template_error_403_invalid_path_checksum(self):
        url = reverse("async_include:get_template")
        post_data = json.dumps(
            {
                "path": "async_include/spinner.html",
                "path_checksum": "invalid_checksum",
                "context": {},
                "language_code": "en-us",
            }
        )
        resp = self.client.post(url, data=post_data, content_type="application/json")
        self.assertEqual(403, resp.status_code)
        self.assertEqual(b"JSON tampering detected when loading template path", resp.content)

    def test_get_template_error_400_path_traversal(self):
        url = reverse("async_include:get_template")
        path = "../secret.html"
        post_data = json.dumps(
            {
                "path": path,
                "path_checksum": checksum.make(path),
                "context": {},
                "language_code": "en-us",
            }
        )
        resp = self.client.post(url, data=post_data, content_type="application/json")
        self.assertEqual(400, resp.status_code)
        self.assertEqual(b"Invalid template path traversal detected", resp.content)
