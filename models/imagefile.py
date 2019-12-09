# -*- coding:utf-8 -*-
import os
import uuid
from datetime import datetime

from PIL import Image
from urllib.parse import quote

from flask import abort, request

from utils import get_file_path, get_nail_path
from ext import database as db


class ImageFile(db.Model):
    __tablename__ = 'ImageFile'
    id = db.Column(db.Integer, primary_key=True)
    imgname = db.Column(db.String(1000), nullable=False)
    filename = db.Column(db.String(1000), nullable=False)
    filehash = db.Column(db.String(128), nullable=False, unique=True)
    nickname = db.Column(db.String(128), nullable=False)
    openid = db.Column(db.String(128), nullable=False)
    dorm = db.Column(db.String(128), nullable=False)
    uploadtime = db.Column(db.DateTime, nullable=False)
    size = db.Column(db.Integer, nullable=False)
    liked = db.Column(db.Integer, nullable=False)

    def __init__(self, imgname='', filename='', nickname='', openid='', dorm='', size=0, liked=0):
        self.imgname = imgname
        self.filename = filename
        self.filehash = self._hash_filename(filename)
        self.nickname = nickname
        self.openid = openid
        self.dorm = dorm
        self.uploadtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.size = int(size)
        self.liked = liked

    @staticmethod
    def _hash_filename(filename):
        # 获得文件名后缀
        _, _, suffix = filename.rpartition('.')
        return '{}.{}'.format(uuid.uuid4().hex, suffix)

    @property
    def path(self):
        return get_file_path(self.filehash)

    @property
    def nail_path(self):
        return get_nail_path(self.filehash)

    @property
    def url(self):
        return self.get_url()

    @property
    def quote_url(self):
        return quote(self.url)

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_filehash(cls, filehash, code=404):
        return cls.query.filter_by(filehash=filehash).first() or abort(code)

    @classmethod
    def get_by_openid(cls, openid):
        return cls.query.filter_by(openid=openid).all()

    @classmethod
    def get_hot(cls, count, code=404):
        return cls.query.order_by(cls.liked.desc()).limit(count) or abort(code)

    @classmethod
    def like_handler(cls, filehash):
        target = cls.query.filter_by(filehash=filehash).first()
        target.liked += 1
        return True

    @classmethod
    def create_by_upload_file(cls, uploaded_file, imgname, filename, nickname, openid, dorm):
        res = cls(imgname, filename, nickname, openid, dorm, 0, 0)
        with open(res.path, 'wb') as f:
            f.write(uploaded_file)
        # uploaded_file.save(res.path)

        thumb = Image.open(res.path)
        thumb.thumbnail((300, 300))
        thumb.save(res.nail_path)

        filestat = os.stat(res.path)
        res.size = filestat.st_size
        return res

    def get_url(self):
        return 'http://{host}/image/{id}'.format(
            host=request.host, id=self.id)
