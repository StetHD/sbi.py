# coding: utf-8

import unittest

import sbi


class SBITestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_repr(self):
        empty_result = sbi.SBIResult()

        self.assertIn('SBIResult', repr(empty_result))
        self.assertIn('SBIResult', str(empty_result))

    def test_normal(self):
        url = 'http://vinta.s3.amazonaws.com/godness_k.jpg'
        result = sbi.search_by(url=url)

        self.assertTrue(result)
        self.assertTrue(result.best_guess)
        self.assertTrue(len(result.images) > 0)
        self.assertEqual(len(result), len(result.images))
        self.assertTrue(isinstance(result.to_dict(), dict))

    def test_no_other_sizes(self):
        """
        "No other sizes of this image found" in Google search result
        """

        url = 'http://files.heelsfetishism.com/media/heels/2013/12/04/23823_5fbbba44bf474496a9b01dfebfb5d135.png.1440x0_q85_progressive.png'
        result = sbi.search_by(url=url)

        self.assertFalse(result)
        self.assertTrue(len(result.images) == 0)

    def test_non_ascii_url(self):
        url = 'https://vinta.s3.amazonaws.com/水原希子.jpg'
        result = sbi.search_by(url=url)

        self.assertTrue(result)

    def test_non_ascii_best_guess(self):
        url = 'http://vinta.s3.amazonaws.com/godness_k_2.jpg'
        result = sbi.search_by(url=url)

        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
