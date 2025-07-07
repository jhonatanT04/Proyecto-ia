from flask import Flask, request, jsonify, send_file
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import io

import os
from fastapi.responses import FileResponse
from flask_cors import CORS
from google.cloud import texttospeech

app = Flask(__name__)
CORS(app)

MODEL_PATH = 'modelo_val.h5'
model = load_model(MODEL_PATH)

def generarAudio(predicted_class, confidence):
    text = f"La predicción es {predicted_class} con una confianza del {round(confidence * 100)} por ciento."
        
    client = texttospeech.TextToSpeechClient.from_service_account_file("gcp_key.json")
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="es-US",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    
    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)
    with open("salida.mp3", "wb") as out:
        out.write(response.audio_content)
        print("Audio guardado en 'salida.mp3'")

LABELS_PATH = 'labels.txt'
with open(LABELS_PATH, 'r', encoding='utf-8') as f:
    class_names = [line.strip() for line in f if line.strip()]
print(f"Clases cargadas: {class_names}")

def preprocess_image(image_bytes, target_size=(500, 500)):
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')  
    img = img.resize(target_size)
    img_array = np.array(img, dtype=np.float32) / 255.0
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
        print(prediction[0])
        predicted_index = int(np.argmax(prediction[0]))
        predicted_class = class_names[predicted_index]
        confidence = float(np.max(prediction[0]))

        #generarAudio(predicted_class, confidence)
        return jsonify({
            'prediction': predicted_class,
            'confidence': round(confidence * 100, 2)  
        })

    except Exception as e:
        print(" Error:", str(e))
        return jsonify({'error': str(e)}), 500


@app.route("/audio", methods=["GET"])
def get_audio():
    return send_file("salida.mp3", mimetype="audio/mpeg")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
