import json
import urllib2
import urllib


def geocode_lookup(address):
    """ Used to convert an address to a geocode, tries using two different services before returning None on fail.
    """
    exception = None
    lat_lng = None
    try:
        lat_lng = HereGeocode.address_lookup(address)

    except urllib2.HTTPError as e:
        exception = e

    if (lat_lng is None) or (exception is not None):
        lat_lng = GoogleGeocode.address_lookup(address)

    return lat_lng


class AbstractGeoCodeService(object):
    """ Abstract class to act as am interoperable interface for geocoding services
    """

    @classmethod
    def _http_get(cls, url, req_values):
        """ Creates a get request using a given url and dictionray of query data
        Args:
            param url (string): base url
            param req_values (dict): query parameters
        Returns:
            return (obj): response
        """

        url_values = urllib.urlencode(req_values)
        full_url = url + '?' + url_values
        try:
            response = urllib2.urlopen(full_url)
            return response
        except urllib2.HTTPError as err:
            raise

    @classmethod
    def address_lookup(cls, addr_loc):
        ''' Interface method to be overriden by service implementation
        Args:
            param addr_loc (string): address to be geocoded
        Returns:
            return (dict): dictionary of the lat and lng values
        '''
        raise NotImplementedError("address_lookup should be implemented when subclassing AbsractGeoCodeService")


class HereGeocode(AbstractGeoCodeService):
    """ Implementation of the AbstractGeoCodeService for the HERE geocoding service
    """
    _app_id = 'VAYcZA9siqQS1YsWym43'
    _app_code = '1K0d7mT_t7I8Nya8kUY4VQ'

    _app_data = {'app_id': _app_id, 'app_code': _app_code}

    @classmethod
    def address_lookup(cls, addr_loc):
        """ Looks up the address using the HERE service
        Args:
            param addr_loc (string):
        Return:
            return json(dict):
        """
        addr_lookup_url = 'https://geocoder.cit.api.here.com/6.2/geocode.json'
        req_values = cls._app_data
        req_values.update({'searchtext': addr_loc})

        try:
            get_resp = super(HereGeocode, cls)._http_get(addr_lookup_url, req_values)

            lat_lng = cls._parse_latlng(get_resp)
            return lat_lng
        except urllib2.HTTPError:
            raise

    @classmethod
    def _parse_latlng(cls, response):
        """ Helper method to parse the response from the HERE service
        Args:
            param response (obj): response from JSON service
        Returns:
            return (dict): dictionary of the lat and lng values
        """
        data = json.load(response)
        # find the latitude and longitude for the navigation coordinates
        if (len(data['Response']['View']) > 0):
            lat_lng = data['Response']['View'][0]['Result'][0]['Location']['NavigationPosition'][0]

            # shorten the key names
            lat_lng['lat'] = lat_lng.pop('Latitude')
            lat_lng['lng'] = lat_lng.pop('Longitude')
        else:
            lat_lng = None
        return lat_lng


class GoogleGeocode(AbstractGeoCodeService):
    """ Implementation of the AbstractGeoCodeService for the Google geocoding service
    """
    _api_key = 'AIzaSyCT9wpoDyO8-M51mSSk4Mllh5Cuh4zHPCI'

    @classmethod
    def address_lookup(cls, addr_loc):
        """ Looks up the address using the Google service
        Args:
            param addr_loc (string): address
        Return:
            return json(dict): lat long coordinates
        """
        addr_lookup_url = 'https://maps.googleapis.com/maps/api/geocode/json'
        req_values = {'key': cls._api_key}
        req_values['address'] = addr_loc
        try:
            get_resp = super(GoogleGeocode, cls)._http_get(addr_lookup_url, req_values)

            lat_lng = cls._parse_latlng(get_resp)
            return lat_lng
        except urllib2.HTTPError:
            raise


    @classmethod
    def _parse_latlng(cls, response):
        """ Helper method to parse the response from the Google service
        Args:
            param response (obj): response from the JSON service
        Returns:
            return (dict): dictionary of the lat and lng values
        """
        data = json.load(response)
        if data['status'] == 'OK':
            if len(data['results']) > 0:
                lat_lng = data['results'][0]['geometry']['location']
            else:
                lat_lng = None
        else:
            lat_lng = None
        return lat_lng


