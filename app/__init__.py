import os
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort
from instance.config import app_config

db = SQLAlchemy()

def create_app(config_name):
    from app.models import ShortURL

    app = FlaskAPI(__name__, instance_path=os.path.join(os.path.abspath(os.curdir), 'instance'), instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/urllist/', methods=['POST', 'GET'])
    def urllist():
        if request.method == "POST":
            title = str(request.data.get('title', ''))
            url = str(request.data.get('url', ''))
            short_url = str(request.data.get('short_url', ''))
            if title:
                url_list = ShortURL(title=title, url=url, short_url=short_url)
                url_list.save()
                response = jsonify({
                    'id': url_list.id,
                    'title': url_list.title,
                    'url': url_list.url,
                    'short_url': url_list.short_url,
                    'date_created': url_list.date_created
                })
                response.status_code = 201
                return response
        else:
            # GET
            url_lists = ShortURL.get_all()
            results = []

            for url in url_lists:
                obj = {
                    'id': url.id,
                    'title': url.title,
                    'url': url.url,
                    'short_url': url.short_url,
                    'date_created': url.date_created
                }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response

    return app
