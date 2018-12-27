from flask import Flask, render_template, request, redirect, url_for, flash, jsonify 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DB_setup import Base, DummyCategory, DummyItem

app=Flask(__name__)
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def landing():
    categories = session.query(DummyCategory).all()
    latestItems=session.query(DummyItem)
    # .order_by(dummy_item.id).limit(10)
    return render_template('landing.html',categories=categories,items=latestItems)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)