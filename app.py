from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)
SHOP_NAME = "FakeShop2"
SHOP_URL = "https://flask-shop3.onrender.com"  # Здесь будет твой публичный URL на Render

# Загрузка данных из JSON-файла
def load_products():
    try:
        with open("products.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        print("Ошибка при загрузке JSON:", e)
        return []

# Загружаем товары
products = load_products()

# Веб-интерфейс: главная страница
@app.route('/')
def home():
    return render_template('index.html', products=products, shop_name=SHOP_NAME, shop_url=SHOP_URL)

# Веб-интерфейс: страница товара
@app.route('/product/<int:product_id>')
def product(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if product:
        return render_template('product.html', product=product, shop_name=SHOP_NAME, shop_url=SHOP_URL)
    return "Товар не найден", 404

# API: получить список товаров
@app.route('/api/products', methods=['GET'])
def api_get_products():
    return jsonify([{"name": p["name"], "url": f"{SHOP_URL}/product/{p['id']}"} for p in products])

# API: получить информацию о конкретном товаре
@app.route('/api/products/<int:product_id>', methods=['GET'])
def api_get_product(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if product:
        return jsonify(product)
    return jsonify({"error": "Товар не найден"}), 404

if __name__ == '__main__':
    app.run(debug=True)