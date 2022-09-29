from . import auth_bluetprint
from flask.views import MethodView
from flask import make_response, request, jsonify
from app.models import User

class RegistrationView(MethodView):
    """This class registers a new user."""

    def post(self):
        """handle POST request for this view | /auth/register """

        # Query to check if the user already exists

        user = User.query.filter_by(email=request.data['email']).first()

        if not user:
            try:
                post_data = request.data
                email = post_data['email']
                password = post_data['password']
                user = User(email=email, password=password)
                user.save()

                response = {
                    'message': 'You registered succssfully. Please log in'
                }
                return make_response(jsonify(response)), 201

            except Exception as e:
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 401
        
        else:
            response = {
                'message': 'User already exists. Please login.'
            }

            return make_response(jsonify(response)), 202   


class LoginView(MethodView):
    """This class-based view handles user login and access token generation."""
    def post():
        try:
            # get a user object using their email
            user = User.query.filter_by(email=request.data['email']).first()

            # try to authenticate the found user using their password
            if user and user.password_is_valid(request.data['password']):
                # generate the access token. 
                access_token = user.generate_token(user.id)
                if access_token:
                    response = {
                        'message': 'You logged in successfully',
                        'access_token': access_token.decode()
                    }
                    return make_response(jsonify(response)), 200
            else:
                # user does not exist
                response = {
                    'message': 'Invalid email or password, Please try again.'
                }
                return make_response(jsonify(response)), 401
        
        except Exception as e:
            # create a response containing an string error message
            response = {
                'message': str(e)
            }
            # return a sever error
            return make_response(jsonify(response)), 500

registration_view = RegistrationView.as_view('register_view')
login_view = LoginView.as_view('login_view')

auth_bluetprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST']
)

auth_bluetprint.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST']
)