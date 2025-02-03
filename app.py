from flask import Flask, render_template, jsonify
import json

try:
    with open("products.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    print("JSON загружен успешно!", data)
except Exception as e:
    print("Ошибка при загрузке JSON:", e)

app = Flask(__name__)
SHOP_NAME = "FakeShop2"

# Загрузка данных из JSON-файла
# Загрузка данных из JSON-файла
def load_products():
    with open("products.json", "r", encoding="utf-8") as file:
        return json.load(file)

products = load_products()

# Веб-интерфейс: главная страница
@app.route('/')
def home():
    return render_template('index.html', products=products, shop_name = SHOP_NAME)

# Веб-интерфейс: страница товара
@app.route('/product/<int:product_id>')
def product(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    return render_template('product.html', product=product, shop_name = SHOP_NAME)

# API: получить список товаров
@app.route('/api/products', methods=['GET'])
def api_get_products():
    return jsonify([{"name": p["name"], "url": f"http://127.0.0.1:5003/product/{p['id']}"} for p in products])

# API: получить информацию о конкретном товаре
@app.route('/api/products/<int:product_id>', methods=['GET'])
def api_get_product(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if product:
        return jsonify(product)
    return jsonify({"error": "Товар не найден"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5003)