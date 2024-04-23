from flask import Flask, Blueprint, render_template, redirect, url_for, jsonify, request
import os
import requests 

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        lat = request.form['lat']
        long = request.form['long']
        grid_info = get_grid(lat, long)
        if grid_info:
            office = grid_info['office']
            gridX = grid_info['gridX']
            gridY = grid_info['gridY']
            return redirect(url_for('forecast', office=office, gridX=gridX, gridY=gridY))
        else:
            print("Failed to fetch grid information. Please try again.")
            return render_template('index.html')
    return render_template('index.html')

@app.route("/forecast", methods=['GET'])
def forecast():
    office = request.args.get('office')
    gridX = request.args.get('gridX')
    gridY = request.args.get('gridY')
    if office and gridX and gridY:
        try:
            forecast_info = get_forecast(office, gridX, gridY)
            return render_template('forecast.html', forecast=forecast_info)
        except Exception as e:
            return render_template('forecast.html', error=str(e))
    else:
        return redirect(url_for('main'))

def get_forecast(office, gridX, gridY):
    url = f'https://api.weather.gov/gridpoints/{office}/{gridX},{gridY}/forecast'
    
    headers = {
        'User-Agent': 'Your Name, Your Institution - your.email@example.com',
        'Accept': 'application/json',
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()['properties']['periods'][0]
        temperature = data.get('temperature')
        temperatureTrend = data.get('temperatureTrend', '')
        shortForecast = data.get('shortForecast')

        forecast = ""
        if temperature is not None:
            forecast += f"{temperature}F "
        if temperatureTrend:
            forecast += f"{temperatureTrend} - "
        if shortForecast:
            forecast += shortForecast

        if not forecast:
            raise ValueError("Forecast data is incomplete.")

        return forecast
    except Exception as e:
        print(f"Failed to fetch forecast: {str(e)}")
        raise Exception('Failed to fetch forecast')
    

def get_grid(latitude, longitude):
    url = f'https://api.weather.gov/points/{latitude},{longitude}'
    
    headers = {
        'User-Agent': 'Leandro Lopez, Merrimack College - lopezl@merrimack.edu',
        'Accept': 'application/json',
    }

    try:
        response = requests.get(url, headers=headers)
        response = requests.get(url)
        if response.ok:
            data = response.json()
            office = data['properties']['gridId']
            gridX = data['properties']['gridX']
            gridY = data['properties']['gridY']
            return {'office': office, 'gridX': gridX, 'gridY': gridY}
        else:
            response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f'Request failed: {e}')
        return None

