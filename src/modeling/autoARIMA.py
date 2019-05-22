import numpy as np
import pandas as pd

df = pd.read_csv('dataset_final.csv')
df['FECHA_ACCIDENTE'] = pd.to_datetime(df['FECHA_ACCIDENTE'], format="%Y-%m-%d %H:%M:%S")
df = df.set_index('FECHA_ACCIDENTE')

train = df.loc[:'2017-12-31']
test = df.loc['2018-01-01':]

# fitting a stepwise model:
from pmdarima.arima import auto_arima

stepwise_fit = auto_arima(train, start_p=1, start_q=1, max_p=3, max_q=3, m=12,
                          start_P=0, seasonal=True, d=1, D=1, trace=True,
                          error_action='ignore',  # don't want to know if an order does not work
                          suppress_warnings=True,  # don't want convergence warnings
                          stepwise=True)  # set to stepwise

stepwise_fit.summary()

y_pred = stepwise_fit.predict(n_periods=365)

from sklearn.metrics import mean_squared_error, mean_absolute_error
print('MSE: {0}'.format(mean_squared_error(test, y_pred)))
print('MAE: {0}'.format(mean_absolute_error(test, y_pred)))