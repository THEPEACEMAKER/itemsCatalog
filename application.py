from flask import Flask, render_template, url_for, request, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# # Fake Restaurants
# restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

# restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name': 'Blue Burgers', 'id': '2'}, {'name': 'Taco Hut', 'id': '3'}]


# # Fake Menu Items
# items = [{'name': 'Cheese Pizza', 'description': 'made with fresh cheese', 'price': '$5.99', 'course': 'Entree', 'id': '1'}, {'name': 'Chocolate Cake', 'description': 'made with Dutch Chocolate', 'price': '$3.99', 'course': 'Dessert', 'id': '2'}, {'name': 'Caesar Salad', 'description':'with fresh organic vegetables', 'price': '$5.99', 'course': 'Entree', 'id': '3'}, {'name': 'Iced Tea', 'description': 'with lemon', 'price': '$.99', 'course': 'Beverage', 'id': '4'}, {'name': 'Spinach Dip', 'description': 'creamy dip with fresh spinach', 'price': '$1.99', 'course': 'Appetizer', 'id': '5'}]
# item = {'name': 'Cheese Pizza', 'description': 'made with fresh cheese','price': '$5.99', 'course': 'Entree'}
# # if a restaurant doesn't have any menu items
# # items = [] 


@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    # return "This page will show all my restaurants"
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showRestaurant(restaurant_id):
	# return "This page shows the menu for restaurant number %s" % restaurant_id
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return render_template('restaurant.html', items=items, restaurant=restaurant)


@app.route('/restaurant/new/', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['name'])
        session.add(newRestaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')
	# return "add a new restaurant in this page"
    # return render_template('newrestaurant.html')


@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            restaurant.name = request.form['name']
            session.add(restaurant)
            session.commit()
            return redirect(url_for('showRestaurants'))
    else:
        return render_template(
            'editRestaurant.html', restaurant=restaurant)

	# return "edit restaurant number %s " % restaurant_id
    # return render_template('editrestaurant.html', restaurant = restaurant)


@app.route('/restaurant/<int:restaurant_id>/delete/')
def deleteRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	# return "delete restaurant number %s" % restaurant_id
    return render_template('deleterestaurant.html', restaurant = restaurant)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:item_id>/')
def showMenuItem(restaurant_id, item_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    item = session.query(MenuItem).filter_by(id=item_id).one()
	# return "This page shows the item number %s" % item_id
    return render_template('menuitem.html', restaurant = restaurant, item = item)


@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
	# return "add a new item in the menu of restaurant number %s" % restaurant_id
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], description=request.form['description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()

        return redirect(url_for('showRestaurant', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)    


@app.route('/restaurant/<int:restaurant_id>/menu/<int:item_id>/edit/')
def editMenuItem(restaurant_id, item_id):
    item = session.query(MenuItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']
        if request.form['description']:
            item.description = request.form['name']
        if request.form['price']:
            item.price = request.form['price']
        if request.form['course']:
            item.course = request.form['course']
        session.add(item)
        session.commit()
        return redirect(url_for('showRestaurant', restaurant_id=restaurant_id))
    else:

        return render_template(
            'editmenuitem.html', restaurant_id=restaurant_id, item=item)
	# return "edit item number %s" % item_id
    # return render_template('editmenuitem.html', restaurant_id = restaurant_id, item = item)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:item_id>/delete/')
def deleteMenuItem(restaurant_id, item_id):
    item = session.query(MenuItem).filter_by(id=item_id).one()
	# return "delete item number %s" % item_id
    return render_template('deletemenuitem.html', restaurant_id = restaurant_id, item = item)



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
