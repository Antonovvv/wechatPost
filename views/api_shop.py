# -*- coding:utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os

from flask import Blueprint, request, abort, jsonify

import requests
import json

from config import *
from utils import get_filename_from_header

from ext import database as db
from ext import logger
from models import ImageFile
from app import client

api = Blueprint('api_shop', __name__, url_prefix='/api/shop')


'''
@api.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        uploaded_files = request.files['files']
        postname = request.form['postname']
        filename = request.form['filename']
        nickname = request.form['nickname']
        openid = request.form['openid']
        logger.info(openid)
        logger.info(uploaded_files)
        # if openid == 'null':
        #    return abort(400)
        # try:
        for file in uploaded_files:
            image_file = ImageFile.create_by_upload_file(file, postname,
                                                         filename, nickname, openid)
            logger.info(image_file)
            db.session.add(image_file)
            db.session.commit()

        return jsonify({
            'url': image_file.url,
            'imgname': image_file.imgname,
            'openid': image_file.openid,
            'time': str(image_file.uploadtime)
        })

        except:
            return jsonify({
                'error': 'failed'
            })

    return 'API Page'
    '''


@api.route('/posts', methods=['GET'])
def posts():
    sortby = request.args.get('sortby', '')
    resp = {}
    data = []

    if sortby == 'liked':
        # 按liked排序
        postlist = ImageFile.get_hot(100)
    else:
        # 直接查询
        postlist = ImageFile.get_all()
        if not postlist:
            return jsonify({
                'empty': 'true'
            })

    for index, item in enumerate(postlist):
        post = {}
        post['filehash'] = item.filehash
        post['imgname'] = item.imgname
        post['nickname'] = item.nickname
        post['uploadtime'] = item.uploadtime
        post['liked'] = item.liked
        post['dorm'] = item.dorm
        data.append(post)
    resp['data'] = data
    return jsonify(resp)
