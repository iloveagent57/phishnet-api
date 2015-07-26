import unittest

import mock

from pnet.api import get_api, has_kwargs, PhishNetApi


class TestHasKwargs(unittest.TestCase):
    @has_kwargs('x', 'y')
    def foo(self, **kwargs):
        return kwargs

    def test_has_kwargs_extra_args(self):
        result = self.foo(x=1, y=2, z=3)

        self.assertEqual({'x', 'y'}, set(result.keys()))

    def test_has_kwargs_no_valid_args(self):
        result = self.foo(z=3)

        self.assertEqual([], result.keys())


class TestPhishNetApi(unittest.TestCase):
    def setUp(self):
        self.requests_patcher = mock.patch('pnet.api.requests')
        self.requests = self.requests_patcher.start()
        self.api = PhishNetApi('my-key')

    def tearDown(self):
        self.requests_patcher.stop()

    def test_get_happy_path(self):
        mock_response = mock.Mock(status_code=200)
        self.requests.get.return_value = mock_response
        result = self.api._get({'foo': 5})

        expected_payload = {
            'api': '2.0',
            'format': 'json',
            'apikey': 'my-key',
            'foo': 5
        }
        self.requests.get.assert_called_once_with(self.api._base_url,
                                                  params=expected_payload)
        self.assertEqual(result, mock_response.json.return_value)

    def test_get_non_200_status_code(self):
        self.requests.get.return_value = mock.Mock(status_code=400)

        with self.assertRaisesRegexp(Exception, '400'):
            self.api._get({'foo': 5})

    def test_get_unsuccessful(self):
        mock_response = mock.Mock(status_code=200)
        mock_response.json.return_value = {
            'success': 0,
            'reason': 'failure'
        }
        self.requests.get.return_value = mock_response

        with self.assertRaisesRegexp(Exception, 'failure'):
            self.api._get({'foo': 5})

    def test_get_method(self):
        with mock.patch('pnet.api.PhishNetApi._get') as _get:
            self.api._get_method('some.endpoint', {'the': 'param'})

            _get.assert_called_once_with({
                'method': 'some.endpoint',
                'the': 'param'
            })

    def test_shows_query(self):
        with mock.patch('pnet.api.PhishNetApi._get_method', return_value=[{'showid': 1}]) as get_method:
            result = self.api.shows_query(year=2014)

            self.assertEqual([{'showid': 1}], result)
            get_method.assert_called_once_with('pnet.shows.query', {'year': 2014})

    def test_shows_setlist(self):
        with mock.patch('pnet.api.PhishNetApi._get_method', return_value=[{'songs': 'reba'}]) as get_method:
            result = self.api.shows_setlist(showid=1)

            self.assertEqual([{'songs': 'reba'}], result)
            get_method.assert_called_once_with('pnet.shows.setlists.get', {'showid': 1})

    def test_reviews_query(self):
        with mock.patch('pnet.api.PhishNetApi._get_method', return_value=[{'likes': 'yes'}]) as get_method:
            result = self.api.reviews_query(showdate='2014-12-31')

            self.assertEqual([{'likes': 'yes'}], result)
            get_method.assert_called_once_with('pnet.reviews.query', {'showdate': '2014-12-31'})

    def test_api(self):
        with mock.patch.dict('pnet.configuration.CONFIGURATION', {'api': {'private_key': 'foo'}}):
            api = get_api()

            self.assertEqual('foo', api.api_key)
            self.assertEqual('json', api.data_format)
