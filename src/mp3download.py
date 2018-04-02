from lxml import etree, html
from urllib.parse import urlparse, urljoin
import requests
import os
import eyed3

def load_urls_from_xml_file(path):

    urls = []
    with open(path) as file:
        xml = file.read()

    root = etree.fromstring(xml)

    for url in root.getchildren():
        if url.text:
            text = url.text
        else:
            text = ""
        if url.attrib['depth']:
            depth = int(url.attrib['depth'])
        else:
            depth = 1

        parsed_uri = urlparse(text)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        urls.append({'source': domain, 'value': text, 'depth': depth});

    return urls


def load_mp3_links_from_urls(urls):

    mp3_links = []
    potential_urls = []

    for url in urls:
        try:
            url_path = urljoin(url['source'], url['value'])
            r = requests.get(url_path)

            result = get_mp3_links_and_potential_urls_from_html(r.text, url, url_path)
            mp3_links += result['mp3_links']
            potential_urls += result['potential_urls']
        except Exception:
            print("Can't  download " + url['value'])

    if potential_urls:
        mp3_links += load_mp3_links_from_urls(potential_urls)

    return mp3_links


def get_mp3_links_and_potential_urls_from_html(html_text, current_url, current_url_path):
    result = {}

    mp3_links = []
    potential_urls = []

    root = html.fromstring(html_text)
    links = root.xpath('//a')

    for link in links:
        if link.attrib['href']:
            if link.attrib['href'].endswith('.mp3'):
                mp3_links.append(
                    {'link': urljoin(current_url['source'], link.attrib['href']), 'source': current_url['value']})
            elif current_url['depth'] > 1 and not link.attrib['href'].startswith('javascript:') and \
                    current_url_path != urljoin(current_url['source'], link.attrib['href']):
                potential_urls.append({'source': current_url['source'],
                                       'value': link.attrib['href'],
                                       'depth': current_url['depth'] - 1})

    result['mp3_links'] = mp3_links
    result['potential_urls'] = potential_urls

    return result


def load_mp3_files_from_links(links, output_path):
    mp3_files = []

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for link in links:
        file_name = link['link'].rsplit('/', 1)[1]
        file_path = os.path.join(output_path, file_name)
        try:
            r = requests.get(link['link'], stream=True)
            song = r.content

            with open(file_path, 'wb') as file:
                file.write(song)
                print("File downloaded successfully: " + file_name + " as " + file_path)

            song_info = get_id3_info_from_mp3_file(file_path)
            song_info['path'] = file_path

            mp3_files.append(song_info)
        except Exception:
            print("File WAS NOT downloaded successfully: " + file_name + " as " + file_path)

    return mp3_files


def get_id3_info_from_mp3_file(mp3_file_path):
    id3_info = {}
    mp3_file = eyed3.load(mp3_file_path)

    id3_info['title'] = mp3_file.tag.title
    id3_info['artist'] = mp3_file.tag.artist
    id3_info['album'] = mp3_file.tag.album

    if mp3_file.tag.genre:
        id3_info['genre'] = mp3_file.tag.genre.name
    else:
        id3_info['genre'] = ""

    return id3_info


def filter_mp3_files_by_genre(mp3_files, genre):

    result = []

    for mp3_file in mp3_files:
        if mp3_file['genre'] == genre:
            result.append(mp3_file)

    return result


def save_mp3_files_to_xml(mp3_files, output_path, **kwargs):
    file_name = kwargs.get('filename', None)

    if not file_name:
        file_name = "songs.xml"

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    page = etree.Element('songs')
    xml_doc = etree.ElementTree(page)
    for mp3_file in mp3_files:
        etree.SubElement(page, 'song',
                         title=mp3_file['title'],
                         artist=mp3_file['artist'],
                         genre=mp3_file['genre'],
                         path=mp3_file['path'])

    xml_string = etree.tostring(xml_doc, pretty_print=True, xml_declaration=True, encoding="UTF-8")

    file_name = os.path.join(output_path, file_name)
    with open(file_name, 'wb') as file:
        file.write(xml_string)


def load_mp3_files_and_filter_by_genre(xml_filename, genre):
    urls = load_urls_from_xml_file(xml_filename)
    mp3_links = load_mp3_links_from_urls(urls)

    for link in mp3_links:
        print(link['link'])

    print("Total links: " + str(len(mp3_links)))

    mp3_files = load_mp3_files_from_links(mp3_links, "songs")
    mp3_files = filter_mp3_files_by_genre(mp3_files, genre)

    save_mp3_files_to_xml(mp3_files, "songs", filename=genre.lower() + "-songs.xml")


load_mp3_files_and_filter_by_genre("mp3links.xml", "Rock")



