from flask import Flask, request, jsonify
from PIL import Image
from pyzbar.pyzbar import decode
import io
import base64


app = Flask(__name__)

@app.route('/process-image', methods=['POST'])
def process_image():
    data = request.get_json()
    if 'image_base64' not in data:
        return jsonify({'error': 'No image data provided'}), 400

    image_data = data['image_base64']
    image_data = image_data.split(",")[-1]  # Remove o prefixo da URL de dados, se presente

    try:
        decoded_image = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(decoded_image))
        decoded_objects = decode(image)
        results = [{'data': obj.data.decode('utf-8'), 'type': obj.type} for obj in decoded_objects]
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)