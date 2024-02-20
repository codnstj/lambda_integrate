# -*- coding: utf-8 -*-

"""Tests for lambda_integrate."""

import json


def test_response(client):
    resp = client.get("/")
    assert resp["statusCode"] == 200
    assert json.loads(resp["body"]) == {"hello": "world"}
