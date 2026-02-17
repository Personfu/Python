# ============================================================
# REST API Server — Complete Implementation
# CIS 425 — Capstone | Preston Furulie
# ============================================================
# Covers: HTTP server, routing, GET/POST/PUT/DELETE, query
# parameters, pagination, JSON request/response, error
# handling, CORS, input validation, authentication tokens,
# middleware pattern, and logging.
# ============================================================

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import time
import hashlib
import secrets
from datetime import datetime


# ── Data Store (In-Memory Database) ─────────────────────────

class DataStore:
    """In-memory data store simulating a database.
    In production, this would be MySQL/PostgreSQL."""

    def __init__(self):
        self.products = [
            {"id": 1, "name": "Fender Stratocaster",     "price": 1199.99, "category": "Guitars",      "stock": 12, "created": "2026-01-15"},
            {"id": 2, "name": "Gibson Les Paul Standard", "price": 2499.99, "category": "Guitars",      "stock": 5,  "created": "2026-01-15"},
            {"id": 3, "name": "Yamaha DGX-670",           "price": 799.99,  "category": "Keyboards",    "stock": 8,  "created": "2026-01-20"},
            {"id": 4, "name": "Roland TD-17KVX",          "price": 1599.99, "category": "Drums",        "stock": 3,  "created": "2026-01-22"},
            {"id": 5, "name": "Shure SM58",               "price": 99.99,   "category": "Accessories",  "stock": 45, "created": "2026-01-25"},
            {"id": 6, "name": "Taylor 214ce",             "price": 1299.99, "category": "Guitars",      "stock": 7,  "created": "2026-02-01"},
            {"id": 7, "name": "Boss Katana 100 MKII",     "price": 369.99,  "category": "Amplifiers",   "stock": 15, "created": "2026-02-05"},
            {"id": 8, "name": "Ibanez RG550",             "price": 999.99,  "category": "Guitars",      "stock": 4,  "created": "2026-02-10"},
        ]
        self._next_id = 9

        self.users = {
            "admin": {
                "password_hash": hashlib.sha256("admin123".encode()).hexdigest(),
                "role": "admin",
                "name": "Admin User"
            },
            "staff": {
                "password_hash": hashlib.sha256("staff123".encode()).hexdigest(),
                "role": "staff",
                "name": "Staff User"
            }
        }
        self.tokens = {}  # token → username mapping

    def get_products(self, category=None, search=None, sort_by="id",
                     order="asc", page=1, limit=10):
        """Query products with filtering, sorting, and pagination."""
        results = self.products.copy()

        # Filter by category
        if category:
            results = [p for p in results if p["category"].lower() == category.lower()]

        # Search by name
        if search:
            results = [p for p in results if search.lower() in p["name"].lower()]

        # Sort
        reverse = order.lower() == "desc"
        if sort_by in ("name", "price", "stock", "id", "category"):
            results.sort(key=lambda p: p.get(sort_by, ""), reverse=reverse)

        # Paginate
        total = len(results)
        start = (page - 1) * limit
        end = start + limit
        page_results = results[start:end]

        return {
            "products": page_results,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "pages": (total + limit - 1) // limit
            }
        }

    def get_product(self, product_id):
        """Get a single product by ID."""
        for p in self.products:
            if p["id"] == product_id:
                return p
        return None

    def create_product(self, data):
        """Create a new product."""
        required = ["name", "price", "category"]
        for field in required:
            if field not in data:
                return None, f"Missing required field: {field}"

        product = {
            "id": self._next_id,
            "name": data["name"],
            "price": float(data["price"]),
            "category": data["category"],
            "stock": int(data.get("stock", 0)),
            "created": datetime.now().strftime("%Y-%m-%d")
        }
        self._next_id += 1
        self.products.append(product)
        return product, None

    def update_product(self, product_id, data):
        """Update an existing product."""
        product = self.get_product(product_id)
        if not product:
            return None, "Product not found"

        for key in ("name", "price", "category", "stock"):
            if key in data:
                if key == "price":
                    product[key] = float(data[key])
                elif key == "stock":
                    product[key] = int(data[key])
                else:
                    product[key] = data[key]
        return product, None

    def delete_product(self, product_id):
        """Delete a product by ID."""
        for i, p in enumerate(self.products):
            if p["id"] == product_id:
                return self.products.pop(i)
        return None

    def authenticate(self, username, password):
        """Validate credentials and return a session token."""
        user = self.users.get(username)
        if not user:
            return None
        pw_hash = hashlib.sha256(password.encode()).hexdigest()
        if pw_hash != user["password_hash"]:
            return None
        token = secrets.token_hex(32)
        self.tokens[token] = username
        return token

    def validate_token(self, token):
        """Check if a token is valid and return the username."""
        return self.tokens.get(token)


# ── Global Store ────────────────────────────────────────────

db = DataStore()


# ── API Request Handler ─────────────────────────────────────

