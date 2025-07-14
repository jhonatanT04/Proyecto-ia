from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import torch
import torchxrayvision as xrv
import torchvision
import skimage
from datetime import datetime
from werkzeug.utils import secure_filename
from google.cloud import texttospeech
import cohere
import psycopg2
from psycopg2.extras import RealDictCursor

co = cohere.Client("HKewuzbrGI2Znjnxe0YJLmxhhUnkbqXjW9GjzuCc")

app = Flask(__name__)
CORS(app)

def get_connection():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        database="ia",
        user="postgres",
        password="root"
    )

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

def generar_audio(texto):
    client = texttospeech.TextToSpeechClient.from_service_account_file("Back/sistemas-463001-f1a542f8516e.json")
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

    with open("Back/salida.mp3", "wb") as out:
        out.write(response.audio_content)
    print("Audio generado")

def generar_explicacion_cohere(condition, confidence):
    prompt = f"""
    Eres un médico. Resume brevemente qué es '{condition}' con una confianza del {round(confidence * 100, 2)}%.
    Describe la enfermedad en una línea, síntomas comunes y una recomendación rápida.
    """
    response = co.chat(
        model="command-xlarge-nightly",
        message=prompt,
        temperature=0.5
    )
    return response.text.strip().replace('*', '')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No se envió ninguna imagen'}), 400

        file = request.files['image']
        filename = secure_filename(file.filename)
        file_path = filename  

        img_tensor = preprocess_image(file)

        with torch.no_grad():
            outputs_logits = model(img_tensor)
            outputs = torch.sigmoid(outputs_logits)

        results = dict(zip(model.pathologies, outputs[0].numpy()))
        top3 = sorted(results.items(), key=lambda x: x[1], reverse=True)[:3]
        top_condition, top_confidence = top3[0]

        explicacion = generar_explicacion_cohere(top_condition, top_confidence)
        generar_audio(explicacion)

        return jsonify({
            "results": {k: round(float(v), 4) for k, v in results.items()},
            "top3": [{"condition": k, "confidence": round(v * 100, 2)} for k, v in top3],
            "explanation": explicacion
        })

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/audio', methods=['GET'])
def get_audio():
    try:
        return send_file("Back/salida.mp3", mimetype="audio/mpeg", as_attachment=False)
    except FileNotFoundError:
        return jsonify({'error': 'El archivo de audio no existe'}), 404

@app.route('/historial', methods=['GET'])
def historial():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT id, fecha, diagnostico, explicacion, ruta_imagen FROM analisis ORDER BY fecha DESC")
    datos = cursor.fetchall()
    cursor.close()
    conn.close()

    resultado = []
    for row in datos:
        resultado.append({
            "id": row["id"],
            "fecha": row["fecha"].strftime("%Y-%m-%d %H:%M"),
            "diagnostico": row["diagnostico"],
            "explicacion": row["explicacion"],
            "imagen": row["ruta_imagen"].replace('\\', '/')  
        })

    return jsonify(resultado)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
