import pandas as pd
import os

folder_path = '/Users/naveenbighan/Desktop/Naukri.com/csvfiles'
files = os.listdir(folder_path)

all_data = []

for file in files:
    if file.endswith('.csv'):
        print(f"Processing file: {file}")
        file_path = os.path.join(folder_path, file)
        data = pd.read_csv(file_path)
        all_data.append(data)


master_data = pd.concat(all_data, ignore_index=True)

master_file_path = os.path.join(folder_path, 'master_file.csv')
master_data.to_csv(master_file_path, index=False, encoding='utf-8-sig')

print(f"Master file saved as: {master_file_path}")
