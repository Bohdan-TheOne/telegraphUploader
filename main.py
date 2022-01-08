'''Publish images to telegraph'''
from os import listdir, path
from collections import namedtuple
from json import load as json_load
from telegraph import Telegraph
import requests
from func import ProgressBar

PublishInfo = namedtuple("PublishInfo",
                         ["title", "auth_name", "auth_name_sh", "img_folder"])
info = PublishInfo(
    'Test',
    'Zumori',
    'Zumori',
    'img'
)


def telegraph_auth():
    '''Authenticate telegraph account'''
    with open('authentification.json', 'r', encoding='utf-8') as f:
        token = json_load(f)['main']
    telegraph = Telegraph(token)
    telegraph.create_account(short_name=info.auth_name_sh,
                             author_name=info.auth_name, replace_token=False)
    return telegraph


def upload_img(img_path):
    '''publish image to telegraph'''
    with open(img_path, 'rb') as f:
        request = requests.post('https://telegra.ph/upload',
                                files={'file': ('file', f, 'image/jpeg')})
        return request.json()[0]['src']


def create_html():
    '''create article html'''
    images = [f'{info.img_folder}/{i}'
              for i in listdir(info.img_folder)
              if path.isfile(f'{info.img_folder}/{i}')]

    progress_bar = ProgressBar(len(images))
    img_urls = [(upload_img(img), progress_bar.print(i+1))[0]
                for i, img in enumerate(images)]

    return '<img src="' + '"/><img src="'.join(img_urls) + '"/>'


def main():
    '''main function'''
    html_page = create_html()
    print(html_page)

    telegraph = telegraph_auth()
    response = telegraph.create_page(
        info.title,
        html_content='hentai test'
    )
    print(f'http://telegra.ph/{response["path"]}')


if __name__ == '__main__':
    main()
