import re
import unittest

from django.test.client import Client

from main.models import Word


class LinkTestCase(unittest.TestCase):
    def tearDown(self):
        Word.objects.all().delete()


class SingleLinkTestCase(LinkTestCase):
    def setUp(self):
        Word.objects.create(title="lion")


class MultipleLinkTestCase(LinkTestCase):
    def setUp(self):
        Word.objects.create(title="lion")
        Word.objects.create(title="snow")
        Word.objects.create(title="fish")


class ValidSingleLinkTestCase(SingleLinkTestCase):
    def test_user_gets_valid_shortened_link_if_provides_valid_link(self):
        client = Client()
        original_link = 'http://www.nytimes.com/'
        response = client.get('/')
        assert response.status_code == 200, \
            'Status code is %s, expected 200' % response.status_code
        response = client.post('/', {'link': original_link})
        assert response.status_code == 200, \
            'Status code is %s, expected 200' % response.status_code
        shortened_link = 'http://testserver/lion/'
        assert shortened_link in response.content, \
            'Link %s is not present in response' % shortened_link
        response = client.get(shortened_link, follow=True)
        expected_redirect = original_link
        response_redirect = response.redirect_chain[0][0]
        assert response_redirect == expected_redirect, \
            'Response redirect %s is not equal to expected redirect %s' \
            % (response_redirect, expected_redirect)


class InvalidSingleLinkTestCase(SingleLinkTestCase):
    def test_user_gets_error_if_link_is_invalid(self):
        client = Client()
        invalid_link = 'invalid_link'
        response = client.get('/')
        assert response.status_code == 200, \
            'Status code is %s, expected 200' % response.status_code
        response = client.post('/', {'link': invalid_link})
        assert response.status_code == 200, \
            'Status code is %s, expected 200' % response.status_code
        expected_error_message = 'The link you provided <b>%s</b> is invalid' % invalid_link
        assert expected_error_message in response.content, \
            'Expected error message %s is not present in response ' % expected_error_message

    def test_404_error_if_non_existing_link_provided(self):
        client = Client()
        response = client.get('/badlink/')
        assert response.status_code == 404, \
            'Status code is %s, expected 404' % response.status_code


class TestsEmptyDataBase(unittest.TestCase):
    def test_500_error_if_database_is_empty(self):
        Word.objects.all().delete()
        client = Client()
        response = client.post('/', {'link': 'http://example.com/'})
        assert response.status_code == 500, \
            'Status code is %s, expected 500' % response.status_code


class WordsAssignedAndReusedCorrectlyTestCase(MultipleLinkTestCase):
    def test_that_words_are_assigned_and_reused_correctly(self):
        client = Client()
        user_links = ['http://en.wikipedia.org/wiki/Snow_Lion',
                      'http://en.wikipedia.org/wiki/List_of_common_fish_names',
                      'http://fa.wikipedia.org/wiki/%D8%B2%D8%A8%D8%A7%D9%86_%D9%81%D8%A7%D8%B1%D8%B3%DB%8C',
                      'http://www.iht.com',
                      'http://example.com']
        shortened_links = ['http://testserver/%s/' % w for w in
                           ('lion', 'fish', 'snow', 'lion', 'fish')]
        # should pick the first word in the wordlist that is a part of this URL
        # so for first link the shortened link should be 'lion', not 'snow'
        # because 'lion' precedes 'snow' in wordlist
        # for second link 'fish' should be picked up ('fish' is part of link)
        # for the third link the only remaining word should be picked ('snow')
        # for the 4th link 'lion' should be reused (the oldest existing)
        # for the 5th link 'fish' should be reused (the oldest existing)
        response = client.get('/')
        assert response.status_code == 200, \
            'Status code is %s, expected 200' % response.status_code
        for i in xrange(len(user_links)):
            response = client.post('/', {'link': user_links[i]})
            assert response.status_code == 200, \
                'Status code is %s, expected 200' % response.status_code
            assert shortened_links[i] in response.content, \
                'Link %s is not present in response' % shortened_links[i]
            response = client.get(shortened_links[i], follow=True)
            expected_redirect = user_links[i]
            response_redirect = response.redirect_chain[0][0]
            assert response_redirect == expected_redirect, \
                'Response redirect %s is not equal to expected redirect %s' \
                % (response_redirect, expected_redirect)
            response = client.get('/')

    def test_cant_create_more_than_one_link_with_the_same_url(self):
        client = Client()
        user_links = ['http://en.wikipedia.org/wiki/Snow_Lion'] * 3
        shortened_links = ['http://testserver/lion/'] * 3
        for i in xrange(len(user_links)):
            response = client.get('/')
            response = client.post('/', {'link': user_links[i]})
            assert response.status_code == 200, \
                'Status code is %s, expected 200' % response.status_code
            assert shortened_links[i] in response.content, \
                'Link %s is not present in response' % shortened_links[i]

    def test_links_with_trailing_slash_and_without_are_treated_as_different(self):
        client = Client()
        user_links = ['http://www.example.com/foo',
                      'http://www.example.com/foo/']
        shortened_links = []
        for i in xrange(len(user_links)):
            client.get('/')
            response = client.post('/', {'link': user_links[i]})
            shortened_link = re.search('http://testserver/(\S+?)/', str(response), re.MULTILINE).group(1)
            shortened_links.append(shortened_link)
        assert shortened_links[0] != shortened_links[1], \
            'Different links gave the same shortened!'
