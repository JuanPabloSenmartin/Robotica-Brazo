from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np

from vector.image_drawer import ImageDrawer
from text.text_drawer import TextDrawer

app = Flask(__name__)
CORS(app)


# flask --app server.py run -p 5000

@app.route('/image', methods=['POST'])
def draw_traces():
    print("CALLED /image")
    decoded_image = cv2.imdecode(np.frombuffer(request.data, np.uint8), -1)
    print("DECODED IMAGE")
    ImageDrawer.draw_image(decoded_image)
    return "Drawing traces..."


@app.route('/text', methods=['POST'])
def draw_text():
    text = request.json['text']
    print("TEXT", text)
    TextDrawer.draw_text(text)
    return "Drawing text..."

if __name__ == '__main__':
    app.run(port=5000)