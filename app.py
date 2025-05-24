from flask import Flask, render_template, request, jsonify
import json, random, os

app = Flask(__name__)
DATA_FILE = 'store_data.json'

# 讀資料
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# 分類邏輯
def classify(drink_name):
    name = drink_name.lower()
    if any(k in name for k in ["奶", "乳"]):
        return "奶茶類"
    elif any(k in name for k in ["烏龍", "紅茶", "綠茶", "青", "四季", "高山"]):
        return "純茶類"
    elif any(k in name for k in ["果", "檸檬", "葡萄", "芒果", "柳橙"]):
        return "水果類"
    else:
        return "其他"

@app.route('/')
def index():
    data = load_data()
    stores = list(data.keys())
    return render_template('index.html', stores=stores)

@app.route('/suggest', methods=['POST'])
def suggest():
    data = load_data()
    budget = float(request.form['budget'])
    store = request.form['store']
    category = request.form['category']

    available = []

    target_stores = [store] if store in data else data.keys()
    for s in target_stores:
        for name, price in data[s].items():
            if price <= budget:
                cat = classify(name)
                if category == "不限" or category == cat:
                    available.append((s, name, price, cat))

    if available:
        s, n, p, c = random.choice(available)
        return jsonify({"store": s, "drink": n, "price": p, "category": c})
    else:
        return jsonify({"error": "找不到符合條件的飲料"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Render 會提供 PORT 變數
    app.run(host='0.0.0.0', port=port)
