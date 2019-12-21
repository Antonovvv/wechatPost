# -*- coding:utf-8 -*-
from flask import Blueprint, render_template

map = Blueprint('map', __name__,
                template_folder='../view_map',
                static_folder='../view_map/static',
                url_prefix='/map')


@map.route('/')
def map_page():
    return render_template('map.html')
