from flask import Flask, render_template, url_for
from flask import request, redirect, jsonify, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
from flask import session as login_session
import random
import string
import httplib2
from oauth2client import client
import json
from flask import make_response
import requests


app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Restaurant Menu Application"

# Connect to Database and create database session
engine = create_engine('sqlite:///restaurantmenu.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # (Receive auth_code by HTTPS POST)

    # If this request does not have `X-Requested-With` header,
    # this could be a CSRF
    if not request.headers.get('X-Requested-With'):
        abort(403)

    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code
    auth_code = request.data

    # Set path to the Web application client_secret_*.json file
    # you downloaded from the
    # Google API Console:
    # https://console.developers.google.com/apis/credentials
    CLIENT_SECRET_FILE = 'client_secrets.json'

    # Exchange auth code for access token, refresh token, and ID token
    credentials = client.credentials_from_clientsecrets_and_code(
        CLIENT_SECRET_FILE,
        ['https://www.googleapis.com/auth/drive.appdata', 'profile', 'email'],
        auth_code)

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    # print result
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        print "there was an error in the access token info"
        return response

    # Verify that the access token is used for the intended user.
    userid = credentials.id_token['sub']
    if result['user_id'] != userid:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        print "Token's user ID doesn't match given user ID."
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        print "Token's client ID does not match app's."
        return response

    # check if the user is already connected.
    stored_access_token = login_session.get('access_token')
    stored_userid = login_session.get('userid')
    if stored_access_token is not None and userid == stored_userid:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash('This user is already connected.')
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['userid'] = userid

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # Get profile info from ID token
    # email = credentials.id_token['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    if request.args.get('status') == '200':
        if 'access_token' in login_session:
            del login_session['access_token']
        if 'userid' in login_session:
            del login_session['userid']
        if 'username' in login_session:
            del login_session['username']
        if 'email' in login_session:
            del login_session['email']
        if 'picture' in login_session:
            del login_session['picture']
        flash("Successfully disconnected.")
        print "Successfully disconnected."
        return redirect(url_for('showRestaurants'))
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        print "Failed to revoke token for given user."
        return response


# JSON APIs to view Restaurant Information
@app.route('/JSON/')
@app.route('/restaurants/JSON/')
def restaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(restaurants=[r.serialize for r in restaurants])


@app.route('/restaurant/<int:restaurant_id>/JSON/')
@app.route('/restaurant/<int:restaurant_id>/menu/JSON/')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurant/<int:restaurant_id>/<int:item_id>/JSON/')
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def menuItemJSON(restaurant_id, menu_id):
    Menu_Item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(Menu_Item=Menu_Item.serialize)


@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template(
        'restaurants.html',
        restaurants=restaurants, login_session=login_session)
    # return "This page will show all my restaurants"


@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return render_template(
        'restaurant.html', items=items, restaurant=restaurant,
        login_session=login_session)
    # return "This page shows the menu for restaurant number %s" %restaurant_id


@app.route('/restaurant/new/', methods=['GET', 'POST'])
def newRestaurant():
    if 'username' not in login_session:
        flash("You must be logged in to view this page")
        return redirect('/login')

    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['name'])
        session.add(newRestaurant)
        session.commit()
        flash("new Restaurant created!")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template(
            'newRestaurant.html', login_session=login_session)
    # return "add a new restaurant in this page"


@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    if 'username' not in login_session:
        flash("You must be logged in to view this page")
        return redirect('/login')

    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            restaurant.name = request.form['name']
            session.add(restaurant)
            session.commit()
            flash("Restaurant was edited successfully!")
            return redirect(url_for('showRestaurants'))
    else:
        return render_template(
            'editRestaurant.html', restaurant=restaurant,
            login_session=login_session)
    # return "edit restaurant number %s " % restaurant_id


@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    if 'username' not in login_session:
        flash("You must be logged in to view this page")
        return redirect('/login')

    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurant)
        session.commit()
        flash("Restaurant was deleted successfully!")
        return redirect(
            url_for('showRestaurants'))
    else:
        return render_template(
            'deleterestaurant.html', restaurant=restaurant,
            login_session=login_session)
    # return "delete restaurant number %s" % restaurant_id


@app.route('/restaurant/<int:restaurant_id>/<int:item_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/<int:item_id>/')
def showMenuItem(restaurant_id, item_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    item = session.query(MenuItem).filter_by(id=item_id).one()
    return render_template(
        'menuitem.html',
        restaurant=restaurant, item=item, login_session=login_session)
    # return "This page shows the item number %s" % item_id


@app.route(
    '/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if 'username' not in login_session:
        flash("You must be logged in to view this page")
        return redirect('/login')

    if request.method == 'POST':
        newItem = MenuItem(
            name=request.form['name'],
            description=request.form['description'],
            price=request.form['price'],
            course=request.form['course'],
            restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("Item was created successfully!")
        return redirect(url_for('showRestaurant', restaurant_id=restaurant_id))
    else:
        return render_template(
            'newmenuitem.html',
            restaurant_id=restaurant_id, login_session=login_session)
    # return "add a new item in the menu of restaurant number %s"%restaurant_id


@app.route(
    '/restaurant/<int:restaurant_id>/menu/<int:item_id>/edit/',
    methods=['GET', 'POST'])
def editMenuItem(restaurant_id, item_id):
    if 'username' not in login_session:
        flash("You must be logged in to view this page")
        return redirect('/login')

    item = session.query(MenuItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']
        if request.form['description']:
            item.description = request.form['description']
        if request.form['price']:
            item.price = request.form['price']
        if request.form['course']:
            item.course = request.form['course']
        session.add(item)
        session.commit()
        flash("Item was edited successfully!")
        return redirect(url_for('showRestaurant', restaurant_id=restaurant_id))
    else:

        return render_template(
            'editmenuitem.html', restaurant_id=restaurant_id, item=item,
            login_session=login_session)
    # return "edit item number %s" % item_id


@app.route(
    '/restaurant/<int:restaurant_id>/menu/<int:item_id>/delete/',
    methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, item_id):
    if 'username' not in login_session:
        flash("You must be logged in to view this page")
        return redirect('/login')

    item = session.query(MenuItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash("Item was deleted successfully!")
        return redirect(url_for('showRestaurant', restaurant_id=restaurant_id))
    else:
        return render_template(
            'deletemenuitem.html', restaurant_id=restaurant_id, item=item,
            login_session=login_session)
    # return "delete item number %s" % item_id


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
