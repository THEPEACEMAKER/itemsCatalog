from flask import Flask, render_template, url_for

# Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {
    'name': 'Blue Burgers', 'id': '2'}, {'name': 'Taco Hut', 'id': '3'}]


# Fake Menu Items
items = [{'name': 'Cheese Pizza', 'description': 'made with fresh cheese', 'price': '$5.99', 'course': 'Entree', 'id': '1'}, {'name': 'Chocolate Cake', 'description': 'made with Dutch Chocolate', 'price': '$3.99', 'course': 'Dessert', 'id': '2'}, {'name': 'Caesar Salad', 'description':
                                                                                                                                                                                                                                                        'with fresh organic vegetables', 'price': '$5.99', 'course': 'Entree', 'id': '3'}, {'name': 'Iced Tea', 'description': 'with lemon', 'price': '$.99', 'course': 'Beverage', 'id': '4'}, {'name': 'Spinach Dip', 'description': 'creamy dip with fresh spinach', 'price': '$1.99', 'course': 'Appetizer', 'id': '5'}]
item = {'name': 'Cheese Pizza', 'description': 'made with fresh cheese',
        'price': '$5.99', 'course': 'Entree'}


app = Flask(__name__)


@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
	# return "This page shows all restaurants"	
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showRestaurant(restaurant_id):
	# return "This page shows the menu for restaurant number %s" % restaurant_id
    return render_template('restaurant.html', items=items, restaurant=restaurant)


@app.route('/restaurant/new/')
def newRestaurant():
	# return "add a new restaurant in this page"
    return render_template('newrestaurant.html')


@app.route('/restaurant/<int:restaurant_id>/edit/')
def editRestaurant(restaurant_id):
	# return "edit restaurant number %s " % restaurant_id
    return render_template('editrestaurant.html', restaurant = restaurant)


@app.route('/restaurant/<int:restaurant_id>/delete/')
def deleteRestaurant(restaurant_id):
	# return "delete restaurant number %s" % restaurant_id
    return render_template('deleterestaurant.html', restaurant = restaurant)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:item_id>/')
def showMenuItem(restaurant_id, item_id):
	# return "This page shows the item number %s" % item_id
    return render_template('menuitem.html', restaurant = restaurant, item = item)


@app.route('/restaurant/<int:restaurant_id>/menu/new/')
def newMenuItem(restaurant_id):
	# return "add a new item in the menu of restaurant number %s" % restaurant_id
    return render_template('newmenuitem.html', restaurant = restaurant)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:item_id>/edit/')
def editMenuItem(restaurant_id, item_id):
	# return "edit item number %s" % item_id
    return render_template('editmenuitem.html', restaurant = restaurant, item = item)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:item_id>/delete/')
def deleteMenuItem(restaurant_id, item_id):
	# return "delete item number %s" % item_id
    return render_template('deletemenuitem.html', restaurant = restaurant, item = item)



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
