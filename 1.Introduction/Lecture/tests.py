import unittest
import unittest.mock
from nums import evens, check_evens_len


class TestEvens(unittest.TestCase):

    def test_check_evens_len_empty(self):
        self.assertEqual(check_evens_len([]), [])

    def test_check_evens_len_non_empty(self):
        self.assertEqual(check_evens_len([1, 2, 3]), [])

    @unittest.mock.patch("nums.evens")
    def test_check_evens_len_non_empty(self, evens_mock):
        evens_mock.return_value = []
        self.assertEqual(check_evens_len([1, 2, 3]), [])

        evens_mock.return_value = [2, 4, 6]
        self.assertEqual(check_evens_len([2, 9, 11]), [2, 4, 6])

        self.assertTrue(evens_mock.called)
        self.assertTrue(evens_mock.called)

        self.assertEqual(
            [
                unittest.mock.call([1, 2, 3]),
                unittest.mock.call([2, 9, 11]),
            ],
            evens_mock.mock_calls
        )
