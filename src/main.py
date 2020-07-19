#!/usr/bin/env python3
import os
import re
import sys

import requests
from bs4 import BeautifulSoup

DOMEN = 'https://unsplash.com/s/photos/'


def download_image_from_url(url, name, load_dir):
    with open(f'{load_dir}/{name}.jpg', 'wb') as handle:
        response = requests.get(url, stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)


def download_images(keywords, load_dir='./bg-downloads', orientation=None, limit=None):
    for keyword in keywords:
        if not os.path.exists(load_dir):
            os.mkdir(load_dir)
        if not os.path.exists(f'{load_dir}/{keyword}'):
            os.mkdir(f'{load_dir}/{keyword}')

        print(f'\nDownloading images on keyword "{keyword}".')

        request = DOMEN + keyword.replace(' ', '-') + f'?orientation={orientation}' if orientation else ''
        response = requests.get(request)

        soup = BeautifulSoup(response.content, 'html.parser')

        links = [link.get('href') for link in soup.find_all(
            'a',
            attrs={'href': re.compile("^https://")}
        )[1:]]

        i = 0
        for link in links:
            print(f'\r>> Downloading image {i + 1} of {min(len(links), limit if limit else 100)}...', end='')
            download_image_from_url(link, f'{keyword}-{i + 1}', f'{load_dir}/{keyword}')
            i += 1

            if limit:
                if i >= limit:
                    break


def main():
    args = sys.argv

    if len(args) == 1:
        print('>> No input parameters specified!')
        return

    orientation = None
    limit = None
    keywords = []
    load_dir = './bg-downloads'

    i = 1
    while i < len(args):
        arg = args[i]
        if arg == '--help':
            print(
                '\n'
                'Hello and welcome to BGD - I will help you manage your backgrounds as CLI!\n'
                '\n'
                '--help opens help info\n'
                '--landscape, --portrait and --square are setting your orientation preferences\n'
                '--limit <n> set a limit of <n> photos for each topic\n'
                '--dir </path/to/dir> sets a directory to download photos\n'
                '\n'
                'Example usage:\n'
                '$ bgd "cute cats" --landscape --dir ~/backgrounds --limit 5\n'
                '\n'
                'Cheers!'
            )
            return
        elif arg == '--landscape':
            orientation = 'landscape'
        elif arg == '--portrait':
            if orientation:
                print(f'Overriding option --{orientation} to {arg}.')
            orientation = 'portrait'
        elif arg == '--square':
            if orientation:
                print(f'Overriding option --{orientation} to {arg}.')
            orientation = 'square'
        elif arg == '--limit':
            limit = int(args[i+1])
            i += 1
        elif arg == '--dir':
            load_dir = args[i+1]
            i += 1
        else:
            keywords.append(arg)

        i += 1

    print(f'Your configurations:\n'
          f'Keywords: {keywords}\n'
          f'Orientation: {orientation if orientation else "Any"}\n'
          f'Limit: {limit}\n'
          f'Folder for photos: {os.path.abspath(load_dir)}\n')

    resp = str(input('Proceed? (yes/no)'))
    if resp.lower() == 'y' or resp.lower() == 'yes':
        download_images(
            keywords=keywords,
            load_dir=load_dir,
            orientation=orientation,
            limit=limit
        )
        print('\nDone.')
    else:
        print('''O'kay, terminating.''')


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
