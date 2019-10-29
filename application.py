from flask import Flask

app = Flask(__name__)


@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
	return "This page shows all restaurants"


@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showRestaurant(restaurant_id):
	return "This page shows the menu for restaurant number %s" % restaurant_id


@app.route('/restaurant/new/')
def newRestaurant():
	return "add a new restaurant in this page"


@app.route('/restaurant/<int:restaurant_id>/edit/')
def editRestaurant(restaurant_id):
	return "edit restaurant number %s " % restaurant_id


@app.route('/restaurant/<int:restaurant_id>/delete/')
def deleteRestaurant(restaurant_id):
	return "delete restaurant number %s" % restaurant_id


@app.route('/restaurant/<int:restaurant_id>/menu/<int:item_id>/')
def showMenuItem(restaurant_id, item_id):
	return "This page shows the item number %s" % item_id


@app.route('/restaurant/<int:restaurant_id>/menu/new')
def newMenuItem(restaurant_id):
	return "add a new item in the menu of restaurant number %s" % restaurant_id


@app.route('/restaurant/<int:restaurant_id>/menu/<int:item_id>/edit/')
def editMenuItem(restaurant_id, item_id):
	return "edit item number %s" % item_id


@app.route('/restaurant/<int:restaurant_id>/menu/<int:item_id>/delete/')
def deleteMenuItem(restaurant_id, item_id):
	return "delete item number %s" % item_id



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
