import numpy as np
import pandas as pd
from fbprophet import Prophet
import holidays

df = pd.read_csv('dataset_final.csv')
df['FECHA_ACCIDENTE'] = pd.to_datetime(df['FECHA_ACCIDENTE'], format="%Y-%m-%d %H:%M:%S")
df = df.set_index('FECHA_ACCIDENTE')

train = df.loc[:'2017-12-31'].reset_index()
train.columns = ['ds', 'y']
train.head()
test = df.loc['2018-01-01':'2018-05-31'].reset_index()

model = Prophet()
model.fit(train)

future = model.make_future_dataframe(periods=151)
forecast = model.predict(future)
forecast.head()

from sklearn.metrics import mean_squared_error, mean_absolute_error
print('MSE: {0}'.format(mean_squared_error(test['CANTIDAD_ACCIDENTES'].values, forecast['yhat'].iloc[-151:].values)))
print('MAE: {0}'.format(mean_absolute_error(test['CANTIDAD_ACCIDENTES'].values, forecast['yhat'].iloc[-151:].values)))

custom_model = Prophet(
    growth="linear",
    seasonality_mode="additive",
    holidays_prior_scale=15,
    seasonality_prior_scale=20,
    daily_seasonality=False,
    weekly_seasonality=False,
    yearly_seasonality=False,
).add_seasonality(
    name='Day_moment',
    period=1,
    fourier_order=3
).add_seasonality(
    name='Weekly_changes',
    period=7,
    fourier_order=3
).add_seasonality(
    name='Yearly_changes',
    period=365.25,
    fourier_order=10
)
custom_model.add_country_holidays(country_name='CO')

custom_model.fit(train)

test = df.loc['2018-06-01':].reset_index()
future = custom_model.make_future_dataframe(periods=214)
forecast = custom_model.predict(future)
forecast.head()

from sklearn.metrics import mean_squared_error, mean_absolute_error
print('MSE: {0}'.format(mean_squared_error(test['CANTIDAD_ACCIDENTES'].values, forecast['yhat'].iloc[-214:].values)))
print('MAE: {0}'.format(mean_absolute_error(test['CANTIDAD_ACCIDENTES'].values, forecast['yhat'].iloc[-214:].values)))