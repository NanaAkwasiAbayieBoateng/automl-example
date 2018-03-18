import os

from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template

from crawler import predict


app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/predict/', methods=['POST'])
def predict_api():
    text = request.form['source']
    resp = predict(text)
    return jsonify({'_class': resp})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
