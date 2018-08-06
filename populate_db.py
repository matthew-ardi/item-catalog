from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Categories, Categories_item
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catalog_items.db'
db = SQLAlchemy(app)

category1 = Categories(name="Soccer")
db.session.add(category1)
db.session.commit()

category2 = Categories(name="Basketball")
db.session.add(category2)
db.session.commit()

category3 = Categories(name="Baseball")
db.session.add(category3)
db.session.commit()

category4 = Categories(name="Frisbee")
db.session.add(category4)
db.session.commit()

category5 = Categories(name="Snowboarding")
db.session.add(category5)
db.session.commit()

category6 = Categories(name="Rock Climbing")
db.session.add(category6)
db.session.commit()

category7 = Categories(name="Foosball")
db.session.add(category7)
db.session.commit()

category8 = Categories(name="Skating")
db.session.add(category8)
db.session.commit()

category9 = Categories(name="Hockey")
db.session.add(category9)
db.session.commit()