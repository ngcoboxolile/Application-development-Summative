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
print(solar_power)
