# Products URLS

PRODUCT_LIST = "/api/products"
PRODUCT_ADD = "/api/products/add"
PRODUCT_UPDATE = "/api/products/update"
PRODUCT_IMG_UPDATE = "/api/products/images/update"
PRODUCT_REMOVE = "/api/products/{id:uuid}"
PRODUCT_DETAIL = "/api/products/{id:uuid}"
PRODUCT_SYNC_TYPESNSE = "/api/products/sync-products-to-typesense"
PRODUCT_SEMANTIC_SEARCH = "/api/products/search/{query_str:str}"
PRODUCT_IMG_UPLOAD = "/api/files/upload"