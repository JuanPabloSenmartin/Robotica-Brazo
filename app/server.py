from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np

app = Flask(__name__)
CORS(app)


# flask --app server.py run -p 5000

@app.route('/image', methods=['POST'])
def draw_traces():
    frame = request.data
    decoded = cv2.imdecode(np.frombuffer(request.data, np.uint8), -1)
    print("IMAGE", decoded)
    return "Drawing traces..."


@app.route('/text', methods=['POST'])
def draw_text():
    text = request.json['text']
    print("TEXT", text)
    return "Drawing text..."
