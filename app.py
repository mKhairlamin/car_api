from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

# Load the car dataset into a pandas DataFrame
car_data = pd.read_csv('car_dataset.csv')

# Define the home route
@app.route('/')
def home():
    return "Car Dataset API is running!"

# Endpoint to retrieve all cars
@app.route('/cars', methods=['GET'])
def get_cars():
    cars = car_data.to_dict(orient='records')
    return jsonify(cars)

# Endpoint to retrieve a car by ID
@app.route('/car/<int:car_id>', methods=['GET'])
def get_car_by_id(car_id):
    car = car_data[car_data['car_id'] == car_id].to_dict(orient='records')
    if car:
        return jsonify(car[0])
    else:
        return jsonify({"error": "Car not found"}), 404

# Endpoint to filter cars by price range
@app.route('/cars/filter', methods=['GET'])
def filter_cars():
    min_price = request.args.get('min_price', default=0, type=int)
    max_price = request.args.get('max_price', default=999999, type=int)
    
    filtered_cars = car_data[(car_data['Price'] >= min_price) & (car_data['Price'] <= max_price)]
    return jsonify(filtered_cars.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
