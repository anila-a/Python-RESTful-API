from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import math
from datetime import datetime

app = Flask(__name__) # Set up a flask application

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

# DATABASE MODEL
class DeliveryFee(db.Model):
    # Define table attributes
    # ID is primary key, no value can be null
    id = db.Column(db.Integer, primary_key=True)
    cart_value = db.Column(db.Integer, nullable=False)
    delivery_distance = db.Column(db.Integer, nullable=False)
    number_of_items = db.Column(db.Integer, nullable=False)
    time = db.Column(db.String(30))
    fee = db.Column(db.Integer, default=0, nullable=False) # Set delivery fee = 0 by default

    # Data representation
    def __repr__(self):
        return f"{self.cart_value} - {self.delivery_distance} - {self.number_of_items} - {self.time} - {self.fee}"

    # Calculate the delivery fee (setter method)
    # NOTE: EUR values are converted to cents (1 EUR = 100 cents)
    def calculate_delivery_fee(self):
        # RULE 1: Cart value < 10 EUR, add surcharge (= 10 EUR - cart value)
        if self.cart_value < 1000:
            self.fee += 1000 - self.cart_value
        # RULE 2: Fee for the first 1000m = 2 EUR ...
        if self.delivery_distance <= 1000:
            self.fee += 200
        else: # ... + 1 EUR for every additional 500m
            self.fee += 200 # Base fee
            distance = math.ceil((self.delivery_distance - 1000) / 500) # Round up!
            self.fee += (distance * 100) # Additional 1 EUR per extra 500m
        # RULE 3: Additional 50 cent for each item (4+)
        if self.number_of_items > 4:
            self.fee += ((self.number_of_items - 4) * 50)
        # SEE RULES 4 & 5 BELOW!!
        # RULE 6: Extra fee during Friday rush (3 - 7 PM UTC)
        if self.get_weekday() == 'Friday' and self.get_hour() >= 15 and self.get_hour() < 19:
            self.fee *= 1.1
        # RULE 4: Reduce every delivery fee > 15 EUR to 15 EUR
        if self.fee > 1500:
            self.fee = 1500
        # RULE 5: For cart value >= 100 EUR, no delivery fee is assigned
        if self.cart_value >= 10000:
            self.fee = 0

    # Getter method for delivery fee
    def get_delivery_fee(self):
        return self.fee

    def get_hour(self):
        dt = datetime.strptime(self.time,'%Y-%m-%dT%H:%M:%S%fZ')
        return dt.strftime('%H') # Return the hour

    def get_weekday(self):
        dt = datetime.strptime(self.time,'%Y-%m-%dT%H:%M:%S%fZ')
        return dt.strftime('%A') # Return the day of the week

@app.route('/request') # Request route
def get_data():
    data = DeliveryFee.query.all()
    list = [] # List of dictionaries

    for d in data:
        delivery_data = {'cart_value': d.cart_value, 'delivery_distance': d.delivery_distance,
                         'number_of_items': d.number_of_items, 'time': d.time}
        list.append(delivery_data) # Add dictionary to list

    return {"delivery_data": list} # Serializable list of dictionaries

@app.route('/response/<id>') # Response route, pass ID as argument
def get_delivery_fee(id):
    data = DeliveryFee.query.get_or_404(id)
    data.calculate_delivery_fee() # Calculate the delivery fee based on rules

    return {"delivery_fee": data.get_delivery_fee()} # Return the delivery fee