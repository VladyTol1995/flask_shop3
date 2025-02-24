from flask import Flask, render_template, jsonify, send_from_directory, request
from dotenv import load_dotenv
import os
import json
import logging
import requests

logging.basicConfig(level=logging.INFO)

# Загружаем переменные окружения из .env
load_dotenv()

app = Flask(__name__)

SHOP_NAME = "FakeShop3"

def get_dynamic_shop_url():
    """Проверяет доступность FAKE_MAGAZ2_URL, если он недоступен — возвращает localhost."""
    shop_url = os.getenv("FAKE_MAGAZ2_URL", "http://localhost:10000")
    try:
        response = requests.get(shop_url, timeout=3)  # Таймаут 3 секунды
        if response.status_code == 200:
            return shop_url
    except requests.RequestException:
        pass
    return "http://localhost:10000"

def load_products():
    """Загружает список товаров из JSON-файла."""
    try:
        with open("products.json", "r", encoding="utf-8-sig") as file:
            return json.load(file)
    except Exception as e:
        logging.error("Ошибка при загрузке JSON: %s", e)
        return []

products = load_products()

@app.route('/')
def home():
    shop_url = get_dynamic_shop_url()
    return render_template('index.html', products=products, shop_name=SHOP_NAME, shop_url=shop_url)

@app.route('/product/<int:product_id>')
def product(product_id):
    shop_url = get_dynamic_shop_url()
    product = next((p for p in products if p["id"] == product_id), None)
    if product:
        return render_template('product.html', product=product, shop_name=SHOP_NAME, shop_url=shop_url), 200, {"Content-Type": "text/html"}
    return "Товар не найден", 404

@app.route('/api/products', methods=['GET'])
def api_get_products():
    """Возвращает список товаров с динамически проверенной ссылкой магазина."""
    shop_url = get_dynamic_shop_url().rstrip('/')  # Убираем лишние слэши в конце
    return jsonify([
        {
            "id": p["id"],
            "name": p["name"],
            "price": p["price"],
            "rating": p["rating"],
            "reviews": p["reviews"],
            "image": p["image"],
            "url": f"{shop_url}/product/{p['id']}"
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