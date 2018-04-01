from lxml import etree, html
from urllib.parse import urlparse, urljoin
import requests


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



