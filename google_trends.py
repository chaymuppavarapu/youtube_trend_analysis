from pytrends.request import TrendReq
import pandas as pd

def fetch_google_trends(keyword="YouTube", timeframe="today 5-y", geo="IN"):
    pytrends = TrendReq()
    pytrends.build_payload([keyword], timeframe=timeframe, geo=geo)
    data = pytrends.interest_over_time()
    if 'isPartial' in data.columns:
        data = data.drop(columns=['isPartial'])
    return data

# Test
if __name__ == "__main__":
    df = fetch_google_trends("YouTube")
    print(df.tail())
