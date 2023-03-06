import unittest
import requests as req
from src.dao import *

class TestPostgreSQL(unittest.TestCase):
    
    def test_encode_bad_img_url_1(self):
        test_url_bad = (1, "https://monuments-and-memorials.s3.us-east-2.amazonaws.com/images/119771-1622222+-+Chen,+Alex+-+Coppini_1955_Austin_GeorgeWashington.jpg")
        sanitized_tuple = encode_bad_img_url(test_url_bad)
        sanitized_url = sanitized_tuple[2]
        resp = req.get(sanitized_url)
        self.assertEqual(200, resp.status_code, "Request for the encoded URL FAILED")
        
    
    def test_encode_bad_img_url_2(self):
        test_url_bad = (2, "https://monuments-and-memorials.s3.us-east-2.amazonaws.com/images/103549-1622222+-+Spencer,+Liz+-+Kaskey_1996_Atlanta_Coubertin+copy.jpg")
        sanitized_tuple = encode_bad_img_url(test_url_bad)
        sanitized_url = sanitized_tuple[2]
        resp = req.get(sanitized_url)
        self.assertEqual(200, resp.status_code, "Request for the encoded URL FAILED")
    
        
    def test_encode_bad_img_url_3(self):
        test_url_bad = (3, "https://monuments-and-memorials.s3.us-east-2.amazonaws.com/images/103549-1622222+-+Spencer,+Liz+-+Berks_1979_Atlanta_Einstein+copy.jpg")
        sanitized_tuple = encode_bad_img_url(test_url_bad)
        sanitized_url = sanitized_tuple[2]
        resp = req.get(sanitized_url)
        self.assertEqual(200, resp.status_code, "Request for the encoded URL FAILED")
    
    
    def test_encode_bad_img_url_4(self):
        test_url_bad = (4, "https://monuments-and-memorials.s3.us-east-2.amazonaws.com/images/103549-1622222+-+Spencer,+Liz+-+French_1910_Atlanta_Spencer+copy.jpg")
        sanitized_tuple = encode_bad_img_url(test_url_bad)
        sanitized_url = sanitized_tuple[2]
        print(sanitized_url)
        resp = req.get(sanitized_url)
        self.assertEqual(200, resp.status_code, "Request for the encoded URL FAILED")
    
    
if __name__ == '__main__':
    unittest.main()
