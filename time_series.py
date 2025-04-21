from prophet import Prophet
import pandas as pd

def forecast_trend(trend_data):
    trend_data = trend_data.reset_index().rename(columns={"date": "ds", "YouTube": "y"})
    model = Prophet()
    model.fit(trend_data)

    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)
    return forecast, model

# Test
if __name__ == "__main__":
    from google_trends import fetch_google_trends
    data = fetch_google_trends("YouTube")
    forecast, model = forecast_trend(data)
    model.plot(forecast)
