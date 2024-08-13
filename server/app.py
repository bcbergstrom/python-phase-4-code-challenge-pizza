#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"


class All_Restaurants(Resource):
    def get(self):
        all_restaurants = Restaurant.query.all()
        return [restaurant.to_dict(rules=["-restaurant_pizzas"]) for restaurant in all_restaurants], 200


class One_Restaurant(Resource):
    def get(self, id):
        
        one_restaurant = Restaurant.query.get(id)
        if not one_restaurant:
            return {"error": "Restaurant not found"}, 404
        return one_restaurant.to_dict(),200
    def delete(self, id):
        one_restaurant = Restaurant.query.get(id)
        if not one_restaurant:
            return {"error": "Restaurant not found"}, 404
        db.session.delete(one_restaurant)
        db.session.commit()
        return {}, 204

class All_Pizzas(Resource):
    def get(self):
        all_pizzas = Pizza.query.all()
        return [pizza.to_dict(rules=["-restaurant_pizzas"]) for pizza in all_pizzas], 200
class One_ResturantPizza(Resource):
    def post(self):
        try:
            data = request.get_json()
            new_restaurant_pizza = RestaurantPizza(price=data["price"],pizza_id=data["pizza_id"],restaurant_id=data["restaurant_id"],)
            db.session.add(new_restaurant_pizza)
            db.session.commit()
            return new_restaurant_pizza.to_dict(), 201
        except Exception as e:
            return {"errors": ['validation errors']}, 400
        
api.add_resource(One_ResturantPizza, "/restaurant_pizzas")
api.add_resource(All_Pizzas, "/pizzas")
api.add_resource(One_Restaurant, "/restaurants/<int:id>")
api.add_resource(All_Restaurants, "/restaurants")
if __name__ == "__main__":
    app.run(port=5555, debug=True)
