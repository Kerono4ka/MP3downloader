import unittest
from src.mp3downloader.mp3downloader import *


class TestMp3Downloader(unittest.TestCase):

    def test_load_urls_from_xml(self):
        test_file_name = os.path.join("Resources", "test-0.xml")
        urls = load_urls_from_xml_file(test_file_name)
        expect_urls = [{'source': 'http://mp3cc.com/', 'value': 'http://mp3cc.com/', 'depth': 1}]
        self.assertEqual(expect_urls, urls)


if __name__ == '__main__':
    unittest.main()
