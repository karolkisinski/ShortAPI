import os
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort, redirect, make_response
import auth
from instance.config import app_config

db = SQLAlchemy()

def create_app(config_name):
    from app.models import ShortURL, User

    app = FlaskAPI(__name__, instance_path=os.path.join(os.path.abspath(os.curdir), 'instance'), instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/urllist/', methods=['POST', 'GET'])
    def urllist():
        # get the access token from the header
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            # attemp to decode the token and get the user id
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):

                # POST
                if request.method == "POST":
                    title = str(request.data.get('title', ''))
                    url = str(request.data.get('url', ''))
                    if title:
                        url_list = ShortURL(title=title, url=url)
                        url_list.save()
                        response = jsonify({
                            'id': url_list.id,
                            'title': url_list.title,
                            'url': url_list.url,
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
            else:
                # user is not legit
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401
    
    @app.route('/urllist/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def urllist_manipulation(id, **kwargs):
        # get the access token from the header
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            # attemp to decode the token and get the user id
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):

                urllist = ShortURL.query.filter_by(id=id).first()

                if not urllist:
                    abort(404)
                
                if request.method == 'DELETE':
                    urllist.delete()
                    return {
                        "message": "urllist {} deleted successfully".format(urllist.id)
                    }, 200

                elif request.method == 'PUT':
                    title = str(request.data.get('title', ''))
                    urllist.title = title
                    urllist.save()
                    response = jsonify({
                        'id': urllist.id,
                        'title': urllist.title,
                        'url': urllist.url,
                        'short_url': urllist.short_url
                    })
                    response.status_code = 200
                    return response
                
                else:
                    # GET
                    response = jsonify({
                        'id': urllist.id,
                        'title': urllist.title,
                        'url': urllist.url,
                        'short_url': urllist.short_url
                    })
                    response.status_code = 200
                    return response
        else:
                # user is not legit
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401
    
    from auth import auth_bluetprint
    app.register_blueprint(auth_bluetprint)

    return app
