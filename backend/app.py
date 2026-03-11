from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import redis
import json

app = Flask(__name__)
CORS(app)

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/ecommerce')
engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

# Redis configuration
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

# Product model
class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    price = Column(Float)
    stock = Column(Integer)
    image_url = Column(String(500))

# Create tables
Base.metadata.create_all(engine)

# Initialize sample data
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
        "message": "E-Commerce API with PostgreSQL & Redis Cache",
        "status": "running",
        "database": "connected",
        "cache": "enabled"
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/products', methods=['GET'])
def get_products():
    # Try to get from cache first
    cache_key = "products:all"
    cached_data = redis_client.get(cache_key)
    
    if cached_data:
        # Cache hit - return cached data
        print("Cache HIT - returning from Redis")
        return jsonify(json.loads(cached_data))
    
    # Cache miss - query database
    print("Cache MISS - querying database")
    session = SessionLocal()
    products = session.query(Product).all()
    result = [
        {"id": p.id, "name": p.name, "price": p.price, "stock": p.stock, "image_url": p.image_url}
        for p in products
    ]
    session.close()
    
    # Store in cache for 5 minutes (300 seconds)
    redis_client.setex(cache_key, 300, json.dumps(result))
    print("Stored in cache for 5 minutes")
    
    return jsonify(result)

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    # Try cache first
    cache_key = f"product:{product_id}"
    cached_data = redis_client.get(cache_key)
    
    if cached_data:
        print(f"Cache HIT - product {product_id}")
        return jsonify(json.loads(cached_data))
    
    # Cache miss - query database
    print(f"Cache MISS - product {product_id}")
    session = SessionLocal()
    product = session.query(Product).filter(Product.id == product_id).first()
    session.close()
    
    if product:
        result = {
            "id": product.id, 
            "name": product.name, 
            "price": product.price, 
            "stock": product.stock,
            "image_url": product.image_url
        }
        # Cache for 5 minutes
        redis_client.setex(cache_key, 300, json.dumps(result))
        return jsonify(result)
    
    return jsonify({"error": "Product not found"}), 404

@app.route('/cache/clear', methods=['POST'])
def clear_cache():
    """Clear all cache - useful for testing"""
    redis_client.flushdb()
    return jsonify({"message": "Cache cleared successfully"})

@app.route('/cache/stats', methods=['GET'])
def cache_stats():
    """Get cache statistics"""
    info = redis_client.info('stats')
    return jsonify({
        "total_keys": redis_client.dbsize(),
        "cache_hits": info.get('keyspace_hits', 0),
        "cache_misses": info.get('keyspace_misses', 0)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)