import requests

def get_forecast(office,gridX,gridY):
    # Construct the API URL for the given latitude and longitude
    url = f'https://api.weather.gov/gridpoints/{office}/{gridX},{gridY}/forecast'

    # Send a GET request to the API URL
    response = requests.get(url)
    # If the response is successful, extract the forecast data
    if response.ok:
        forecast = str(response.json()['properties']['periods'][0]['temperature'])
        forecast += "F "+response.json()['properties']['periods'][0]['temperatureTrend']
        forecast += " - "+response.json()['properties']['periods'][0]['shortForecast']
        return forecast

    # If the response is not successful, raise an exception
    else:
        raise Exception('Failed to fetch forecast.')

# Example usage information to New York, NY
office = "OKX"
gridX = 33
gridY = 35
forecast = get_forecast(office, gridX, gridY)
print(forecast)


