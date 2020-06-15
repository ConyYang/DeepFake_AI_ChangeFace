import argparse
import json
import os
import time
from pathlib import Path

from tqdm import tqdm
from selenium import webdriver

website = 'https://www.google.com/imghp?hl=en&&q={}'


class Size:
    LARGE = 'tbs=isz%3Al'
    MEDIUM = 'tbs=isz%3Am'
    ICON = 'tbs=isz%3Ai'


def init_dir(dir_name):
    path = Path(dir_name)
    path.mkdir(parents=True, exist_ok=True)
    os.chdir(path)


def search_keyword(args):
    web_link = website.format(args.keyword)
    if args.size == 'L':
        web_link += f'&{Size.LARGE}'
    elif args.size == 'M':
        web_link += f'&{Size.MEDIUM}'
    elif args.size == 'I':
        web_link += f'&{Size.ICON}'

    driver.get(web_link)
    driver.find_element_by_css_selector('#sbtc > button').click()


def obtain_image_src(timeout: float = 30):
    tock = tick = time.time()
    image_src = ''

    # get src of the image from side bar of big image
    while tock - tick < timeout:  # skip for timeout

        # get for image loading
        element_style = driver.find_element_by_css_selector(
            '#Sva75c > div > div > div.pxAole > div.tvh9oe.BIB1wf > c-wiz > div.OUZ5W > div.zjoqD > div > '
            'div.v4dQwb > div'
        ).get_attribute('style')

        # Check for loading. If the image finishes loading, the below div style will be set to `display:none`.
        if 'none' in element_style:  # finish loading.
            # wait for page reload
            time.sleep(0.2)
            image_src: str = driver.find_element_by_css_selector(
                '#Sva75c > div > div > div.pxAole > div.tvh9oe.BIB1wf > c-wiz > div.OUZ5W > div.zjoqD > div '
                '> div.v4dQwb > a > img'
            ).get_attribute('src')
            break
        else:
            time.sleep(1)
            tock = time.time()

    return image_src


def fetch_image(args):
    init_dir(args.output)
    search_keyword(args)

    image = list()
    image_counter = index = 0

    # verbose
    t = tqdm(total=args.image_num)
    while image_counter < args.image_num:
        try:
            index += 1

            # find image tag and click
            driver.find_element_by_css_selector(
                f'#islrg > div.islrc > div:nth-child({index}) > a.wXeWr.islib.nfEiy.mM5pbd > div.bRMDJf.islir > img'
            ).click()
            image_src = obtain_image_src()

            image.append(image_src)
            image_counter += 1

            # update verbose
            t.update()
        except:  # fetched a related search tag, pass
            pass

    driver.close()

    print('Saving...')
    with open('src.json', 'w') as f:
        json.dump(image, f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetching images from Google.')
    parser.add_argument('-o', '--output', type=str, default='dataset/WuJing3', help='Image saving directory. Default to "image".')
    parser.add_argument('-num', '--image-num', type=int, default=200, help='Fetching image number.')
    parser.add_argument('-k', '--keyword', type=str, required=True,  help='Search keyword')
    parser.add_argument(
        '--size', type=str, default='',
        help='Search option: image size. Options are: L (large), M (medium) and I (icon)'
    )
    args_ = parser.parse_args()

    driver = webdriver.Chrome()
    driver.implicitly_wait(0.1)
    fetch_image(args=args_)
