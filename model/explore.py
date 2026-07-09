import os
import pandas as pd
import pickle

CSV_PATH = os.path.join(os.path.dirname(__file__), 'spam.csv')

data = pd.read_csv(CSV_PATH, encoding='latin-1')

# first 5 rows
print(data.head())

# column names
print("\nColumns:", data.columns)

# Count if mssg isd  spam vs ham
print("\nLabel counts:")
print(data['v1'].value_counts())

data = data.rename(columns={"v1": "label", "v2": "message"})

print("\nCleaned Data:")
print(data.head())

