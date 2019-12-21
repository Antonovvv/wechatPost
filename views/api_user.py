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

api = Blueprint('api_user', __name__, url_prefix='/api/user')


@api.route('/')
def get_user():
    code = request.args.get('code', '')
    if code != '':
        open_url = 'https://api.weixin.qq.com/sns/oauth2/access_token?' \
                   + 'appid={}&secret={}&code={}&grant_type=authorization_code'
        access_token_url = open_url.format(APPID, APPSECRET, code)
        resp = requests.get(access_token_url)
        access_data = json.loads(resp.text)
        openid = access_data['openid']
        resp_user = client.user.get(openid)
        # logger.info(resp_user)
        return jsonify(resp_user)
    else:
        return abort(403)


@api.route('/my', methods=['GET', 'POST', 'DELETE'])
def my():
    if request.method == 'GET':
        # 获取该用户的上传记录
        openid = request.args.get('openid', '')
        imglist = ImageFile.get_by_openid(openid)
        resp = {}
        data = []
        if not imglist:
            return jsonify({
                'empty': 'true'
            })
        else:
            for index, item in enumerate(imglist):
                post = {}
                post['filehash'] = item.filehash
                post['imgname'] = item.imgname
                post['uploadtime'] = item.uploadtime
                post['liked'] = item.liked
                data.append(post)
            resp['data'] = data
            return jsonify(resp)

    elif request.method == 'POST':
        # 上传
        postname = request.form['postname']
        nickname = request.form['nickname']
        openid = request.form['openid']
        dorm = request.form['dorm']
        serverids = request.form.getlist('serverids[]')
        # logger.info(serverids)
        for serverid in serverids:
            url = client.media.get_url(serverid)
            # logger.info(url)

            data = client.media.download(serverid)
            logger.info(data.headers)

            filename = get_filename_from_header(data.headers['Content-disposition'])

            image_file = ImageFile.create_by_upload_file(data.content, postname, filename,
                                                         nickname, openid, dorm)
            # logger.info(image_file)
            db.session.add(image_file)
            db.session.commit()

        return jsonify({
            'openid': openid
        })

    elif request.method == 'DELETE':
        # 删除一条记录
        filehash = request.args.get('filehash')
        choosen_img = ImageFile.get_by_filehash(filehash)
        try:
            db.session.delete(choosen_img)
            os.remove(choosen_img.path)
            os.remove(choosen_img.nail_path)
            db.session.commit()
            return jsonify({
                'deleted': 'true'
            })

        except:
            return jsonify({
                'deleted': 'false'
            })


@api.route('/actions', methods=['PATCH'])
def actions():
    action = request.form['action']
    logger.info('action: ' + action)

    if action == 'like':
        filehash = request.form['filehash']
        s = ImageFile.like_handler(filehash)
        if s:
            db.session.commit()
            return jsonify({
                'liked': 'true'
            })
        else:
            return jsonify({
                'liked': 'false'
            })
