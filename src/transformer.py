# -*- coding: utf-8 -*-

import bs4


class Transformer:
    """
    Defines required logic to transform a html page according the rule:
    symbol '\u2122' follows every word with length of 6 chars
    """

    def __init__(self, target_domain):
        self.target_domain = target_domain
        self.soup = None

    @staticmethod
    def _transform_word(word: str) -> str:
        """
        Transforms a series of symbols that can be considered as a word

        Examples of words: 'word', 'word25', 'some-word25', etc

        Note: tokens like 'some@word' considered as 2 words - 'some' and 'word'
              as '-' and '_' is the only allowed inner delimiters

        :param word: word as string
        :return: transformed word as string
        """
        out = ''
        counter = 0
        for c in word:
            if c.isalpha() or c in ['-', '_']:
                counter += 1
            else:
                if counter == 6:
                    out += '\u2122'
                counter = 0
            out += c
        if counter == 6:
            out += '\u2122'
        return ''.join(out)

    @staticmethod
    def _transform_element_text(text: str) -> str:
        """
        Performs transformation of an element text
        :param text: element text as string
        :return:  transformed element text as string
        """
        words = []
        for word in text.split(' '):
            word = Transformer._transform_word(word)
            words.append(word)
        return ' '.join(words)

    def _transform_tag(self, tag):
        """
        Performs transformation on a certain tag of the <self.soup>
        :param tag: soup tag
        :return: None (modifies <self.soup>)
        """

        def _(e):
            if isinstance(e, bs4.element.Comment):  # do not modify comments
                return
            if e.name in ['script']:  # do not modify contents of 'script' tag
                return
            if isinstance(e, bs4.element.NavigableString):  # has no children
                e.replaceWith(self._transform_element_text(e))
                return
            for i in e.children:
                _(i)

        for el in self.soup.find(tag):
            _(el)

    def _transform_hyperlinks(self, request_source):
        """
        Transforms all the hyperlinks on a page (inside <self.soup> object)
        This will keep the user within proxy
        Note:
            1. Proxy not serving https
            2. We don't want to keep 'www'
        :return: None (modifies <self.soup>)
        """
        for a in self.soup.findAll('a'):
            try:
                a['href'] = a['href'] \
                    .replace(self.target_domain, request_source) \
                    .replace('https', 'http') \
                    .replace('www.', '')
            except KeyError:
                pass

    def transform(self, page, request_source):
        """
        Top-level method for page transformation
        Generates the <self.soup> from given plain html
        :param page:
        :param request_source: request netloc
        :return:
        """
        self.soup = bs4.BeautifulSoup(page, 'lxml')
        self._transform_hyperlinks(request_source)
        for tag in ['body', 'title']:  # only parse what we need
            self._transform_tag(tag)

        # fix & symbols issue after bs4 processing
        output = str(self.soup).replace('amp;', '')

        # fix paths to favicons
        output = output.replace('/images/favicons',
                                'http://{}/images/favicons'.format(
                                    self.target_domain))

        return output
