# phishnet-api
A nicer wrapper for the [phish.net](http://phish.net/) API.  Requires [requests](http://docs.python-requests.org/en/latest/) and [mock](http://www.voidspace.org.uk/python/mock/) (to run unit tests).

## Usage
```python
In [1]: from pnet.api import PhishNetApi
In [2]: api = PhishNetApi('my-key')
In [3]: api
Out[3]: PhishNetApi(api_key='my-key', data_format='json')
In [4]: first = api.shows_query(year=1983)[0]
Out[5]: 
{u'artist': u'Phish',
 u'city': u'Burlington',
 u'country': u'USA',
 u'date_day': u'30',
 u'date_dow': u'Sunday',
 u'date_month': u'October',
 u'link': u'http://phish.net/setlists/?d=1983-10-30',
....
In [6]: setlist = api.shows_setlist(showid=first['showid'])
In [7]: setlist
Out[7]: 
[{u'artist': u'1',
  u'artist-name': u'Phish',
  u'city': u'Burlington',
  u'country': u'USA',
  u'meta': u'',
  u'mmddyy': u'10/30/1983',
  u'nicedate': u'October 30, 1983',
  u'relativetime': u'32 years ago',
  u'setlistdata': u"....
```