class APIHandler(BaseHTTPRequestHandler):
    """HTTP request handler implementing REST API patterns."""

    def _send_json(self, data, status=200):
        """Send a JSON response with CORS headers."""
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())

    def _read_body(self):
        """Read and parse JSON request body."""
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length == 0:
            return {}
        body = self.rfile.read(content_length)
        try:
            return json.loads(body.decode())
        except json.JSONDecodeError:
            return None

    def _get_token(self):
        """Extract Bearer token from Authorization header."""
        auth = self.headers.get("Authorization", "")
        if auth.startswith("Bearer "):
            return auth[7:]
        return None

    def _require_auth(self):
        """Middleware: require valid authentication token."""
        token = self._get_token()
        if not token:
            self._send_json({"error": "Authorization header required"}, 401)
            return None
        username = db.validate_token(token)
        if not username:
            self._send_json({"error": "Invalid or expired token"}, 401)
            return None
        return username

    def log_message(self, format, *args):
        """Override default logging for cleaner output."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"  [{timestamp}] {args[0]}")

    # ── GET Routes ──────────────────────────────────────────

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        # Health check
        if path == "/api/health":
            self._send_json({
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "version": "1.0.0"
            })

        # List products (with query params)
        elif path == "/api/products":
            category = params.get("category", [None])[0]
            search = params.get("search", [None])[0]
            sort_by = params.get("sort", ["id"])[0]
            order = params.get("order", ["asc"])[0]
            page = int(params.get("page", [1])[0])
            limit = int(params.get("limit", [10])[0])
            limit = min(limit, 100)  # cap at 100

            result = db.get_products(category, search, sort_by, order, page, limit)
            self._send_json(result)

        # Get single product
        elif path.startswith("/api/products/"):
            try:
                pid = int(path.split("/")[-1])
                product = db.get_product(pid)
                if product:
                    self._send_json(product)
                else:
                    self._send_json({"error": "Product not found"}, 404)
            except ValueError:
                self._send_json({"error": "Invalid product ID"}, 400)

        # List categories
        elif path == "/api/categories":
            categories = list(set(p["category"] for p in db.products))
            self._send_json({"categories": sorted(categories)})

        # Stats
        elif path == "/api/stats":
            total_products = len(db.products)
            total_value = sum(p["price"] * p["stock"] for p in db.products)
            avg_price = sum(p["price"] for p in db.products) / total_products if total_products else 0
            low_stock = [p for p in db.products if p["stock"] < 5]
            self._send_json({
                "total_products": total_products,
                "total_inventory_value": round(total_value, 2),
                "average_price": round(avg_price, 2),
                "low_stock_count": len(low_stock),
                "low_stock_items": [p["name"] for p in low_stock]
            })

        else:
            self._send_json({"error": "Not found", "path": path}, 404)

    # ── POST Routes ─────────────────────────────────────────

    def do_POST(self):
        path = urlparse(self.path).path

        # Login
        if path == "/api/auth/login":
            body = self._read_body()
            if not body:
                self._send_json({"error": "Invalid JSON body"}, 400)
                return
            username = body.get("username", "")
            password = body.get("password", "")
            token = db.authenticate(username, password)
            if token:
                self._send_json({"token": token, "user": username}, 200)
            else:
                self._send_json({"error": "Invalid credentials"}, 401)

        # Create product (requires auth)
        elif path == "/api/products":
            username = self._require_auth()
            if not username:
                return
            body = self._read_body()
            if not body:
                self._send_json({"error": "Invalid JSON body"}, 400)
                return
            product, error = db.create_product(body)
            if error:
                self._send_json({"error": error}, 400)
            else:
                self._send_json(product, 201)

        else:
            self._send_json({"error": "Not found"}, 404)

    # ── PUT Routes ──────────────────────────────────────────

    def do_PUT(self):
        path = urlparse(self.path).path

        if path.startswith("/api/products/"):
            username = self._require_auth()
            if not username:
                return
            try:
                pid = int(path.split("/")[-1])
            except ValueError:
                self._send_json({"error": "Invalid product ID"}, 400)
                return
            body = self._read_body()
            if not body:
                self._send_json({"error": "Invalid JSON body"}, 400)
                return
            product, error = db.update_product(pid, body)
            if error:
                self._send_json({"error": error}, 404)
            else:
                self._send_json(product)

        else:
            self._send_json({"error": "Not found"}, 404)

    # ── DELETE Routes ───────────────────────────────────────

    def do_DELETE(self):
        path = urlparse(self.path).path

        if path.startswith("/api/products/"):
            username = self._require_auth()
            if not username:
                return
            try:
                pid = int(path.split("/")[-1])
            except ValueError:
                self._send_json({"error": "Invalid product ID"}, 400)
                return
            deleted = db.delete_product(pid)
            if deleted:
                self._send_json({"message": f"Deleted product {pid}", "product": deleted})
            else:
                self._send_json({"error": "Product not found"}, 404)

        else:
            self._send_json({"error": "Not found"}, 404)

    # ── OPTIONS (CORS Preflight) ────────────────────────────

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()


# ── Server Entry Point ──────────────────────────────────────

if __name__ == "__main__":
    HOST = "localhost"
    PORT = 8080

    print("=" * 60)
    print("  GUITAR SHOP REST API — CIS 425 | Preston Furulie")
    print("=" * 60)
    print(f"\n  Server: http://{HOST}:{PORT}")
    print(f"\n  Endpoints:")
    print(f"    GET    /api/health                 Health check")
    print(f"    GET    /api/products               List (filter, sort, paginate)")
    print(f"    GET    /api/products/:id            Get one")
    print(f"    GET    /api/categories              List categories")
    print(f"    GET    /api/stats                   Inventory stats")
    print(f"    POST   /api/auth/login              Login (get token)")
    print(f"    POST   /api/products               Create (auth required)")
    print(f"    PUT    /api/products/:id            Update (auth required)")
    print(f"    DELETE /api/products/:id            Delete (auth required)")
    print(f"\n  Query params: ?category=Guitars&search=fender&sort=price&order=desc&page=1&limit=5")
    print(f"\n  Test credentials: admin/admin123 or staff/staff123")
    print(f"\n  Press Ctrl+C to stop.\n")

    server = HTTPServer((HOST, PORT), APIHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server stopped.")
        server.server_close()
