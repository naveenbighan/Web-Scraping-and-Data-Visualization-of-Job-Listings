import pandas as pd
from pymongo import MongoClient

file_path = '/Users/naveenbighan/Desktop/Naukri.com/analyzed_data.csv'  # Replace with your CSV file path
df = pd.read_csv(file_path)

for column in df.columns:
    if df[column].dtype == 'object':  # Check if the column is non-numeric
        df[column].fillna("N/A", inplace=True)

df['Min_Experience'] = df['Min_Experience'].fillna(0)
df['Max_Experience'] = df['Max_Experience'].fillna(0)

        


client = MongoClient('mongodb://localhost:27017/')
db = client['Job_Listing']
collection = db['Job_Listing_data']


data_dict = df.to_dict(orient='records')
collection.insert_many(data_dict)

print(f"Inserted {len(data_dict)} records into MongoDB")
