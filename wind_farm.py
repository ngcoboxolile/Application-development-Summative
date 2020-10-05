import requests
import pandas as pd
url2 = 'http://www.7timer.info/bin/api.pl?lon=8.598&lat=53.557&product=meteo&output=json' # Get the wind weather data
data_wind = requests.get(url2).json()
wind_speed = []
wind_direction = []
for i in range(7):
    ws = data_wind['dataseries'][i]['wind_profile'][0]['speed']
    wd = data_wind['dataseries'][i]['wind_profile'][0]['direction']
    wind_speed.append(ws)
    wind_direction.append(wd)
# I need to manipulate the speed. I randomyly chose values as specified in the documentation info of the api as per interval
speed_value ={'1': 0.15, '2': 2.4, '3':5.2, '4':7.4, '5':14.5, '6':19.3, '7':27.6, '8':33.5, '9':38.2, '10':43.5, '11':48.3, '12':53.5, '13':60.0}
wind_speed = []
wind_direction = []
for i in range(7):
    s = data_wind['dataseries'][i]['wind_profile'][0]['speed']
    ws = speed_value[str(s)] #Use created dictionary labeled speed_value
    wd = data_wind['dataseries'][i]['wind_profile'][0]['direction']
    wind_speed.append(ws)
    wind_direction.append(wd)
#Create a data frame now
data1 = pd.DataFrame([wind_speed, wind_direction]).transpose()
data1["wind_speed"]=data1[0]
data1["wind_diection"]=data1[1]
data1.drop([0,1], inplace=True, axis=1)
import pickle
wind_model = pickle.load(open('wind_data_model.sav','rb'))# load the wind_model
wind_power = wind_model.predict(data1.values)# pridicted values
print(wind_power)
