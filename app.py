from flask import Flask, jsonify, request, abort
import pymongo
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

connectionString = os.environ['MONGODB_CLUSTER_URL']
client = pymongo.MongoClient(connectionString)

try:
     if(client):
        print("Connected to mongodb cluster successfully!")
except Exception as e:
    print("Error:", e)

db = client['MyAwesomeCart']
productsCollection = db.products

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello World!\nView the api routes: <a href=\"/api\">Click here</a>"

@app.route("/api")
def get_api_routes():
    routes = [
        {
            'route': '/api/products',
            'methods': 'GET',
            'description': 'Returns all the products.'
        },
        {
            'route': '/api/product/:slug',
            'methods': 'GET',
            'description': 'Returns a particular product.'
        },
        {
            'route': '/api/search',
            'methods': 'GET',
            'description': 'Returns the products related to the serach query.'
        },
        {
            'route': '/api/products/add',
            'methods': 'POST',
            'description': 'Adds a product in the database.'
        },
        {
            'route': '/api/products/update',
            'methods': 'POST, PUT',
            'description': 'Updates a product in the database.'
        },
        {
            'route': '/api/products/delete',
            'methods': 'POST, DELETE',
            'description': 'Deletes a product in the database.'
        }
    ]
    return jsonify({"total:": len(routes), "routes": routes})

@app.route("/api/products")
def product_items():
    products = []
    for product in productsCollection.find({}):
        products.append({
            "title": product['title'],
            "slug": product['slug'],
            "price": product['price'],
            "qtyAvailable": product['qtyAvailable'],
            "image": product['image'],
            "description": product['description'],
            "timestamp": product['timestamp']
        })
    return jsonify({"total:": len(products), "products": products})

@app.route("/api/product/<string:product_slug>")
def product_item(product_slug):
    product = []
    myproduct = productsCollection.find_one({"slug": product_slug})
    if not myproduct:
        return jsonify({"message": "No such product is avialble right now!"})
    else:
        product.append({
            "title": myproduct['title'],
            "slug": myproduct['slug'],
            "price": myproduct['price'],
            "qtyAvailable": myproduct['qtyAvailable'],
            "image": myproduct['image'],
            "description": myproduct['description'],
            "timestamp": myproduct['timestamp']
        })
        return jsonify({"product": product})

@app.route("/api/search")
def search_products():
    query = request.args.get("query")
    products = []
    for product in productsCollection.find({"title": {"$regex": query, "$options": "i"}}):
        products.append({
            "title": product['title'],
            "slug": product['slug'],
            "price": product['price'],
            "qtyAvailable": product['qtyAvailable'],
            "image": product['image'],
            "description": product['description'],
            "timestamp": product['timestamp']
        })
    return jsonify({"total:": len(products), "products": products})

@app.route("/api/products/add", methods=["POST"])
def add_product():
    if request.method == "POST":
        title = request.form.get("title")
        slug = request.form.get("slug")
        price = request.form.get("price")
        qtyAvailable = request.form.get("qtyAvailable")
        imageUrl = request.form.get("imageUrl")
        description = request.form.get("description")
        timestamp = datetime.now()

        product = {
            "title": title,
            "slug": slug,
            "price": float(price),
            "qtyAvailable": int(qtyAvailable),
            "image": imageUrl,
            "description": description,
            "timestamp": timestamp
        }

        createProduct = productsCollection.insert_one(product)
        if createProduct:
            return jsonify({"message": "Product has been inserted successfully!", "status": "success"})
        else:
            return jsonify({"message": "Some error occurred while creating a new product!", "status": "success"})
    else:
        abort(400, f"{request.method} method is not allowed!")

@app.route("/api/products/update", methods=["POST", "PUT"])
def update_product():
    if request.method == "POST" or request.method == "PUT":
        title = request.form.get("title")
        slug = request.form.get("slug")
        price = request.form.get("price")
        qtyAvailable = request.form.get("qtyAvailable")
        imageUrl = request.form.get("imageUrl")
        description = request.form.get("description")

        updateProduct = productsCollection.update_one({"slug": slug}, {"$set": {
            "title": title,
            "slug": slug,
            "price": float(price),
            "qtyAvailable": int(qtyAvailable),
            "image": imageUrl,
            "description": description
        }})
        if updateProduct:
            return jsonify({"message": "Product has been updated successfully!", "status": "success"})
        else:
            return jsonify({"message": "Some error occurred while updating the product!", "status": "success"})
    else:
        abort(400, f"{request.method} method is not allowed!")

@app.route("/api/products/delete", methods=["POST", "DELETE"])
def delete_product():
    if request.method == "POST" or request.method == "DELETE":
        slug = request.form.get("slug")

        deleteProduct = productsCollection.delete_one({"slug": slug})
        if deleteProduct:
            return jsonify({"message": "Product has been deleted successfully!", "status": "success"})
        else:
            return jsonify({"message": "Some error occurred while deleteing the product!", "status": "success"})
    else:
        abort(400, f"{request.method} method is not allowed!")

if __name__ == "__main__":
    app.run(debug=True)