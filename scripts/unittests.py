import unittest
import re
import countmedia

class TestCountMedia(unittest.TestCase):
    """
    Check that the script countmedia.py returns a valid media count.
    This makes sure that the links are still valid and the structure
    of the pages didn't change.
    """

    def setUp(self):
        self.number = re.compile('\d+')

    def test_count_books(self):
        media = str(countmedia.count_books())
        self.assertRegex(media, self.number)

    def test_count_ebooks(self):
        media = str(countmedia.count_ebooks())
        self.assertRegex(media, self.number)

    def test_count_journals(self):
        media = str(countmedia.count_journals())
        self.assertRegex(media, self.number)

    def test_count_databases(self):
        media = str(countmedia.count_databases())
        self.assertRegex(media, self.number)


if __name__ == '__main__':
    unittest.main()
