from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from datetime import datetime

# Data contoh produk smartphone yang lebih lengkap
smartphone_products = [
    {"id": "1", "name": "Smartphone A", "description": "Smartphone dengan kamera 48MP dan RAM 6GB.", "price": 2500000},
    {"id": "2", "name": "Smartphone B", "description": "Kinerja cepat dengan prosesor terbaru.", "price": 3000000},
    {"id": "3", "name": "Smartphone C", "description": "Desain premium dengan layar AMOLED.", "price": 3500000},
    {"id": "4", "name": "Smartphone D", "description": "Baterai tahan lama dengan pengisian cepat.", "price": 2000000},
    {"id": "5", "name": "Smartphone E", "description": "Smartphone gaming dengan refresh rate tinggi.", "price": 4000000}
]

# Detail produk yang lebih lengkap
product_details = {product['id']: {**product, "customerReviews": []} for product in smartphone_products}

app = Flask(__name__)
api = Api(app)

class ProductList(Resource):
    def get(self):
        return {
            "error": False,
            "message": "success",
            "count": len(smartphone_products),
            "products": smartphone_products
        }

class ProductDetail(Resource):
    def get(self, product_id):
        if product_id in product_details:
            return {
                "error": False,
                "message": "success",
                "product": product_details[product_id]
            }
        return {"error": True, "message": "Product not found"}, 404

class ProductSearch(Resource):
    def get(self):
        query = request.args.get('q', '').lower()
        result = [p for p in smartphone_products if query in p['name'].lower() or query in p['description'].lower()]
        return {
            "error": False,
            "found": len(result),
            "products": result
        }

class AddReview(Resource):
    def post(self):
        data = request.get_json()
        product_id = data.get('id')
        name = data.get('name')
        review = data.get('review')
        
        if product_id in product_details:
            new_review = {
                "name": name,
                "review": review,
                "date": datetime.now().strftime("%d %B %Y")
            }
            product_details[product_id]['customerReviews'].append(new_review)
            return {
                "error": False,
                "message": "Review added successfully",
                "customerReviews": product_details[product_id]['customerReviews']
            }
        return {"error": True, "message": "Product not found"}, 404

class UpdateReview(Resource):
    def put(self):
        data = request.get_json()
        product_id = data.get('id')
        name = data.get('name')
        new_review_text = data.get('review')
        
        if product_id in product_details:
            reviews = product_details[product_id]['customerReviews']
            review_to_update = next((r for r in reviews if r['name'] == name), None)
            if review_to_update:
                review_to_update['review'] = new_review_text
                review_to_update['date'] = datetime.now().strftime("%d %B %Y")
                return {
                    "error": False,
                    "message": "Review updated successfully",
                    "customerReviews": reviews
                }
            return {"error": True, "message": "Review not found"}, 404
        return {"error": True, "message": "Product not found"}, 404

class DeleteReview(Resource):
    def delete(self):
        data = request.get_json()
        product_id = data.get('id')
        name = data.get('name')
        
        if product_id in product_details:
            reviews = product_details[product_id]['customerReviews']
            review_to_delete = next((r for r in reviews if r['name'] == name), None)
            if review_to_delete:
                reviews.remove(review_to_delete)
                return {
                    "error": False,
                    "message": "Review deleted successfully",
                    "customerReviews": reviews
                }
            return {"error": True, "message": "Review not found"}, 404
        return {"error": True, "message": "Product not found"}, 404

# Menambahkan resource ke API
api.add_resource(ProductList, '/list')
api.add_resource(ProductDetail, '/detail/<string:product_id>')
api.add_resource(ProductSearch, '/search')
api.add_resource(AddReview, '/review')
api.add_resource(UpdateReview, '/review/update')
api.add_resource(DeleteReview, '/review/delete')

if __name__ == '__main__':
    app.run(debug=True)
