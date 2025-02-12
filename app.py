from flask import Flask, render_template, jsonify, send_from_directory
from dotenv import load_dotenv
import os
import json

# Загружаем переменные из .env
load_dotenv()

app = Flask(__name__)

SHOP_NAME = "FakeShop3"
SHOP_URL = os.getenv("FAKE_MAGAZ2_URL")  # Ссылка на магазин
API_KEY = os.getenv("FAKE_MAGAZ2_API_KEY")  # Ключ API
PORT = int(os.getenv("PORT", 10000))  # Уникальный порт

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

@app.route('/product/<int:product_id>')
def product(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if product:
        return render_template('product.html', product=product, shop_name=SHOP_NAME, shop_url=SHOP_URL)
    return "Товар не найден", 404

@app.route('/api/products', methods=['GET'])
def api_get_products():
    return jsonify([{"name": p["name"], "url": f"{SHOP_URL}/product/{p['id']}"} for p in products])

@app.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT, debug=True)