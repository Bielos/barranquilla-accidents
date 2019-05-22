# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 11:09:10 2019

@author: danie
"""

import sys
sys.path.append('../../../resources')
import numpy as np
import pandas as pd
import EDA_framework as EDA

def main():
    df = pd.read_csv('../../../data/raw/Victimas.csv')
    df = EDA.delete_null_observations(df, 'EDAD_VICTIMA')
    df = df.drop('mes', axis='columns')
    df.to_csv('../../../data/processed/Victimas_clean.csv', index=False)

if __name__ == "__main__":
    main()