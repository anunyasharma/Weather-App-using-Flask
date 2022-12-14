from flask import Flask, render_template, request
import configparser
import requests

app = Flask (__name__) 
app.debug = True

@app.route('/')
def weather_dashboard():
    return render_template('weather_input.html')

@app.route('/results', methods=['POST'])
def render_results():
    area_code=request.form['zipCode']
    country_code=request.form['countryCode']
    my_apikey=get_api_key()
    data=get_weather_results(area_code, country_code, my_apikey)
    temp="{0:.2f}".format(data["main"]["temp"])
    feels_like="{0:.2f}".format(data["main"]["feels_like"])
    temp_min="{0:.2f}".format(data["main"]["temp_min"])
    temp_max="{0:.2f}".format(data["main"]["temp_max"])
    pressure="{0:.2f}".format(data["main"]["pressure"])
    weather=data["weather"][0]["main"]
    location=data["name"]
    return render_template('weather_output.html',
                            location=location, temp=temp,
                            feels_like=feels_like, weather=weather,
                            temp_min=temp_min, temp_max=temp_max, 
                            pressure=pressure)

def get_api_key():
    config = configparser.ConfigParser()
    config.read('myapi.ini')
    return config['openweathermap']['my_apikey']

def get_weather_results(area_code, country_code, my_apikey):
    api_url = "https://api.openweathermap.org/"\
             "data/2.5/weather?zip={},{}&units=metric&appid={}".format(area_code,country_code,my_apikey)

if __name__== '__main__':
    app.run()