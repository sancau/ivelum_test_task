# -*- coding: utf-8 -*-

import traceback

from urllib.parse import urlparse

import falcon
import fire
import requests
import waitress

from transformer import Transformer


class Proxy:
    """
    A falcon middleware acting as a proxy server
    """
    def __init__(self, target):
        """
        :param target: target domain to serve

        Also configures a Transformer instance that will be used to transform
        the html response of the target domain
        """
        self.target_domain = target.split('/')[-1]  # remove possible 'http://'
        self.transformer = Transformer(target_domain=self.target_domain)

    def process_request(self, req, resp):
        """
        Middleware defining the proxy logic itself

        :param req: initial http request
        :param resp: http response that the middleware is acting on
        :return: None
        """
        try:
            # redirects request to the target domain
            request_source = urlparse(req.url).netloc
            url = req.url.replace(request_source, self.target_domain)
            _ = requests.get(url)
            _.raise_for_status()
            page = _.text
            resp.body = self.transformer.transform(page, request_source)
        except Exception as e:
            resp.status = falcon.HTTP_500
            error_info = {  # object to render in case of exception
                'exc': e,
                'exc_info': traceback.format_exc(),
                'url': req.url,
                'target': self.target_domain
            }
            resp.body = """
                <h3>Exception: {exc} </h4>
                <hr /> {exc_info} <hr />
                <h4>URL: {url} </h4>
                <h4>Target: {target} </h4>""".format(**error_info)

    def process_response(self, req, resp, resource, req_succeeded):
        """
        Sets appropriate Content-Type
        Prevents server from responding 404, does nothing if resp code is 500
        """
        resp.set_header('Content-Type', 'text/html;charset=UTF-8')

        if resp.status == falcon.HTTP_NOT_FOUND:
            resp.status = falcon.HTTP_200


def main(host='localhost', port=8080, target='http://habrahabr.ru'):
    api = falcon.API(middleware=[Proxy(target), ])
    print('Target domain: {}'.format(target))
    waitress.serve(api, host=host, port=port)


if __name__ == '__main__':
    fire.Fire(main)  # Fire wrapper adds CLI behaviour
