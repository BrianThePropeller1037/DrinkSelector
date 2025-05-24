from flask import Flask, render_template, jsonify
import json, random

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_drink")
def get_drink():
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    if not data:
        return jsonify({"error": "沒有店家資料"})
    shop = random.choice(list(data.keys()))
    drink = random.choice(data[shop])
    return jsonify({"shop": shop, "drink": drink})

if __name__ == "__main__":
    app.run(debug=True)