# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 11:13:21 2019

@author: danie
"""

import sys
sys.path.append('../../../resources')
import numpy as np
import pandas as pd
import EDA_framework as EDA

def main():
    df = pd.read_csv('../../../data/raw/Accidentes.csv')
    # Delete null observations
    df = EDA.delete_null_observations(df, 'SITIO_EXACTO_ACCIDENTE')
    df = EDA.imput_nan_values(df, 'CANT_HERIDOS_EN _SITIO_ACCIDENTE', 'constant', fill_value=0)
    df = EDA.imput_nan_values(df, 'CANT_MUERTOS_EN _SITIO_ACCIDENTE', 'constant', fill_value=0)
    
    # Get coordinates
    import googlemaps
    KEY = 'INSERT_MAPS_API_KEY_HERE'
    gmaps = googlemaps.Client(key=KEY)
    
    def get_coordinates(address):
        city = 'Barranquilla, Colombia'
        geocode_result = gmaps.geocode(str(address) +' '+ city)
        if len(geocode_result) > 0:
            return list(geocode_result[0]['geometry']['location'].values())
        else:
            return [np.NaN, np.NaN]
    
    coordinates = df['SITIO_EXACTO_ACCIDENTE'].apply(lambda x: pd.Series(get_coordinates(x), index=['LATITUD', 'LONGITUD']))
    df = pd.concat([df[:], coordinates[:]], axis="columns")
    
    df = EDA.delete_null_observations(df,'LATITUD')
    df = df.drop(df[(df['LONGITUD'] < -75) | (df['LONGITUD'] > -74.5)].index)
    df = df.drop(df[(df['LATITUD'] < 10.8) | (df['LATITUD'] > 11.1)].index)
    
    # Converting exact hour of accident to time in the day
    dates = df['FECHA_ACCIDENTE'].apply(lambda x: str(x).split(' ')[0].strip())
    times = df['HORA_ACCIDENTE']
    dates = dates + ' ' + times
    df['FECHA_ACCIDENTE'] = pd.to_datetime(dates, format="%m/%d/%Y %I:%M:%S:%p")
    
    def convertion(time):
        if (6, 0) <= (time.hour, time.minute) < (11, 0):
            return 'Mañana'
        elif (11, 0) <= (time.hour, time.minute) < (14, 0):
            return 'Medio dia'
        elif (14, 0) <= (time.hour, time.minute) < (19, 0):
            return 'Tarde'
        elif (19, 0) <= (time.hour, time.minute) < (24, 0):
            return 'Noche'
        else:
            return 'Madrugada'
            
    time_in_day = []
    for time in df['FECHA_ACCIDENTE']:
        time_in_day.append(convertion(time))
    
    df['MOMENTO_DIA'] = time_in_day
    df = pd.concat([df.iloc[:,:5], df.iloc[:,13:14], df.iloc[:,5:8], df.iloc[:,11:13], df.iloc[:, 8:11]], axis='columns')
    
    # Finding conflict zones in the city
    lat = df.iloc[:, 9:10].values # latitude
    lng = df.iloc[:, 10:11].values # longitude
    
    from sklearn.cluster import KMeans
    from sklearn import metrics
    from scipy.spatial.distance import cdist
    
    k = 3;
    X = np.array(list(zip(lng, lat))).reshape(len(lng), 2)
    kmeanModel = KMeans(n_clusters=k, random_state=0).fit(X)
    cluster = kmeanModel.predict(X)
    cluster_df = pd.DataFrame()
    cluster_df['LONGITUDE'] = df['LONGITUD']
    cluster_df['LATITUDE'] = df['LATITUD']
    cluster_df['CLUSTER'] = cluster
    
    clusters_data = cluster_df['CLUSTER'].values
    df['ZONA'] = clusters_data
    encode = {'ZONA' : {0 : 'NORTE', 1 : 'CENTRO', 2 : 'SUR'}}
    df.replace(encode, inplace=True)
    
    # Day of accident to weekday or weekend
    def transformation(day):
        weekend_days = ['Vie', 'Sab', 'Dom']
        if day in weekend_days:
            return 'FIN DE SEMANA'
        else:
            return 'DIA DE SEMANA'
        
    day_of_week = pd.DataFrame()
    day_of_week['DIA_SEMANA_ACCIDENTE'] = df['DIA_ACCIDENTE'].copy().apply(transformation)
    day_of_week.head()
    
    df.to_csv('../../../data/processed/Accidentes_clean.csv', index=False)

if __name__ == "__main__":
    main()
    