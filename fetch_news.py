import requests
import pandas as pd
import os

api_key = "60b799439110459993fc3855b11d599a"

categories = ['business', 'entertainment', 'health', 'science', 'sports', 'technology']

all_data = []

for cat in categories:
    url = f"https://newsapi.org/v2/everything?q={cat} news&language=en&sortBy=publishedAt&apiKey={api_key}"
    
    res = requests.get(url).json()
    
    print(f"{cat} ->", len(res.get('articles', [])))
    
    for article in res.get('articles', []):
        data = {
            'title': article.get('title'),
            'source': article.get('source', {}).get('name'),
            'publishedAt': article.get('publishedAt'),
            'category': cat
        }
        all_data.append(data)

df = pd.DataFrame(all_data)

print("Total articles fetched:", len(df))

if not df.empty:
    if not os.path.exists("news_data.csv"):
        df.to_csv("news_data.csv", index=False)
    else:
        df.to_csv("news_data.csv", mode='a', index=False, header=False)

    print("Data saved ✅")
else:
    print("Still no data ❌")
    
pandas__version__ = pd.__version__
    