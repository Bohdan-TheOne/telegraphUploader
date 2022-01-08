'''Publish images to telegraph'''
from os import listdir, path
from json import load as json_load
from telegraph import Telegraph
import requests
from func import ProgressBar
from dict_to_class import Converter


def get_config(file_path=None):
    '''Get configuration data from file'''
    file_path = file_path or 'config.txt'
    with open(file_path, 'r', encoding='utf-8') as f:
        return Converter.dict2class(json_load(f))


def telegraph_auth(config):
    '''Authenticate telegraph account'''
    telegraph = Telegraph(config.auth_token)
    return telegraph


def upload_img(img_path):
    '''publish image to telegraph'''
    with open(img_path, 'rb') as f:
        request = requests.post('https://telegra.ph/upload',
                                files={'file': ('file', f, 'image/jpeg')})
        return request.json()[0]['src']


def create_html(config):
    '''create article html'''
    images = [f'{config.img_folder}/{i}'
              for i in listdir(config.img_folder)
              if path.isfile(f'{config.img_folder}/{i}')]

    progress_bar = ProgressBar(len(images))
    img_urls = [(upload_img(img), progress_bar.print(i+1))[0]
                for i, img in enumerate(images)]

    return '<img src="' + '"/><img src="'.join(img_urls) + '"/>'


def main():
    '''main function'''
    config = get_config()
    html_page = create_html(config)
    print(html_page)

    telegraph = telegraph_auth(config)
    response = telegraph.create_page(
        config.title,  # pylint: disable=no-member
        html_content=html_page,
        author_name=config.author_name  # pylint: disable=no-member
    )
    # pylint: disable=no-member
    with open(config.output_file, 'w', encoding='utf-8') as f:
        f.write(f'http://telegra.ph/{response["path"]}')


if __name__ == '__main__':
    main()
