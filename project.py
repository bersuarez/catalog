from flask import Flask, render_template, request, redirect, url_for, flash, jsonify 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DB_setup import Base, DummyCategory, DummyItem, User

from flask import session as login_session
import random, string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(open('client_secrets.json','r').read())['web']['client_id']

app=Flask(__name__)
engine = create_engine('sqlite:///catalogandusers.db',connect_args={'check_same_thread':False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/login')
def showLogin():
    state=''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state']=state
    return render_template('login.html', STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'% access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1].decode('utf-8'))
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    #check if user exists, if not make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print("done!")
    return output

@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is %s' %access_token)
    print('User name is: ')
    print(login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' %access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response
     
@app.route('/')
def landing():
    categories = session.query(DummyCategory).all()
    latestItems=session.query(DummyItem)
    # .order_by(dummy_item.id).limit(10)
    return render_template('landing.html',categories=categories,items=latestItems)

@app.route('/catalog/<string:category_name>/')
def categoryItems(category_name):
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(DummyCategory).filter_by(name=category_name).one()
    items=session.query(DummyItem).filter_by(category_id=category.id).all()
    return render_template('category.html',category=category, items=items)

@app.route('/catalog/<string:category_name>/<string:item_name>/')
def itemDescription(category_name, item_name):
    category=session.query(DummyCategory).filter_by(name=category_name).one()
    item=session.query(DummyItem).filter_by(name=item_name).one()
    return render_template('item.html', category=category, item=item)

@app.route('/catalog/<string:category_name>/<string:item_name>/edit/', methods=['GET', 'POST'])
def editItem(category_name, item_name):
    editedItem = session.query(DummyItem).filter_by(name=item_name).one()
    print(editedItem.name)
    category=session.query(DummyCategory).filter_by(name=category_name).one()
    categories=session.query(DummyCategory).all()
    if request.method =='POST':
        if request.form['updatedName']:
            editedItem.name=request.form['updatedName']
        if request.form['updatedAttribute']:
            editedItem.attribute=request.form['updatedAttribute']
        if request.form['updatedCategory']:
            updatedCategory=session.query(DummyCategory).filter_by(name=request.form['updatedCategory'])
            editedItem.category=updatedCategory
        session.add(editedItem)
        session.commit()
        return redirect(url_for('landing'))
    else:
        return render_template('editItem.html', category=category, item=editedItem, allcategories=categories)

@app.route('/catalog/<string:category_name>/<string:item_name>/delete/', methods=['GET', 'POST'])
def deleteItem(category_name,item_name):
    itemToDelete = session.query(DummyItem).filter_by(name=item_name).one()
    category=session.query(DummyCategory).filter_by(name=category_name).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('landing'))
    else:
        return render_template('deleteItem.html', category=category,item=itemToDelete)

@app.route('/catalog/new/', methods=['GET', 'POST'])
def newItem():
    categories=session.query(DummyCategory).all()
    if request.method =='POST':
        category=session.query(DummyCategory).filter_by(name=request.form['category']).one()
        newItem = DummyItem(name=request.form['name'],attribute=request.form['attribute'], category=category)#request.form['category'])
        session.add(newItem)
        session.commit()
        return redirect(url_for('landing'))
    else: 
        return render_template('newItem.html', allcategories=categories)

@app.route('/catalog/<string:category_name>/JSON')
def categoryItemsJSON(category_name):
    category = session.query(DummyCategory).filter_by(name=category_name).one()
    items=session.query(DummyItem).filter_by(category_id=category.id)
    return jsonify(DummyClass=[i.serialize for i in items])

def createUser(login_session):
    newUser = User(name = login_session['username'], email = login_session['email'], picture = login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

def getUserInfo(user_id):
    user=session.query(User).filter_by(id = user_id).one()
    return user

def getUserID(email):
    try:
        user = session.query(User).filter_by(email = email).one()
        return user.id
    except:
        return None

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
