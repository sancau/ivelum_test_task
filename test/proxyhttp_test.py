# -*- coding: utf-8 -*-

import falcon

from proxyhttp import Proxy
from transformer import Transformer


def test_api_runs(client):
    resp = client.simulate_get('/')
    assert resp.status == falcon.HTTP_200


def test_proxy_middleware_instance_initializes_correctly():
    for port in ['', 5000, None]:
        p = Proxy(host='proxy', port=port, target='target')
        assert p.proxy_domain == 'proxy:{}'.format(port) if port else 'proxy'
        assert p.target_domain == 'target'
        assert isinstance(p.transformer, Transformer)
        assert p.transformer.proxy_domain == p.proxy_domain
        assert p.transformer.target_domain == p.target_domain


def test_app_returns_expected_data_with_not_existing_url(client):
    resp = client.simulate_get('/something_that_not_exists')
    content = resp.content.decode('utf-8')
    assert 'Exception: 404 Client Error' in content
    assert 'https://habrahabr.ru/something_that_not_exists' in content


def test_app_returns_expected_data_with_existing_url(client):
    resp = client.simulate_get('/')
    content = resp.content.decode('utf-8')
    assert '<title>Лучшие™ публикации за сутки / Хабрахабр</title>' in content
