from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from datetime import datetime

app = Flask(__name__)
api = Api(app)

# Data contoh untuk toko smartphone
products = [
    {"id": "1", "name": "iPhone 13", "brand": "Apple", "description": "Smartphone Apple terbaru", "price": 1000},
    {"id": "2", "name": "Galaxy S22", "brand": "Samsung", "description": "Smartphone flagship Samsung", "price": 900},
    {"id": "3", "name": "Xiaomi Mi 11", "brand": "Xiaomi", "description": "Smartphone Xiaomi dengan harga terjangkau", "price": 700}
]

details = {
    "1": {"specs": "A15 Bionic, 128GB Storage", "customerReviews": []},
    "2": {"specs": "Snapdragon 8 Gen 1, 128GB Storage", "customerReviews": []},
    "3": {"specs": "Snapdragon 888, 128GB Storage", "customerReviews": []}
}

# Endpoint untuk daftar produk
class ProductList(Resource):
    def get(self):
        return {
            "error": False,
            "message": "success",
            "count": len(products),
            "products": products
        }

# Endpoint untuk detail produk berdasarkan ID
class ProductDetail(Resource):
    def get(self, product_id):
        if product_id in details:
            product = next((p for p in products if p["id"] == product_id), None)
            if product:
                return {
                    "error": False,
                    "message": "success",
                    "product": product,
                    "details": details[product_id]
                }
        return {"error": True, "message": "Product not found"}, 404

# Endpoint untuk mencari produk berdasarkan nama atau deskripsi
class ProductSearch(Resource):
    def get(self):
        query = request.args.get('q', '').lower()
        result = [p for p in products if query in p['name'].lower() or query in p['description'].lower()]
        return {
            "error": False,
            "found": len(result),
            "products": result
        }

# Tambahkan semua endpoint ke API
api.add_resource(ProductList, '/products')
api.add_resource(ProductDetail, '/products/<string:product_id>')
api.add_resource(ProductSearch, '/products/search')

if __name__ == '__main__':
    app.run(debug=True)
