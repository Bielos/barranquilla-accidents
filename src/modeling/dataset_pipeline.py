# -*- coding: utf-8 -*-
"""
Created on Thr Mar 28 23:00:34 2019

@author: Daniel Martinez Bielostotzky
"""
import numpy as np
import pandas as pd

def main():

    df = pd.read_csv('../../data/processed/Accidentes_clean.csv')
    df['FECHA_ACCIDENTE'] = pd.to_datetime(df['FECHA_ACCIDENTE'], format="%Y-%m-%d %H:%M:%S")
    daily_data = df.set_index('FECHA_ACCIDENTE').groupby(pd.Grouper(freq='d')).agg({'CANTIDAD_ACCIDENTES':sum}).reset_index()
    daily_data.head()

    daily_data.to_csv('dataset_final.csv', index=False)

if __name__ == "__main__":
    main()