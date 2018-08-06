from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Categories, Categories_item
from flask_sqlalchemy import SQLAlchemy
from flask_dance.contrib.google import make_google_blueprint, google

import os

app = Flask(__name__)

blueprint = make_google_blueprint(
    client_id=os.environ['GOOGLE_CLIENT_ID'],
    client_secret=os.environ['GOOGLE_CLIENT_SECRET'],
    scope=["profile", "email"]
)
app.register_blueprint(blueprint, url_prefix="/login")


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catalog_items.db'
db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/dashboard/', methods=['GET', 'POST'])
def dashboard():
    
        categories_all = db.session.query(Categories).all()  
        try:     
            latest_items = db.session.query(Categories_item).all()
        except:
            pass
        return render_template('dashboard.html', categories=categories_all, latest_items=latest_items)

@app.route('/catalog/<int:categories_id>/')
def catalog_view(categories_id):
    category = db.session.query(Categories).filter_by(id=categories_id).one()
    categories_all = db.session.query(Categories).all()
    items = db.session.query(Categories_item).filter_by(categories_item_id=categories_id)
    items_num = items.count()
    return render_template('dashboard.html', categories = categories_all, items=items, category=category, items_num=items_num)


@app.route('/create_categories/')
def new_categories():
    return render_template('new_categories.html')

@app.route('/create_items/', methods=['GET', 'POST'])
def new_items():
    if request.method == 'POST':
        selected_category = request.form['selected_category']
        categories = db.session.query(Categories).filter_by(name=selected_category).one()
        categories_id = categories.id
        categories_name = categories.name

        new_item_title = request.form['title']
        new_item_description = request.form['description']

        newItem = Categories_item(
            title=new_item_title, description=new_item_description, categories_item_id=categories_id)
        db.session.add(newItem)
        db.session.commit()

        categories_all = db.session.query(Categories).all()
        category_items = db.session.query(Categories_item).filter_by(categories_item_id=categories_id)
        success_flag = 'new_item'

        try:     
            latest_items = db.session.query(Categories_item).all()
        except:
            pass

        return redirect(url_for('dashboard', categories = categories_all, items = category_items, flag = success_flag, latest_items=latest_items, new_item_title = new_item_title))
    else:
        categories = db.session.query(Categories).all()
        return render_template(
            'new_items.html', categories=categories
            )

@app.route('/catalog/<int:categories_id>/<int:categories_item_id>/delete/', methods=['GET', 'POST'])
def delete_item(categories_id, categories_item_id):
    if request.method == 'POST':
        # category = db.session.query(Categories).filter_by(id=categories_id).one()
        categories_all = db.session.query(Categories).all()
        item = db.session.query(Categories_item).filter_by(id=categories_item_id).one()
        deleted_item_title = item.title
        db.session.delete(item)
        db.session.commit()
        success_flags = 'delete_item'

        try:     
            latest_items = db.session.query(Categories_item).all()
        except:
            pass
        return redirect(url_for('dashboard', categories=categories_all, latest_items=latest_items, flags = success_flags, deleted_item_title=deleted_item_title))
    else:
        return render_template('delete_item.html', categories_id=categories_id, categories_item_id=categories_item_id)


@app.route('/catalog/<int:categories_id>/<int:categories_item_id>/')
def catalog_description(categories_id, categories_item_id):
    category = db.session.query(Categories).filter_by(id=categories_id).one()
    item = db.session.query(Categories_item).filter_by(id=categories_item_id).one()
    return render_template('description.html', category=category, item=item, categories_id=categories_id, categories_item_id=categories_item_id)

@app.route("/test")
def home():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    return "You are {email} on Google".format(email=resp.json()["email"])

if __name__ == '__main__':
    app.secret_key = 'dkwkdo390fl201d0xl3kd'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)