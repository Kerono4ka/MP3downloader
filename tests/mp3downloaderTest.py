import unittest
from os import path
from mp3downloader import *


class TestMp3Downloader(unittest.TestCase):
    def test_load_urls_from_xml_file(self):
        test_file_name = path.join(path.dirname(path.realpath(__file__)),
                                   path.join("Resources", "test-0.xml"))
        urls = load_urls_from_xml_file(test_file_name)
        expect_urls = [
            {'source': 'http://mp3cc.com/',
             'value': 'http://mp3cc.com/',
             'depth': 1
             }]
        self.assertEqual(expect_urls, urls)

    def test_get_mp3_links_and_potential_urls_from_html(self):
        test_file_name = path.join(path.dirname(path.realpath(__file__)),
                                   path.join("Resources", "test-0.html"))
        with open(test_file_name) as file:
            html_text = file.read()

        current_url = {
            'source': 'http://mp3cc.com/',
            'value': 'http://mp3cc.com/', 'depth': 2
        }
        filename_link = path.join(path.dirname(path.realpath(__file__)),
                                  path.join("Resources", "test-mp3-link.txt"))
        with open(filename_link) as file:
            test_link = file.read()

        expected_mp3_links = [{'link': test_link,
                               'source': 'http://mp3cc.com/'}]
        expected_potential_urls = [
            {
             'source': 'http://mp3cc.com/',
             'value': '/online_radio/russia/',
             'depth': 1
             },
            {
             'source': 'http://mp3cc.com/',
             'value': '/music_genre/russian_top/',
             'depth': 1
            }
        ]

        source = 'http://mp3cc.com/'
        result = get_mp3_links_and_potential_urls_from_html(html_text,
                                                            current_url,
                                                            source)
        self.assertEqual(expected_mp3_links, result['mp3_links'])
        self.assertEqual(expected_potential_urls, result['potential_urls'])

    def test_get_id3_info_from_mp3_file(self):
        test_file_name = path.join(path.dirname(path.realpath(__file__)),
                                   path.join("Resources", "test-song.mp3"))
        expected_id3_info = {
            'title': "Ain't It Fun (The Dead Boys cover)",
            'album': "Toggle 80'S Hair Metal Band: Guns 'N Roses",
            'artist': "Guns N' Roses",
            'genre': "Hair Metal"
        }
        id3_info = get_id3_info_from_mp3_file(test_file_name)
        self.assertEqual(expected_id3_info, id3_info)

    def test_load_mp3_links_from_urls(self):
        urls = [
            {
             'source': 'http://mp3cc.com/',
             'value': 'http://mp3cc.com/',
             'depth': 1
            }
        ]
        try:
            mp3_links = load_mp3_links_from_urls(urls)
            self.assertEqual(30, len(mp3_links))
        except Exception as e:
            self.assertEqual(str(e), "No connection with internet")

    def test_load_mp3_files_from_links(self):
        filename_link = path.join(path.dirname(path.realpath(__file__)),
                                  path.join("Resources", "test-mp3-link.txt"))
        with open(filename_link) as file:
            test_link = file.read()

        links = [{'link': test_link, 'source': 'http://mp3cc.com/'}]
        try:
            mp3_files = load_mp3_files_from_links(links, 'songs')
            self.assertEqual(1, len(mp3_files))

            if os.path.exists(mp3_files[0]['path']):
                os.remove(mp3_files[0]['path'])
                os.removedirs('songs')
            else:
                self.assertTrue(os.path.exists(mp3_files[0]['path']))

        except Exception as e:
            self.assertEqual(str(e), "No connection with internet")

    def test_filter_mp3_files_by_genre(self):
        mp3_files = [
            {
                'title': "Ain't It Fun (The Dead Boys cover)",
                'album': "Toggle 80'S Hair Metal Band: Guns 'N Roses",
                'artist': "Guns N' Roses",
                'genre': "Hair Metal",
                'path': "folder/file01.mp3"
            },
            {
                'title': "Swish swish",
                'album': "Katy Perry",
                'artist': "Katy Perry",
                'genre': "Pop",
                'path': "folder/file02.mp3"
            },
            {
                'title': "Dolce Gabbana",
                'album': "Dolce Gabbana",
                'artist': "Verka Serdyuchka",
                'genre': "Pop",
                'path': "folder/file03.mp3"
            }
        ]
        expected_mp3_files = [{
            'title': "Swish swish",
            'album': "Katy Perry",
            'artist': "Katy Perry",
            'genre': "Pop",
            'path': "folder/file02.mp3"
        },
            {
                'title': "Dolce Gabbana",
                'album': "Dolce Gabbana",
                'artist': "Verka Serdyuchka",
                'genre': "Pop",
                'path': "folder/file03.mp3"
            }]

        result = filter_mp3_files_by_genre(mp3_files, "Pop")

        self.assertEqual(expected_mp3_files, result)

    def test_save_mp3_files_to_xml(self):
        mp3_files = [
            {
                'title': "Swish swish",
                'album': "Katy Perry",
                'artist': "Katy Perry",
                'genre': "Pop",
                'path': "folder/file02.mp3"
            },
            {
                'title': "Dolce Gabbana",
                'album': "Dolce Gabbana",
                'artist': "Verka Serdyuchka",
                'genre': "Pop",
                'path': "folder/file03.mp3"
            }
        ]

        file_name = "pop-songs.xml"

        save_mp3_files_to_xml(mp3_files,
                              path.dirname(path.realpath(__file__)),
                              filename=file_name)

        file_path = path.join(path.dirname(path.realpath(__file__)), file_name)
        self.assertTrue(os.path.exists(file_path))

        with open(file_path) as file:
            result = file.read()

        os.remove(file_path)
        test_filename = path.join(path.dirname(path.realpath(__file__)),
                                  path.join("Resources", "test-pop-songs.xml"))

        with open(test_filename) as file:
            expected_result = file.read()

        self.assertEqual(expected_result, result)
