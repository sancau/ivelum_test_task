# -*- coding: utf-8 -*-


def test_transformer_instance_initializes_correctly(transformer):
    assert transformer.proxy_domain == 'proxy'
    assert transformer.target_domain == 'target'
    assert transformer.soup is None


def test_transform_adds_tm_symbols(transformer, test_input):
    actual = transformer.transform(test_input)
    expected_count = (
        test_input.count('change') +
        test_input.count('chang5') +
        test_input.count('cha-ge') +
        test_input.count('cha_ge')
    )
    assert actual.count('\u2122') == expected_count
    assert (
        actual.count('change') +
        actual.count('chang5') +
        actual.count('cha-ge') +
        actual.count('cha_ge')
    ) == expected_count


def test_transform_changes_urls(transformer, test_input):
    actual = transformer.transform(test_input)
    expected_count = test_input.count('http://proxy/replacethis')
    expected_url = 'http://{}/replace_this'.format(transformer.target_domain)
    assert actual.count(expected_url) == expected_count


def test_transform_changes_favicon_paths(transformer, test_input):
    actual = transformer.transform(test_input)
    expected_count = test_input.count('/images/favicons')
    expected_url = 'http://{}/images/favicons'.format(transformer.target_domain)
    assert actual.count(expected_url) == expected_count
