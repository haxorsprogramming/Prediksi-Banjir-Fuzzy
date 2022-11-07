from flask import Flask, redirect, url_for, render_template, request, jsonify
import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
import sys
import uuid

app = Flask(__name__)

BASE_URL = "http://127.0.0.1:6000/"
dr = {'content': 'Sistem prediksi banjir menggunakan Fuzzy Logic'}

@app.route('/')
def index():
    dr = {'BASE_URL': BASE_URL}
    return render_template('home.html', dRes=dr)

@app.route('/prediksi')
def prediksi():
    dr = {'BASE_URL':BASE_URL}
    return render_template('prediksi.html', dRes=dr)

@app.route('/proses-prediksi', methods=('GET', 'POST'))
def prosesPrediksi():
    kdPengujian = uuid.uuid4()
    CURRENT_RIVER_LEVEL = request.form['level']
    CURRENT_RAINFALL = request.form['curah']

    x_riverlevel = np.arange(0, 6, 1)
    x_rainfall = np.arange(0, 300, 1)
    x_floodstatus = np.arange(0, 10, 1)

    riverlevel_normal = fuzz.trimf(x_riverlevel, [0,1,2])
    riverlevel_berjaga = fuzz.trimf(x_riverlevel, [1,2,3])
    riverlevel_amaran = fuzz.trimf(x_riverlevel, [2,3,4])
    riverlevel_bahaya = fuzz.trimf(x_riverlevel, [3,4,5])

    rainfall_low = fuzz.trimf(x_rainfall, [0, 30, 61])
    rainfall_moderate = fuzz.trimf(x_rainfall, [40, 122, 183])
    rainfall_high = fuzz.trimf(x_rainfall, [160, 200, 300])

    flood_none = fuzz.trapmf(x_floodstatus, [0, 1, 2, 3])
    flood_minor = fuzz.trapmf(x_floodstatus, [1, 3, 4, 5])
    flood_moderate = fuzz.trimf(x_floodstatus, [4, 5, 6])
    flood_major = fuzz.trapmf(x_floodstatus, [5.5, 6, 7, 9])

    fig, ax = plt.subplots(figsize=(18,5))
    ax.set_title('Level keamanan sungai')
    ax.set_xlabel('level sungai')
    ax.plot(x_riverlevel, riverlevel_normal,linewidth=1.5, label='normal')
    ax.plot(x_riverlevel, riverlevel_berjaga,linewidth=1.5, label='berjaga')
    ax.plot(x_riverlevel, riverlevel_amaran,linewidth=1.5, label='Peringatan')
    ax.plot(x_riverlevel, riverlevel_bahaya,linewidth=1.5, label='bahaya')
    ax.legend()
    plt.savefig('img_save/level_'+str(kdPengujian)+'.png')
    plt.close()

    

    dr = {
        'status' : 'sukses',
        'x_tingkat_sungai': str(x_riverlevel),
        'x_curah_hujan' : str(x_rainfall),
        'x_status_banjir' : str(x_floodstatus),
        'level_normal' : str(riverlevel_normal),
        'level_berjaga' : str(riverlevel_berjaga),
        'level_amaran' : str(riverlevel_amaran),
        'level_bahaya' : str(riverlevel_bahaya),
        'rain_low' : str(rainfall_low),
        'rain_moderate' : str(rainfall_moderate),
        'rain_high' : str(rainfall_high)
    }

    return jsonify(dr)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7001)