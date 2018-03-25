import unittest
import urllib2
import sys
import os.path
import json
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import geocoding_proxy.geocode as gc
import geocoding_proxy.rest_server as rs

COORDINATE_TOLERANCE = 3


class TestGoogleGeoCode(unittest.TestCase):
    """ Tests the google geocode service
    """

    def test_correct_address(self):
        lat_lng = gc.GoogleGeocode.address_lookup("2727 Milvia St, Berkeley, CA 94703")
        self.assertAlmostEqual(lat_lng['lat'], 37.8596569, COORDINATE_TOLERANCE)
        self.assertAlmostEqual(lat_lng['lng'], -122.2686676, COORDINATE_TOLERANCE)


    def test_empty_address(self):
        ''' Should raise an error if an empty address was passed'''
        with self.assertRaises(urllib2.HTTPError) as context:
            gc.GoogleGeocode.address_lookup("")

    def test_bad_address(self):
        lat_lng = gc.GoogleGeocode.address_lookup("-")
        self.assertIsNone(lat_lng)


class TestHereGeoCode(unittest.TestCase):
    """ Tests the here geocode service
    """

    def test_correct_address(self):
        lat_lng = gc.HereGeocode.address_lookup("2727 Milvia St, Berkeley, CA 94703")
        self.assertAlmostEqual(lat_lng['lat'], 37.85958, COORDINATE_TOLERANCE)
        self.assertAlmostEqual(lat_lng['lng'], -122.26939, COORDINATE_TOLERANCE)

    def test_empty_address(self):
        with self.assertRaises(urllib2.HTTPError):
            gc.HereGeocode.address_lookup("")

    def test_bad_address(self):
        lat_lng = gc.HereGeocode.address_lookup("-")
        self.assertIsNone(lat_lng)


class TestGeocodeService(unittest.TestCase):
    """ Tests the RESTful interface
    """
    addr_lookup_url = "http://127.0.0.1:8000/geocode/json"
    server = rs.GeoCodeServer

    def setUp(self):
        self.server.start()
        time.sleep(2)

    def tearDown(self):
        try:
            self.server.stop()
        except urllib2.HTTPError, urllib2.URLError:
            pass

    def test_correct_address(self):
        response = urllib2.urlopen("http://127.0.0.1:8000/geocode/json?address=2727%Milvia%St,%Berkeley,%CA%94703")
        data = json.load(response)
        self.assertAlmostEqual(first=data['lat'], second=37.85958, delta=COORDINATE_TOLERANCE)
        self.assertAlmostEqual(first=data['lng'], second=-122.26939, delta=COORDINATE_TOLERANCE)

    def test_bad_address(self):
        test_path = "http://127.0.0.1:8000/geocode/json?address=----"
        response = urllib2.urlopen(test_path)
        data = json.load(response)
        self.assertIsNone(data)

    def test_no_address(self):
        test_path = "http://127.0.0.1:8000/geocode/json?address="
        with self.assertRaises(urllib2.HTTPError):
            urllib2.urlopen(test_path)

    def test_no_query(self):
        test_path = "http://127.0.0.1:8000/geocode/json"
        with self.assertRaises(urllib2.HTTPError):
            urllib2.urlopen(test_path)

    def test_undefined(self):
        test_path = "http://127.0.0.1:8000/geocode/"
        with self.assertRaises(urllib2.HTTPError):
            urllib2.urlopen(test_path)

