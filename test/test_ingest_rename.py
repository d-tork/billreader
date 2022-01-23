import unittest
import os

from billingest import create_file_hash


class FileRenamerTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_file_path = os.path.join(os.getcwd(), 'mock_file.pdf')
        self._create_mock_file()

    def _create_mock_file(self):
        with open(self.mock_file_path, 'w') as f:
            f.write('Example file')

    def test_create_file_hash(self):
        expected = 'ef8bd64e7142cdfda9ee236f041cc5bdf857191c'
        actual = create_file_hash(self.mock_file_path)
        self.assertEqual(expected, actual)

    def tearDown(self):
        os.remove(self.mock_file_path)


if __name__ == '__main__':
    unittest.main()
