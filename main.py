from flask import Flask, redirect, url_for, render_template, request, jsonify

app = Flask(__name__)

BASE_URL = "http://127.0.0.1:6000/"
dr = {'content': 'Sistem prediksi banjir menggunakan Fuzzy Logic'}

@app.route('/')
def index():
    dr = {'BASE_URL': BASE_URL}
    return render_template('home.html', dRes=dr)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7001)