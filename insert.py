from app import productsCollection
from datetime import datetime

productItems = [
    {
        "title": "Tshirt 1",
        "slug": "tshirt-1",
        "price": float(799),
        "qtyAvailable": 12,
        "image": "https://m.media-amazon.com/images/I/717UqXOrCNL._UX342_.jpg",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam odio mauris, varius a ultricies quis, vulputate id tellus. Fusce dignissim sed felis sit amet dapibus. Maecenas nibh dui, fringilla a nulla non, hendrerit euismod ipsum.",
        "timestamp": datetime.now()
    },
    {
        "title": "Jeans 1",
        "slug": "jeans-1",
        "price": float(599),
        "qtyAvailable": 12,
        "image": "https://m.media-amazon.com/images/I/71lvJqwMtoL._UX522_.jpg",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam odio mauris, varius a ultricies quis, vulputate id tellus. Fusce dignissim sed felis sit amet dapibus. Maecenas nibh dui, fringilla a nulla non, hendrerit euismod ipsum.",
        "timestamp": datetime.now()
    },
    {
        "title": "Laptop 1",
        "slug": "laptop-1",
        "price": float(60000),
        "qtyAvailable": 12,
        "image": "https://m.media-amazon.com/images/I/710NRdecQtL._SY355_.jpg",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam odio mauris, varius a ultricies quis, vulputate id tellus. Fusce dignissim sed felis sit amet dapibus. Maecenas nibh dui, fringilla a nulla non, hendrerit euismod ipsum.",
        "timestamp": datetime.now()
    }
]
insertMultipleProducts = productsCollection.insert_many(productItems)
if insertMultipleProducts:
    print("All products have been inserted successfully")
