from tkinter import *
from tkinter import simpledialog, messagebox, ttk
import json
import os

# JSON 檔案名稱
json_file = "store_data.json"

# 載入資料
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

# 儲存資料
def save_data():
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(store_data, f, ensure_ascii=False, indent=2)

# 新增店家
def add_store():
    store = simpledialog.askstring("新增店家", "請輸入店家名稱：")
    if store:
        if store not in store_data:
            store_data[store] = {}
            update_ui()
            save_data()
        else:
            messagebox.showinfo("提示", "該店家已存在")

# 新增飲料與價格
def add_drink():
    store = store_var.get()
    if not store:
        messagebox.showerror("錯誤", "請先選擇店家")
        return
    drink = simpledialog.askstring("新增飲料", "請輸入飲料名稱：")
    if not drink:
        return
    try:
        price = float(simpledialog.askstring("新增價格", f"{drink} 的價格："))
    except (ValueError, TypeError):
        messagebox.showerror("錯誤", "價格需為數字")
        return

    store_data[store][drink] = price
    update_ui()
    save_data()

# 刪除飲料
def delete_drink():
    selected = tree.selection()
    if not selected:
        return
    for item in selected:
        parent = tree.parent(item)
        if parent:  # 飲料
            store = tree.item(parent, "text")
            drink_name = tree.item(item, "text").split("（")[0]
            if drink_name in store_data[store]:
                del store_data[store][drink_name]
        else:
            messagebox.showwarning("提示", "這是店家，請用『刪除店家』")
    update_ui()
    save_data()

# 刪除店家
def delete_store():
    selected = tree.selection()
    if not selected:
        return
    for item in selected:
        if not tree.parent(item):  # 是店家
            store = tree.item(item, "text")
            if messagebox.askyesno("確認刪除", f"確定要刪除店家「{store}」嗎？"):
                store_data.pop(store, None)
    update_ui()
    save_data()

# 更新下拉選單與樹狀顯示
def update_ui():
    menu = store_menu["menu"]
    menu.delete(0, "end")
    for store in store_data:
        menu.add_command(label=store, command=lambda value=store: store_var.set(value))

    tree.delete(*tree.get_children())
    for store, drinks in store_data.items():
        store_node = tree.insert("", "end", text=store)
        for name, price in drinks.items():
            tree.insert(store_node, "end", text=f"{name}（${price:.0f}）")

# GUI 主介面
root = Tk()
root.title("店家與飲料管理")
root.geometry("550x550")

frame = Frame(root)
frame.pack(pady=10)

Label(frame, text="選擇店家：").grid(row=0, column=0)
store_var = StringVar(root)
store_keys = list(store_data.keys())
store_var.set(store_keys[0] if store_keys else "")
store_menu = OptionMenu(frame, store_var, *(store_keys if store_keys else ["請先新增店家"]))
store_menu.grid(row=0, column=1)

Button(frame, text="➕ 新增店家", command=add_store).grid(row=1, column=0, pady=5)
Button(frame, text="🥤 新增飲料", command=add_drink).grid(row=1, column=1, pady=5)
Button(frame, text="❌ 刪除飲料", command=delete_drink).grid(row=1, column=2, pady=5)
Button(frame, text="🗑️ 刪除店家", command=delete_store).grid(row=1, column=3, pady=5)

tree = ttk.Treeview(root)
tree.heading("#0", text="店家與飲料（含價格）")
tree.pack(expand=True, fill=BOTH, padx=10, pady=10)

update_ui()
root.mainloop()
