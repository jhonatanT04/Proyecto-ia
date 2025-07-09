from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import torch
import torchxrayvision as xrv
import torchvision
import skimage
import io
import numpy as np
from PIL import Image
from google.cloud import texttospeech
import os

app = Flask(__name__)
CORS(app)

with torch.serialization.safe_globals([xrv.models.DenseNet, torch.nn.modules.container.Sequential]):
    model = torch.load("Back/densenet121_res224_all_completo.pth", weights_only=False, map_location="cpu")

model.eval()


transform = torchvision.transforms.Compose([
    xrv.datasets.XRayCenterCrop(),
    xrv.datasets.XRayResizer(224),
])

def preprocess_image(file_storage):
    img = skimage.io.imread(file_storage)
    img = xrv.datasets.normalize(img, 255)

    if len(img.shape) == 3:
        img = img.mean(2)  
    img = img[None, ...]  
    img = transform(img)
    img = torch.from_numpy(img).float()
    return img[None, ...]  

def generar_audio(predicted_class, confidence):
    texto = f"La predicción más probable es {predicted_class} con una confianza del {round(confidence * 100)} por ciento."

    client = texttospeech.TextToSpeechClient.from_service_account_file("gcp_key.json")
    input_text = texttospeech.SynthesisInput(text=texto)
    voice = texttospeech.VoiceSelectionParams(
        language_code="es-US",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    response = client.synthesize_speech(
        input=input_text,
        voice=voice,
        audio_config=audio_config
    )

    with open("salida.mp3", "wb") as out:
        out.write(response.audio_content)
    print("Audio generado en salida.mp3")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No se envió ninguna imagen'}), 400

        file = request.files['image']
        img_tensor = preprocess_image(file)

        with torch.no_grad():
            outputs_logits = model(img_tensor)
            outputs = torch.sigmoid(outputs_logits)

        results = dict(zip(model.pathologies, outputs[0].numpy()))
        top3 = sorted(results.items(), key=lambda x: x[1], reverse=True)[:3]
        top_condition, top_confidence = top3[0]

        if top_confidence >= 0.7:
            generar_audio(top_condition, top_confidence)

        return jsonify({
            "results": {k: round(float(v), 4) for k, v in results.items()},
            "top3": [{"condition": k, "confidence": round(v * 100, 2)} for k, v in top3]
        })

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
