from flask import Flask, request, jsonify
import hashlib
import os

app = Flask(__name__)

# Dummy user database (for simplicity)
users = {}
messages = {}

# Home Route
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Flask Chat API is running!"}), 200

# Register User
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = hashlib.sha256(data.get("password").encode()).hexdigest()
    
    if not data or "username" not in data or "password" not in data:
        return jsonify({"message": "Username and password are required"}), 400
    
    if username in users:
        return jsonify({"message": "User already exists"}), 400
    
    users[username] = password
    return jsonify({"message": "User registered successfully"}), 201

# Login User
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = hashlib.sha256(data.get("password").encode()).hexdigest()

    if not data or "username" not in data or "password" not in data:
        return jsonify({"message": "Username and password are required"}), 400

    if users.get(username) == password:
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Invalid credentials"}), 401

# Send Message (Simple Storage)
@app.route("/send", methods=["POST"])
def send_message():
    data = request.json
    sender = data.get("sender")
    receiver = data.get("receiver")
    message = data.get("message")

    if not data or "sender" not in data or "receiver" not in data or "message" not in data:
        return jsonify({"message": "Sender, receiver, and message are required"}), 400

    if sender not in users or receiver not in users:
        return jsonify({"message": "User not found"}), 400

    if receiver not in messages:
        messages[receiver] = []
    
    messages[receiver].append({"sender": sender, "message": message})
    return jsonify({"message": "Message sent"}), 200

# Get Messages for a User
@app.route("/messages/<username>", methods=["GET"])
def get_messages(username):
    if username not in messages:
        return jsonify({"messages": []})
    return jsonify({"messages": messages[username]})

# Run the App (Dynamic Port for Deployment)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 if no PORT is set
    app.run(host="0.0.0.0", port=port, debug=True)  # Start the app with dynamic port
s