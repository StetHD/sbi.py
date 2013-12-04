# coding: utf-8

import unittest

import sbi


class SBITestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_normal(self):
        url = 'http://vinta.s3.amazonaws.com/godness_k.jpg'
        result = sbi.search_by(url=url)

        self.assertTrue(len(result.images) > 0)

    def test_no_other_sizes(self):
        """
        "No other sizes of this image found" in Google search result
        """

        url = 'http://files.heelsfetishism.com/media/heels/2013/12/04/23823_5fbbba44bf474496a9b01dfebfb5d135.png.1440x0_q85_progressive.png'
        result = sbi.search_by(url=url)

        self.assertTrue(len(result.images) == 0)

    def test_to_dict(self):
        url = 'http://vinta.s3.amazonaws.com/godness_k.jpg'
        result = sbi.search_by(url=url)

        result_dict = result.to_dict()
        self.assertIsInstance(result_dict, dict)


if __name__ == '__main__':
    unittest.main()
