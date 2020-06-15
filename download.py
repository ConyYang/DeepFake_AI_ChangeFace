import argparse
import base64
import json
import os
import re
from pathlib import Path
from typing import List

import requests
from tqdm import tqdm


def download(name):
    path = Path(name)
    path.mkdir(exist_ok=True, parents=True)
    os.chdir(name)

    with open('src.json') as f:
        image_list: List[str] = json.load(f)

    for i, image_src in enumerate(tqdm(image_list), 1):
        try:
            if image_src.startswith('data:image'):  # base64
                matched = re.search(r'^data:image/([a-zA-Z]+);base64,(.*)$', image_src)
                ext = matched.group(1)
                b64_string = matched.group(2)

                image_binary = base64.b64decode(b64_string)
            else:
                ext = image_src.split('.')[-1]
                if len(ext) > 4:
                    ext = 'png'
                response = requests.get(image_src)
                image_binary = response.content

            with open(f'{i}.{ext}', 'wb') as f:
                f.write(image_binary)
        except:
            pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetching images from Google.')
    parser.add_argument(
        'output', metavar='N', nargs='?', type=str, default='Image', help='Image saving directory. Default to "image".'
    )
    args_ = parser.parse_args()

    download(args_.output)
