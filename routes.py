from flask import redirect, render_template, request
import user
import restaurants
from app import app

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/manage_account')
def manage_account():
    return render_template('manage_account.html')

@app.route('/manage_restaurant')
def manage_restaurant():
    if user.user_isAdmin() == True:
        return render_template('manage_restaurant.html', restaurants=restaurants.getRestaurants())
    elif user.has_restaurant() == True:
        return render_template('manage_restaurant.html', restaurants=restaurants.getRestaurantsOwnedByUser(user.user_id()))
    else:
        return redirect("/")

@app.route('/admin_accept_restaurant', methods=['POST'])
def admin_accept_restaurant():
    if user.user_isAdmin():
        print(request.form)
        restaurantName = request.form.get("restaurantName")
        restaurants.acceptRestaurantApplication(restaurantName)
        return admin_panel()
    else:
        return redirect("/")

@app.route('/order_food', methods=['POST'])
def order_food():
    if user.user_id():
        print(request.form)
        return redirect("/shop")
    else:
        return redirect("/")

@app.route('/shop')
def shop():
    if user.user_id():
        return render_template("shop.html", restaurants=restaurants.getRestaurantsWithFood())

@app.route('/admin_panel')
def admin_panel():
    if user.user_isAdmin():
        return render_template('admin_panel.html', restaurants=restaurants.getRestaurantApplications())
    else:
        return redirect("/")

@app.route('/add_food_to_restaurant', methods=["POST"])
def add_food_to_restaurant():
    restaurantId = request.form.get("restaurantId")
    if user.user_ownsRestaurant(restaurantId) == True or user.user_isAdmin() == True:
        foodName = request.form.get("foodName")
        foodDescription = request.form.get("foodDescription")
        foodPrice = request.form.get("foodPrice")
        restaurants.addFoodToRestaurant(foodName, foodDescription, foodPrice, restaurantId)
        restaurantList = None
        if user.user_ownsRestaurant(restaurantId) == True:
            restaurantList = restaurants.getRestaurantsOwnedByUser()
        elif user.user_isAdmin() == True:
            restaurantList = restaurants.getRestaurants()
        return render_template("manage_restaurant.html", restaurants=restaurantList, messageForRestaurantId=restaurantId, message=f"Added food {foodName} to restaurant.")
    return render_template("manage_restaurant.html", restaurants=restaurants.getRestaurantsOwnedByUser(), messageForRestaurantId=restaurantId, message=f"Error adding food {foodName} to restaurant.")

@app.route('/apply_restaurant', methods=['POST'])
def apply_restaurant():
    restaurantName = request.form.get("restaurantName")
    applier = user.user_name()
    success = restaurants.apply_restaurant(restaurantName, applier)
    if success == True:
        return render_template('manage_account.html', message_restaurant=f"Succesfully applied for restaurant {restaurantName}!")
    return render_template('manage_account.html', message_restaurant=f"An application already exists for a restaurant with the same name!")

@app.route('/apply_admin', methods=['POST'])
def apply_admin():
    action = request.form.get("action")
    password = request.form.get('password')
    if action != None and action == "apply" and password != None and password != "":
        user.elevate_user(password)
    return render_template('manage_account.html')

@app.route('/logout', methods=['POST'])
def logout():
    user.logout()
    return redirect("/")

@app.route('/auth', methods=['POST'])
def login():
    action = request.form.get("action")
    username = request.form.get('username')
    password = request.form.get('password')
    if action == None:
        return render_template("index.html", message="Something wrong happened!")
    if action == "login":
        if password != None and username != None and username != "" and password != "" and user.login(username, password) == True:
            return redirect('/shop')
        else:
            return render_template("index.html", message="Wrong password or username!")
    elif action == "register":
        if username != None and len(username) < 6:
            return render_template("index.html", message="Username must be 6 or more characters!")
        elif password != None and len(password) < 6:
            return render_template("index.html", message="Password must be 6 or more characters!")
        elif user.register(username, password) == True:
            return redirect('/shop')
        else:
            return render_template("index.html", message="User already exists!")
    else:
        return render_template("index.html", message="Something wrong happened!")