#!/usr/bin/env python

from flask import (Flask, render_template, request, redirect)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import (Base, Categories, Categories_item)
from flask_sqlalchemy import SQLAlchemy
from flask_dance.contrib.google import (make_google_blueprint, google)
from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from flask import (make_response, url_for, flash, jsonify)
from flask_oauth import OAuth
from flask_wtf.csrf import CSRFProtect
import requests
import time
import os
import random
import string
import json
import httplib2
import base64

app = Flask(__name__)

# CSRF set up
csrf = CSRFProtect()
csrf.init_app(app)

# getting environment variables
GOOGLE_CLIENT_ID = os.environ['GOOGLE_CLIENT_ID']
GOOGLE_CLIENT_SECRET = os.environ['GOOGLE_CLIENT_SECRET']

# Setting up blueprint for Google Auth
blueprint = make_google_blueprint(
    client_id=os.environ['GOOGLE_CLIENT_ID'],
    client_secret=os.environ['GOOGLE_CLIENT_SECRET'],
    scope=["profile", "email"]
)
app.register_blueprint(blueprint, url_prefix="/login")

# Setting up config for database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catalog_items.db'
db = SQLAlchemy(app)

# Setting up Google Oauth
oauth = OAuth()
REDIRECT_URI = '/oauth2callback'
google = oauth.remote_app(
    'google',
    base_url='https://www.google.com/accounts/',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    request_token_url=None,
    request_token_params={
        'scope': 'https://www.googleapis.com/auth/userinfo.email',
        'response_type': 'code'
        },
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_method='POST',
    access_token_params={'grant_type': 'authorization_code'},
    consumer_key=GOOGLE_CLIENT_ID,
    consumer_secret=GOOGLE_CLIENT_SECRET)

@app.route('/')
def home():
    redirect(url_for('dashboard'))

@app.route('/dashboard/', methods=['GET', 'POST'])
# route for dashboard
def dashboard():

        # Generate state token for login authentication
        state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                for x in xrange(32))
        login_session['state'] = state

        # Checking login status and set flag
        if 'username' in login_session:
            logged_in = True
        else:
            logged_in = False

        # Getting data fro the database
        categories_all = db.session.query(Categories).all()
        try:
            latest_items = db.session.query(Categories_item).all()
        except:
            pass
        if logged_in:
            return render_template(
                'dashboard.html',
                logged_in=logged_in,
                categories=categories_all,
                latest_items=latest_items,
                username=login_session['username'],
                google_client_id=os.environ['GOOGLE_CLIENT_ID'],
                STATE=state
                )
        else:
            return render_template(
                'dashboard.html',
                logged_in=logged_in,
                categories=categories_all,
                latest_items=latest_items,
                google_client_id=os.environ['GOOGLE_CLIENT_ID'],
                STATE=state)


@app.route('/catalog/<int:categories_id>/<username>')
# route to render dashboard view when user click categories section
def catalog_view(categories_id, username):
    category = db.session.query(Categories).filter_by(id=categories_id).one_or_none()
    categories_all = db.session.query(Categories).all()
    items = db.session.query(Categories_item).filter_by(
        categories_item_id=categories_id
        )
    items_num = items.count()

    if username == 'none':
        username = None

    return render_template(
        'dashboard.html',
        username=username,
        categories=categories_all,
        items=items,
        category=category,
        items_num=items_num
        )



@app.route('/create_items/<username>', methods=['GET', 'POST'])
# function to create new items
def new_items(username):
    if request.method == 'POST':
        selected_category = request.form['selected_category']
        categories = db.session.query(Categories).filter_by(
            name=selected_category
            ).one_or_none()
        categories_id = categories.id
        categories_name = categories.name

        new_item_title = request.form['title']
        new_item_description = request.form['description']
        file = request.files['inputImage']

        new_item_image = file.read()

        newItem = Categories_item(
            title=new_item_title,
            description=new_item_description,
            picture=new_item_image,
            categories_item_id=categories_id
            )
        db.session.add(newItem)
        db.session.commit()

        categories_all = db.session.query(Categories).all()
        category_items = db.session.query(Categories_item).filter_by(
            categories_item_id=categories_id
            )

        try:
            latest_items = db.session.query(Categories_item).all()
        except:
            pass

        flash(
            "item " +
            new_item_title +
            " has been successfully added.", "success")

        return redirect(url_for(
                            'dashboard',
                            categories=categories_all,
                            items=category_items,
                            username=username,
                            latest_items=latest_items,
                            new_item_title=new_item_title))
    else:
        categories = db.session.query(Categories).all()
        return render_template(
            'new_items.html',
            categories=categories,
            username=username
            )

@app.route(
    '/catalog/<int:categories_id>/<int:categories_item_id>/delete/<username>',
    methods=['GET','POST']
    )
#function to delete items
def delete_item(categories_id, categories_item_id, username):
    if 'username' not in login_session:
        flash("You need to login to delete items", "info")
        time.sleep(1)
        return redirect(url_for('dashboard'))

    categories_all = db.session.query(Categories).all()
    item = db.session.query(Categories_item).filter_by(
        id=categories_item_id
        ).one_or_none()
    deleted_item_title = item.title
    if request.method == 'POST':
        db.session.delete(item)
        db.session.commit()
        flash("item " + deleted_item_title + " has been successfully deleted.", "success")
        try:     
            latest_items = db.session.query(Categories_item).all()
        except:
            pass
        return redirect(
            url_for(
                'dashboard',
                username=username,
                categories=categories_all,
                latest_items=latest_items,
                deleted_item_title=deleted_item_title
                )
            )
    else:
        return render_template(
            'delete_item.html',
            username=username,
            deleted_item_title=deleted_item_title,
            categories_id=categories_id,
            categories_item_id=categories_item_id
            )


