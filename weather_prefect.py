from pyowm import OWM
from pyowm.utils import timestamps
from prefect import task, flow

owm = OWM('abee36f6eea7f6071283480f8c593544')
city =  'Guadalajara,MX'
mgr = owm.weather_manager()

@task(retries=3, retry_delay_seconds=3)
def get_temperature(city):
    observation = mgr.weather_at_place(city)
    weather = observation.weather
    weather.status
    weather.detailed_status  
    print('\033[1;33m' + '--- TODAY ---' + '(' + city + ')')
    print('Weather Status: ', weather.status)
    print('Temperature: ', weather.temperature('celsius'))
    print()
    return weather

@task(retries=3, retry_delay_seconds=3)
def get_forecast(city):
    daily_forecaster = mgr.forecast_at_place(city, '3h')
    tomorrow = timestamps.tomorrow()                               
    fweather = daily_forecaster.get_weather_at(tomorrow)
    print('\033[1;36m' + '--- TOMORROW ---' + '(' + city + ')')
    print('Weather Status: ', fweather.status)
    print('Temperature: ', fweather.temperature('celsius'))
    print()
    return fweather

@flow
def myflow():
    today = get_temperature(city)
    tomorrow = get_forecast(city)

myflow()
