# Item Catalog - Restaurants and Menus
- This application views restaurants called from a database and their menu items.
- All CRUD operations are working effiecntly
- Authenticated users can add, edit and delete restaurants and menu items.

## Third-party
- This application uses google sign in.

## oAuth
- oAuth is used to authenticate users.

## How to run?
- To get started, I recommend the user use a virtual machine to ensure they are using the same environment that this project is developed on, running on your computer. You can download [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1) to install and manage your virtual machine.
Use `vagrant up` to bring the virtual machine online and `vagrant ssh` to login.
- Clone this repo on your local machine.
- Put the cloned folder inside the Vagrant folder. 
- In your `terminal` change directory to the cloned folder.
- Run `vagrant up` then `vagrant ssh`
- Install the database required for this project `python database_setup.py` & `python lotsofmenus.py`
- Run the application `python application.py`
- Open your favourite browser and head to `http://localhost:5000` and enjoy the application.
