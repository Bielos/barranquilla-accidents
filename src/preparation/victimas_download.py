# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 09:13:57 2019

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
        
url = 'https://www.datos.gov.co/api/views/y628-5q9a/rows.csv?accessType=DOWNLOAD'
file_name = '../../data/raw/Victimas.csv'

if __name__ == "__main__":
    download(url, file_name)