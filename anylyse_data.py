import pandas as pd
import matplotlib.pyplot as plt
import os
from wordcloud import WordCloud

df = pd.read_csv('new_all_cleaned.csv')

print(df.info())

print(df.isnull().sum())

print(df.describe())
print(df.describe(include=['object']))

df['Company-Name'] = df['Company-Name'].str.upper()

graph_dir = 'graphs'
if not os.path.exists(graph_dir):
    os.makedirs(graph_dir)
    

color_list = [
    '#FF5733',  # Red-Orange
    '#33FFBD',  # Aqua
    '#FFC300',  # Yellow
    '#DAF7A6',  # Light Green
    '#C70039',  # Crimson
    '#900C3F',  # Dark Red
    '#581845',  # Purple
    '#1E90FF',  # Dodger Blue
    '#FF69B4',  # Hot Pink
    '#8A2BE2',  # Blue Violet
    '#00FF7F',  # Spring Green
    '#FFD700',  # Gold
    '#FF4500',  # Orange Red
    '#7FFFD4',  # Aquamarine
    '#4B0082',  # Indigo
    '#ADFF2F',  # Green Yellow
    '#FF6347',  # Tomato
    '#4682B4',  # Steel Blue
    '#32CD32',  # Lime Green
    '#FF1493'   # Deep Pink
]

plt.figure(figsize=(12, 8))
df['Title'].value_counts().head(20).plot(kind='bar',color=color_list )
plt.title("Top 20 Most Common Job Titles")
plt.xlabel("Job Title")
plt.ylabel("Count")
plt.xticks(rotation=60)
plt.savefig(os.path.join(graph_dir, 'top_20_job_titles.png'), bbox_inches='tight')  
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
skills_df['skills_split'] = skills_df['skills_split'].str.lower().str.strip()

plt.figure(figsize=(12, 8))
skills_df['skills_split'].value_counts().head(10).plot(kind='pie')
plt.title("Top 10 Skills in Job Listings")
plt.xlabel("Skills")
# plt.ylabel("Frequency")
plt.xticks(rotation=45)

plt.savefig(os.path.join(graph_dir, 'top_10_skills.png'), bbox_inches='tight')
plt.close()


pivot_table = pd.pivot_table(df, index='Title', columns='Company-Name', aggfunc='size', fill_value=0)
print("\nPivot Table (Job Title and Company-Name):")
print(pivot_table)

software_dev_jobs = df[df['Title'].str.contains('Software Developer', case=False, na=False)]

all_skills = software_dev_jobs['skills'].str.split(',').explode().str.strip().str.lower()

skill_counts = all_skills.value_counts()

plt.figure(figsize=(10,6))
skill_counts.head(10).plot(kind='barh', color='skyblue')
plt.title('Top 10 Skills for Software Developers',fontsize=16)
plt.xlabel('Number of Job Postings', fontsize=12)
plt.ylabel('Skills',fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.savefig( os.path.join( graph_dir, 'software_dev_skills.png'), bbox_inches='tight')


wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(skill_counts)
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')  
plt.title('Skills Word Cloud for Software Developers')
plt.savefig( os.path.join( graph_dir, 'cloud_skills.png'), bbox_inches='tight')

plt.show()


df.to_csv("analyzed_data.csv", index=False)

print(f"Graphs saved in the '{graph_dir}' folder.")
