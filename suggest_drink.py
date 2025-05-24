import tkinter as tk
from tkinter import messagebox
import json
import os
import random

# 資料來源
json_file = "store_data.json"

def load_data():
    if os.path.exists(json_file):
        with open(json_file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
            except json.JSONDecodeError:
                pass
    return {}

store_data = load_data()

# 建立主介面
root = tk.Tk()
root.title("飲料隨機推薦機")
root.geometry("450x420")
root.configure(bg="#fff8dc")

tk.Label(root, text="請輸入預算 (台幣)", font=("Helvetica", 14), bg="#fff8dc").pack(pady=10)
budget_entry = tk.Entry(root, font=("Helvetica", 12))
budget_entry.pack(pady=5)

# 店家選擇
tk.Label(root, text="選擇店家（可選）", font=("Helvetica", 14), bg="#fff8dc").pack(pady=5)
store_var = tk.StringVar(root)
store_list = list(store_data.keys())
store_var.set("全部店家")
store_dropdown = tk.OptionMenu(root, store_var, "全部店家", *store_list)
store_dropdown.pack(pady=5)

# 類別選擇
tk.Label(root, text="選擇飲料類別（可選）", font=("Helvetica", 14), bg="#fff8dc").pack(pady=5)
category_var = tk.StringVar(root)
category_options = ["不限", "奶茶類", "純茶類", "水果類", "其他"]
category_var.set("不限")
category_dropdown = tk.OptionMenu(root, category_var, *category_options)
category_dropdown.pack(pady=5)

# 結果
result_label = tk.Label(root, text="", font=("Helvetica", 12), bg="#fff8dc", wraplength=400, justify="center")
result_label.pack(pady=20)

# 推薦邏輯
def suggest_drink():
    try:
        budget = float(budget_entry.get())
    except ValueError:
        messagebox.showerror("錯誤", "請輸入有效的數字")
        return

    selected_store = store_var.get()
    selected_category = category_var.get()
    available = []

    target_stores = [selected_store] if selected_store in store_data else store_data.keys()

    for store in target_stores:
        for drink_name, price in store_data[store].items():
            if price <= budget:
                name = drink_name.lower()
                # 分類判斷
                if any(k in name for k in ["奶", "乳"]):
                    category = "奶茶類"
                elif any(k in name for k in ["烏龍", "紅茶", "綠茶", "青", "四季", "高山"]):
                    category = "純茶類"
                elif any(k in name for k in ["果", "檸檬", "葡萄", "芒果", "柳橙"]):
                    category = "水果類"
                else:
                    category = "其他"

                if selected_category == "不限" or selected_category == category:
                    available.append((store, drink_name, price, category))

    if available:
        store, drink, price, category = random.choice(available)
        result_label.config(
            text=f"🎉 推薦：{store} 的「{drink}」\n💰 價格：${price:.0f} 元\n📋 類別：{category}"
        )
    else:
        result_label.config(text="😭 沒有符合條件的飲料")

tk.Button(root, text="幫我想想！", font=("Helvetica", 12), command=suggest_drink).pack(pady=10)

root.mainloop()
