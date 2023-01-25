import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima.model import ARIMA

# Load the historical data into a pandas DataFrame
data = pd.read_csv("eth_4hrs_data.csv", parse_dates=[0])
data.set_index('time', inplace=True)

data.index = pd.to_datetime(data.index, utc=True)

if 'close' in data.columns:
    # Decompose the time series data
    data = data.resample('4H').mean()
    result = seasonal_decompose(data['close'], model='multiplicative')

    # Fit an ARIMA model to the residuals
    model = ARIMA(result.resid, order=(0,1,1))
    model_fit = model.fit()

    # Make predictions for the next 30 days
    predictions = model_fit.forecast(steps=30)[0]
    predictions_7_days = model_fit.forecast(steps=7)[0]


    # Print the predictions
    print(predictions)
    print(predictions_7_days)
else:
    print("'close' column not found in the dataframe.")
