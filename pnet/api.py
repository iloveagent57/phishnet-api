import json
import requests


def has_kwargs(*args):
    allowed_kwargs = set(args)
    def wrapper(function):
        def inner(*args, **kwargs):
            kwargs = {k: v for k, v in kwargs.iteritems() if k in allowed_kwargs}
            return function(*args, **kwargs)
        return inner
    return wrapper


class PhishNetApi(object):
    def __init__(self, api_key, data_format='json'):
        """
        :param api_key: Your phish.net API private key
        :param data_format: The format of data to return, default is JSON.
        :returns: A new API object with methods to access data from several endpoints.
        """
        self.api_key = api_key
        self.data_format = data_format
        self._base_url = 'https://api.phish.net/api.js'
        self._base_params = {
            'api': '2.0',
            'format': self.data_format,
            'apikey': self.api_key
        }

    def __repr__(self): # pragma: no cover
        return 'PhishNetApi(api_key={0}, data_format={1})'.format(repr(self.api_key), repr(self.data_format))

    def _get(self, params):
        payload = self._base_params
        payload.update(params)
        response = requests.get(self._base_url, params=payload)
        if response.status_code != 200:
            raise Exception(response.status_code)

        data = response.json()

        # Could get a response with status code 200, but some other error could occur,
        # possibly due to a bad parameter.
        if isinstance(data, dict) and (data.get('success') == 0):
            raise Exception(data.get('reason'))

        return data

    def _get_method(self, method_name, params):
        params = params or {}
        params.update({'method': method_name})
        return self._get(params)

    @has_kwargs('year', 'venueid', 'state', 'country', 'month', 'day', 'artist', 'showids')
    def shows_query(self, **kwargs):
        """
        Optional kwargs:
        :param year: 4 digit year
        :param venueid: Integer venue id
        :param state: 2 haracter string
        :param country: Name of a country
        :param month: 1 or 2 digit month
        :param day: 1 or 2 digit day
        :param artist: Integer artist id (1 is Phish)
        :param showids: Comma separated string of show ids
        :returns: A list of shows filtered according to kwargs.
        """
        return self._get_method('pnet.shows.query', kwargs)

    @has_kwargs('showdate', 'showid')
    def shows_setlist(self, **kwargs):
        """
        :param showdate: The date of the show in YYYY-mm-dd format
        :param showid: The id of the show.  If both ``showdate`` and ``showid`` are specified, showid is used.
        :returns: A setlist for a given show.
        """
        return self._get_method('pnet.shows.setlists.get', kwargs)

    @has_kwargs('username', 'showdate')
    def reviews_query(self, **kwargs):
        """
        Optional kwargs:
        :param username: If a username is provided, it will return reviews posted by a given user.
        :param showdate: If a showdate is provided in YYYY-mm-dd format, it will return reviews attached to a given show.
        If both username and showdate are provided, it will filter by both showdate AND username.
        :returns: A list of reviews filtered by username, the date of the show, or both.
        """
        return self._get_method('pnet.reviews.query', kwargs)


def get_api(config_filename):
    with open(config_filename) as config_file:
        config = json.load(config_file)
        return PhishNetApi(config['api']['private_key'])
