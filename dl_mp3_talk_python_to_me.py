#! python3

import os

import regex as re
import requests
from tqdm import tqdm

destination = input('\nPlease enter the path where you would\n'
                    'like to store the downloaded files: ')

pattern_show = re.compile(r'/episodes/show/\d+/[\w.\s-]+')

episode_cache = r'https://downloads.talkpython.fm/episodes/download'
home_page = r'https://talkpython.fm'
list_page = r'https://talkpython.fm/episodes/all'

page = requests.get(list_page)
show_links = re.findall(pattern_show, page.text)


def download_file(url, local_filename):
    chunk_size = 1024
    with requests.get(url, stream=True) as r:
        total_size = int(r.headers['content-length'])
        with open(local_filename, 'wb') as f:
            for data in tqdm(iterable=r.iter_content(chunk_size=chunk_size),
                             total=total_size / chunk_size,
                             unit='KB'):
                f.write(data)
    return local_filename


for link in show_links:
    show_page = home_page + link
    show_link = show_page + '.mp3'
    download_link = show_link.replace('show', 'download')
    print(download_link)

    grab = download_link[40:]
    filename = (grab[:grab.index('/')].zfill(4) + grab[grab.index('/'):]).replace('/', '_')
    print(filename)

    if filename not in os.listdir(destination):
        download_file(download_link, os.path.join(destination, filename))
        print("Download complete: ", filename)
        print()

