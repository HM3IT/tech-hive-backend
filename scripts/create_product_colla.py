import typesense
from product_schema_typesense import product_schema

HOST = "6fu5w7p0ksgon83zp-1.a1.typesense.net"
TYPESENSE_API_KEY = "I1v85264rZoL6r11vh3BNZkuQDQqcN7n"

client = typesense.Client({
    "nodes": [{
        "host": HOST,
        "port": "443",
        "protocol": "https"
    }],
    "api_key": TYPESENSE_API_KEY,
    "connection_timeout_seconds": 180
})

client.collections.create(product_schema)
