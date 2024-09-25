import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

df = pd.read_csv('new_csv_title.csv')

print(df.info())

print(df.isnull().sum())

print(df.describe())
print(df.describe(include=['object']))

df['Company-Name'] = df['Company-Name'].str.upper()

graph_dir = 'graphs'
if not os.path.exists(graph_dir):
    os.makedirs(graph_dir)

plt.figure(figsize=(12, 8))
df['Title'].value_counts().head(20).plot(kind='bar')
plt.title("Top 20 Most Common Job Titles")
plt.xlabel("Job Title")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.savefig(os.path.join(graph_dir, 'top_20_job_titles.png'), bbox_inches='tight')  # Save the graph
plt.close()  

plt.figure(figsize=(12, 8))
df['Company-Name'].value_counts().head(10).plot(kind='bar')
plt.title("Top 10 Companies by Job Listings")
plt.xlabel("Company")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.savefig(os.path.join(graph_dir, 'top_10_companies.png'), bbox_inches='tight')  # Save the graph
plt.close()

df['skills_split'] = df['skills'].str.split(',')
skills_df = df.explode('skills_split')

plt.figure(figsize=(12, 8))
skills_df['skills_split'].value_counts().head(10).plot(kind='bar')
plt.title("Top 10 Skills in Job Listings")
plt.xlabel("Skills")
plt.ylabel("Frequency")
plt.xticks(rotation=45)
plt.savefig(os.path.join(graph_dir, 'top_10_skills.png'), bbox_inches='tight')
plt.close()


pivot_table = pd.pivot_table(df, index='Title', columns='Company-Name', aggfunc='size', fill_value=0)
print("\nPivot Table (Job Title and Company-Name):")
print(pivot_table)

df.to_csv("analyzed_data.csv", index=False)

print(f"Graphs saved in the '{graph_dir}' folder.")
