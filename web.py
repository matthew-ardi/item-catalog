from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Categories, Categories_item
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catalog_items.db'
db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/dashboard/', methods=['GET', 'POST'])
def dashboard():
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
        return render_template('dashboard.html', categories = categories_all, items = category_items, flag = success_flag, new_item_title = new_item_title)
    else:
        categories = db.session.query(Categories).all()

        try:
            items = db.session.query(Categories_item).all()
        except:
            items = None

        return render_template('dashboard.html', categories=categories, items=items)


@app.route('/create_categories/')
def new_categories():
    return render_template('new_categories.html')

@app.route('/create_items/', methods=['GET', 'POST'])
def new_items():
    
    
        categories = db.session.query(Categories).all()
        return render_template(
            'new_items.html', categories=categories
            )

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)