from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan_barcode():
    data = request.get_json()
    barcode = data.get('barcode')

    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    res = requests.get(url)
    product = res.json()

    if product.get('status') != 1:
        return jsonify({'error': 'Product not found in OpenFoodFacts'}), 404

    p = product['product']
    return jsonify({
        "title": p.get("product_name", "Unknown Product"),
        "brand": p.get("brands", "Unknown Brand"),
        "description": p.get("categories", ""),
        "image": p.get("image_front_small_url", "")
    })

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
