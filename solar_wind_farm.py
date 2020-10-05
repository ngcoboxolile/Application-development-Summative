# Solar Farm
import requests
import pandas as pd
url = 'http://www.7timer.info/bin/api.pl?lon=142.11.17&lat=-19.46&product=civillight&output=json'
data_solar = requests.get(url).json()
date = []
temp_hi = []
temp_low = []
for i in range(7):
    dt = data_solar['dataseries'][i]['date']
    th = data_solar['dataseries'][i]['temp2m']['max']
    tl = data_solar['dataseries'][i]['temp2m']['min']
    date.append(dt)
    temp_hi.append(th)
    temp_low.append(tl)
url_1 = 'http://www.7timer.info/bin/api.pl?lon=142.11.17&lat=-19.46&product=meteo&output=json'
data_solar1 = requests.get(url_1).json()# gets wind data
cloud_cover =[]
for i in range(7):
    cloud = data_solar1['dataseries'][i]['cloudcover']
    cloud_cover.append(cloud)
data = pd.DataFrame([date,temp_hi, temp_low, cloud_cover]).transpose()
import pickle
data.drop([0], inplace = True, axis = 1)#dropping date column
data['temp_hi']= (data[1]*9/5) + 32 # convert
data['temp_low']= (data[2]*9/5) + 32
data["cloud_cover"] = data[3]
data.drop([1,2,3], inplace =True, axis = 1)# Drop the other columns unnamed columns
solar_model = pickle.load(open('solar_data_model.sav', 'rb')) # Load model
solar_power = solar_model.predict(data.values) # The predicted value

# Wind Farm
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

Total_power = wind_power + solar_power
print(Total_power)
