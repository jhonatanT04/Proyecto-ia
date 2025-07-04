from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import io
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

MODEL_PATH = 'modelo_val.h5'
model = load_model(MODEL_PATH)
print("Modelo cargado correctamente.")

# Cargar las clases desde un archivo de texto
LABELS_PATH = 'labels.txt'
with open(LABELS_PATH, 'r', encoding='utf-8') as f:
    class_names = [line.strip() for line in f if line.strip()]
print(f"Clases cargadas: {class_names}")

def preprocess_image(image_bytes, target_size=(128, 128)):
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    img = img.resize(target_size)
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No se envió ninguna imagen'}), 400

        file = request.files['image']
        image_bytes = file.read()
        image_array = preprocess_image(image_bytes)

        prediction = model.predict(image_array)
        predicted_index = int(np.argmax(prediction[0]))
        predicted_class = class_names[predicted_index]
        confidence = float(np.max(prediction[0]))

        return jsonify({
            'prediction': predicted_class,
            'confidence': round(confidence * 100, 2)  
        })

    except Exception as e:
        print(" Error:", str(e))
        return jsonify({'error': str(e)}), 500
@app.route('/')
def index():
    return jsonify({'message': 'API imagenes'}), 200
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
