from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

app = Flask(__name__)
CORS(app)

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/ecommerce')
engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

# Product model with image
class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    price = Column(Float)
    stock = Column(Integer)
    image_url = Column(String(500))

# Create tables
Base.metadata.create_all(engine)

# Initialize sample data with images
def init_db():
    session = SessionLocal()
    if session.query(Product).count() == 0:
        products = [
            Product(
                id=1, 
                name="Laptop", 
                price=2999, 
                stock=15,
                image_url="https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400"
            ),
            Product(
                id=2, 
                name="Mouse", 
                price=99, 
                stock=50,
                image_url="https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400"
            ),
            Product(
                id=3, 
                name="Keyboard", 
                price=299, 
                stock=30,
                image_url="https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400"
            ),
            Product(
                id=4, 
                name="Monitor", 
                price=1499, 
                stock=20,
                image_url="https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=400"
            ),
        ]
        session.add_all(products)
        session.commit()
    session.close()

init_db()

@app.route('/')
def home():
    return jsonify({
        "message": "E-Commerce API with PostgreSQL",
        "status": "running",
        "database": "connected"
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/products', methods=['GET'])
def get_products():
    session = SessionLocal()
    products = session.query(Product).all()
    result = [
        {
            "id": p.id, 
            "name": p.name, 
            "price": p.price, 
            "stock": p.stock,
            "image_url": p.image_url
        }
        for p in products
    ]
    session.close()
    return jsonify(result)

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    session = SessionLocal()
    product = session.query(Product).filter(Product.id == product_id).first()
    session.close()
    
    if product:
        return jsonify({
            "id": product.id, 
            "name": product.name, 
            "price": product.price, 
            "stock": product.stock,
            "image_url": product.image_url
        })
    return jsonify({"error": "Product not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)