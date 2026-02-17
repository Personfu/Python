# Capstone REST API Server (Flask)
# CIS 425 — Capstone | Preston Furulie

from http.server import HTTPServer, BaseHTTPRequestHandler
import json

# In-memory data store for demo
products = [
    {"id": 1, "name": "Fender Stratocaster", "price": 1199.99, "category": "Guitars", "stock": 12},
    {"id": 2, "name": "Gibson Les Paul", "price": 2499.99, "category": "Guitars", "stock": 5},
    {"id": 3, "name": "Yamaha DGX-670", "price": 799.99, "category": "Keyboards", "stock": 8},
    {"id": 4, "name": "Roland TD-17KVX", "price": 1599.99, "category": "Drums", "stock": 3},
    {"id": 5, "name": "Shure SM58", "price": 99.99, "category": "Accessories", "stock": 45},
]


class APIHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        if self.path == "/api/products":
            self._send_json({"products": products, "count": len(products)})

        elif self.path.startswith("/api/products/"):
            pid = int(self.path.split("/")[-1])
            product = next((p for p in products if p["id"] == pid), None)
            if product:
                self._send_json(product)
            else:
                self._send_json({"error": "Not found"}, 404)

        elif self.path == "/api/health":
            self._send_json({"status": "healthy"})

        else:
            self._send_json({"error": "Not found"}, 404)


if __name__ == "__main__":
    server = HTTPServer(("localhost", 8080), APIHandler)
    print("API server running on http://localhost:8080")
    print("Endpoints: /api/products, /api/products/<id>, /api/health")
    server.serve_forever()
