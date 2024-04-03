from flask import Flask, Blueprint, render_template, redirect, url_for, jsonify, request
import os

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def main():
    error = None
    if request.method == 'POST':
        lat = request.form['lat']
        long = request.form['long']
        response = get_grid(lat, long)
        print(response)
    else:
        print('TEST: Nothing')
    return render_template('index.html')

def get_forecast(office, gridX, gridY):
    '''This function returns the forecast for the given
    office and grid coordinates.
    Parameters: Office, gridX, gridY (given by the get_grid() function.)
    Returns: Forecast
    '''
    url = f'https://api.weather.gov/gridpoints/{office}/{gridX},{gridY}/forecast'
    
    try:
        response = requests.get(url)
        if response.ok:
            forecast = str(response.json()['properties']['periods'][0]['temperature'])
            forecast += "F "+response.json()['properties']['periods'][0]['temperatureTrend']
            forecast += " - "+response.json()['properties']['periods'][0]['shortForecast']
            return forecast

    except:
        raise Exception('Failed to fetch forecast')
    

def get_grid(latitude, longitude):
    url = f'https://api.weather.gov/points/{latitude},{longitude}'

    response = requests.get(url)
    return response

