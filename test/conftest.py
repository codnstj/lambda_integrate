# -*- coding: utf-8 -*-

"""Test configuration for lambda_integrate."""

import pytest

from chalice.config import Config
from chalice.local import LocalGateway

from app import app


class TestClient(object):
    """Simulates requests to the local gateway

    Keyword Arguments:
        headers (dict): Default headers to set on every request (default: ``None``).
    """

    def __init__(self, app, headers=None):
        self.app = app
        self._default_headers = headers

    def request(self, method="GET", path="/", headers=None, body=None):

        if not path.startswith("/"):
            raise ValueError("path must start with '/'")

        valid_methods = ["GET", "HEAD", "POST", "PUT", "DELETE"]
        if method not in valid_methods:
            raise ValueError(f"method must be one of: {valid_methods}")

        body = body or ""
        headers = headers or {}

        gateway = LocalGateway(self.app, Config())
        response = gateway.handle_request(method, path, headers, body)
        return response

    def get(self, path="/", **kwargs):
        """Simulates a GET request to the local gateway"""
        return self.request("GET", path, **kwargs)

    def head(self, path="/", **kwargs):
        """Simulates a HEAD request to the local gateway"""
        return self.request("HEAD", path, **kwargs)

    def post(self, path="/", **kwargs):
        """Simulates a POST request to the local gateway"""
        return self.request("POST", path, **kwargs)

    def put(self, path="/", **kwargs):
        """Simulates a PUT request to the local gateway"""
        return self.request("PUT", path, **kwargs)

    def delete(self, path="/", **kwargs):
        """Simulates a DELETE request to the local gateway"""
        return self.request("DELETE", path, **kwargs)


@pytest.fixture(scope="module")
def client():
    return TestClient(app)
