import unittest

from utils.auth import validate_auth_token


class MockRequest(dict):
    token = None

MOCK_TOKENS = {
    "123": "BUY4",
    "321": "STONE"
}


class Auth(unittest.TestCase):
    def test_auth_ok(self):
        request = MockRequest()
        request.token = "123"
        data = validate_auth_token(request, MOCK_TOKENS)
        self.assertIsNone(data)
        self.assertEqual(request["company"], MOCK_TOKENS["123"])

    def test_auth_fail(self):
        request = MockRequest()
        request.token = "0"
        data = validate_auth_token(request, MOCK_TOKENS)
        self.assertEqual(data.status, 401)


if __name__ == '__main__':
    unittest.main()
