product_schema = {
    "name": "products-collection",
    "fields": [
        {"name": "id", "type": "string", "facet": False},
        {"name": "name", "type": "string", "facet": False},
        {"name": "description", "type": "string", "facet": False},
        {"name": "imageUrl", "type": "string", "facet": False},
        {"name": "price", "type": "float", "facet": True},
        {"name": "discountPercent", "type": "float", "facet": True},
        {"name": "discountPrice", "type": "float", "facet": True},
        {"name": "brand", "type": "string", "facet": True},
        {"name": "stock", "type": "int32", "facet": True},
        {"name": "sold", "type": "int32", "facet": True},
        {"name": "tags", "type": "string[]", "facet": True},
        {"name": "categoryName", "type": "string", "facet": True},
        {"name": "productRating", "type": "float", "facet": False},
        {"name": "embedding", "type": "float[]", "num_dim": 384}
    ],
    "default_sorting_field": "sold"
}
