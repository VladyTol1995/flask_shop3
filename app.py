from flask import Flask, render_template, jsonify, send_from_directory, request
from dotenv import load_dotenv
import os
import json
import logging
logging.basicConfig(level=logging.INFO)

# Загружаем переменные из .env
load_dotenv()

app = Flask(__name__)

SHOP_NAME = "FakeShop3"
SHOP_URL = os.getenv("FAKE_MAGAZ2_URL")

def load_products():
    try:
        with open("products.json", "r", encoding="utf-8-sig") as file:
            return json.load(file)
    except Exception as e:
        print("Ошибка при загрузке JSON:", e)
        return []

products = load_products()

@app.route('/')
def home():
    return render_template('index.html', products=products, shop_name=SHOP_NAME, shop_url=SHOP_URL)


# Новый маршрут API для получения данных о конкретном товаре
@app.route('/product/<int:product_id>')
def product(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if product:
        return render_template('product.html', product=product, shop_name=SHOP_NAME, shop_url=SHOP_URL), 200, {"Content-Type": "text/html"}
    return "Товар не найден", 404

# Исправленный маршрут API для получения списка товаров с корректными ссылками
@app.route('/api/products', methods=['GET'])
def api_get_products():
    base_url = SHOP_URL.rstrip('/api/products')
    return jsonify([
        {
            "id": p["id"],
            "name": p["name"],
            "price": p["price"],
            "rating": p["rating"],
            "reviews": p["reviews"],
            "image": p["image"],
            "url": f"{base_url}/product/{p['id']}"  # Исправленная ссылка
        }
        for p in products
    ])

@app.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.before_request
def log_request():
    logging.info(f"Запрос: {request.method} {request.path}")

if __name__ == '__main__':
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)