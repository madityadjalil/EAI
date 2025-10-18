from flask import Flask, request, jsonify
import jwt
import datetime
from functools import wraps
from dotenv import load_dotenv
import os

load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET", "defaultsecret")
PORT = int(os.getenv("PORT", 5000))

app = Flask(__name__)

demo_user = {
    "email": "user1@example.com",
    "password": "pass123",
    "name": "DJALIL KIRANA KHADAFI FARISHA"
}

items = [
    {"id": 1, "name": "Laptop", "price": 10000000},
    {"id": 2, "name": "Headphone", "price": 500000},
    {"id": 3, "name": "Mouse", "price": 150000}
]

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"error": "Missing or invalid Authorization header"}), 401

        try:
            decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            request.user = decoded
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)
    return decorated


# Endpoint 1: Login 
@app.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if email == demo_user["email"] and password == demo_user["password"]:
        payload = {
            "sub": email,
            "email": email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
        return jsonify({"access_token": token})

    return jsonify({"error": "Invalid credentials"}), 401


# Endpoint 2: Items (Public)
@app.route("/items", methods=["GET"])
def get_items():
    return jsonify({"items": items}), 200


#Endpoint 3: Profile (Protected)
@app.route("/profile", methods=["PUT"])
@token_required
def update_profile():
    data = request.get_json()
    name = data.get("name") 
    email = data.get("email")

    user_email = request.user["email"]

    if user_email != demo_user["email"]:
        return jsonify({"error": "User not found"}), 404

    if name:
        demo_user["name"] = name
    if email:
        demo_user["email"] = email

    return jsonify({
        "message": "Profile updated",
        "profile": {"name": demo_user["name"], "email": demo_user["email"]}
    }), 200

if __name__ == "__main__":
    print(f"Server running on http://127.0.0.1:{PORT}")
    app.run(port=PORT, debug=True)
