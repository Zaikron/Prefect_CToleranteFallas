> # UDG - CUCEI 
> #### 06 de Marzo de 2023
### <p align="center"> Anthony Esteven Sandoval Marquez, 215660767</p>
#### <p align="center"> Materia: Computacion Tolerante a Fallas </p>
#### <p align="center"> Profesor: Michel Emanuel López Franco </p>
#### <p align="center"> Ciclo: 2023-A </p>

> ## Workflow managers, Prefect


#### Para esta práctica se uso Prefect 2 el cual mejora considerablemente la tolerancia a fallas de los sistemas a base de creación de tareas con un flujo determinado. De ejemplo yo elegí crear un flujo relacionado con la obtención del clima de la ciudad, la api utilizada fue la de OpenWeatherMap.
```python
from pyowm import OWM
from pyowm.utils import timestamps
from prefect import task, flow

owm = OWM('abee36f6eea7f6071283480f8c593544')
city =  'Guadalajara,MX'
mgr = owm.weather_manager()
```
#### La primera tarea realizada fue la de obtención del clima actual, que quedaría de la siguiente forma:

```python
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
```

#### Y la segunda fue la obtención del pronóstico para mañana, además se creó el flujo:
```python
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
```

#### Al ejecutarlo se obtuvieron los siguientes resultados para el clima de mi ciudad:
<p align="center"> <img src="https://github.com/Zaikron/Prefect_CToleranteFallas/blob/main/workIm/c1.png"/> </p>

#### Concluyendo, creo que esto es muy útil para tener un buen control de ciertas tareas y así poder encontrar los errores mas fácilmente, pues siempre se sabrá en que orden se ejecutaron y las dependencias de estas.

