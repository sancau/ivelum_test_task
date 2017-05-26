# -*- coding: utf-8 -*--

import falcon
import pytest

from falcon import testing

from proxyhttp import Proxy
from transformer import Transformer


@pytest.fixture
def transformer():
    return Transformer('proxy', 'target')


@pytest.fixture
def test_input():
    with open('test_input.html', encoding='utf-8') as f:
        return f.read()


@pytest.fixture
def client():
    print(falcon.testing.helpers.DEFAULT_HOST)
    proxy = Proxy(host=falcon.testing.helpers.DEFAULT_HOST,
                  port='',
                  target='habrahabr.ru')
    api = falcon.API(middleware=[proxy, ])
    return testing.TestClient(api)
