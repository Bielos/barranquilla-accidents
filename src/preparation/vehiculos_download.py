# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 09:12:01 2019

@author: danie
"""

from requests import get  # to make GET request

def download(url, file_name):
    # open in binary mode
    with open(file_name, "wb") as file:
        # get request
        response = get(url)
        # write to file
        file.write(response.content)
        
url = 'https://www.datos.gov.co/api/views/nfa3-wgxy/rows.csv?accessType=DOWNLOAD'
file_name = '../../data/raw/Vehiculos.csv'

if __name__ == "__main__":
    download(url, file_name)