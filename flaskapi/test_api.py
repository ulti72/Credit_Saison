import unittest
import app
import requests

class TestApi(unittest.TestCase):
    
    STATS_URL = "http://127.0.0.1:8081/card_scheme/stats?start={start}&limit={limit}"
    CARD_URL = "http://127.0.0.1:8081/card_scheme/verify/{card_number}"



    def test_get_stats(self):
        limit =3 
        start = 1
        r = requests.get(TestApi.STATS_URL.format(start=start, limit=limit))
        self.assertEqual(r.status_code,200)


    def test_get_verify(self):
        card_number = 123
        r = requests.get(TestApi.CARD_URL.format(card_number=card_number))
        self.assertEqual(r.status_code,200)