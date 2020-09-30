from __future__ import absolute_import, division, print_function

import os
import unittest

import vcr
tape = vcr.VCR(
    cassette_library_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures'),
    path_transformer = vcr.VCR.ensure_suffix('.yaml'),
    filter_headers = ['x-account-id', 'x-api-key'],
    match_on = ['uri', 'method', 'body'],
)

import passninja

account_id = 'dummy-account-id'
api_key = 'dummy-api-key'


class PassNinjaAPITest(unittest.TestCase):

    def test(self):
        self.assertRaises(passninja.PassNinjaInvalidArgumentsException,
            passninja.PassNinjaClient, None, None)
        test_client = passninja.PassNinjaClient(account_id, api_key)
        self.assertIsInstance(test_client, passninja.PassNinjaClient)

        with tape.use_cassette('test_create'):
            self.assertRaises(passninja.PassNinjaInvalidArgumentsException,
                test_client.passes.create, None, None)
            self.assertRaises(passninja.PassNinjaInvalidArgumentsException,
                test_client.passes.create, 'demo.coupon', {'firstName': None})
            self.assertRaises(passninja.PassNinjaInvalidArgumentsException,
                test_client.passes.create, 'demo.coupon', {'barcode': '12345', 'description': 'This is a test description.'})
            pass_object = test_client.passes.create('demo.coupon', {
                'logoText': 'Example Loyalty',
                'organizationName': 'My org',
                'description': 'This is a loyalty card',
                'expiration': '2025-12-01T23:59:59Z',
                'memberName': 'Tasio Victoria',
                'specialOffer': 'Free Drinks at 4:30PM!',
                'loyaltyLevel': 'level one',
                'barcode': 'www.google.com',
            })
            self.assertEqual(pass_object.url, 'https://www.passninja.com/installs/xKnNLODqz.html')
            self.assertEqual(pass_object.serialNumber, '2dcf7187-4eea-42a2-aabe-d7ca5a78f3dd')

        with tape.use_cassette('test_get'):
            self.assertRaises(passninja.PassNinjaInvalidArgumentsException,
                test_client.passes.get, None, None)
            resp = test_client.passes.get(pass_object.passType, pass_object.serialNumber, )
            self.assertEqual(resp['serialNumber'], pass_object.serialNumber)

        with tape.use_cassette('test_put'):
            self.assertRaises(passninja.PassNinjaInvalidArgumentsException,
                test_client.passes.put, None, None, {})
            resp = test_client.passes.put(pass_object.passType, pass_object.serialNumber, {
                'logoText': 'Put Example Loyalty',
                'organizationName': 'Put my org',
                'description': 'Put this is a loyalty card',
                'expiration': '2025-12-01T23:59:59Z',
                'memberName': 'Put Victoria',
                'specialOffer': 'Put Free Drinks at 4:30PM!',
                'loyaltyLevel': 'put level one',
                'barcode': 'www.put.com',
            })
            self.assertEqual(resp['serialNumber'], pass_object.serialNumber)

        with tape.use_cassette('test_delete'):
            self.assertRaises(passninja.PassNinjaInvalidArgumentsException,
                test_client.passes.delete, None, None)
            resp = test_client.passes.delete(pass_object.passType, pass_object.serialNumber)


if __name__ == '__main__':
    unittest.main()
