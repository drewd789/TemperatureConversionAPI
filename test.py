import unittest
import urllib
import math
from random import random, randrange
from urllib.request import urlopen

API = 'http://localhost/temperature'

class TestTemperatureAPI(unittest.TestCase):
    # Test Fahrenheit to Celsius conversion within expected ranges.
    def test_normal_ftoc(self):
        upper = 500
        lower = -500
        for _ in range(100):
            fahr = random()*(upper - lower) + lower
            cels = (fahr - 32)*(5/9)
            response = urlopen(f'{API}?f={fahr}')
            self.assertEqual(200, response.code)
            self.assertEqual(cels, float(response.read()))
        
    # Test Celsius to Fahrenheit conversion within expected ranges.
    def test_normal_ctof(self):
        upper = 500
        lower = -500
        for _ in range(100):
            cels = random()*(upper - lower) + lower
            fahr = cels*(9/5) + 32
            response = urlopen(f'{API}?c={cels}')
            self.assertEqual(200, response.code)
            self.assertEqual(fahr, float(response.read()))
            
    # Test Fahrenheit to Celsius conversion for extreme values.
    def test_extreme_ftoc(self):
        upper = -308
        lower = 308
        for _ in range(100):
            m = random()
            e = randrange(lower, upper)
            fahr = float(f'{m}e{e}')
            cels = (fahr - 32)*(5/9)
            response = urlopen(f'{API}?f={fahr}')
            self.assertEqual(200, response.code)
            self.assertEqual(cels, float(response.read()))

    # Test Celsius to Fahrenheit conversion for extreme values.
    def test_extreme_ctof(self):
        upper = -308
        lower = 308
        for _ in range(100):
            m = random()
            e = randrange(lower, upper)
            cels = float(f'{m}e{e}')
            fahr = cels*(9/5) + 32
            response = urlopen(f'{API}?c={fahr}')
            self.assertEqual(200, response.code)
            self.assertEqual(fahr, float(response.read()))

    # Test API uses first Celsius if more than one is specified.
    def test_multiple_ctof(self):
        response = urlopen(f'{API}?c=0&c=10&c=20&c=30')
        self.assertEqual(200, response.code)
        self.assertEqual(32.0, float(response.read()))
        
    # Test API uses first Fahrenheit if more than one is specified.
    def test_multiple_ftoc(self):
        response = urlopen(f'{API}?f=212&f=112&f=12&f=-2')
        self.assertEqual(200, response.code)
        self.assertEqual(100.0, float(response.read()))
        
    # Test API uses first Celsius if both scales specified.
    def test_multiple_both(self):
        response = urlopen(f'{API}?c=100&f=100')
        self.assertEqual(200, response.code)
        self.assertEqual(212.0, float(response.read()))
        
    # Test special floats for Celsius.
    def test_cels_special(self):
        for t in (float('inf'), float('-inf')):
            response = urlopen(f'{API}?c={t}')
            self.assertEqual(200, response.code)
            self.assertEqual(t, float(response.read()))
        response = urlopen(f'{API}?c=nan')
        self.assertEqual(200, response.code)
        self.assertTrue(math.isnan(float(response.read())))
        
    # Test special floats for Fahrenheit.
    def test_fahr_special(self):
        for t in (float('inf'), float('-inf')):
            response = urlopen(f'{API}?f={t}')
            self.assertEqual(200, response.code)
            self.assertEqual(t, float(response.read()))
        response = urlopen(f'{API}?f=nan')
        self.assertEqual(200, response.code)
        self.assertTrue(math.isnan(float(response.read())))
        
    # Test error on no arguments.
    def test_error_noarg(self):
        with self.assertRaises(urllib.error.HTTPError) as context:
            urlopen(f'{API}?')

    # Test error on invalid Celsius argument.
    def test_error_badcels(self):
        with self.assertRaises(urllib.error.HTTPError) as context:
            urlopen(f'{API}?c=100C')

    # Test error on invalid Fahrenheit argument.
    def test_error_badfahr(self):
        with self.assertRaises(urllib.error.HTTPError) as context:
            urlopen(f'{API}?c=100F')