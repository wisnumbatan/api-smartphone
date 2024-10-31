from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from datetime import datetime

app = Flask(__name__)
api = Api(app)

# Data contoh untuk toko smartphone
products = [
    {"id": "1", "name": "iPhone 13", "brand": "Apple", "description": "Smartphone Apple terbaru dengan A15 Bionic.", "price": 1000},
    {"id": "2", "name": "Galaxy S22", "brand": "Samsung", "description": "Smartphone flagship Samsung dengan Snapdragon 8 Gen 1.", "price": 900},
    {"id": "3", "name": "Xiaomi Mi 11", "brand": "Xiaomi", "description": "Smartphone Xiaomi dengan harga terjangkau dan performa tinggi.", "price": 700},
    {"id": "4", "name": "OnePlus 9", "brand": "OnePlus", "description": "OnePlus dengan kecepatan refresh layar 120Hz.", "price": 800},
    {"id": "5", "name": "Google Pixel 6", "brand": "Google", "description": "Smartphone Google dengan AI kamera yang canggih.", "price": 850},
    {"id": "6", "name": "Sony Xperia 5 III", "brand": "Sony", "description": "Smartphone Sony dengan layar OLED 120Hz.", "price": 950},
    {"id": "7", "name": "Huawei P50 Pro", "brand": "Huawei", "description": "Smartphone flagship Huawei dengan kamera Leica.", "price": 900},
    {"id": "8", "name": "Oppo Find X5", "brand": "Oppo", "description": "Smartphone Oppo dengan desain premium dan kamera unggul.", "price": 780},
    {"id": "9", "name": "Realme GT 2 Pro", "brand": "Realme", "description": "Realme dengan layar AMOLED dan Snapdragon 8 Gen 1.", "price": 650},
    {"id": "10", "name": "Asus ROG Phone 5", "brand": "Asus", "description": "Smartphone gaming Asus dengan baterai 6000 mAh.", "price": 1000}
]

details = {
    "1": {"specs": "A15 Bionic, 128GB Storage, 12MP Camera", "customerReviews": []},
    "2": {"specs": "Snapdragon 8 Gen 1, 128GB Storage, 50MP Camera", "customerReviews": []},
    "3": {"specs": "Snapdragon 888, 128GB Storage, 108MP Camera", "customerReviews": []},
    "4": {"specs": "Snapdragon 888, 256GB Storage, 48MP Camera", "customerReviews": []},
    "5": {"specs": "Google Tensor, 128GB Storage, 50MP Camera", "customerReviews": []},
    "6": {"specs": "Snapdragon 888, 128GB Storage, OLED Display", "customerReviews": []},
    "7": {"specs": "Kirin 9000, 256GB Storage, 50MP Leica Camera", "customerReviews": []},
    "8": {"specs": "Snapdragon 888, 128GB Storage, 50MP Camera", "customerReviews": []},
    "9": {"specs": "Snapdragon 8 Gen 1, 128GB Storage, 50MP Camera", "customerReviews": []},
    "10": {"specs": "Snapdragon 888, 128GB Storage, 6000 mAh Battery", "customerReviews": []}
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
