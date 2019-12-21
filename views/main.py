# -*- coding:utf-8 -*-
from flask import Blueprint, render_template

main = Blueprint('main', __name__,
                 template_folder='../view_main',
                 static_folder='../view_main/static',
                 url_prefix='/wechat')


@main.route('/<view>')
def catch_view(view):
    if view == 'error':
        return '请从微信公众号进入'
    return render_template('main.html')
