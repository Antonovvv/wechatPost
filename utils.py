# -*- coding:utf-8 -*-
import os
import time
import random
import string
from functools import partial

from config import UPLOAD_FOLDER, THUMBNAIL_FOLDER

get_file_path = partial(os.path.join, UPLOAD_FOLDER)
get_nail_path = partial(os.path.join, THUMBNAIL_FOLDER)


def get_filename_from_header(header):
    # 'Content-disposition': 'attachment; filename="xxx.jpg"'
    _, _, fileinfo = header.partition(';')
    _, _, filequote = fileinfo.partition('=')
    filename = filequote[1:-1]
    return filename


def humanize_bytes(bytesize, precision=2):
    # 缩写
    abbrevs = (
        (1 << 50, 'PB'),
        (1 << 40, 'TB'),
        (1 << 30, 'GB'),
        (1 << 20, 'MB'),
        (1 << 10, 'KB'),
        (1, 'bytes')
    )
    if bytesize == 1:
        return '1 bytes'
    for factor, suffix in abbrevs:
        if bytesize >= factor:
            break
    return '{:.{}f} {}'.format(bytesize / factor, precision, suffix)


def create_nonce_str():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))


def create_timestamp():
    return int(time.time())
