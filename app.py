from flask import Flask, redirect, request, render_template, make_response, jsonify
from flask_bootstrap import Bootstrap
from simple_settings import settings
from requests_oauthlib import OAuth2Session
from json import loads
from wtforms import Form, StringField, validators


# Set-up Flask application
app = Flask(__name__)
app.config.from_object(settings.as_dict())
Bootstrap(app)

# Initialize OAuth session
medium_oauth = OAuth2Session(settings.MEDIUM_CLIENT_ID,
                             redirect_uri=settings.MEDIUM_REDIRECT_URI,
                             scope=settings.MEDIUM_SCOPE)

# Just used as a marker to say we've authorized Medium, not needed in the session
access_token = None


class PostForm(Form):
    """ WTForms class to validate form
    """
    postdata = StringField('Medium Post as Markdown', [validators.Length(min=1)])


@app.errorhandler(Exception)
def unhandled_error(e):
    """ Generic exception handler
    :return:
    """
    response = make_response('Unhandled exception on server: {}'.format(str(e)), 500)
    response.headers['Content-Type'] = 'text/plain'
    return response


@app.route('/', methods=['GET'])
def index():
    """ Application homepage
    :return:
    """
    if access_token is None:
        url, state = medium_oauth.authorization_url(settings.MEDIUM_AUTHORIZATION_URL)
        return redirect(url)

    return render_template('index.html')


@app.route('/publish', methods=['POST'])
def publish():
    """ Post form data for submission to Medium
    :return:
    """
    form = PostForm(request.form)

    # Validate the form and carry on if good
    if form.validate():
        # Get the user ID for the current user
        try:
            user_id_response = medium_oauth.get('https://api.medium.com/v1/me')
            user_id = loads(user_id_response.content.decode('utf-8'))['data']['id']

        except KeyError:
            return make_response()

        except:
            raise

        # Post the data
        response = medium_oauth.post(
            'https://api.medium.com/v1/users/{}/posts'.format(user_id),
            json={'title': 'Example post', 'contentFormat': 'markdown', 'content': form.postdata.data})

        # If posted successfully send the user to their post
        if response.status_code == 201:
            return redirect(loads(response.content.decode('utf-8'))['data']['url'])

        # Send back bad response to the user
        return jsonify({'status_code': response.status_code, 'response': response.content.decode('utf-8')})

    return make_response('Invalid form', 400)


@app.route('/callback')
def callback():
    """ Handle OAuth callback
    :return: Redirect to index
    """
    global access_token
    access_token = medium_oauth.fetch_token(settings.MEDIUM_TOKEN_URL,
                                            client_secret=settings.MEDIUM_CLIENT_SECRET,
                                            authorization_response=request.url)
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True, ssl_context=('./crypto/server.crt', './crypto/server.key'))
