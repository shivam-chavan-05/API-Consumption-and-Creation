from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Setup Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

# Define Model
class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.description}"

# Ensure database is created within the application context
with app.app_context():
    db.create_all()

# Endpoint to initialize the database manually
@app.route('/init_db')
def init_db():
    with app.app_context():
        db.create_all()
    return "Database initialized!"

# API Endpoints
@app.route('/')
def index():
    return 'Hello World'

# Get all drinks
@app.route('/drinks', methods=['GET'])
def get_drinks():
    drinks = Drink.query.all()
    output = [{'id': drink.id, 'name': drink.name, 'description': drink.description} for drink in drinks]
    return jsonify({'drinks': output})

# Add a new drink (POST)
@app.route('/drinks', methods=['POST'])
def add_drink():
    data = request.get_json()
    new_drink = Drink(name=data['name'], description=data['description'])
    db.session.add(new_drink)
    db.session.commit()
    return jsonify({'message': 'Drink added successfully!'})

# Update an existing drink (PUT)
@app.route('/drinks/<int:id>', methods=['PUT'])
def update_drink(id):
    drink = Drink.query.get(id)
    if drink is None:
        return jsonify({'message': 'Drink not found'}), 404

    data = request.get_json()
    drink.name = data.get('name', drink.name)
    drink.description = data.get('description', drink.description)
    db.session.commit()
    return jsonify({'message': 'Drink updated successfully!'})

# Delete a drink (DELETE)
@app.route('/drinks/<int:id>', methods=['DELETE'])
def delete_drink(id):
    drink = Drink.query.get(id)
    if drink is None:
        return jsonify({'message': 'Drink not found'}), 404

    db.session.delete(drink)
    db.session.commit()
    return jsonify({'message': 'Drink deleted successfully!'})

if __name__ == "__main__":
    app.run(debug=True)
