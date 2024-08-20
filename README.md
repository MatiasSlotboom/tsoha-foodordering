# FoodOrdering
Foodordering is a Flask project where you can register a restaurant, add foods to your restaurants and sell them. Users can order food from these restaurants. Administrators are responsible for accepting restaurant requests, and can manage all functions.

# Using
Define as environment variables SECRET_KEY with your secret key and ADMIN_PASSWORD as the password that will allow a user to grant themselves admin rights.

# Foodordering

Foodordering is a project that allows restaurant owners to apply to host their restaurant on the website, and after being accepted by an administrator can add different foods on their menus.
Users can look through the different restaurants and order from them.

# Setup

1. Make sure you have postgresql running.
2. psql < schema.sql
3. python3 -m venv venv
4. source venv/bin/activate
5. pip3 install -r requirements
6. Define as environment variables SECRET_KEY with your secret key and ADMIN_PASSWORD as the password that will allow a user to grant themselves admin rights
7. flask run