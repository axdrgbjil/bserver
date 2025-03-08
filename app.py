from flask import Flask, request, jsonify
import bcrypt
import random

app = Flask(__name__)

# Pre-selected hard passwords from RockYou.txt
HARD_PASSWORDS = [
"caitlyn", "whiskers", "watson", "angel01", "therese", "monster1", "forever21", "crazygirl", "master1", "pazaway", "1princess", "terry", "pangga", "klapaucius", "gemma", "froggie", "felix", "washington", "reading", "qwertyui", "pinkgirl"
]


# Secret modification function
def modify_password(password):
    return "!" + password[::-1]  # Reverse and add '!' in front

# Generate challenge
@app.route('/get_hash', methods=['GET'])
def get_hash():
    original_password = random.choice(HARD_PASSWORDS)  # Select a hard password
    modified_password = modify_password(original_password)  # Apply the secret modification
    hashed_password = bcrypt.hashpw(modified_password.encode(), bcrypt.gensalt())

    # Store for verification
    app.config["CURRENT_PASSWORD"] = modified_password

    return jsonify({"hash": hashed_password.decode(), "hint": "Think about transformations!"})

# Verify the solution
@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    if not data or "password" not in data:
        return jsonify({"error": "Missing password field"}), 400

    user_password = data["password"]

    # Check if the password matches
    if user_password == app.config.get("CURRENT_PASSWORD", ""):
        return jsonify({"flag": "CTF{bCryP7_7r4n5f0rm4710n_IS_FuN}"}), 200
    else:
        return jsonify({"error": "Incorrect password"}), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