@app.route('/catalog/<int:categories_id>/<int:categories_item_id>/<username>')
# function to render description page of each item
def catalog_description(categories_id, categories_item_id, username):
    category = db.session.query(Categories).filter_by(id=categories_id).one_or_none()
    item = db.session.query(Categories_item).filter_by(id=categories_item_id).one_or_none()
    image = base64.b64encode(item.picture).decode('ascii')
    if username == 'none':
        username = None

    return render_template(
        'description.html',
        username=username,
        category=category,
        item=item,
        image=image,
        categories_id=categories_id,
        categories_item_id=categories_item_id
        )


@app.route('/catalog_categories.json')
# function to provide Categories API endpoint
def catalog_categoriesJSON():
    if 'username' not in login_session:
        flash("You need to login to access API endpoints", "info")
        time.sleep(1)
        return redirect(url_for('dashboard'))

    categories = db.session.query(Categories).all()
    return jsonify(Category=[category.serialize for category in categories])


@app.route('/<int:categories_id>/category.json')
def categoryJSON(categories_id):
    if 'username' not in login_session:
        flash("You need to login to access API endpoints", "info")
        time.sleep(1)
        return redirect(url_for('dashboard'))

    category = db.session.query(Categories).filter_by(id=categories_id).one_or_none()
    return jsonify(category.serialize)

@app.route('/<int:categories_id>/<int:categories_item_id>/item.json')
def itemJSON(categories_id, categories_item_id):
    if 'username' not in login_session:
        flash("You need to login to access API endpoints", "info")
        time.sleep(1)
        return redirect(url_for('dashboard'))

    category = db.session.query(Categories).filter_by(id=categories_id).one_or_none()
    item = db.session.query(Categories_item).filter_by(
        id=categories_item_id
        ).one_or_none()
    return jsonify(item.serialize)

@app.route('/<int:categories_id>/all_items.json')
def category_itemsJSON(categories_id):
    if 'username' not in login_session:
        flash("You need to login to access API endpoints", "info")
        time.sleep(1)
        return redirect(url_for('dashboard'))

    category = db.session.query(Categories).filter_by(id=categories_id).one_or_none()
    items = db.session.query(Categories_item).filter_by(
        categories_item_id=categories_id
        )
 
    return jsonify([item.serialize_items for item in items])


@app.route('/catalog_items.json')
# function to provide items API endpoint
def catalog_itemsJSON():
    if 'username' not in login_session:
        flash("You need to login to access API endpoints", "info")
        time.sleep(1)
        return redirect(url_for('dashboard'))

    items = db.session.query(Categories_item).all()
    return jsonify(Items=[item.serialize for item in items])


@app.route('/login')
# Create anti-forgery state token
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return redirect(url_for('check_google_login', STATE=state))


@app.route('/check_google_login/<STATE>')
# Validate state token
def check_google_login(STATE):
    if STATE != login_session['state']:
        flash("Invalid state parameter.", "error")
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('google_login'))


@app.route('/google_login')
# Sending Oauth request to Google and requesting user info
def google_login():

    access_token = login_session.get('access_token')
    if access_token is None:
        return redirect(url_for('google_auth_login'))

    access_token = access_token[0]
    from urllib2 import Request, urlopen, URLError

    headers = {'Authorization': 'OAuth ' + access_token}
    req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
                  None, headers)
    try:
        res = urlopen(req)
        data = json.loads(res.read())
        login_session['username'] = data['name']
        login_session['user_email'] = data['email']
        flash(
            "You just logged in as " +
            str(login_session['username']) +
            " using your " +
            str(login_session['user_email']) +
            " account.", "success"
            )
    except URLError, e:
        if e.code == 401:
            # Unauthorized - bad token
            login_session.pop('access_token', None)
            return redirect(url_for('google_login'))
        return res.read()
    return redirect(url_for('dashboard'))


@app.route('/google_auth_login')
def google_auth_login():
    callback = url_for('authorized', _external=True)
    return google.authorize(callback=callback)

@app.route(REDIRECT_URI)
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    login_session['access_token'] = access_token, ''
    return redirect(url_for('google_login'))

@google.tokengetter
def get_access_token():
    return login_session.get('access_token')


@app.route('/gdisconnect')
# account logout function
def gdisconnect():
    access_token = login_session.get('access_token')
    if 'username' in login_session:
        del login_session['access_token']
        del login_session['username']
    else:
        flash('You are not logged in', "error")
        return redirect(url_for('dashboard'))

    if access_token is None:
        print 'Access Token is None'
        if 'username' in login_session:
            del login_session['username']

        flash('You are not logged in', "error")
        return redirect(url_for('dashboard'))

    result = requests.post(
        'https://accounts.google.com/o/oauth2/revoke',
        params={'token': access_token},
        headers={'content-type': 'application/x-www-form-urlencoded'}
        )

    response = make_response(json.dumps('Successfully disconnected.'), 200)
    response.headers['Content-Type'] = 'application/json'
    flash('Logout was successful.', "success")
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.secret_key = 'dkwkdo390fl201d0xl3kd'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
