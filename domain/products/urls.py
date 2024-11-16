# Products URLS

PRODUCT_LIST = "/api/products/list"
PRODUCT_ADD = "/api/products/add"
PRODUCT_UPDATE = "/api/products/update"
PRODUCT_IMG_UPDATE = "/api/products/images/update/{id:uuid}"
PRODUCT_REMOVE = "/api/products/delete/{id:uuid}"
PRODUCT_DETAIL = "/api/products/detail/{id:uuid}"
PRODUCT_SYNC_TYPESNSE = "/api/products/sync-products-to-typesense"
PRODUCT_SEMANTIC_SEARCH = "/api/products/ai_search"
PRODUCT_ADVANCED_SEARCH = "/api/products/search"
PRODUCT_EMBEDDING = "/api/products/embedding"

PRODUCT_IMG_UPLOAD = "/api/files/upload"
GET_IMG = "/api/products/images/{image_name:str}"