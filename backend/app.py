from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# In-memory data (we'll add database later)
products = [
    {"id": 1, "name": "Laptop", "price": 2999, "stock": 15},
    {"id": 2, "name": "Mouse", "price": 99, "stock": 50},
    {"id": 3, "name": "Keyboard", "price": 299, "stock": 30},
    {"id": 4, "name": "Monitor", "price": 1499, "stock": 20},
]

orders = []

@app.route('/')
def home():
    return jsonify({
        "message": "E-Commerce API",
        "status": "running",
        "endpoints": ["/products", "/orders"]
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return jsonify(product)
    return jsonify({"error": "Product not found"}), 404

@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify(orders)

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    order = {
        "id": len(orders) + 1,
        "product_id": data.get('product_id'),
        "quantity": data.get('quantity'),
        "timestamp": datetime.now().isoformat()
    }
    orders.append(order)
    return jsonify(order), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)