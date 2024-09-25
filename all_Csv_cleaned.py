import pandas as pd

df= pd.read_csv("/Users/naveenbighan/Desktop/Naukri.com/csvfiles/master_file.csv")
df= df.drop_duplicates()

df['salary_package'].fillna('N/A', inplace=True)

df['salary_package'] = df['salary_package'].replace('Not disclosed', 'N/A')
df['salary_package'] = df['salary_package'].replace('Unpaid', 'N/A')

df['Requirement'].fillna('N/A',inplace= True)

df['Timings'].fillna('N/A', inplace=True)
df['Timings']= df['Timings'].replace("Permanent","Full-Time")
print(df.info())


# df.to_csv("all_cleaned.csv",index=False, encoding='utf-8-sig')



