import unittest
import cleangpr

class TestScript(unittest.TestCase):

    def test_split_filename(self):
        name = cleangpr.get_filename('/home/user/file.ext')
        self.assertEquals(name, 'file')

if __name__ == '__main__':
    unittest.main()
