# Item Catalog - Restaurants and Menus
- This application views restaurants called from a database and their menu items.
- All CRUD operations are working effiecntly
- Authenticated users can add, edit and delete restaurants and menu items which they have created.

## Third-party
- This application uses google sign in.

## oAuth
- oAuth is used to authenticate users.

## How to run?
- To get started, I recommend the user use a virtual machine to ensure they are using the same environment that this project is developed on, running on your computer. You can download [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1) to install and manage your virtual machine.
- Clone the [fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm) repo
- Clone this repo on your local machine.
- Put the cloned folder inside the Vagrant folder. 
- In your `terminal` change directory to the vagrant folder.
- Run `vagrant up` to bring the virtual machine online then `vagrant ssh` to login.
 -Run `cd /vagrant/itemscatalog` to access the folder via the virtual machine.
- Install the database required for this project `python database_setup.py` then `python lotsofmenus.py`
- Run the application `python application.py`
- Open your favourite browser and head to `http://localhost:5000` and enjoy the application.

### JSON End Points
The restaurants page, one restaurant page and item details page show thier JSON end points, which can be created by appending `/JSON` to the URL

- For the restaurants page, use `http://localhost:5000/restaurants/JSON/`
- For items in a particular category use `http://localhost:5000/restaurant/rstaurantID/JSON/`
- For a single item, use `http://localhost:5000/restaurant/rstaurantID/itemID/JSON/`
