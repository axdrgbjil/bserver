from flask import Flask, request, jsonify
import bcrypt
import random

app = Flask(__name__)

# Pre-selected hard passwords from RockYou.txt
HARD_PASSWORDS = [
"caitlyn", "whiskers", "watson", "angel01", "therese", "monster1", "forever21", "crazygirl", "master1", "pazaway", "1princess", "terry", "pangga", "klapaucius", "gemma", "froggie", "felix", "washington", "reading", "qwertyui", "pinkgirl"
]

# Secret modification function (harder to guess)
def modify_password(password):
    return "!" + password[::-1]  # Change '!' to 'X'

# Store hashes in memory for validation
app.config["STORED_HASHES"] = {}

@app.route('/get_hash', methods=['GET'])
def get_hash():
    original_password = random.choice(HARD_PASSWORDS)
    modified_password = modify_password(original_password)
    hashed_password = bcrypt.hashpw(modified_password.encode(), bcrypt.gensalt())

    # Store the correct hash
    app.config["STORED_HASHES"][hashed_password.decode()] = modified_password

    return jsonify({"hash": hashed_password.decode(), "hint": "Think about transformations!"})

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    if not data or "password" not in data or "hash" not in data:
        return jsonify({"error": "Missing password or hash field"}), 400

    user_password = data["password"]
    received_hash = data["hash"]

    # Verify password using stored hash
    correct_password = app.config["STORED_HASHES"].get(received_hash)

    if correct_password and user_password == correct_password:
        return jsonify({"flag": "CTF{bCryP7_7r4n5f0rm4710n_IS_FuN}"}), 200
    else:
        return jsonify({"error": "Incorrect password"}), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
