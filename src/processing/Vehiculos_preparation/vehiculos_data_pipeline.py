# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 11:04:44 2019

@author: danie
"""


import sys
sys.path.append('../../../resources')
import numpy as np
import pandas as pd
import EDA_framework as EDA

def main():
    df = pd.read_csv('../../../data/raw/Vehiculos.csv')
    df = EDA.imput_nan_values(df, 'CLASE_VEHICULO_ACCIDENTADO', strateg='constant', fill_value='DESCONOCIDA')
    df = EDA.imput_nan_values(df, 'SERVICIO_VEHICULO_ACCIDENTADO', strateg='constant', fill_value='DESCONOCIDO')
    df = df.rename(columns={'CLASE ACCIDENTE':'CLASE_ACCIDENTE'})
    df.to_csv('../../../data/processed/Vehiculos_clean.csv', index=False)
    
if __name__ == "__main__":
    main()