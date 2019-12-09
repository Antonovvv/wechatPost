# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os
from random import *
# from datetime import timedelta

from flask import Flask, request, abort, jsonify, redirect
# from flask_session import Session

# from flask_cors import CORS
import requests
from urllib.parse import quote
import json

from wechatpy import parse_message, create_reply
from wechatpy import WeChatClient
from wechatpy.utils import check_signature
# from wechatpy.oauth import WeChatOAuth
from wechatpy.exceptions import (
    InvalidSignatureException,
    InvalidAppIdException,
)

# import redis
from werkzeug.utils import import_string

from config import *
from utils import create_nonce_str, create_timestamp
# from emotion_rec.emotion import Emotion
from ext import database as db
from ext import logger
from models import ImageFile

blueprints = [
    'views.main:main',
    'views.api_shop:api',
    'views.api_user:api'
]
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS	'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db.init_app(app)
client = WeChatClient(APPID, APPSECRET)
waclient = WeChatClient(WAID, WASECRET)

for bp_name in blueprints:
    bp = import_string(bp_name)
    app.register_blueprint(bp)


'''
app.config['SESSION_USE_SIGNER'] = False
app.config['SECRET_KEY'] = 'salty980813'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)  # 保存一小时
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1', port='6379')
Session(app)

pool_0 = redis.ConnectionPool(host='127.0.0.1', port='6379', db=0)
pool_1 = redis.ConnectionPool(host='127.0.0.1', port='6379', db=1)
conn_user = redis.Redis(connection_pool=pool_0)
conn_text = redis.Redis(connection_pool=pool_1)
'''


@app.route('/')
def index():
    return 'sorry'


@app.route('/wechatapp')
def wea():
    code = request.args.get('code', '')
    res = waclient.wxa.code_to_session(code)
    logger.info(res)
    return jsonify(res['openid'])


@app.route('/oauth')
def oauth():
    view = request.args.get('view', 'shop')
    my_url = quote('http://www.yyandii.com/wechat/{}'.format(view), safe='')
    open_url = 'https://open.weixin.qq.com/connect/oauth2/authorize?'\
        + 'appid={}&redirect_uri={}&response_type=code'\
        + '&scope=snsapi_base&state=1024#wechat_redirect'
    redirect_url = open_url.format(APPID, my_url)
    return redirect(redirect_url)


@app.route('/jsapi')
def wx_js_sdk():
    # 返回weixin-js-sdk权限配置
    url = request.args.get('url')
    if not url:
        abort(404)
    ticket = client.jsapi.get_jsapi_ticket()
    noncestr = create_nonce_str()
    timestamp = create_timestamp()
    signature = client.jsapi.get_jsapi_signature(noncestr=noncestr, ticket=ticket,
                                                 timestamp=timestamp, url=url)
    return jsonify({
        'appId': APPID,
        'timestamp': timestamp,
        'nonceStr': noncestr,
        'signature': signature
    })


@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


@app.route('/wx', methods=['GET', 'POST'])
def wechat():
    signature = request.args.get('signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    try:
        check_signature(TOKEN, signature, timestamp, nonce)  # noqa
    except InvalidSignatureException:
        abort(403)
    if request.method == 'GET':
        echo_str = request.args.get('echostr', '')
        return echo_str

    else:
        push = parse_message(request.data)
        reply = create_reply('', message=push)
        '''
        if not conn_user.exists(push.source):
            conn_user.set(push.source, '')

        if push.type == 'event' and push.event == 'click':
            conn_user.set(push.source, push.key)
            conn_user.expire(push.source, 15)  # 30s to delete automatically
            if push.key == 'repeat':
                reply = create_reply('说话呀', message=push)
            elif push.key == 'emotion':
                reply = create_reply('说句话让俺瞧瞧', message=push)

        elif push.type == 'text':
            conn_text.rpush(push.source, push.content)
            if conn_user.get(push.source) == b"":
                reply = create_reply('闭嘴', message=push)

            else:
                conn_user.expire(push.source, 10)  # 30s to delete automatically
                if conn_user.get(push.source) == b"repeat":
                    reply = create_reply(push.content, message=push)

                elif conn_user.get(push.source) == b"emotion":
                    rec = Emotion(push.content)
                    recognized = rec.recognize()
                    reply = create_reply(recognized, message=push)
        '''
        return reply.render()


if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)
