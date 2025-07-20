from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    barcode = request.json.get('barcode')
    print("Scanned Barcode:", barcode)

    # UPCitemDB lookup
    api_url = f"https://api.upcitemdb.com/prod/trial/lookup?upc={barcode}"
    response = requests.get(api_url)
    data = response.json()

    if data.get("items"):
        product = data["items"][0]
        return jsonify({
            'barcode': barcode,
            'title': product.get("title"),
            'brand': product.get("brand"),
            'description': product.get("description"),
            'image': product.get("images", [None])[0]
        })
    else:
        return jsonify({'barcode': barcode, 'error': 'Product not found'})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
